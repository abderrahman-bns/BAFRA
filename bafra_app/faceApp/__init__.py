from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = 'G:/PROJET/PYTHON/FACE_RECOGNITION/Real_time_face_recognition_with_GPU_FLASK_V2/faceApp/static/dataset/vid/'

app.config['SECRET_KEY'] = "5791628bb0b13ce0c676dfde280ba245"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/dbflask'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "abderrahmanbns21@gmail.com"
app.config['MAIL_PASSWORD'] = "xDEVELYNNx0771+-*"
mail = Mail(app)

from faceApp import routes