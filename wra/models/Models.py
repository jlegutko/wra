from wra import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('user', lazy=True))

    def __init__(self, username, password, role_id=1):
        self.username = username
        self.password = password
        self.role_id = role_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.username


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(150))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.id


class Profile(db.Model):
    __tablename__='profile'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(155), nullable=False)
    surname = db.Column(db.String(155), nullable=False)
    email = db.Column(db.String(155), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('profile', lazy=True))

    def __init__(self, name, surname, email, phone, user_id):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.user_id = user_id

    def __repr__(self):
        return self.id


class Artwork(db.Model):
    __tablename__='artwork'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_name = db.Column(db.String(155), nullable=False)
    author_surname = db.Column(db.String(155), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    technique = db.Column(db.String(155))
    size = db.Column(db.String(45))
    description = db.Column(db.Text, nullable=False)
    detail_1 = db.Column(db.Text, nullable=False)
    detail_2 = db.Column(db.Text, nullable=False)
    exhibition_id = db.Column(db.Integer, db.ForeignKey('exhibition.id'), nullable=False)
    exhibition = db.relationship('Exhibition', backref=db.backref('artwork', lazy=True))

    def __init__(self, title, author_name, author_surname, year, description, detail_1, detail_2, exhibition_id, technique=None, size=None):
        self.title = title
        self.author_name = author_name
        self.author_surname = author_surname
        self.year = year
        self.technique = technique
        self.size = size
        self.description = description
        self.detail_1 = detail_1
        self.detail_2 = detail_2
        self.exhibition_id = exhibition_id

    def __repr__(self):
        return str(self.id)


class Exhibition(db.Model):
    __tablename__='exhibition'
    id = db.Column('id', db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, year, title, description, date=None):
        self.year = year
        self.date = date
        self.title = title
        self.description = description

    def __repr__(self):
        return '<User %r>' % self.title


class Picture(db.Model):
    __tablename__='picture'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    alt = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('picture', lazy=True))
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    artwork = db.relationship('Artwork', backref=db.backref('picture', lazy=True))

    def __init__(self, name, alt, category_id, artwork_id):
        self.name = name
        self.alt = alt
        self.category_id = category_id
        self.artwork_id = artwork_id

    def __repr__(self):
        return str(self.id)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name


class Comment(db.Model):
    __tablename__='comment'
    id = db.Column('id', db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment', lazy=True))
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    artwork = db.relationship('Artwork', backref=db.backref('comment', lazy=True))

    def __init__(self, content, user_id, artwork_id):
        self.content = content
        self.user_id = user_id
        self.artwork_id = artwork_id

    def __repr__(self):
        return str(self.id)


class Grade(db.Model):
    __tablename__='grade'
    id = db.Column('id', db.Integer, primary_key=True)
    grade = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('grade', lazy=True))
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    artwork = db.relationship('Artwork', backref=db.backref('grade', lazy=True))

    def __init__(self, grade, user_id, artwork_id):
        self.grade = grade
        self.user_id = user_id
        self.artwork_id = artwork_id

    def __repr__(self):
        return str(self.id)


class Favourite(db.Model):
    __tablename__='favourite'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('favourite', lazy=True))
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    artwork = db.relationship('Artwork', backref=db.backref('favourite', lazy=True))

    def __init__(self, user_id, artwork_id):
        self.user_id = user_id
        self.artwork_id = artwork_id

    def __repr__(self):
        return str(self.id)


class About(db.Model):
    __tablename__='about'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture_name = db.Column(db.String(255))
    picture_alt = db.Column(db.String(255))

    def __init__(self, title, description, picture_name=None, picture_alt=None):
        self.title = title
        self.description = description
        self.picture_name = picture_name
        self.picture_alt = picture_alt

    def __repr__(self):
        return str(self.id)


class Inspiration(db.Model):
    __tablename__='inspiration'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(300), nullable=False)

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __repr__(self):
        return str(self.id)


class PrintedSource(db.Model):
    __tablename__ = 'printed_source'
    id = db.Column('id', db.Integer, primary_key=True)
    author = db.Column(db.String(400))
    joint_publication = db.Column(db.Boolean)
    title = db.Column(db.String(300), nullable=False)
    translation = db.Column(db.String(200))
    collection = db.Column(db.String(200))
    edit = db.Column(db.String(200))
    publisher = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, publisher, year, title, author=None, translation=None, collection=None, edit=None, joint_publication=False):
        self.author = author
        self.joint_publication = joint_publication
        self.title = title
        self.translation = translation
        self.collection = collection
        self.edit = edit
        self.publisher = publisher
        self.year = year

    def __repr__(self):
        return str(self.id)


class OnlineSource(db.Model):
    __tablename__ = 'online_source'
    id = db.Column('id', db.Integer, primary_key=True)
    author = db.Column(db.String(400))
    title = db.Column(db.String(300), nullable=False)
    publisher = db.Column(db.String(200))
    date = db.Column(db.Date)
    url = db.Column(db.String(300), nullable=False)
    access = db.Column(db.Date, nullable=False)

    def __init__(self, title, url, access, author=None, publisher=None, date=None):
        self.author = author
        self.title = title
        self.publisher = publisher
        self.date = date
        self.url = url
        self.access = access

    def __repr__(self):
        return str(self.id)


class ImageSource(db.Model):
    __tablename__ = 'image_source'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    author = db.Column(db.String(400))
    url = db.Column(db.String(300), nullable=False)
    access = db.Column(db.Date, nullable=False)

    def __init__(self, title, description, url, access, author=None):
        self.title = title
        self.description = description
        self.author = author
        self.url = url
        self.access = access

    def __repr__(self):
        return str(self.id)