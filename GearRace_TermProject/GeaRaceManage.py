# By Jae-Eun (Esther) Lim 
# jaeeunl
# Section R
###############################################################################
import os
import random
###############################################################################
###############################################################################

# (CITATION: readFile() and writeFile() are from course notes)

def readFile(filename, mode="rt"):
    with open(filename, mode) as fin:
        return str(fin.read())

def writeFile(filename, contents, mode="wt"):
    with open(filename, mode) as fout:
        fout.write(contents)

# saves account information, any saved work, and scores
def saveUserInfo(username, userInfo, saved, savedYourGame, score):
    accountFile = "GeaRaceAccount.txt"
    scoreFile = username+"Score.txt"
    writeFile(accountFile, str(userInfo))
    writeFile(scoreFile, str(score))

# retrieves account
def fetchAccount():
    accountFile = "GeaRaceAccount.txt"
    account = readFile(accountFile)
    return eval(account)

# retrieves saved scores                                      
def fetchUserInfo(username):
    scoreFile = username+"Score.txt"
    score = readFile(scoreFile)
    return eval(score)  

###############################################################################
###############################################################################

def shuffleDirections():
    direct = [(0,-1),(+1,0),(0,+1),(-1,0),(-1,-1),(+1,-1),(+1,+1),(-1,+1)]
    newList = []
    while (len(direct) > 0):
        i = random.randint(0, len(direct)-1)
        newList.append(direct[i])
        direct.pop(i)
    return newList

###############################################################################
###############################################################################
### Basic Classes ###

# (CITATION: Struct class from course notes with some changes)
class Struct(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # made change with repr method
    def __repr__(self):
        return type(self).__name__ + "()"

###############################################################################

# Details about each level
class Levels(Struct): 
    def __init__(self, level=1, yourgame=None):
        self.level = level
        self.levels = dict()
        self.levelDetail(1,3,3,0,2,5,"clockwise",2,0,10,"clockwise",1,2)
        self.levelDetail(2,3,4,0,0,10,"clockwise",2,3,5,"counterclockwise",2,3)
        self.levelDetail(3,4,4,0,3,6,"counterclockwise",3,0,3,
                         "counterclockwise",3,6)
        self.levelDetail(4,4,5,0,2,12,"counterclockwise",3,0,6,"clockwise",4,2)
        self.levelDetail(5,5,5,0,0,3,"clockwise",4,4,9,"clockwise",5,5)
        self.levelDetail(6,5,6,4,0,6,"clockwise",0,5,12,"counterclockwise",6,3)
        self.levelDetail(7,5,6,4,5,6,"counterclockwise",1,0,3,"clockwise",6,6)
        self.levelDetail(8,6,6,0,0,6,"counterclockwise",5,0,12,"clockwise",8,4)
        self.levelDetail(9,6,7,5,6,3,"clockwise",0,0,9,"clockwise",9,2)
        self.levelDetail(10,7,7,0,0,6,"counterclockwise",6,6,3,
                         "counterclockwise",9,6)
        if (yourgame != None):
            self.levels["Your Game"] = yourgame
        # Level Information
        self.levelDetails = self.levels[self.level]                                                

    # makes a list of level details
    def levelDetail(self, level, rows, cols, motorRows, motorCols, motorSpeed,   
                    motorDir, wheelRows, wheelCols, wheelSpeed, wheelDir, 
                    axles, wheelRadius):                                        
        self.levels[level] = ([(rows, cols),
                              [(motorRows, motorCols),motorSpeed,motorDir],
                              [(wheelRows, wheelCols),wheelSpeed,wheelDir], 
                              axles, wheelRadius])

# Window Size Information
class Window(Levels):
    def __init__(self, level=1, yourgame=None):
        Levels.__init__(self, level, yourgame)
        self.width = 900
        self.height = 700 

# Standard Button Dimensions
class Button(Window):
    def __init__(self):
        Window.__init__(self)
        verticalDivision = 1.0/5.0
        horizontalDivision = 1.0/13.0
        self.x = self.width*2*verticalDivision # left side of buttons
        self.buttonW = self.width*verticalDivision # width
        self.buttonH = self.height*horizontalDivision # height
        self.dy = self.buttonH/3 # space between buttons
        self.textSize = "25"