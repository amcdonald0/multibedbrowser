#!/usr/bin/env python3

from flask import Flask, render_template, request
from app import app
import json
import sys
import mariadb

@app.route('/')
def home():
    return render_template("search.html")

@app.route('/projects', methods-["GET"])
def get_projects():
    #variables

    try:
        connection = query_db()
        cursor = connection.cursor()
        
    query1 = """
    SELECT * project_name
    FROM Projects; 
    """
    
    #execute query
    cursor