import json

sampleJson = 0 #Pass in JSON here

def balance(sampleJson):
    x

#------------------Helper-Functions-------------------------#
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
        for j in range(6):
            index = makeIndex(i+1,j+1)
            if checkDesc(i+1,j+1,sampleJson) == "UNUSED":
                return index
    return False

def ifRightEmpty(sampleJson): # This function needs to be workshopped into finding the nearest empty space TO FIX
    for i in range(1):
        for j in range(6):
        if j > 2:
            index = makeIndex(i+1,j+7)
        else:
            index = makeIndex(i+1,j+7)
        if checkDesc(i+1,j+7,sampleJson) == "UNUSED":
            return index
    return False

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

def getWeights(sampleJson): #This function will return 5 values, int right_weight, int left_weight, int maxWeight, string max_Index, and string heavy.
    total = 0
    maxWeight = 0
    max_Index = ""
    heavySide = ""
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
    
    if right_weight > left_weight:
        heavy = "Right"   
    
    if left_weight > left_weight:
        heavy = "Left"
        
    if right_weight > left_weight:
        heavy = "Balanced"      
    
    return right_weight, left_weight, maxWeight, max_Index, heavy
            
            
    