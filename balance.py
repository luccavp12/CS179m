import json

sampleJson = 0 #Pass in JSON here

def balance(sampleJson):
    l_weight = getLeftWeight(sampleJson)
    r_weight = getRightWeight(sampleJson)
    weight_diff = 0
    if r_weight > l_weight:
        right_heavy = True
    else:
        right_heavy = False
    balance = max(l_weight/r_weight, r_weight/l_weight)
    if balance > 1.1:
        
        # Attempt 1 at balancing function, check layer 1,
        # if right_heavy is True:
        #     weight_diff = r_weight-l_weight
        #     for i in range(1,9):
        #         for j in range(7,13):
        #             heavy_container = sampleJson[makeIndex(i,j)]["weight"]
        #             for y in range(1,9):
        #                 for x in range(1,7):
        #                     light_container = sampleJson[makeIndex(y,x)]["weight"]
        #                     balance_level = (getRightWeight() - heavy_container + light_container) / (getLeftWeight() - light_container + heavy_container)
        #                     if balance_level <= 1.1 and balance_level >= .9:
        #                         #swap(makeIndex(i,j),makeIndex(y,x))
        #                         #BREAK -- balance might need to be a while loop, after first run of swap, break so that we go back to top of loop
        # else:
        #     weight_diff = l_weight-r_weight
        #     for i in range(1,9):
        #         for j in range(1,7):
        #             heavy_container = sampleJson[makeIndex(i,j)]["weight"]
        #             for y in range(1,9):
        #                 for x in range(7,13):
        #                     light_container = sampleJson[makeIndex(y,x)]["weight"]
        #                     balance_level = (getLeftWeight() - heavy_container + light_container) / (getRightWeight() - light_container + heavy_container)
        #                     if balance_level <= 1.1 and balance_level >= .9:
        #                         #swap(makeIndex(i,j),makeIndex(y,x))


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
            
            
    