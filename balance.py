import json

sampleJson = 0 #Pass in JSON here

def balance():
  l_weight = getLeftWeight(sampleJson)
  r_weight = getRightWeight(sampleJson)
  balance = max(l_weight/r_weight, r_weight/l_weight)
  if balance >= 1.1:
    print("Unbalanced")
  else:
    print("Balanced!")


#------------------Helper-Functions-------------------------#
def checkDesc(y, x, sampleJson):
  if x > 9:
    index = "[0"+ str(y) + "," + str(x) + "]"
  else:
    index = "[0"+ str(y) + ",0" + str(x) + "]"
  return sampleJson[index]["description"]

def ifLeftEmpty(sampleJson):
  for i in range(1):
    for j in range(6):
      index = "[0"+ str(i+1) + ",0" + str(j+1) + "]"
      if checkDesc(i+1,j+1,sampleJson) == "UNUSED":
        return index
  return False

def getLeftWeight(sampleJson):
  total = 0
  for i in range(1):
    for j in range(6):
      index = "[0"+ str(i+1) + ",0" + str(j+1) + "]"
      total += int(sampleJson[index]["weight"])
  return total

def ifRightEmpty(sampleJson):
  for i in range(1):
    for j in range(6):
      if j > 2:
        index = "[0"+ str(i+1) + "," + str(j+7) + "]"
      else:
        index = "[0"+ str(i+1) + ",0" + str(j+7) + "]"
      if checkDesc(i+1,j+7,sampleJson) == "UNUSED":
        return index
  return False

def getRightWeight(sampleJson):
  total = 0
  for i in range(1):
    for j in range(6):
      if j > 2:
        index = "[0"+ str(i+1) + "," + str(j+7) + "]"
      else:
        index = "[0"+ str(i+1) + ",0" + str(j+7) + "]"
      total += int(sampleJson[index]["weight"])
  return total