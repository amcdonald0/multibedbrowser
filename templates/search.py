#!/usr/bin/env python3

from flask import Flask, render_template, request
import json
import mariadb

app = Flaks(__search__)

@app.route('/')
def home():
    return render_template("search.html")

@app.route('/projects')
def get_projects():

    query1 = """
    SELECT * project_name
    FROM Projects; 
    """
    return