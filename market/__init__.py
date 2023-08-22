import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, configure_uploads

from market.celery_utils import make_celery

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db:5432/market"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'marker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '06a09495199cd7ea9ff14c79'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')  # you'll need to create a folder named uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
celery = make_celery(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes
