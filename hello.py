from unicodedata import name
from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

@app.route("/")

@app.route("/")
def content():
    with open('Manifests/ShipCase5.txt', mode = 'r', encoding= 'utf-8-sig') as f:
        lines = f.readlines() # list containing lines of file
        columns = ['position', 'weight', 'description']
        infoList = []

        i = 1
        for line in lines:
            line = line.strip() # remove the leading/trailing white spaces
            if line:
                d = {}
                data = [item.strip() for item in line.split(',(?![^\[]*])')]
                # print(data)
                for index, elem in enumerate(data):
                    print(index)
                    print(data[index])
                    # d[columns[index]] = data[index]
            infoList.append(d)
    return render_template('hello.html', text = infoList)


# def hello_world(name=None):
#     return render_template('hello.html', name=name)