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
    with open('Manifests/ShipCase5.txt', mode = 'r', encoding= 'utf-8-sig') as f:
        lines = f.readlines() # list containing lines of file
        columns = ['position', 'weight', 'description']
        infoList = []

        i = 1
        for line in lines:
            line = line.strip() # remove the leading/trailing white spaces
            if line:
                d = {}
                data = [item.strip() for item in re.split(',(?![^\[]*])', line)]
                for index, elem in enumerate(data):
                    d[columns[index]] = data[index]
            infoList.append(d)
    return render_template('operations.html', text = infoList)

