import json
operations_dict = 0
sampleJson = 0

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
    global tot_distance
    tot_distance += distance
    global moves
    moves += 1
    global move_Dict
    move_Dict[str(moves)] = {}
    move_Dict[str(moves)]["origin"] = start_index
    move_Dict[str(moves)]["destination"] = goal_index
    
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


#-----------------------------------------------------------------------MAIN CODE--------------------------------------------------------------------------------#


for i in operations_dict:
    index = i
    y, x = index[1:3], index[4:6]
    if operations_dict[i]["loadUnload"] == 0: #Unload 
        move(y,x,8,1,sampleJson)
        sampleJson[i]["weight"] = "00000"
        sampleJson[i]["description"] = "UNUSED"
        tot_distance += 3
    else: #Load
        tot_distance += abs(8-y) + abs(1-x) + 3
        sampleJson[i]["weight"] = "00000"
        sampleJson[i]["description"] = "NEWCONTAINER"