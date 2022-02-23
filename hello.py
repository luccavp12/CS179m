from crypt import methods
from unicodedata import name
from flask import Flask, url_for, redirect, request, render_template
import re
import json
import easygui

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/operations")
def operations():
    manifestPath = easygui.fileopenbox()    # Prompts the user with the file explorer to choose a manifest
    print(manifestPath)                     
    with open(manifestPath, mode = 'r', encoding= 'utf-8-sig') as f:    # Uses manifest path to open file
        lines = f.readlines()   # List containing lines of file
        columns = ['position', 'weight', 'description'] # Creates a list of column names
        infoList = []

        i = 1
        for line in lines:
            line = line.strip() # Remove the leading/trailing white spaces
            if line:
                d = {}
                data = [item.strip() for item in re.split(',(?![^\[]*])', line)]    # Uses regex to split the manifest data by the correct commas
                for index, elem in enumerate(data):
                    d[columns[index]] = data[index]
            infoList.append(d)
    return render_template('operations.html', text = infoList)

