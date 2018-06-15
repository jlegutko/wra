from wra import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    profile = db.relationship('Profile', backref=db.backref('user', lazy=True), cascade="all, delete-orphan", single_parent=True)
    comment = db.relationship('Comment', backref=db.backref('user', lazy=True), cascade="all, delete-orphan",
                              single_parent=True)
    grade = db.relationship('Grade', backref=db.backref('user', lazy=True), cascade="all, delete-orphan",
                              single_parent=True)
    favourite = db.relationship('Favourite', backref=db.backref('user', lazy=True), cascade="all, delete-orphan",
                              single_parent=True)

    def __init__(self, username=None, password=None, role_id=2):
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
        return self.id

    def __repr__(self):
        return str(self.id)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    user = db.relationship('User', backref=db.backref('role', lazy=True), cascade="all, delete-orphan", single_parent=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name


class Profile(db.Model):
    __tablename__='profile'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(155), nullable=False)
    surname = db.Column(db.String(155), nullable=False)
    email = db.Column(db.String(155), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name=None, surname=None, email=None, phone=None, user_id=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.user_id = user_id

    def __repr__(self):
        return str(self.id)


class Artwork(db.Model):
    __tablename__='artwork'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    technique = db.Column(db.String(155))
    size = db.Column(db.String(45))
    description = db.Column(db.Text, nullable=False)
    detail_1 = db.Column(db.Text)
    detail_2 = db.Column(db.Text)
    exhibition_id = db.Column(db.Integer, db.ForeignKey('exhibition.id'), nullable=False)
    picture = db.relationship('Picture', backref=db.backref('artwork', lazy=True), cascade="all, delete-orphan",
                              single_parent=True)
    comment = db.relationship('Comment', backref=db.backref('artwork', lazy=True), cascade="all, delete-orphan",
                              single_parent=True)
    grade = db.relationship('Grade', backref=db.backref('artwork', lazy=True), cascade="all, delete-orphan",
                              single_parent=True)
    favourite = db.relationship('Favourite', backref=db.backref('artwork', lazy=True), cascade="all, delete-orphan",
                              single_parent=True)

    def __init__(self, title=None, author_name=None, author_surname=None, year=None, description=None, detail_1=None,
                 detail_2=None, exhibition_id=None, technique=None, size=None):
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
        return str(self.title)


class Exhibition(db.Model):
    __tablename__='exhibition'
    id = db.Column('id', db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(300), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    artwork = db.relationship('Artwork', backref=db.backref('exhibition', lazy=True), cascade="all, delete-orphan", single_parent=True)

    def __init__(self, year=None, title=None, short_description=None, description=None):
        self.year = year
        self.title = title
        self.short_description = short_description
        self.description = description

    def __repr__(self):
        return self.title


class Picture(db.Model):
    __tablename__='picture'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    alt = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)

    def __init__(self, name=None, alt=None, category_id=None, artwork_id=None):
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
    picture = db.relationship('Picture', backref=db.backref('category', lazy=True), cascade="all, delete-orphan",
                              single_parent=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name


class Comment(db.Model):
    __tablename__='comment'
    id = db.Column('id', db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)

    def __init__(self, content=None, user_id=None, artwork_id=None):
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
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)

    def __init__(self, grade=None, user_id=None, artwork_id=None):
        self.grade = grade
        self.user_id = user_id
        self.artwork_id = artwork_id

    def __repr__(self):
        return str(self.id)


class Favourite(db.Model):
    __tablename__='favourite'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)

    def __init__(self, user_id=None, artwork_id=None):
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

    def __init__(self, title=None, description=None, picture_name=None, picture_alt=None):
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
    image = db.Column(db.String(300), nullable=True)

    def __init__(self, title=None, url=None):
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

    def __init__(self, publisher=None, year=None, title=None, author=None, translation=None, collection=None, edit=None,
                 joint_publication=False):
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

    def __init__(self, title=None, url=None, access=None, author=None, publisher=None, date=None):
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

    def __init__(self, title=None, description=None, url=None, access=None, author=None):
        self.title = title
        self.description = description
        self.author = author
        self.url = url
        self.access = access

    def __repr__(self):
        return str(self.id)