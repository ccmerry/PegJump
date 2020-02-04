# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 00:41:04 2019

@author: Connor
"""
import tkinter
#from tkinter import *
from tkinter.ttk import *
import numpy as np
import random
import pickle
import operator
import copy

root = tkinter.Tk()
root.title("Pegs")
root.geometry('500x310')

'''File with weights and bias for the neural network'''

with open('PegGameRandNeuron.pickle','rb') as handle:
    wandb = pickle.load(handle)

dNameList = ("Huey","Duey","Luey","Muey","Puey","Buey","Suey","Quey","Ruey","Ouey","Nuey","Kuey","Guey","Vuey","tDog")

Huey={}
Duey={}
Luey={}
Muey={}
Puey={}
Buey={}
Suey={}
Quey={}
Ruey={}
Ouey={}
Nuey={}
Kuey={}
Guey={}
Vuey={}
tDog={}
dFullList = (Huey,Duey,Luey,Muey,Puey,Buey,Suey,Quey,Ruey,Ouey,Nuey,Kuey,Guey,Vuey,tDog)
mutationDict = {}
#creates random weights and biases to start
def createDict(dName,stringDict):
    neurons = [15,30,30,21]
    
    layers = len(neurons)-1
    y = 0
    
    for x in range(layers):
        dName["wmat{0}".format(y+1)] = np.zeros(shape=(neurons[y+1],neurons[y]))
        dName["bmat{0}".format(y+1)] = np.zeros(shape=(neurons[y],1))
        y = y + 1
    
    for s in range(len(neurons)-1):
        dName["wmat{0}".format(s+1)] = np.random.randn(neurons[s+1],neurons[s]) * np.sqrt(2/neurons[s])
        dName["bmat{0}".format(s+1)] = np.random.randn(neurons[s+1],1) * np.sqrt(2/neurons[s])
    
    dName["dictName"] = stringDict
    dName["maxscore"] = 0

def mutateDict(dname,newdname,costError):
    neurons = [15,30,30,21]
    
    for s in range(len(neurons)-1):
        dname["wmat{0}".format(s+1)] = newdname["wmat{0}".format(s+1)] + np.random.randn(neurons[s+1],neurons[s]) * np.square(costError)
        dname["bmat{0}".format(s+1)] = newdname["bmat{0}".format(s+1)] + np.random.randn(neurons[s+1],1) * np.square(costError)

def ZeroScore(listName = dNameList):
    for x in listName:
        scoreDict[x] = 0

def setRandDict(nameList = dFullList,stringList = dNameList):
    for x,y in zip(nameList,stringList):
        createDict(x,y)
    #Huey = {}
    '''
    createDict(Huey,"Huey")
    #Duey = {}
    createDict(Duey,"Duey")
    #Luey = {}
    createDict(Luey,"Luey")
    createDict(tDog,"tDog")'''

setRandDict()

#Rows should be changeable
rows = 5

points = 0

triangle = np.zeros(shape=(rows,rows))

triangleCheck = 1

#Find sum of pegs
totalPegs = (rows*(rows+1)/2)

startPeg = random.randint(1,totalPegs)
pegCounter = 0

#custom 3 dictioanries references to compare scores
scoreDict ={}
def CreateScoreDict(stringList = dNameList):
    
    for x in dNameList:
        scoreDict[x] = 0

CreateScoreDict()

def startTriangle(startRows=rows,beginPeg = startPeg):
    pegCounter = 0
    triangleCheck = 1
    sTriangle = np.zeros(shape=(rows,rows))
    for r in range(rows):
        for c in range(rows):
            if c < triangleCheck:
                pegCounter += 1
                if pegCounter!= beginPeg:
                    sTriangle[r][c] = 1
        triangleCheck += 1
    return sTriangle
'''
triangle = startTriangle()
print(triangle)'''

def startGame(sPeg):
    sPeg = random.randint(1,totalPegs)
    print(sPeg)
    return sPeg

#Creates blank triangles for allowable jumps
downTriangle = np.zeros(shape=(rows,rows))
upTriangle = np.zeros(shape=(rows,rows))
lTriangle = np.zeros(shape=(rows,rows))
rTriangle = np.zeros(shape=(rows,rows))
dRight = np.zeros(shape=(rows,rows))
uLeft = np.zeros(shape=(rows,rows))

def triangleCheck(firstTriangle,secondTriangle,rowVar,colVar,startCount,mainTriangle = triangle,rowsCount = rows):
    checkCount = startCount
    for r in range(rowsCount - 2):
        for c in range(rowsCount):
            if c < checkCount:
                if (mainTriangle[r][c] == 1
                and mainTriangle[r + rowVar][c + colVar] == 1
                and mainTriangle[r + 2*rowVar][c + 2*colVar] == 0):
                    firstTriangle[r][c] = 1
                else:
                    firstTriangle[r][c] = 0
                if (mainTriangle[r][c] == 0
                and mainTriangle[r + rowVar][c + colVar] == 1
                and mainTriangle[r + 2*rowVar][c + 2*colVar] == 1):
                    secondTriangle[r + 2*rowVar][c + 2*colVar] = 1
                else:
                    secondTriangle[r + 2*rowVar][c + 2*colVar] = 0
        checkCount += 1

def triangleCheck2(rowVar,colVar,returnTriangle,mainTriangle,rowsCount = rows):
    checkCount = 1
    firstTriangle = np.zeros(shape=(rows,rows))
    secondTriangle = np.zeros(shape=(rows,rows))
    for r in range(rowsCount - 2):
        for c in range(rowsCount):
            if c < checkCount:
                if (mainTriangle[r][c] == 1
                and mainTriangle[r + rowVar][c + colVar] == 1
                and mainTriangle[r + 2*rowVar][c + 2*colVar] == 0):
                    firstTriangle[r][c] = 1
                else:
                    firstTriangle[r][c] = 0
                if (mainTriangle[r][c] == 0
                and mainTriangle[r + rowVar][c + colVar] == 1
                and mainTriangle[r + 2*rowVar][c + 2*colVar] == 1):
                    secondTriangle[r + 2*rowVar][c + 2*colVar] = 1
                else:
                    secondTriangle[r + 2*rowVar][c + 2*colVar] = 0
        checkCount += 1
    if returnTriangle == 1:
        return firstTriangle
    else:
        return secondTriangle

def triangleLRCheck(rowVar,colVar,returnTriangle,mTriangle,rowsCount = rows):
    checkCount = 1
    firstTriangle = np.zeros(shape=(rows,rows))
    secondTriangle = np.zeros(shape=(rows,rows))
    for r in range(rowsCount - 2):
        for c in range(rowsCount):
            if c < checkCount:
                if (mTriangle[r + 2][c] == 1
                and mTriangle[r + 2 + rowVar][c + colVar] == 1
                and mTriangle[r + 2 + 2*rowVar][c + 2*colVar] == 0):
                    firstTriangle[r + 2][c] = 1
                else:
                    firstTriangle[r + 2][c] = 0
                if (mTriangle[r + 2][c] == 0
                and mTriangle[r + 2 + rowVar][c + colVar] == 1
                and mTriangle[r + 2 + 2*rowVar][c + 2*colVar] == 1):
                    secondTriangle[r + 2 + 2*rowVar][c + 2*colVar] = 1
                else:
                    secondTriangle[r + 2 + 2*rowVar][c + 2*colVar] = 0
        checkCount += 1
    if returnTriangle == 1:
        return firstTriangle
    else:
        return secondTriangle
'''
triangleCheck(downTriangle,upTriangle,1,0,1)
triangleLRCheck(rTriangle,lTriangle,0,1,1)
triangleCheck(dRight,uLeft,1,1,1)'''

'''
colorList = ["","","","","","","","","","","","","","",""]
triangleCheck = 1
pegCounter = 0
for r in range(rows):
    for c in range(rows):
        if c < triangleCheck:
            pegCounter += 1
            if triangle[r][c] == 1:
                colorList[pegCounter-1] = "red"
            else:
                colorList[pegCounter-1] = "black"
    triangleCheck += 1
print(colorList)
redvar1 = "red"'''
'''
testLabel1 = Label(root, text = "    ", background=colorList[10])
testLabel1.grid(column=1,row=5)
testLabel2 = Label(root, text = "    ", background=colorList[11])
testLabel2.grid(column=3,row=5)
testLabel3 = Label(root, text = "    ", background=colorList[12])
testLabel3.grid(column=5,row=5)
testLabel4 = Label(root, text = "    ", background=colorList[13])
testLabel4.grid(column=7,row=5)
testLabel5 = Label(root, text = "    ", background=colorList[14])
testLabel5.grid(column=9,row=5)

testLabel6 = Label(root, text = "    ", background=colorList[6])
testLabel6.grid(column=2,row=4)
testLabel7 = Label(root, text = "    ", background=colorList[7])
testLabel7.grid(column=4,row=4)
testLabel8 = Label(root, text = "    ", background=colorList[8])
testLabel8.grid(column=6,row=4)
testLabel9 = Label(root, text = "    ", background=colorList[9])
testLabel9.grid(column=8,row=4)

testLabel10 = Label(root, text = "    ", background=colorList[3])
testLabel10.grid(column=3,row=3)
testLabel11 = Label(root, text = "    ", background=colorList[4])
testLabel11.grid(column=5,row=3)
testLabel12 = Label(root, text = "    ", background=colorList[5])
testLabel12.grid(column=7,row=3)

testLabel13 = Label(root, text = "    ", background=colorList[1])
testLabel13.grid(column=4,row=2)
testLabel14 = Label(root, text = "    ", background=colorList[2])
testLabel14.grid(column=6,row=2)

testLabel15 = Label(root, text = "    ", background=colorList[0])
testLabel15.grid(column=5,row=1)'''

'''
print(triangle)
print("Down")
print(downTriangle)
print("Up")
print(upTriangle)
print("Right")
print(rTriangle)
print("Left")
print(lTriangle)
print("Down Right")
print(dRight)
print("Up Left")
print(uLeft)'''

#points = totalPegs - sum(sum(triangle)) - 1
print("Score: {}".format(points))

#tCheck = np.zeros(shape=(rows,rows))

def jumpPeg(rowNum,colNum,mainTriangle,dList,pts=points):
    direction = dList
    if direction == "Down":
        rowVar = 1
        colVar = 0
        tCheck = triangleCheck2(rowVar,colVar,1,mainTriangle,5)
    elif direction == "Up":
        rowVar = -1
        colVar = 0
        tCheck = triangleCheck2(rowVar,colVar,2,mainTriangle,5)
    elif direction == "Left":
        rowVar = 0
        colVar = -1
        tCheck = triangleLRCheck(rowVar,colVar,2,mainTriangle,5)
    elif direction == "Right":
        rowVar = 0
        colVar = 1
        tCheck = triangleLRCheck(rowVar,colVar,1,mainTriangle,5)
    elif direction == "Down Right":
        rowVar = 1
        colVar = 1
        tCheck = triangleCheck2(rowVar,colVar,1,mainTriangle,5)
    else:
        rowVar = -1
        colVar = -1
        tCheck = triangleCheck2(rowVar,colVar,2,mainTriangle,5)
    newRow = int(rowNum)
    newCol = int(colNum)
    if(tCheck[newRow][newCol] == 1):
        mainTriangle[newRow][newCol] = 0
        mainTriangle[newRow + rowVar][newCol + colVar] = 0
        mainTriangle[newRow + rowVar*2][newCol + colVar*2] = 1
        '''
        diagonalCheck()
        udTriangleCheck()
        lrTriangleCheck()'''
        pts += 1
        #print("SUCCESS")
        return "success"
    else:
        return "fail"

def pmain(ptriangle):
    print(ptriangle)

def formData(startTriangle=triangle,formRows=rows):
    triangleCheck = 1
    rowCounter = 0
    formTriangle = np.zeros(shape=(int((formRows*(formRows+1)/2)),1))
    for r in range(formRows):
        for c in range(formRows):
            if c < triangleCheck:
                if startTriangle[r][c] == 1:
                    formTriangle[rowCounter] = 1
                else:
                    formTriangle[rowCounter] = 0
                rowCounter += 1
        triangleCheck += 1
    return formTriangle

'''Dropdown to select Row'''
rowBox = Combobox(root)
rowList = [0,1,2,3,4]
rowBox['values']= (rowList)
rowBox.grid(column=0,row=0)

'''Dropdown to select Column'''
colBox = Combobox(root)
colList = [0,1,2,3,4]
colBox['values']= (colList)
colBox.grid(column=1,row=0)

'''Dropdown to select Direction'''
directionBox = Combobox(root)
directionList = ["Down","Up","Left","Right","Down Right", "Up Left"]
directionBox['values']= (directionList)
directionBox.grid(column=2,row=0)

'''Button for jumpRight'''
jumpPegBtn = Button(root, text="Jump Peg", command= lambda: jumpPeg(rowBox.get(),colBox.get(),triangle,directionBox.get()),width=15)
jumpPegBtn.grid(column=0,row=1)

'''Button for printing the triangle'''
printPegBtn = Button(root, text="Print", command= lambda: pmain(triangle),width=15)
printPegBtn.grid(column=0,row=2)

'''Button for printing the triangle'''
dataPegBtn = Button(root, text="Data", command= lambda: formData(),width=15)
dataPegBtn.grid(column=0,row=3)

def costfunction(answerLocation,finalActivation):
    #answerRows = finalActivation.shape
    answerMatrix = np.zeros(shape=(len(finalActivation),1))
    answerMatrix[answerLocation][0] = 1
    cost = (finalActivation - answerMatrix)
    costMatrix = np.square(cost)
    totalCost = np.sum(costMatrix)
    return totalCost

def sigmoid(x):
    return 1/(1+np.exp(-x))

def newactivation(dweight,dbias,prevact):
    newactw = dweight * prevact
    newactb = dbias + newactw
    newactivation = sigmoid(newactb)
    return newactivation

'''Finds the choice from current weights and biases'''
def newneuronmatrix(inputs,dictName):
    '''Formats the input'''
    inputm = np.matrix(inputs)
    inputmatrix = np.transpose(inputm)
    inputmatrix2 = np.transpose(inputmatrix)
    
    activation1 = newactivation(dictName["wmat1"],dictName["bmat1"],inputmatrix2)
    activation2 = newactivation(dictName["wmat2"],dictName["bmat2"],activation1)
    activation3 = newactivation(dictName["wmat3"],dictName["bmat3"],activation2)
    '''activation4 = newactivation(wandb["wmat4"],wandb["bmat4"],activation3)'''
    
    return activation3

def aiRowCol(finalActivation):
    choicemax = finalActivation
    outputlist = choicemax.tolist()
    aiposchoice = outputlist.index(max(outputlist[0:14]))
    
    flatchoices = ['00','10', '11', '20', '21', '22', '30', '31','32','33','40','41','42','43','44',\
                   'Up', 'Down', 'Left','Right','Up Left','Down Right']
    
    aiplayerselection = flatchoices[aiposchoice]
    return aiplayerselection

def aiDirection(finalActivation):
    choicemax = finalActivation
    outputlist = choicemax.tolist()
    aidirchoice = outputlist.index(max(outputlist[15:]))
    
    flatchoices = ['00','10', '11', '20', '21', '22', '30', '31','32','33','40','41','42','43','44',\
                   'Up', 'Down', 'Left','Right','Up Left','Down Right']
    
    aidirectionselection = flatchoices[aidirchoice]
    return aidirectionselection

def aiChoice(finalActivation,neuronTriangle,results):
    choicemax = finalActivation
    outputlist = choicemax.tolist()
    aiposchoice = outputlist.index(max(outputlist[0:14]))
    aibadpos = outputlist[aiposchoice]
    aibadposformat = sum(aibadpos)
    aidirchoice = outputlist.index(max(outputlist[15:]))
    aibaddir = outputlist[aidirchoice]
    aibaddirformat = sum(aibaddir)
    posCost = costfunction(aiposchoice,outputlist[0:14])
    dirCost = costfunction(aidirchoice-15,outputlist[15:])
    if results == "fail":
        completeCost = 20
        completeCost = (-1*(aibadposformat + aibaddirformat))/100
        scorePct = completeCost
    else:
        #completeCost = posCost + dirCost
        #scoreCost = 20 - completeCost
        #scorePct = float(scoreCost/20)
        scorePct = float(1)
    #print(scoreCost)
    #print(scorePct)
    return scorePct

def aiRun(testTriangle,aidName,sdName,printCheck):
    choiceResults = "success"
    aiScore = 0
    beginTriangle = testTriangle
    while choiceResults == "success":
        aiInputs = formData(beginTriangle)
        factivation = newneuronmatrix(aiInputs,aidName)
        aiPos = aiRowCol(factivation)
        aiDir = aiDirection(factivation)
        aiPass = jumpPeg(aiPos[0],aiPos[1],beginTriangle,aiDir)
        if aiPass == "success":
            '''
            print("")
            print(beginTriangle)
            print("")'''
            aiScore += aiChoice(factivation,beginTriangle,aiPass)
            aidName["maxscore"] += 1
            if aidName["maxscore"] > overallscore["topscore"]:
                overallscore["topscore"] += 1
                print(overallscore["topscore"])
            if printCheck == "pYes":
                print(beginTriangle)
        else:
            aiScore += aiChoice(factivation,beginTriangle,aiPass)
            scoreDict[sdName] += aiScore
            aidName["maxscore"] = 0
            #print(scoreDict[sdName])
            choiceResults = aiPass

def aiBulk(passDict):
    i = 0
    while i < 500:
        aiLearn(passDict)
        '''
        if i % 5 == 0:
            print(overallscore["topscore"])'''
        i += 1
    print("done")
        

def aiLearn(topDict,nameList = dFullList, stringList = dNameList):
    i = 0
    while i < 15:
        startPeg = random.randint(1,totalPegs)
        #tryTriangle = startTriangle(5,startPeg)
        '''
        HaiT = startTriangle(5,startPeg)
        DaiT = startTriangle(5,startPeg)
        LaiT = startTriangle(5,startPeg)
        TaiT = startTriangle(5,startPeg)'''
        for x,y in zip(nameList,stringList):
            tryTriangle = startTriangle(5,i+1)
            aiRun(tryTriangle,x,y,"pNo")
        '''
        aiRun(HaiT,Huey,"Huey")
        aiRun(DaiT,Duey,"Duey")
        aiRun(LaiT,Luey,"Luey")
        aiRun(TaiT,tDog,"tDog")'''
        i += 1
    winner = max(scoreDict.items(), key=operator.itemgetter(1))[0]
    dref = stringList.index(winner)
    winDict = nameList[dref]
    topDog(winDict,topDict)

def topDog(copyDict,dDict,nameList = dFullList):
    mutateDict(dDict,copyDict,0)
    errorAmount = .01
    for x in nameList[:-1]:
        mutateDict(x,dDict,errorAmount)
        errorAmount += .025
    '''
    mutateDict(Huey,tDog,.5)
    mutateDict(Duey,tDog,.5)
    mutateDict(Luey,tDog,.5)'''
    ZeroScore()

def SingleRun():
    startPeg = random.randint(1,totalPegs)
    i = 0
    while  i < 15:
        firstTriangle = startTriangle(5,i + 1)
        aiRun(firstTriangle,tDog,"tDog","pYes")
        i += 1
    print("done")
    
overallscore = {}
overallscore["topscore"]=0
'''Button for AI'''
aiBtn = Button(root, text="AI", command= lambda: aiBulk(tDog),width=15)
aiBtn.grid(column=0,row=4)

aiSingleBtn = Button(root, text="AI Single", command= lambda: SingleRun(),width=15)
aiSingleBtn.grid(column=0,row=5)

#aiLearn(startPeg)

root.mainloop()




