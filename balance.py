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
        if right_heavy is True:
            weight_diff = r_weight-l_weight
            for i in range(1,9):
                for j in range(7,13):
                    heavy_container = sampleJson[makeIndex(i,j)]["weight"]
                    for y in range(1,9):
                        for x in range(1,7):
                            light_container = sampleJson[makeIndex(y,x)]["weight"]
                            balance_level = (getRightWeight() - heavy_container + light_container) / (getLeftWeight() - light_container + heavy_container)
                            if balance_level <= 1.1 and balance_level >= .9:
                                #swap(makeIndex(i,j),makeIndex(y,x))
        else:
            weight_diff = l_weight-r_weight
            for i in range(1,9):
                for j in range(1,7):
                    heavy_container = sampleJson[makeIndex(i,j)]["weight"]
                    for y in range(1,9):
                        for x in range(7,13):
                            light_container = sampleJson[makeIndex(y,x)]["weight"]
                            balance_level = (getLeftWeight() - heavy_container + light_container) / (getRightWeight() - light_container + heavy_container)
                            if balance_level <= 1.1 and balance_level >= .9:
                                #swap(makeIndex(i,j),makeIndex(y,x))


#------------------Helper-Functions-------------------------#
def makeIndex(y, x):
    if y > 9:
        if x > 9:
            index = "["+ str(y) + "," + str(x) + "]"
        else:
            index = "["+ str(y) + ",0" + str(x) + "]"
    else:
        if x > 9:
            index = "[0"+ str(y) + "," + str(x) + "]"
        else:
            index = "[0"+ str(y) + ",0" + str(x) + "]"
    return index

def checkDesc(y, x, sampleJson):
    index = makeIndex(y,x)
    return sampleJson[index]["description"]

def ifLeftEmpty(sampleJson):
    for i in range(8):
        for j in range(6):
            index = makeIndex(i+1,j+1)
            if checkDesc(i+1,j+1,sampleJson) == "UNUSED":
                return index
    return False

def getLeftWeight(sampleJson):
    total = 0
    for i in range(1):
        for j in range(6):
            index = makeIndex(i+1,j+1)
            total += int(sampleJson[index]["weight"])
    return total

def ifRightEmpty(sampleJson):
    for i in range(1):
        for j in range(6):
        if j > 2:
            index = makeIndex(i+1,j+7)
        else:
            index = makeIndex(i+1,j+7)
        if checkDesc(i+1,j+7,sampleJson) == "UNUSED":
            return index
    return False

def getRightWeight(sampleJson):
    total = 0
    for i in range(1):
        for j in range(6):
        if j > 2:
            index = makeIndex(i+1,j+7)
        else:
            index = makeIndex(i+1,j+7)
        total += int(sampleJson[index]["weight"])
    return total