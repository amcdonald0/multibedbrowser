#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)
 
#import route files to register routes
from .import search
from .import upload
from .import users
from .import login


