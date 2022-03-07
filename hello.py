from crypt import methods
from unicodedata import name
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import make_response
from datetime import datetime
from datetime import date
import re
import json
#import easygui

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
    #manifestPath = easygui.fileopenbox()                                            # Prompts the user with the file explorer to choose a manifest
    #print(manifestPath)
    manifestPath = "Manifests/ShipCase5.txt"                     
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

@app.route("/balance")
def balance():
    #manifestPath = easygui.fileopenbox()                                            # Prompts the user with the file explorer to choose a manifest
    #print(manifestPath)
    manifestPath = "Manifests/ShipCase4.txt"                     
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
    return render_template('balance.html', text = infoList)

# algrithm() is the proper format of how a function should handle accepting the json and returning it 
# CURRENTLY UNUSED
@app.route("/algorithm", methods=["POST"])
def algorithm():
    # This is where we can implement the python coding for algorithm
    req = request.get_json()
    print("Printing JSON of changes to be made")
    print(req)

    res = make_response(jsonify({
            "1": {"weight": 110, "name": "toys"},
            "2": {"weight": 90, "name": "medicine"},
            "3": {"weight": 300, "name": "car parts"}
        }), 200)
    # res = make_response(jsonify({"bruh":"hello"}   ), 200)

    return res

# Where the manifest json is sent in correct format, needing to be balanced
@app.route("/balanceAlgorithm", methods=["POST"])
def balanceAlgorithm():
    # This is where we can implement the python coding for algorithm
    req = request.get_json()
    print("Printing JSON of changes to be made")
    print(req)

    # ADD BALANCING FUNCTION HERE

    # RETURN JSON OF CORRECT MOVES HERE
    res = make_response(jsonify({
            "1": {
                "origin": "[05,03]", 
                "destination": "[02,02]"
            },
            "2": {
                "origin": "[01,08]", 
                "destination": "[01,09]"
            },
            "3": {
                "origin": "[02,01]", 
                "destination": "[02,06]"
            }
        }), 200)

    return res

# Where the manifest json is sent in correct format, needing to be balanced
@app.route("/operationsAlgorithm", methods=["POST"])
def operationsAlgorithm():
    # This is where we can implement the python coding for algorithm
    req = request.get_json()
    print("Printing JSON of changes to be made")
    print(req)

    # ADD BALANCING FUNCTION HERE

    # RETURN JSON OF CORRECT MOVES HERE
    res = make_response(jsonify({
            "1": {
                "condition": "0",
                "origin": "[01,01]", 
                "destination": "[01,02]"
            },
            "2": {
                "condition": "1",
                "destination": "[01,06]"
            },
            "3": {
                "condition": "2",
                "destination": "[03,06]"
            }
        }), 200)

    return res