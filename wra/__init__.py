from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import markdown
from flask import Markup


app = Flask(__name__)

md = markdown.Markdown(
    extensions=['footnotes']
)


@app.template_filter('md_footnotes')
def md_foootnotes(text):
    return Markup(md.reset().convert(text))


@app.template_filter('date_format')
def date_format(date):
    return date.strftime("%d.%m.%Y")


# BCrypt
bcrypt = Bcrypt(app)

# SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://jlegutko:lisizawodnik18@localhost/wra'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


from wra.models.Models import User, Role, Profile, Artwork, Exhibition, Picture, Category, Comment, Grade, Favourite, \
    About, Inspiration, PrintedSource, OnlineSource, ImageSource


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Secret key
app.secret_key = 'C~\xb2\x95\x00:\xca\xc8b\x83\x89\xee\xf7)w&\xed\x96\xbe\x13\xfd\x88\x92\x81'

login_manager.login_view = 'login'


from wra import views