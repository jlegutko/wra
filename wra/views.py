from flask import render_template, request, redirect, url_for, flash, g
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from wra import db, app, login_manager, bcrypt
from flask_admin.contrib.sqla import ModelView

from flask_admin import Admin, AdminIndexView, helpers, expose
from flask_admin.contrib.sqla import ModelView

from .models.Models import User, Role, Profile, Artwork, Exhibition, Picture, Category, Comment, Grade, Favourite, \
    About, Inspiration, PrintedSource, OnlineSource, ImageSource


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    g.page = request.url_rule.rule


class WraAdminIndexView(AdminIndexView):
    """
    Custom Admin View
    """
    @expose('/')
    def index(self):
        """

        :return:
        """
        if current_user.role.name != 'admin':
            return redirect(url_for('index'))
        return super(WraAdminIndexView, self).index()


# Administrator panel
admin = Admin(app, index_view=WraAdminIndexView(), name='admin_panel', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Profile, db.session))
admin.add_view(ModelView(Artwork, db.session))
admin.add_view(ModelView(Exhibition, db.session))
admin.add_view(ModelView(Picture, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Grade, db.session))
admin.add_view(ModelView(Favourite, db.session))
admin.add_view(ModelView(About, db.session))
admin.add_view(ModelView(Inspiration, db.session))
admin.add_view(ModelView(PrintedSource, db.session))
admin.add_view(ModelView(OnlineSource, db.session))
admin.add_view(ModelView(ImageSource, db.session))


@app.route('/')
def index():
    """

    :return:
    """
    exhibitions = Exhibition.query.all()
    artworks = Artwork.query.all()
    return render_template('index.html', exhibitions=exhibitions, artworks=artworks, body_class="page-home")


@app.route('/wystawa/<int:exhibition_id>')
def exhibition(exhibition_id):

    if exhibition_id > 4:
        return render_template('404.html')
    exhibition = Exhibition.query.filter_by(id=exhibition_id).first()
    prev_exhibition = Exhibition.query.filter_by(id=exhibition_id - 1).first()
    next_exhibition = Exhibition.query.filter_by(id=exhibition_id + 1).first()
    artworks = Artwork.query.filter_by(exhibition_id=exhibition_id).all()

    return render_template('exhibition.html', exhibition_id=exhibition_id, artworks=artworks, exhibition=exhibition, prev_exhibition=prev_exhibition, next_exhibition=next_exhibition)


@app.route('/dzielo/<int:artwork_id>')
def artwork(artwork_id):
    artwork = Artwork.query.filter_by(id=artwork_id).first()
    if artwork is None:
        return render_template('404.html')
    artwork_comments = Comment.query.filter_by(artwork_id=artwork_id).order_by(Comment.date.desc()).all()
    avg = db.session.query(func.avg(Grade.grade).label('average')).first()
    average = avg[0]
    if average is None:
        average_grade = 0.0
    else:
        average_grade = round(average, 1)

    favourited = Favourite.query.filter_by(user_id=g.user.id, artwork_id=artwork_id).first()
    rated = Grade.query.filter_by(user_id=g.user.id).filter_by(artwork_id=artwork_id).first()
    rated_grade = round(float(rated.grade), 1)

    return render_template('artwork.html', artwork_id=artwork_id, artwork_comments=artwork_comments, artwork=artwork,
                           average_grade=average_grade, favourited=favourited, rated=rated, rated_grade=rated_grade)


@app.route('/logowanie', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    registered_user = User.query.filter_by(username=username).first()

    if registered_user is None or not bcrypt.check_password_hash(registered_user.password, request.form['password']):
        return redirect(url_for('login'))

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    login_user(registered_user, remember=remember_me)

    next = request.args.get('next')
    return redirect(next or url_for('index'))


@app.route('/wylogowywanie')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/rejestracja', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        error = dict()
        if request.form['username'] and request.form['name'] and request.form['surname'] and request.form['email'] \
                and request.form['phone'] and request.form['password'] and request.form['repeat-password']:
            if len(request.form['password']) < 6:
                error['password-short'] = 'Password must be at least 6 characters long.'
            if request.form['password'] != request.form['repeat-password']:
                error['password-different'] = 'Passwords do not match.'

            password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            user = User(request.form['username'], password)

            try:
                db.session.add(user)
                db.session.commit()
                profile = Profile(request.form['name'], request.form['surname'], request.form['email'],
                                  request.form['phone'], str(User.query.filter_by(username=user.username).first()))
                db.session.add(profile)
                db.session.commit()
                return redirect(url_for('index'))
            except IntegrityError:
                db.session.rollback()
                error['username-taken'] = 'This username is already taken.'
                flash(error['username-taken'], 'error')

            return render_template('register.html', error=error)
        else:
            flash('Fill all the inputs, please.', 'error')
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/dzielo/<artwork_id>/komentarz', methods=['POST', 'GET'])
def comment(artwork_id):
    if request.method == 'POST':
        error = dict()
        if request.form['content']:
            comment = Comment(request.form['content'], g.user.id, artwork_id)
            try:
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('artwork', artwork_id=artwork_id))
            except IntegrityError:
                db.session.rollback()

            return render_template('404.html', error=error)


@app.route('/dzielo/<artwork_id>/ocena', methods=['POST'])
def grade(artwork_id):
    if request.method == 'POST':
        error = dict()
        if request.form['grade']:
            grade = Grade(request.form['grade'], g.user.id, artwork_id)
            active_grade = Grade.query.filter_by(user_id=g.user.id).filter_by(artwork_id=artwork_id).first()
            if active_grade is None:
                try:
                    db.session.add(grade)
                    db.session.commit()
                    return redirect(url_for('artwork', artwork_id=artwork_id))
                except IntegrityError:
                    db.session.rollback()
            elif active_grade is not None:
                try:
                    active_grade.grade = request.form['grade']
                    db.session.commit()
                    return redirect(url_for('artwork', artwork_id=artwork_id))
                except IntegrityError:
                    db.session.rollback()

            return render_template('404.html', error=error)


@app.route('/dzielo/<artwork_id>/ulubione', methods=['POST'])
def favourite(artwork_id):
    if request.method == 'POST':
        error = dict()
        if request.form['favourite']:
            favourite = Favourite(g.user.id, artwork_id)
            fav = Favourite.query.filter_by(user_id=g.user.id).filter_by(artwork_id=artwork_id).first()
            if fav is None:
                try:
                    db.session.add(favourite)
                    db.session.commit()
                    return redirect(url_for('artwork', artwork_id=artwork_id))
                except IntegrityError:
                    db.session.rollback()
            elif fav is not None:
                try:
                    db.session.delete(fav)
                    db.session.commit()
                    return redirect(url_for('artwork', artwork_id=artwork_id))
                except IntegrityError:
                    db.session.rollback()

            return render_template('404.html', error=error)


@app.route('/profil/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    profile = Profile.query.filter_by(user_id=user_id).first()
    favourites = Favourite.query.filter_by(user_id=user_id).all()
    grades = Grade.query.filter_by(user_id=user_id).all()

    return render_template('profile.html', user_id=user_id, user=user, profile=profile, favourites=favourites, grades=grades, body_class="page-profile")


@app.route('/profil/edycja', methods=['POST', 'GET'])
@login_required
def edit():
    user = User.query.filter_by(id=g.user.id).first()
    profile = Profile.query.filter_by(user_id=g.user.id).first()

    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_name = request.form.get('new_name')
        new_surname = request.form.get('new_surname')
        new_email = request.form.get('new_email')
        new_phone = request.form.get('new_phone')

        user.username = new_username
        profile.name = new_name
        profile.surname = new_surname
        profile.email = new_email
        profile.phone = new_phone

        try:
            db.session.commit()
            return redirect(url_for('profile', user_id=g.user.id))
        except IntegrityError:
            db.session.rollback()

        return render_template('404.html')

    return render_template('edit_profile.html', user=user, profile=profile)


@app.route('/profil/haslo', methods=['POST', 'GET'])
@login_required
def change():
    user = User.query.filter_by(id=g.user.id).first()
    if request.method == 'GET':
        return render_template('change_pswd.html', user=user)

    old_password = request.form.get('old_password')
    new_password_1 = request.form.get('new_password_1')
    new_password_2 = request.form.get('new_password_2')

    if not bcrypt.check_password_hash(user.password, old_password) or (new_password_1 != new_password_2):
        return redirect(url_for('change_pswd'))
    else:
        user.password = bcrypt.generate_password_hash(new_password_1).decode('utf-8')
        try:
            db.session.commit()
            return redirect(url_for('profile', user_id=g.user.id))
        except IntegrityError:
            db.session.rollback()

        return render_template('404.html')


@app.route('/profil/usuwanie', methods=['POST', 'GET'])
@login_required
def delete_profile():
    user = User.query.get(g.user.id)
    if request.method == "POST":
        try:
            logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()

    elif request.method == "GET":
        return render_template('delete_profile.html', user=user)


@app.route('/o-serwisie')
def about():
    about = About.query.all()
    return render_template('about.html', about=about)


@app.route('/inspiracje')
def inspirations():
    inspirations = Inspiration.query.all()
    return render_template('inspirations.html', inspirations=inspirations)


@app.route('/bibliografia')
def bibliography():
    printed_source = PrintedSource.query.all()
    online_source = OnlineSource.query.all()
    image_source = ImageSource.query.all()
    return render_template('bibliography.html', printed_source=printed_source, online_source=online_source, image_source=image_source)



