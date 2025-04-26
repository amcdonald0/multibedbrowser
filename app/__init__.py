from flask import Flask
from app.config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
 
#import route files to register routes
from . import search
from . import upload
from . import users
from . import login
