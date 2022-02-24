from crypt import methods
from unicodedata import name
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from datetime import datetime
from datetime import date #Does not import
import re
import json
import easygui

app = Flask(__name__)

@app.route("/")
def sign_in():
    return render_template('sign_in.html')

@app.route("/storeCreds", methods=['GET', 'POST'])
def storeCreds():
    if request.method == 'POST':

        tag = request.form['tag']
        user = tag
        today = date.today()
        today_formated = today.strftime("%b-%d-%Y")
        time = datetime.now()
        currTime = time.strftime("%H:%M:%S")
        userlog_name = "User Logs " + today_formated + ".txt"
        
        with open("UserLogs/" + userlog_name, "a") as f:
            f.write("Login from " + user + " @ " + currTime + "\n")
            f.close()

    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/operations")
def operations():
    manifestPath = easygui.fileopenbox()                                            # Prompts the user with the file explorer to choose a manifest
    print(manifestPath)
    # manifestPath = "Manifests/ShipCase5.txt"                     
    with open(manifestPath, mode = 'r', encoding= 'utf-8-sig') as f:                # Uses manifest path to open file
        lines = f.readlines()                                                       # List containing lines of file
        columns = ['position', 'weight', 'description']                             # Creates a list of column names
        infoList = []

        i = 1
        for line in lines:
            line = line.strip()                                                     # Remove the leading/trailing white spaces
            if line:
                d = {}
                data = [item.strip() for item in re.split(',(?![^\[]*])', line)]    # Uses regex to split the manifest data by the correct commas
                for index, elem in enumerate(data):
                    d[columns[index]] = data[index]
            infoList.append(d)
    return render_template('operations.html', text = infoList)

