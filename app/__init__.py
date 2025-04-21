#!/usr/bin/env python3

from flask import Flask, render_template, request, Template
import sys
import mariadb

#import route files to register routes
from .import search
from .import upload
from .import users
from .import login

app = Flask(__name__)
 
def query_db():

    # connect to database on host
    return mariadb.connect(
        host='bioed-new.bu.edu',
        port=4253,
        database='miRNA',
        user='aretham',
        password='WaitWell024!'
    )
