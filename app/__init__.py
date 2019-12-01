from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)#Starts the flask app
app.config.from_object(Config)#Configures the app
login = LoginManager(app)#Begins the login manager

import routes