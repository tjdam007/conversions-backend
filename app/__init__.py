import firebase_admin
from firebase_admin import credentials
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import ProductionConfig, TestingConfig, DevelopmentConfig
from .middleware import MiddleWare

# Instance of flask app
app = Flask(__name__)

# load Environment configurations
if app.config["ENV"] == "production":
    app.config.from_object(ProductionConfig())
elif app.config["ENV"] == "testing":
    app.config.from_object(TestingConfig())
else:
    app.config.from_object(DevelopmentConfig())
app.wsgi_app = MiddleWare(app.wsgi_app)

db = SQLAlchemy(app)
from rq import Queue
from worker import conn

app.queue = Queue(connection=conn)
from app.routes import conversion
from app.routes import user

cred = credentials.Certificate(app.config.get('GOOGLE_CERTIFICATE_FILE_PATH'))
firebase_admin.initialize_app(cred)
