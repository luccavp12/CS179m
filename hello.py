from crypt import methods
from curses import nonl
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
    return render_template('balance.html', text = infoList)

# algrithm() is the proper format of how a function should handle accepting the json and returning it 
# CURRENTLY UNUSED
# @app.route("/algorithm", methods=["POST"])
# def algorithm():
#     # This is where we can implement the python coding for algorithm
#     req = request.get_json()
#     print("Printing JSON of changes to be made")
#     print(req)

#     res = make_response(jsonify({
#             "1": {"weight": 110, "name": "toys"},
#             "2": {"weight": 90, "name": "medicine"},
#             "3": {"weight": 300, "name": "car parts"}
#         }), 200)
#     # res = make_response(jsonify({"bruh":"hello"}   ), 200)

#     return res

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
    print("Printing JSON of changes to be made in operationsAlgo")
    print(req)

    # ADD load/unload FUNCTION HERE

    moves = 0
    move_Dict = {}
    tot_distance = 0        
            
    #------------------------------------------------------Helper Functions------------------------------------------------------------#
    def move(start_y, start_x, dest_y, dest_x, sampleJson, flag=0):
        
        clearPath(start_y, start_x, sampleJson) #This function will ensure we only move a container once all containers above it are gone
        
        if flag == 1: # This is for when we move containers to the nearest unused spot, since it can change while in clearPath, we must reassess what is the nearestUnused spot
            dest_y, dest_x = findNearestUnused(start_y, start_x, sampleJson)
            move(start_y, start_x, dest_y, dest_x, sampleJson)
            return
        
        start_index = makeIndex(start_y, start_x)
        goal_index = makeIndex(dest_y, dest_x)
        start_Weight = sampleJson[start_index]["weight"]
        start_Desc = checkDesc(start_y, start_x, sampleJson)
        
        distance = abs(start_y-dest_y) + abs(start_x-dest_x)
        nonlocal tot_distance
        tot_distance += distance
        nonlocal moves
        moves += 1
        nonlocal move_Dict
        move_Dict[str(moves)] = {}
        move_Dict[str(moves)]["origin"] = start_index
        move_Dict[str(moves)]["destination"] = goal_index
        move_Dict[str(moves)]["condition"] = 0
        
        #We only move to UNUSED containers, so by swapping it simulates the movement perfectly
        sampleJson[start_index]["weight"] = sampleJson[goal_index]["weight"]
        sampleJson[start_index]["description"] = sampleJson[goal_index]["description"]
        
        sampleJson[goal_index]["weight"] = start_Weight
        sampleJson[goal_index]["description"] = start_Desc
        

    def clearPath(y, x, sampleJson):                                # Will move containers above our start container if nessessary-
        if y < 8:
            if checkDesc(y+1,x,sampleJson) != "UNUSED":       # URGENT: Check if y != 8 before checkDesc
                dest_y, dest_x = findNearestUnused(y+1, x, sampleJson)
                move(y+1, x, dest_y, dest_x, sampleJson, 1)

    def findNearestUnused(y,x,sampleJson):                          # Finds nearest column to move blocking containers to
        if x < 7:                                                   # If container is on the left half, we ideally want to move it left
            if x == 1:                                              # Leftmost column can't move more left
                return findFirstRightCol(y, x, sampleJson)
            else:       
                dest_y, dest_x = findFirstLeftCol(y, x, sampleJson) # If no space on left, then search to the right
                if dest_y == -1 and dest_x == -1:
                    return findFirstRightCol(y, x, sampleJson)
                else:
                    return dest_y, dest_x
        else:                                                       # Containers on right half want to go more right
            if x == 12:                                             # Rightmost container can't move more right
                return findFirstLeftCol(y, x, sampleJson)           
            else:                                                   # If no space on right, then search to the left
                dest_y, dest_x = findFirstRightCol(y, x, sampleJson)
                if dest_y == -1 and dest_x == -1:
                    return findFirstLeftCol(y, x, sampleJson)
                else:
                    return dest_y, dest_x
                
    def findFirstRightCol(y, x, sampleJson):                        # Returns y and x coordinate if there is a space available
        for i in range(x+1, 7):                                     # in the columns to the right, else, return (-1, -1) to go left
            for j in range(8):
                if checkDesc(j+1, i, sampleJson) == "UNUSED":
                    print(j+1, i)
                    return j+1, i
            return -1, -1

    def findFirstLeftCol(y, x, sampleJson):                         # Returns y and x coordinate if there is a space available 
        for i in range(x-1, 0, -1):                                 # in the columns to the left, else, return (-1, -1) to go right 
            for j in range(8):
                if checkDesc(j+1, i, sampleJson) == "UNUSED":
                    print(j+1, i)
                    return j+1, i
        return -1, -1

    def makeIndex(y, x):
        if y > 9:   # If the index if greater than 9, then we format as a double digit instead of appending a 0 to the end
            if x > 9: # Same situation as y
                index = "["+ str(y) + "," + str(x) + "]"
            else:
                index = "["+ str(y) + ",0" + str(x) + "]"
        else:
            if x > 9:
                index = "[0"+ str(y) + "," + str(x) + "]"
            else:
                index = "[0"+ str(y) + ",0" + str(x) + "]"
        return index

    def checkDesc(y, x, sampleJson): #This function will take the y and x as well as the Json we are operating on and check the description of the package
        index = makeIndex(y,x) 
        return sampleJson[index]["description"]

    def ifLeftEmpty(sampleJson): # This function needs to be workshopped into finding the nearest empty space TO FIX
        for i in range(8):
            for j in range(6,0,-1):
                index = makeIndex(i+1,j)
                if checkDesc(i+1,j,sampleJson) == "UNUSED":
                    return i+1, j
        return -1, -1

    def ifRightEmpty(sampleJson): # This function needs to be workshopped into finding the nearest empty space TO FIX
        for i in range(8):
            for j in range(7,13):
                index = makeIndex(i+1,j)
                if checkDesc(i+1,j,sampleJson) == "UNUSED":
                    return i+1, j
        return -1, -1

    def getLeftWeight(sampleJson): #This function will return as a int the entire weight of the left hand side.
        total = 0
        for i in range(8): #Height
            for j in range(6):
                index = makeIndex(i+1,j+1)
                total += int(sampleJson[index]["weight"])
        return total

    def getRightWeight(sampleJson): #This function will return as a int the entire weight of the right hand side.
        total = 0
        for i in range(8): #Height
            for j in range(6):
                index = makeIndex(i+1,j+7)
                total += int(sampleJson[index]["weight"])
                
        return total

    def getWeights(sampleJson): #This function will return 5 values, int right_weight, int left_weight, int maxWeight, string max_Index, int total, and string heavy.
        total = 0
        maxWeight = 0
        max_Index = ""
        isBalanced = False
        right_weight = getRightWeight(sampleJson)
        left_weight = getLeftWeight(sampleJson)
        
        for i in range(8):
            for j in range(12):
                index = makeIndex(i+1,j+1)
                currWeight = int(sampleJson[index]["weight"])
                total += currWeight
                if currWeight > maxWeight:
                    maxWeight = currWeight
                    max_Index = index
                    
        
        if left_weight == 0 and right_weight == 0:
            isBalanced = True
        elif left_weight == 0 or right_weight == 0:
            isBalanced = False
        elif left_weight/right_weight < 1.1 and left_weight/right_weight > .9:
            isBalanced = True
        
        return right_weight, left_weight, maxWeight, max_Index, isBalanced, total


    #-----------------------------------------------------------------------MAIN CODE--------------------------------------------------------------------------------#
    # with open('./loadUnloadTest3.json', 'r') as f:
    #     operations_dict = json.load(f)
    operations_dict = req

    #operations_dict has on layer 1: manifest, or changes. Manifest = sampleJson and operations_dict is changes
    for i in operations_dict["changes"]:
        index = i
        final_loc = makeIndex(8,1)
        y, x = int(index[1:3]), int(index[4:6])
        if operations_dict["changes"][i]["loadUnload"] == 2: #Unload 
            move(y,x,8,1,operations_dict["manifest"])
            move_Dict[str(moves)]["condition"] = 2
            move_Dict[str(moves)]["destination"] = i
            move_Dict[str(moves)]["origin"] = "NAN"
            operations_dict["manifest"][final_loc]["weight"] = "00000"
            operations_dict["manifest"][final_loc]["description"] = "UNUSED"
            tot_distance += 3
        else: #Load
            tot_distance += abs(8-y) + abs(1-x) + 3
            operations_dict["manifest"][i]["weight"] = "00000"
            operations_dict["manifest"][i]["description"] = "NEWCONTAINER"
            moves += 1
            move_Dict[str(moves)] = {}
            move_Dict[str(moves)]["origin"] = "NAN"
            move_Dict[str(moves)]["destination"] = i
            move_Dict[str(moves)]["condition"] = 1
            
    print(operations_dict["manifest"])
    print(move_Dict)

    res = make_response(jsonify(move_Dict), 200)

    return res
    # RETURN JSON OF CORRECT MOVES HERE
    # res = make_response(jsonify({
    #         "1": {
    #             "condition": "0",
    #             "origin": "[01,01]", 
    #             "destination": "[01,02]"
    #         },
    #         "2": {
    #             "condition": "1",
    #             "destination": "[01,06]"
    #         },
    #         "3": {
    #             "condition": "2",
    #             "destination": "[03,06]"
    #         }
    #     }), 200)
