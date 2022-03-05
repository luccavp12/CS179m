import json

sampleJson = 0 #Pass in JSON here

def balance(sampleJson):
    right_weight, left_weight, maxWeight, max_Index, isBalanced, total = getWeights(sampleJson)
    balance_ratio = left_weight/right_weight
    best_balance = 100000.0 #This value will hold the ratio closest to balanced
    best_index = ""
    curr_balance = 100000.0 #This value will hold the ratio of the containers we are currently considering swapping.
    
    if isBalanced == True: #When ship is balanced
        print("The ship is already balanced!")
        
    while(balance_ratio > 1.1 or balance_ratio < .9):
        if balance_ratio > 1.1: #Left side is heavier we need to move something from here to right side
            
            for i in range(8,0,-1):
                for j in range(6,0,-1):
                    left_cont = makeIndex(i,j) #left_cont is just the index so we can access the weight values
                    new_left = left_weight - sampleJson[left_cont]["weight"]
                    new_right = right_weight + sampleJson[left_cont]["weight"]
                    curr_balance = new_left/new_right
                    if curr_balance < 1.1 and curr_balance > 0.9:
                        #MOVE left_cont to nearest rightside spot CODE MUST BREAK HERE SINCE WE BALANCED THE SHIP
                    else:
                        if abs(curr_balance-1) < abs(best_balance-1):
                            best_balance = curr_balance
                            best_index = left_cont
                            
            #If we made it here in our code that means that no move balanced the ship, so we will make the best move we can currently make.
            #MOVE best_index to the nearest rightside spot, and continue the while loop.
            
        if balance_ratio < .9: #Right side is heavier we need to move something from here to left side.
            
            for i in range(8,0,-1):
                for j in range(7,13):
                    right_cont = makeIndex(i,j)
                    new_right = right_weight - sampleJson[right_cont]["weight"]
                    new_left = left_weight + sampleJson[right_cont]["weight"]
                    curr_balance = new_left/new_right
                    if curr_balance < 1.1 and curr_balance > 0.9:
                        #Move right_cont to nearest leftside spot CODE MUST BREAK HERE SINCE WE BALANACED THE SHIP
                    else:
                        if abs(curr_balance-1) < abs(best_balance-1):
                            best_balance = curr_balance
                            best_index = right_cont
                            
            #If we made it here in our code that means that no move balanced the ship, so we will make the best move we can currently make.
            #Move best_index to the nearest leftside spot, and continue the while loop.
            
        #After making some sort of change by either doing the right and left movement, we need to recalculate balance_ratio.
        left_weight = getLeftWeight(sampleJson)
        right_weight = getRightWeight(sampleJson)
        balance_ratio = left_weight/right_weight
#----------------------------------------------------------balance() ends here--------------------------------------------------------------#
    

#----------------------------------------------------------Helper-Functions-----------------------------------------------------------------#
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
    
    if left_weight/right_weight < 1.1 and left_weight/right_weight > .9:
        isBalanced = True  
    
    return right_weight, left_weight, maxWeight, max_Index, isBalanced, total
            
            
    