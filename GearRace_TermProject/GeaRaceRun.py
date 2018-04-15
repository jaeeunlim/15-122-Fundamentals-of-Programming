# By Jae-Eun (Esther) Lim 
# jaeeunl
# Section R
###############################################################################
import math
import copy
import os
import random

import eventBasedAnimation
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
from GeaRaceGame import *
from GeaRaceMenu import *
from GeaRaceCustomize import *
###############################################################################
###############################################################################
### Run! ###

# (CITATION: eventBasedAnimation is from course notes)
class GeaRace(eventBasedAnimation.Animation):
    def onInit(self, account=dict(), choice="Menu", score=4000, level=1, 
                username=None, saved=None, color="purple", 
                yourgame=None, savedYourGame=None, scoreRecord=None):
        self.windowTitle = "GeaRace"
        self.Account = fetchAccount()
        self.Account.update(account)
        self.saved = saved
        self.savedYourGame = savedYourGame
        self.choice = choice
        self.yourgame = yourgame
        self.error = False
        # Score and Time
        self.score = score
        self.scoreRecordInit(scoreRecord)
        self.startingScore = self.score
        self.time = 300 # 5 minutes
        self.choiceInit(level, yourgame)
        self.currentUsername = username
        self.yourCarColor = color
        self.main = Car(self.yourCarColor)
        self.resultInit()

    def scoreRecordInit(self, scoreRecord):
        if (scoreRecord == None):
            self.scoreRecord = dict()
            totalLevels = 10
            for level in xrange(1, totalLevels+1):
                self.scoreRecord[level] = 0
        else: self.scoreRecord = scoreRecord

    def choiceInit(self, level, yourgame):
        if (self.choice == "Menu"):
            self.geaRaceMenuInit()
        elif (self.choice == "Instruction"):
            self.instructionInit()
        elif (self.choice == "Game"):
            self.geaRaceGameInit(level, yourgame)
        elif (self.choice == "Customize"):
            self.customizeInit()

    def resultInit(self):
        # Race Scene
        self.result = Result()
        self.raceOver = False

################################ Init Functions ################################

############
### Menu ###
############

    def geaRaceMenuInit(self):
        self.menu = MainMenu()
        self.highlightColor = "blue"
        self.maxEntryChar = 12   

###################
### Instruction ###
###################

    def instructionInit(self):
        self.instruction = Instruction()

############
### Game ###
############

    def geaRaceGameInit(self, level=1, yourgame=None): 
        self.currentLevel = level 
        self.levelScore = 4000
        self.win = False
        self.doneSelected = False
        # Board Scene
        self.board = Board(self.currentLevel, yourgame)
        self.gameInit(yourgame)
        # Result Screen
        self.highlightResult = False 
        # Car Traveling Distance
        wheelRadiusIndex = 4
        wheelR = self.board.levelDetails[wheelRadiusIndex]
        meter = 100.0 # centimeter
        wheelSpeed = self.board.levelDetails[2][1]/meter
        self.main.distance = round(math.pi*wheelR*wheelSpeed/3, 2) 

    def gameInit(self, yourgame):                                                          
        self.level = self.currentLevel
        # Gear that is being moved
        self.gear = None 
        self.preview = Preview(self.currentLevel, yourgame)
        # Highlights
        self.highlightHole = False
        self.highlightEntry = False
        self.highlightGameButton = None
        self.highlightExitButton = None
        self.highlightSolutionButton = None
        self.row, self.col = None, None # for hole on board
        self.Row, self.Col = None, None # for previously selected hole
        # check selection
        self.selection()
        # Tag
        self.tagLocation = None

    def selection(self):
        # Buttons
        self.clickedButton = None
        self.hintButtonSelected = False
        self.clearButtonSelected = False
        self.solutionButtonClicked = None
        # Gears
        self.selectedGear = None # to change depth
        self.gearPreviewSelected = False
        self.gearBoardSelected = False
        self.gearDepthSelected = False
        # Axles
        self.axlePreviewSelected = False
        self.axleBoardSelected = False

#################
### Customize ###
#################

    def customizeInit(self):
        self.customize = Customize(self.currentUsername, self.yourCarColor)

################################ Draw Functions ################################

    def onDraw(self, canvas):
        if (self.choice == "Menu"):
            self.menuDraw(canvas)
        elif (self.choice == "Instruction"):
            self.instruction.draw(canvas)
        elif(self.choice == "Customize"):
            self.customize.draw(canvas)
        elif (self.doneSelected == False):
            self.drawGame(canvas)
        else:
            self.main.draw(canvas)
            self.drawRace(canvas)
            if (self.raceOver == True) and (self.highlightResult == True):
                self.highlightResultButton(canvas)
############
### Menu ###
############

    def menuDraw(self, canvas):
        self.menu.draw(canvas)
        if ((repr(self.menu)=="NewGameMenu()") or 
            (repr(self.menu)=="LogInMenu()")  ):
            if (self.menu.I != None):
                self.drawHighlightEntry(canvas)
        if (repr(self.menu) == "LevelMenu()"):
            if (self.menu.row != None):
                self.highlightLevel(canvas)
        elif (self.menu.i != None):
            self.highlightButton(canvas)
        # View Score
        if (self.result.scoreRecordSelected == True):
            self.result.drawScoreRecord(canvas)

    def highlightButton(self, canvas):
        if (repr(self.menu)=="MainMenu()") or (repr(self.menu)=="PlayMenu()"):
            (x, y) = (self.menu.x, self.menu.y)
            (buttonW, buttonH) = (self.menu.buttonW, self.menu.buttonH)
            y = y + (buttonH+self.menu.dy)*self.menu.i
            canvas.create_rectangle(x, y, x+buttonW, y+buttonH, 
                                    outline=self.highlightColor, width=2)
        elif (  (repr(self.menu)=="NewGameMenu()") or 
                (repr(self.menu)=="LogInMenu()")  ):
            (x, y) = (self.menu.x, self.menu.y)
            (buttonW, buttonH) = (self.menu.buttonW, self.menu.buttonH)
            x = x + (buttonW+self.menu.dy)*self.menu.i
            canvas.create_rectangle(x, y, x+buttonW, y+buttonH, 
                                    outline=self.highlightColor, width=2)

    # Username and Password
    def drawHighlightEntry(self, canvas):
        entryHeight = self.menu.entryHeight
        (x, y) = (self.width/2, self.menu.y-(2-self.menu.I)*entryHeight)
        (buttonW, rowWidth) = (self.menu.buttonW, self.menu.rowWidth)
        canvas.create_rectangle(x, y, x+buttonW, y-rowWidth/2,
                                outline="cyan", width=2)

    # Level buttons
    def highlightLevel(self, canvas):
        for row in xrange(self.menu.rows):
            for col in xrange(self.menu.cols):
                x = self.menu.x+self.menu.col*(2*self.menu.dx)
                y = self.menu.y+self.menu.row*(self.menu.buttonH+self.menu.dy)
                canvas.create_rectangle(x, y, 
                                        x+self.menu.buttonW,y+self.menu.buttonH,
                                        outline=self.highlightColor, width=2)
############
### Game ###
############

    def drawGame(self, canvas):
        # Level label
        self.writeLevel(canvas)
        # Username
        Player(self.currentUsername, self.yourCarColor).draw(canvas)
        # Score
        self.writeScore(canvas)
        # Time
        self.drawTime(canvas)
        # Board
        self.board.draw(canvas)
        # Highlight holes
        self.highlightHoles(canvas)
        # Highlight entry box
        self.highlightEntryBox(canvas)
        # Previews
        self.preview.draw(canvas)
        # Highlight Axle Box
        if (self.axlePreviewSelected == True):
            self.preview.highlightAxleBox(canvas)
        # Highlight buttons
        self.highlightButtons(canvas)
        # Draw gear being dragged
        if (self.gear != None):
            self.gear.draw(canvas)
        # Show hint
        if (self.hintButtonSelected == True):
            self.showHint(canvas)
        # Draw Tag
        if (self.tagLocation != None): self.drawTag(canvas)

    def writeLevel(self, canvas):
        if (self.currentLevel == "Your Game"):
            text = "Your Game"
        else:
            text = "Level " + str(self.level)
        size = "25"
        margin = 10
        canvas.create_text( margin, margin, text=text, anchor="nw", 
                            font="Courier "+size+" bold underline" )

    def drawTag(self, canvas):
        i1, i2, i3, i4 = 0, 1, 2, 3
        row, col = self.tagLocation[i1], self.tagLocation[i2]
        x, y = self.tagLocation[i3], self.tagLocation[i4]
        gearList = self.board.findGears()
        gearDict = self.board.makeDict(gearList)
        speed, direction = 0, None
        for depth in xrange(self.board.depths):
            if (self.board.board[row-1][col-1][depth] != None):
                for gear in gearDict:
                    rowI, colI = 2, 3
                    row2, col2 = gearDict[gear][rowI], gearDict[gear][colI]
                    if (row-1 == row2) and (col-1 == col2):
                        speedI, dirI = 0, 1
                        speed = int(round(gearDict[gear][speedI]))
                        direction = gearDict[gear][dirI]
                        break
                # Background
                width, height = 200, 25
                canvas.create_rectangle(x, y, x+width, y+height, fill="white")
                # Text
                size = "10"
                text = "Speed = "+str(speed)+" rpm\nDirection = "+str(direction)
                canvas.create_text(x+width/2, y+height/2, text=text, 
                                   font="Courier "+size)
                break

    def showHint(self, canvas):
        # Background
        proportion = 8.0/9.0
        vertDiv = 1.0/5.0
        horiDiv = 1.0/7.0
        (x, y) = (self.width*proportion, self.height*proportion) # bottom right
        width, height = self.width*vertDiv, self.height*horiDiv
        canvas.create_rectangle(x-width, y-height, x, y, fill="white")
        # Texts
        size1 = "10"
        size2 = "17"
        margin = 10
        minHighLevel = 9
        if (self.currentLevel < minHighLevel):
            text1 = "n = number of teeth\nr = gear radius\ns = rotational speed"
            text2 = "n1/n2 = r1/r2 = s2/s1"
            canvas.create_text( x-width+margin, y-height+margin, text=text1,
                            anchor="nw", font="Arial "+size1)
        else:
            text2 = "No Hint"
        canvas.create_text( x-width+margin, y-margin, text=text2,
                            anchor="sw", font="Arial "+size2)

#### Highlight ####

    def highlightButtons(self, canvas):
        # Highlight Game Button
        if (self.highlightGameButton != None):
            button = self.highlightGameButton
            self.preview.highlightGameButton(canvas, button)
        # Highlight Exit Button
        if (self.highlightExitButton != None):
            button = self.highlightExitButton
            self.preview.highlightExitButton(canvas, button)
        # Highlight Solution Button
        if (self.highlightSolutionButton != None):
            button = self.highlightSolutionButton
            self.preview.highlightSolutionButton(canvas, button)

    # highlight hole
    def highlightHoles(self, canvas):
        if (self.highlightHole == True):
            if (self.axleBoardSelected == True): 
                (row, col) = (self.Row, self.Col)
            else: 
                (row, col) = (self.row, self.col)
            (x, y) = (self.board.x0, self.board.y0)
            color = "green"
            dx = self.board.boardW / (self.board.cols+1)
            dy = self.board.boardH / (self.board.rows+1)
            (x0, y0) = (x + dx*col - self.board.R, y + dy*row - self.board.R)
            (x1, y1) = (x + dx*col + self.board.R, y + dy*row + self.board.R)
            canvas.create_oval(x0, y0, x1, y1, outline=color, width=2)

    def highlightEntryBox(self, canvas):
        if (self.highlightEntry == True):
            x = self.preview.width-self.preview.size/2
            y = self.preview.size+self.preview.dy
            entryH = self.preview.size/self.preview.dy
            entryW = self.preview.size/3
            canvas.create_rectangle(x, y, x+entryW, y+entryH,
                                    outline="cyan", width=2)

    # for Result() window
    def highlightResultButton(self, canvas):
        (x, y) = (self.result.x, self.result.y)
        (buttonW, buttonH) = (self.result.buttonW, self.result.buttonH)
        x = x + (buttonW+self.result.dy)*self.result.i
        color = "purple"
        canvas.create_rectangle(x, y, x+buttonW, y+buttonH, 
                                outline=color, width=2)

#### Score and Time ####

    def writeScore(self, canvas):
        text = "Score: "+str(self.score)
        color = "blue"
        size = "20"
        dx, dy = 10, 80
        canvas.create_text( dx, dy, text=text, anchor="nw", 
                            fill=color, font="Courier "+size)

    def drawTime(self, canvas):
        text = "Time "
        size = "20"
        dx, dy = 10, 110
        canvas.create_text( dx, dy, text=text, anchor="nw",
                            font="Courier "+size)
        dx = 70
        proportion = 2.0/3.0
        width, height = self.time*proportion, 20
        color = "green"
        canvas.create_rectangle(dx, dy, dx+width, dy+height, 
                                fill=color, width=0)

############
### Race ###
############

    def drawRace(self, canvas):
        if (self.raceOver == True):             
            self.result.draw(canvas)

############################## onMouse Functions ###############################

    def onMouse(self, event):
        if (self.choice == "Menu"):
            self.menuMouse(event)
        elif (self.choice == "Customize"):
            self.customizeMouse(event)
        elif (self.choice == "Instruction"):
            self.instructionMouse(event)
        elif (self.choice == "Game"):
            if (self.doneSelected == False):
                self.gameMouse(event)
            else:
                self.resultMouse(event)

############
### Menu ###
############

    def menuMouse(self, event):                                                    
        (x, y) = (event.x, event.y)                                      
        button = self.menu.contain(x, y)
        if (button != None): 
            self.buttonMouse(button)
        elif (repr(self.menu) == "NewGameMenu()" or 
              repr(self.menu) == "LogInMenu()"):
            self.menu.I = self.menu.containEntry(event.x, event.y)
        self.levelMenuMouse(x, y)
        self.chooseCarColor(x, y)

    def buttonMouse(self, button):
        if (button == "Play") or (button == "Back"):
            self.menu, self.highlightColor = PlayMenu(), "red"
        elif (button == "Instruction"): 
            self.onInit(self.Account, "Instruction")
        elif (button=="Menu"): self.gotoMainMenu()
        elif (button == "New Game"):
            self.menu, self.highlightColor = NewGameMenu(), "green"
        elif (button == "Log In"):
            self.menu, self.highlightColor = LogInMenu(), "orange"
        elif (repr(self.menu)=="NewGameMenu()" or 
              repr(self.menu)=="LogInMenu()"): self.createAccount(button)
        elif (repr(self.menu) == "LevelMenu()"): self.choosePath(button)

    def levelMenuMouse(self, x, y):
        if (repr(self.menu) == "LevelMenu()"):
            account = self.Account
            username = self.currentUsername
            saved = self.saved
            savedYourGame = self.savedYourGame
            button = self.menu.containLogOutOrViewScoreButton(x, y)
            if (button == "Log Out"): 
                score = self.scoreRecord
                saveUserInfo(username, account, saved, savedYourGame, score)
                self.gotoMainMenu()                
            elif self.menu.containMakeYourGameButton(x, y):
                self.backToSavedYourGame()

    def backToSavedYourGame(self, response=None):
        if (self.savedYourGame != None):
            usernameI = 6
            if (self.savedYourGame[usernameI] == self.currentUsername):
                message = "Would you like to resume your saved work?"
                title = "GeaRace"
                response = tkMessageBox.askquestion(title, message)
                if (response == "yes"): self.resumeSavedYourGame()
                else:
                    message1 = "You will lose your saved work. " 
                    message2 = "Do you want to continue?"
                    message = message1 + message2
                    title = "GeaRace"
                    response = tkMessageBox.askquestion(title, message) 
                    username = self.currentUsername
                    if (response == "yes"): self.makeNewGame()
                    else: self.backToSavedYourGame(response)
        else: self.makeNewGame()

    def makeNewGame(self):
        account = self.Account
        username = self.currentUsername
        saved = self.saved
        score = 4000
        color = self.yourCarColor
        self.onInit(account, "Customize", score, None, username, saved, color,
                    None, None, self.scoreRecord)

    def chooseCarColor(self, x, y):
        if (repr(self.menu) == "ChooseColor()"):
            button = self.menu.contain(x, y)
            if (button != None):
                account = self.Account
                score = self.score
                level = 1
                username = self.currentUsername
                self.onInit(account,"Menu",score,level,username,None,button,
                            None,None,self.scoreRecord)
                self.goToLevelMenu()
                self.Account[username].extend([self.yourCarColor])
                saved = self.savedYourGame
                scoreRec = self.scoreRecord
                saveUserInfo(username, account, None, saved, scoreRec)

    def gotoMainMenu(self):
        self.menu = MainMenu()
        self.highlightColor = "blue"

    # player can choose to go back to saved or not
    def choosePath(self, button):
        if (self.saved == None): 
            self.goToLevel(button)
        else: self.backToSaved(button)

    def goToLevel(self, button):
        row, col = button
        if (col == 0): # Levels 1 to 5
            level = row+1
        elif (col == 1): # Levels 6 to 10
            prevLevel = 5
            level = col+row+prevLevel
        account = self.Account
        username = self.currentUsername
        color = self.yourCarColor
        score = 4000
        self.onInit(account, "Game", score, level, username, None, color,
                    self.yourgame, self.savedYourGame, self.scoreRecord)

    def backToSaved(self, button, response=None):
        if (self.saved != None):
            usernameI = 6
            if (self.saved[usernameI] == self.currentUsername):
                message = "Would you like to resume your saved work?"
                title = "GeaRace"
                response = tkMessageBox.askquestion(title, message)
                if (response == "yes"): self.resumeSavedWork()
                else:
                    message1 = "You will lose your saved work. " 
                    message2 = "Do you want to continue?"
                    message = message1 + message2
                    title = "GeaRace"
                    response = tkMessageBox.askquestion(title, message) 
                    username = self.currentUsername
                    if (response == "yes"): 
                        self.goToLevel(button)
                    else: self.backToSaved(button, response)

    def createAccount(self, button):
        (username, password) = (self.menu.username, self.menu.password)
        if (len(username) > 0) and (len(password) > 0):
            if (button == "Create"):
                self.create(username, password)
            elif (button == "Go"): 
                self.login(username, password)
                self.scoreRecord = fetchUserInfo(username)
            self.error = False
        else:
            if (len(username) == 0): message = "Please type username!"
            elif (len(password) == 0): message = "Please type password!"
            self.error = True
            title = "Error"
            tkMessageBox.showerror(title, message)

    def create(self, username, password):
        if username in self.Account: 
            message = "This username already exists!"
            title = "Error"
            tkMessageBox.showerror(title, message)                 
        else:
            self.menu = ChooseColor()
            self.currentUsername = username
            self.Account[username] = ([password, self.score])

    def login(self, username, password):
        try:
            if (self.Account[username][0] == password):
                self.currentUsername = username
                self.yourCarColor = self.Account[username][2]
                self.menu = LevelMenu(username, self.yourCarColor)
                self.highlightColor = "black"
                self.error = False
            else:
                message = "Incorrect password!"
                title = "Error"
                tkMessageBox.showerror(title, message)
        except: 
            self.error = True
            message = "The username does not exist!"
            title = "Error"
            tkMessageBox.showerror(title, message)

    def resumeSavedWork(self):
        timeI, scoreI, levelI = 3, 4, 5
        score = 4000
        level = self.saved[levelI]
        account = self.Account
        username = self.currentUsername
        color = self.yourCarColor
        self.onInit(account, "Game", score, level, username, self.saved, color,
                    self.yourgame, self.savedYourGame, self.scoreRecord)
        self.board.board = self.saved[0]
        self.board.holes = self.saved[1]
        self.preview.axles = self.saved[2]
        self.time = self.saved[timeI]
        self.score = self.saved[scoreI]
        self.level = self.saved[levelI]

    def resumeSavedYourGame(self):
        account = self.Account
        username = self.currentUsername
        color = self.yourCarColor
        saved = self.saved
        savedYourGame = self.savedYourGame
        yourgame = self.yourgame
        level = "Your Game"
        self.onInit(account, "Game", self.score, level, username, saved, color, 
                    yourgame, savedYourGame, self.scoreRecord)
        timeI, scoreI, levelI = 3, 4, 5
        self.board.board = self.savedYourGame[0]
        self.board.holes = self.savedYourGame[1]
        self.preview.axles = self.savedYourGame[2]
        self.time = self.savedYourGame[timeI]
        self.score = self.savedYourGame[scoreI]
        self.level = self.savedYourGame[levelI]

###################
### instruction ###
###################

    def instructionMouse(self, event):
        (x, y) = (event.x, event.y)
        button = self.instruction.contain(x, y)
        self.instructionBackMouse(button)
        self.instructionNextMouse(button)

    def instructionBackMouse(self, button):
        if (button == "Back"):
            if (self.instruction.firstPage == True):
                self.onInit(self.Account, "Menu")
            elif (self.instruction.secondPage == True):
                self.instruction.secondPage = False
                self.instruction.firstPage = True
            elif (self.instruction.thirdPage == True):
                self.instruction.thirdPage = False
                self.instruction.secondPage = True
            elif (self.instruction.lastPage == True):
                self.instruction.lastPage = False
                self.instruction.thirdPage = True

    def instructionNextMouse(self, button):
        if (button == "Next"):
            if (self.instruction.firstPage == True):
                self.instruction.firstPage = False
                self.instruction.secondPage = True
            elif (self.instruction.secondPage == True):
                self.instruction.secondPage = False
                self.instruction.thirdPage = True
            elif (self.instruction.thirdPage == True):
                self.instruction.thirdPage = False
                self.instruction.lastPage = True
        elif (button == "Menu"):
            self.onInit(self.Account, "Menu")

############
### Game ###
############

    def resultMouse(self, event):                                   
        button = self.result.contain(event.x, event.y)
        account = self.Account
        username = self.currentUsername
        level = self.currentLevel
        color = self.yourCarColor
        score = self.startingScore
        record = self.scoreRecord
        if (button != None): 
            if (button == "Play Again"):
                self.onInit(account, "Game", score, level, username, None, 
                            color, self.yourgame, self.savedYourGame, record)
            elif (button == "Next Level"):
                self.onInit(account, "Game", score, self.level+1, username, 
                        None, color, self.yourgame, self.savedYourGame, record) 
            elif (button == "Menu"):
                self.onInit(account,"Menu",score,level,username,None,color,
                            self.yourgame, self.savedYourGame, record)
                self.goToLevelMenu()

    def gameMouse(self, event):
        (x, y) = (event.x, event.y)                                       
        if (self.highlightHole == True): self.highlightHole = False
        # Entry
        if self.preview.containEntry(x, y):
            self.highlightEntry = True
            self.preview.entryText = ""
        else: self.highlightEntry = False
        # Axle
        if (self.preview.contain(x, y) == "Axle"):
            if (self.axlePreviewSelected == False):
                if (self.preview.axles > 0): self.axlePreviewSelected = True
            else: self.axlePreviewSelected = False
        if (self.board.contain(x, y) != None): self.placeAxle(event, x, y)
        if (self.clearButtonSelected == True):
            self.geaRaceGameInit(self.currentLevel, self.yourgame)
        # Quit
        self.quit(x, y)
        # Select gear to change depth
        self.selectGear(event)
        # Game Button
        self.clickGameButton(event)
        # Run Errors
        self.runErrors()
        # Tag
        self.mouseTagButton(x, y)
        # Solution
        self.solveOnClick(event)

#### Gear and Axle ####

    # to change gear depth
    def selectGear(self, event):
        (x, y) = (event.x, event.y)
        selected = self.board.contain(x, y)
        if (selected != None) and (self.selectedGear == None):
            (row, col, cx, cy) = self.board.contain(x, y)
            for depth in xrange(self.board.depths):
                gear = self.board.board[row-1][col-1][self.board.depths-1-depth]
                if (gear != None):
                    self.highlightHole = True
                    self.row, self.col = row, col
                    self.selectedGear = gear
                    self.gearDepthSelected = True
        elif (selected != None) and (self.selectedGear != None):
                self.highlightHole = False
                self.selectedGear = None
                self.gearDepthSelected == False

    def moveAxle(self, event):
        (x, y) = (event.x, event.y)
        (row, col, cx, cy) = self.board.contain(x, y)
        if ((self.gear == None) and (self.gearBoardSelected == False) and
            (self.selectedGear == None)):
            if (self.axleBoardSelected == False):
                if (self.board.holes[row-1][col-1] == "yellow"):
                    self.axleBoardSelected = True
                    self.highlightHole = True
                    self.Row, self.Col = row, col
            elif (  (self.axleBoardSelected == True) and 
                    (self.board.holes[row-1][col-1] == "white")):
                self.board.holes[row-1][col-1] = "yellow"
                (Row, Col) = (self.Row, self.Col)
                self.board.holes[Row-1][Col-1] = "white"
                self.highlightHole = False
                self.axleBoardSelected = False
            else: 
                self.highlightHole = False
                self.axleBoardSelected = False

    def placeAxle(self, event, x, y):
        (row, col, cx, cy) = self.board.contain(x, y)
        if (self.axlePreviewSelected == True):
            if (self.board.holes[row-1][col-1] == "white"):
                self.board.holes[row-1][col-1] = self.preview.axleColor
                self.preview.axles -= 1
                self.axlePreviewSelected = False
                self.highlightHole = False
        # Change axle position
        else: self.moveAxle(event)

#### Buttons ####

    def clickGameButton(self, event):
        (x, y) = (event.x, event.y)
        button = self.preview.containGameButton(x, y)
        if (button != None):
            self.clickedButton = button
            if (button == "Run"):
                if (self.board.isLegalRun() and 
                    (self.board.moreThanOneInputGear() == False) and
                    (self.board.noGearOnBoard() == False) and
                    (self.board.noInputGear() == False)):
                    self.preview.gameButtons[0] = "Stop"
                    self.highlightGameButton = "Stop"
            elif (button == "Stop"):
                self.preview.gameButtons[0] = "Run"
                self.highlightGameButton = "Run"
            elif (button == "Done"):  
                if self.isReady():
                    self.doneSelected = True

    # checks if the gear train is complete
    def isReady(self):
        if self.board.moreThanOneInputGear(): 
            message = "More than one input gear is not allowed!"
        elif not self.board.isLegalRun():
            message1 = "Two adjacent axles cannot both "
            message2 = "contain more than one matching gears!"
            message = message1 + message2
        elif (self.preview.axles > 0):
            message = "You have not used all the axles!"
        elif not self.board.noEmptyAxles():
            message = "You have axle without gear!"
        elif not self.wheelAxleHasWorkingGear():
            message = "Your board is incomplete!"
        elif self.board.checkIsolation() or not self.board.checkAllGearWork():
            message = "There is free or non-working gear!"
        else: return True
        title = "Error"
        tkMessageBox.showerror(title, message)

    # checks if wheel axle has working gear
    def wheelAxleHasWorkingGear(self):
        # row and col of wheel axle
        Row = self.board.levelDetails[2][0][0]
        Col = self.board.levelDetails[2][0][1] 
        gearList = self.board.findGears() # dictionary of working gears
        gearDict = self.board.makeDict(gearList)
        for gear in gearDict:
            row, col = gearDict[gear][2], gearDict[gear][3]
            if (row == Row) and (col == Col): return True
        return False  

    def quit(self, x, y):                                               
        button = self.preview.containExitButton(x, y)
        account, username = self.Account, self.currentUsername
        level = 1
        color = self.yourCarColor
        if (button == "Quit"):
            message, title = "Are you sure you want to quit?", "GeaRace"
            response = tkMessageBox.askquestion(title, message)
            if (response == "yes"):
                if (self.currentLevel == "Your Game"):
                    saved = self.saved
                    yourgame = savedYourGame = None
                else:
                    saved = None
                    yourgame, savedYourGame = self.yourgame, self.savedYourGame
                score = self.startingScore
                self.onInit(account,"Menu",score,level,username,saved,color,
                            yourgame, savedYourGame, self.scoreRecord)
                self.goToLevelMenu()
        self.saveAndExit(button) 

    def saveAndExit(self, button):             
        if (button == "Save and Exit"):
            score = self.startingScore
            axles = self.preview.axles
            board, holes = self.board.board, self.board.holes
            time, level = self.time, self.currentLevel
            score = self.score
            color = self.yourCarColor
            username = self.currentUsername
            account = self.Account
            if (self.currentLevel == "Your Game"):
                yourgame = self.board.levelDetails
                savedYourGame = (board,holes,axles,time,score,level,username)
                self.onInit(account, "Menu", score, 1, username, self.saved, 
                            color, yourgame, savedYourGame, self.scoreRecord)
            else:   
                saved = (board,holes,axles,time,score,level,username)
                self.onInit(account, "Menu", score, 1, username, saved, color, 
                            self.yourgame, self.savedYourGame, self.scoreRecord)
            self.goToLevelMenu()

    def goToLevelMenu(self):
        self.menu = LevelMenu(self.currentUsername, self.yourCarColor) 
        self.highlightColor = "black" 

    def runErrors(self):
        if (self.clickedButton == "Run"):
            if self.board.noGearOnBoard():
                message = "No gears!"
            elif self.board.noInputGear():
                message = "There is no input gear!"
            elif self.board.moreThanOneInputGear():
                message = "More than one input gear is not allowed!"
            elif not self.board.isLegalRun():
                message1 = "Two adjacent axles cannot both "
                message2 = "contain more than one matching gears!"
                message = message1 + message2
            else: return None
            title = "Error"
            tkMessageBox.showerror(title, message)
            self.clickedButton = None

#### Tag ####

    def mouseTagButton(self, x, y):
        if self.preview.containTagButton(x, y):
            if (self.preview.tagButtonSelected == False):
                self.preview.tagButtonSelected = True
            else:
                self.preview.tagButtonSelected = False

#### Solver ####

    def solveOnClick(self, event):
        (x, y) = (event.x, event.y)
        button = self.preview.containSolutionButton(x, y)
        if (button != None):
            self.solutionButtonClicked = button
        else: 
            self.solutionButtonClicked = None
        if (self.solutionButtonClicked == "Solution"):
            self.solveGame()    
        elif (self.solutionButtonClicked == "Place Axles"):  
            self.solvePlaceAxles()   

    def solveGame(self):
        try: 
            #first clear out everything
            self.geaRaceGameInit(self.currentLevel, self.yourgame) 
            board = self.board.board
            axles = self.preview.axles
            motorRow = self.board.levelDetails[1][0][0]
            motorCol = self.board.levelDetails[1][0][1]
            directions = shuffleDirections()
            self.randomlyPlaceAxles(board,axles,motorRow,motorCol,directions)
            self.findMatch(board, motorRow, motorCol)
            self.findRest(board, motorRow, motorCol)
            if not self.solvedGame():
                self.geaRaceGameInit(self.currentLevel, self.yourgame)
                self.solvedGame()
        except:
            self.solveGame()


    def solvedGame(self): # see if achieved the desired output
        wheelRow = self.board.levelDetails[2][0][0]
        wheelCol = self.board.levelDetails[2][0][1]
        wheelSpeed = self.board.levelDetails[2][1]
        wheelDirection = self.board.levelDetails[2][2]
        gearList = self.board.findGears() 
        gearDict = self.board.makeDict(gearList)   
        if not self.board.noEmptyAxles(): return False
        for gear in gearDict:                                                                    
            row, col = gearDict[gear][2], gearDict[gear][3]
            if (row == wheelRow) and (col == wheelCol):
                speed, direction = gearDict[gear][0], gearDict[gear][1]
                if (speed == wheelSpeed) and (direction == wheelDirection):
                    return True
        return False

    def solvePlaceAxles(self):
        # first first clear out everything and solve
        self.geaRaceGameInit(self.currentLevel, self.yourgame)
        self.solveGame() 
        # then remove gears and only leave axles
        for row in xrange(self.board.rows):
            for col in xrange(self.board.cols):
                for depth in xrange(self.board.depths):
                    self.board.board[row][col][depth] = None

########## Place Axles ##########

    def randomlyPlaceAxles(self, board, axles, row, col, directions):
        if (axles == 0): # check if wheel axle is adjacent
            for direct in directions:
                (drow, dcol) = direct
                row2, col2 = row+drow, col+dcol
                if self.isWithinBoard(board, row2, col2):
                    if (self.board.holes[row2][col2] == "red"): return board
        else:
            for direct in directions:
                (drow, dcol) = direct
                row2, col2 = row+drow, col+dcol
                if self.isLegalDirection(board, row2, col2, row, col):
                    self.board.holes[row2][col2] = "yellow"
                    self.preview.axles -= 1
                    solution = self.randomlyPlaceAxles(board, axles-1, 
                                                       row2, col2, directions)
                    if (solution != None): return solution
                    else: 
                        self.board.holes[row2][col2] = "white"
                        self.preview.axles += 1

    def isLegalDirection(self, board, row, col, prevRow, prevCol):
        # row, col is the current hole
        # prevRow, prevCol is the previous hole
        if (self.isWithinBoard(board, row, col) and 
            self.isEmptyHole(board, row, col) and
            self.isNotCrowded(board, row, col, prevRow, prevCol)):
            return True
        else: return False

    def isWithinBoard(self, board, row, col):
        boardRows = len(board)
        boardCols = len(board[0])
        if (row < 0) or (row >= boardRows) or (col < 0) or (col >= boardCols):
            return False
        else: return True

    def isEmptyHole(self, board, row, col):
        if self.isWithinBoard(board, row, col):
            if (self.board.holes[row][col] == "white"):
                return True
        else: return False

    # checks if the axles are not crowded together
    def isNotCrowded(self, board, row, col, prevRow, prevCol):
        directions = [(0,-1),(+1,0),(0,+1),(-1,0)] # exclude diagonal directions
        for direct in directions:
            (drow, dcol) = direct
            row2, col2 = row+drow, col+dcol
            if self.isWithinBoard(board, row2, col2):
                if (row2 != prevRow) or (col2 != prevCol):
                    if (self.board.holes[row2][col2] != "white"):
                        return False
        return True

########## Place Gears ##########

    # initially takes motorRow and motorCol
    # finds matching gears that would generate desired speed and direction
    def findMatch(self, board, row, col, prevRow=None, prevCol=None):                       
        # distances between holes
        horiDis, vertDis, diagDis = self.getHoleDistances()
        disList = [horiDis, vertDis, diagDis]
        # directions to check
        vertDir, horiDir = [(+1,0),(-1,0)], [(0,-1),(0,+1)]
        diagDir = [(-1,-1),(+1,+1),(-1,+1),(+1,-1)]
        dirList = [horiDir, vertDir, diagDir]
        for i in xrange(len(dirList)):
            directions, dist = dirList[i], disList[i]
            for direct in directions:
                (drow, dcol) = direct
                row2, col2 = row+drow, col+dcol
                if (row2 == prevRow) and (col2 == prevCol): continue
                for depth in xrange(self.board.depths):
                    if (self.isWithinBoard(board, row2, col2) and 
                        (self.board.holes[row2][col2] != "white") and
                        (self.board.holes[row2][col2] != "blue") and
                        (self.board.board[row2][col2][depth] == None)):
                        if self.gotMatch(dist, row, col, row2, col2): return
                        self.findMatch(board, row2, col2, row, col)
                        return

    # once the gears of desired ratio is found, 
    # the rest can be filled with same-sized gears
    def findRest(self, board, row, col):
                         
        # distances between holes
        horiDis, vertDis, diagDis = self.getHoleDistances()
        disList = [horiDis, vertDis, diagDis]
        # directions to check
        vertDir, horiDir = [(+1,0),(-1,0)], [(0,-1),(0,+1)]
        diagDir = [(-1,-1),(+1,+1),(-1,+1),(+1,-1)]
        dirList = [horiDir, vertDir, diagDir]
        # first fill the first linear axles
        self.fillLinearly(board, dirList, disList, row, col)
        # find disconnection if any
        disconnection=self.findDisconnection(board, dirList, disList, row, col)
        if (disconnection != None): 
            row1, col1 = disconnection
            self.fillDisconnection(board, dirList, disList, row1, col1)
        # fill the rest
        nextPoint = self.findNextStartingPoint(board,dirList,disList,row,col)
        if (nextPoint != None):
            row1, col1 = nextPoint
            self.fillRest(board, dirList, disList, row1, col1)
        if not self.board.noEmptyAxles(): 
            nextPoint=self.findNextStartingPoint(board,dirList,disList,row,col)
            if (nextPoint != None):
                row1, col1 = nextPoint
                self.fillRest(board, dirList, disList, row1, col1)

    def findNextStartingPoint(self, board, dirList, disList, row, col, 
                                prevRow=None, prevCol=None):
        for i in xrange(len(dirList)):
            directions, dis = dirList[i], disList[i]
            for direct in directions:
                (drow, dcol) = direct
                row2, col2 = row+drow, col+dcol
                if (((row2 != prevRow) or (col2 != prevCol)) and
                    self.isWithinBoard(board, row2, col2) and 
                    (self.board.holes[row2][col2] != "white") and
                    (self.board.holes[row2][col2] != "blue")):
                    if self.isEmptyAxle(row2, col2):
                        return row, col
                    else: 
                        return self.findNextStartingPoint(board, dirList, 
                                                disList, row2, col2, row, col)

    # find the point where two adjacent gears aren't in the same depth
    def findDisconnection(self, board, dirList, disList, row, col, 
                            prevRow=None, prevCol=None):
        for i in xrange(len(dirList)):
            directions, dis = dirList[i], disList[i]
            for direct in directions:
                (drow, dcol) = direct
                row2, col2 = row+drow, col+dcol
                if (((row2 != prevRow) or (col2 != prevCol)) and
                    self.isWithinBoard(board, row2, col2) and 
                    (self.board.holes[row2][col2] != "white") and
                    (self.board.holes[row2][col2] != "blue")):
                    if self.isEmptyAxle(row2, col2): return None
                    elif not self.moreThanOneGear(board, row, col):
                        if not self.isSameDepth(board, row, col, row2, col2):
                            return row2, col2
                        elif self.isNotInContact(board, row, col, row2, col2):
                            return row2, col2
                    self.findDisconnection(board, dirList, disList, 
                                           row2, col2, row, col)

    def isNotInContact(self, board, row1, col1, row2, col2):
        for depth in xrange(self.board.depths):
            gear1 = self.board.board[row1][col1][depth]
            gear2 = self.board.board[row2][col2][depth]
            if (gear1 != None) and (gear2 != None):
                if not self.board.isLegalGear(gear1, gear2): # checks contact
                    return True
        return False

    # check if two adjacent gears are on the same depth
    def isSameDepth(self, board, row1, col1, row2, col2):
        for depth in xrange(self.board.depths):
            if ((self.board.board[row1][col1][depth] != None) and
                (self.board.board[row2][col2][depth] != None)):
                return True
        return False          

    # checks if there is more than one gear on an axle
    def moreThanOneGear(self, board, row, col):
        count = 0
        for depth in xrange(self.board.depths):
            if (self.board.board[row][col][depth] != None): count += 1
        if (count > 1): return True
        else: return False

    def fillRest(self, board, dirList, disList, row, col, 
                 prevR=None, prevC=None, depth=2):
        if (self.board.holes[row][col] == "red"): return # done!
        for i in xrange(len(dirList)):
            directions, dis = dirList[i], disList[i]
            for direct in directions:
                (drow, dcol) = direct
                row2, col2 = row+drow, col+dcol
                if (((row2 != prevR) or (col2 != prevC)) and
                    self.isWithinBoard(board, row2, col2) and 
                    (self.board.holes[row2][col2] != "white") and
                    (self.board.holes[row2][col2] != "blue") and
                    self.isEmptyAxle(row2, col2)):
                    # get the next starting point of linear axles
                    nextRow, nextCol, prevRow, prevCol = self.fillSameGears(dis,
                                        drow, dcol, row, col, depth, board)
                    if (depth < 2): depth += 1
                    else: depth -=1
                    self.fillRest(board, dirList, disList, nextRow, nextCol,
                                  prevRow, prevCol, depth)

    def fillDisconnection(self, board, dirList, disList, row, col, 
                 prevRow=None, prevCol=None, depth=2):
        for i in xrange(len(dirList)):
            directions, dis = dirList[i], disList[i]
            for direct in directions:
                (drow, dcol) = direct
                row2, col2 = row+drow, col+dcol
                if (((row2 != prevRow) or (col2 != prevCol)) and
                    self.isWithinBoard(board, row2, col2) and 
                    (self.board.holes[row2][col2] != "white") and
                    (self.board.holes[row2][col2] != "blue")):
                    # get the next starting point of linear axles
                    nextRow, nextCol, prevRow, prevCol = self.fillSameGears(dis,
                                        drow, dcol, row, col, depth, board)
                    if (not self.isEmptyAxle(row, col) and 
                        not self.isEmptyAxle(row2, col2)): 
                        return # done!
                    elif (depth < 2): depth += 1
                    else: depth -=1
                    self.fillDisconnection(board, dirList, disList, nextRow, 
                                        nextCol, prevRow, prevCol, depth)

    def fillLinearly(self, board, dirL, disL, row, col, prevR=None, prevC=None):
        maxDepth = 3
        for i in xrange(len(dirL)):
            directions, dis = dirL[i], disL[i]
            for direct in directions:
                (drow, dcol) = direct
                row2, col2 = row+drow, col+dcol
                if (((row2 != prevR) or (col2 != prevC)) and
                    self.isWithinBoard(board, row2, col2) and 
                    (self.board.holes[row2][col2] != "white") and
                    (self.board.holes[row2][col2] != "blue")):
                    if (self.board.board[row][col][0] == None): # no gear
                        self.fillSameGears(dis,drow,dcol,row,col,maxDepth,board)
                        return
                    elif (self.board.board[row2][col2][0] != None): 
                        self.fillLinearly(board,dirL,disL,row2,col2,row,col)
                        return
                    else: 
                        self.fillSameGears(dis,drow,dcol,row,col,maxDepth,board)
                        return

    # fills the board with same-sized gears along the same direction
    def fillSameGears(self, distance, drow, dcol, row, col, depth, board):
        row2, col2 = row+drow, col+dcol
        nextRow, nextCol = row2+drow, col2+dcol
        gear = self.board.board[row][col][depth]
        if (gear != None):
            depth = 0
        self.getSameSizedMatch(distance, row, col, row2, col2, depth)
        prevRow, prevCol = row, col
        while (self.isWithinBoard(board, nextRow, nextCol) and 
              (self.board.holes[nextRow][nextCol] != "white")):
            self.getSameSizedMatch(distance,row2,col2,nextRow,nextCol,depth)
            prevRow, prevCol = nextRow-drow, nextCol-dcol
            nextRow, nextCol = nextRow+drow, nextCol+dcol
        return nextRow-drow, nextCol-dcol, prevRow, prevCol

    def isEmptyAxle(self, row, col):                                  
        for depth in xrange(self.board.depths):
            if (self.board.board[row][col][depth] != None):
                return False
        return True

    def getHoleDistances(self):
        (x, y) = (self.board.x0, self.board.y0) # left top of board
        (boardW, boardH) = (self.board.boardW, self.board.boardH)
        (rows, cols) = (self.board.rows, self.board.cols)
        # centers of the first hole
        cx1 = x + (boardW/(cols+1))
        cy1 = y + (boardH/(rows+1))
        # and the one on the right of the first hole
        cx2 = x + (boardW/(cols+1))*2
        cy2 = y + (boardH/(rows+1))
        # and the one on the bottom of the first hole
        cx3 = x + (boardW/(cols+1))
        cy3 = y + (boardH/(rows+1))*2
        # and one diagonal to it
        cx4 = x + (boardW/(cols+1))*2
        cy4 = y + (boardH/(rows+1))*2
        # horizontal distance
        horiDis = math.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
        # vertical distance
        vertDis = math.sqrt((cx1-cx3)**2 + (cy1-cy3)**2)
        # diagonal distance
        diagDis = math.sqrt((cx1-cx4)**2 + (cy1-cy4)**2)
        return horiDis, vertDis, diagDis
    
    def gotMatch(self, distance, row1, col1, row2, col2):
        # get ratio of wheel and motor speed
        motorSpeed = float(self.board.levelDetails[1][1])
        wheelSpeed = float(self.board.levelDetails[2][1])
        ratio = wheelSpeed/motorSpeed
        # find the matching gears
        minTeeth, maxTeeth = 6, 24
        if (ratio > 1):
            return self.increaseRatio(distance, row1, col1, row2, col2, ratio)
        elif (ratio < 1):
            return self.decreaseRatio(distance, row1, col1, row2, col2, ratio)

    def increaseRatio(self, distance, row1, col1, row2, col2, ratio):
        depth = 0
        minTeeth, maxTeeth = 6, 24
        teeth1 = maxTeeth
        teeth2 = int(round(teeth1/ratio))
        while (teeth2 > minTeeth):
            gearR1 = self.getGearRadius(teeth1)
            gearR2 = self.getGearRadius(teeth2)
            if self.isMatching(distance, gearR1, gearR2):
                if self.board.isLegal(row1, col1, depth, gearR1):
                    self.placeGearOnBoard(row1, col1, teeth1, depth)
                    self.placeGearOnBoard(row2, col2, teeth2, depth)
                    return True
            teeth1 -= 1
            teeth2 = int(round(teeth1/ratio))
        return False

    def decreaseRatio(self, distance, row1, col1, row2, col2, ratio):
        depth = 0
        minTeeth, maxTeeth = 6, 24
        teeth1 = minTeeth
        teeth2 = int(round(teeth1/ratio))
        while (teeth2 < maxTeeth):
            gearR1 = self.getGearRadius(teeth1)
            gearR2 = self.getGearRadius(teeth2)
            if self.isMatching(distance, gearR1, gearR2):
                if self.board.isLegal(row1, col1, depth, gearR1):
                    self.placeGearOnBoard(row1, col1, teeth1, depth)
                    self.placeGearOnBoard(row2, col2, teeth2, depth)
                    return True
            teeth1 += 1
            teeth2 = int(round(teeth1/ratio))
        return False

    def getSameSizedMatch(self, distance, row1, col1, row2, col2, depth):     
        minTeeth, maxTeeth = 6, 24
        teeth = maxTeeth
        while (teeth > minTeeth):
            gearR = self.getGearRadius(teeth)
            if self.isMatching(distance, gearR, gearR):
                if not self.board.isLegal(row1, col1, depth, gearR):
                    if (depth < 3): depth += 1
                    else: depth -= 1
                #     (self.board.board[row2][col2][depth] == None)):
                self.placeGearOnBoard(row1, col1, teeth, depth)
                self.placeGearOnBoard(row2, col2, teeth, depth)
                return 
            teeth -= 1

    def getGearRadius(self, teeth):
        maxSpacing = 30.0
        scale = 4.0
        minRows = 3.0
        rows = self.board.levelDetails[0][0]
        toothSpacing = maxSpacing - scale*(rows - minRows)
        r = (toothSpacing*teeth)/(2*math.pi) # radius of gear
        return r

    def isMatching(self, distance, r1, r2):
        row = self.board.levelDetails[0][0]
        minRows = 3
        # max distance between gears
        maxDistance = 20
        maxDistance = maxDistance - 2*(row - minRows)
        # min distance between gears
        minDistance = 10
        minDistance = minDistance - (row - minRows)
        # check if matching distance
        if (distance-maxDistance <= r1+r2 <= distance-minDistance):
            return True
        return False

    def placeGearOnBoard(self, row, col, teeth, depth):
        cx, cy = self.getHoleCoordinate(row, col)
        level = self.currentLevel
        gear = Gear(cx, cy, teeth, level, depth, self.yourgame)
        holeColor = self.board.holes[row][col]
        gear.holeColor = holeColor
        self.board.board[row][col][depth] = gear

    def getHoleCoordinate(self, row, col):
        (x, y) = (self.board.x0, self.board.y0) # left top of board
        (boardW, boardH) = (self.board.boardW, self.board.boardH)
        (rows, cols) = (self.board.rows, self.board.cols)
        # centers of the first hole
        cx = x + (boardW/(cols+1))*(col+1)
        cy = y + (boardH/(rows+1))*(row+1)
        return cx, cy

#################
### Customize ###
#################

    def customizeMouse(self, event):
        (x, y) = (event.x, event.y)
        contain = self.customize.contain(x, y)
        self.boardMouse(contain)
        self.motorInfoMouse(contain)
        self.wheelInfoMouse(contain)
        self.motorAxleMouse(contain)
        self.wheelAxleMouse(contain)
        self.submitMouse(event)
        self.backMouse(event)

    def boardMouse(self, contain):
        if (contain == "Rows"):
            if (self.customize.rowsSelected == False): 
                self.undoRest()
                self.customize.rowsSelected = True
            else: self.customize.rowsSelected = False
        elif (contain == "Cols"):
            if (self.customize.colsSelected == False):
                self.undoRest() 
                self.customize.colsSelected = True
            else: self.customize.colsSelected = False
        elif (contain == "Axles"):
            if (self.customize.axlesSelected == False):
                self.undoRest() 
                self.customize.axlesSelected = True
            else: self.customize.axlesSelected = False

    def motorInfoMouse(self, contain):
        if (contain == "Motor Speed"):
            if (self.customize.motorSpeedSelected == False): 
                self.undoRest()
                self.customize.motorSpeedSelected=True
            else: self.customize.motorSpeedSelected = False
        elif (contain == "Motor Direction"):
            if (self.customize.motorDirSelected == False): 
                self.undoRest()
                self.customize.motorDirSelected = True
            else: self.customize.motorDirSelected = False

    def wheelInfoMouse(self, contain):
        if (contain == "Wheel Speed"):
            if (self.customize.wheelSpeedSelected == False): 
                self.undoRest()
                self.customize.wheelSpeedSelected=True
            else: self.customize.wheelSpeedSelected = False
        elif (contain == "Wheel Direction"):
            if (self.customize.wheelDirSelected == False): 
                self.undoRest()
                self.customize.wheelDirSelected = True
            else: self.customize.wheelDirSelected = False
        elif (contain == "Wheel Radius"):
            if (self.customize.wheelRadiusSelected == False):
                self.undoRest()
                self.customize.wheelRadiusSelected = True
            else: self.customize.wheelRadiusSelected = False

    def motorAxleMouse(self, contain):
        if (contain == "Motor Row"):
            if (self.customize.motorRowSelected == False): 
                self.undoRest()
                self.customize.motorRowSelected=True
            else: self.customize.motorRowSelected = False
        elif (contain == "Motor Col"):
            if (self.customize.motorColSelected == False): 
                self.undoRest()
                self.customize.motorColSelected = True
            else: self.customize.motorColSelected = False

    def wheelAxleMouse(self, contain):
        if (contain == "Wheel Row"):
            if (self.customize.wheelRowSelected == False):
                self.undoRest()
                self.customize.wheelRowSelected = True
            else: self.customize.wheelRowSelected = False
        elif (contain == "Wheel Col"):
            if (self.customize.wheelColSelected == False):
                self.undoRest()
                self.customize.wheelColSelected = True
            else: self.customize.wheelColSelected = False          

    def undoRest(self):
        self.customize.rowsSelected = False
        self.customize.colsSelected = False
        self.customize.axlesSelected = False
        self.customize.motorSpeedSelected = False
        self.customize.motorDirSelected = False
        self.customize.wheelSpeedSelected = False
        self.customize.wheelDirSelected = False
        self.customize.wheelRadiusSelected = False
        self.customize.motorRowSelected = False
        self.customize.motorColSelected = False
        self.customize.wheelRowSelected = False
        self.customize.wheelColSelected = False

    def submitMouse(self, event):
        (x, y) = (event.x, event.y)
        contain = self.customize.contain(x, y)
        if (contain == "Submit"):
            if self.isLegalSubmit():
                self.makeYourGame()
                self.solveGame()
                if self.board.noGearOnBoard():
                    # Error message
                    message, title = "It is an unsolvable game!", "Error"
                    tkMessageBox.showerror(title, message)
                    # Go back to customizing
                    account = self.Account
                    score = self.score
                    level = 1
                    username = self.currentUsername
                    saved = self.saved
                    color = self.yourCarColor
                    self.onInit(account, "Customize", score, level, username, 
                                saved, color, None, None, self.scoreRecord)
                else: self.geaRaceGameInit(self.currentLevel, self.yourgame) 

    def backMouse(self, event):
        (x, y) = (event.x, event.y)
        contain = self.customize.contain(x, y)
        if (contain == "Back"):
            account = self.Account
            score = self.score
            level = 1
            username = self.currentUsername
            color = self.yourCarColor
            self.onInit(account,"Menu",score,level,username,self.saved,color,
                        None, None, self.scoreRecord)
            self.goToLevelMenu()


    # checks if all entries are valid 
    def isLegalSubmit(self):
        if (self.isLegalBoard() != True): return 
        elif (self.isLegalDirections() != True): return 
        elif (self.isLegalWheelMotorRow() != True): return 
        elif (self.isLegalWheelMotorCol() != True): return 
        elif (self.isLegalWheelMotorPosition() != True): return
        else: return True

    def isLegalBoard(self):
        minVal, maxVal = 3, 7
        minAxle, maxAxle = 1, 10
        if ((len(self.customize.rows) > 0) and (len(self.customize.cols) > 0)
            and (len(self.customize.axles) > 0)): 
            if ((minVal > int(self.customize.rows)) or 
                (maxVal < int(self.customize.rows)) or 
                (minVal > int(self.customize.cols)) or 
                (maxVal < int(self.customize.cols))):
                message1 = "Board rows and columns should be "
                message2 = "integer between 3 and 7!"
                message = message1 + message2
            elif ((minAxle > int(self.customize.axles)) or 
                  (maxAxle < int(self.customize.axles))):
                message="Number of axles should be integer between 1 and 10!"
            else: return True
        else: 
            message = "Fill in everything!"
        title = "Error"
        tkMessageBox.showerror(title, message)

    def isLegalDirections(self):
        directions = ["clockwise", "counterclockwise"]
        if ((self.customize.motorDirection.lower() not in directions) or
            (self.customize.wheelDirection.lower() not in directions)):
            message="Direction should be clockwise or counterclockwise!"
            title = "Error"
            tkMessageBox.showerror(title, message)
        else: return True

    def isLegalWheelMotorRow(self):
        if ((len(self.customize.motorRow) > 0) and
            (len(self.customize.motorRow) > 0) and
            (len(self.customize.wheelRow) > 0) and
            (len(self.customize.wheelRow) > 0)):
            minVal = 1
            maxRowVal = int(self.customize.rows)
            if ((minVal > int(self.customize.motorRow)) or 
                (maxRowVal < int(self.customize.motorRow)) or
                (minVal > int(self.customize.wheelRow)) or 
                (maxRowVal < int(self.customize.wheelRow))):
                message1 = "Motor and wheel axle row should "
                message2 = "be between 1 and "+str(maxRowVal)+"!"
                message = message1 + message2
            else: return True
        else: 
            message = "Fill in everything!"
        title = "Error"
        tkMessageBox.showerror(title, message)

    def isLegalWheelMotorCol(self):
        if ((len(self.customize.motorCol) > 0) and
            (len(self.customize.motorCol) > 0) and
            (len(self.customize.wheelCol) > 0) and
            (len(self.customize.wheelCol) > 0)):
            minVal = 1
            maxColVal = int(self.customize.cols)
            if ((minVal > int(self.customize.motorCol)) or 
                (maxColVal < int(self.customize.motorCol)) or
                (minVal > int(self.customize.wheelCol)) or 
                (maxColVal < int(self.customize.wheelCol))):
                message1 = "Motor and wheel axle row should "
                message2 = "be between 1 and "+str(maxColVal)+"!"
                message = message1 + message2
            else: return True
        else: 
            message = "Fill in everything!"
        title = "Error"
        tkMessageBox.showerror(title, message)

    def isLegalWheelMotorPosition(self):
        if ((self.customize.motorRow == self.customize.wheelRow) and 
            (self.customize.motorCol == self.customize.wheelCol)):
            message = "Motor and wheel axles cannot be in the same location!"
            title = "Error"
            tkMessageBox.showerror(title, message)
        else: return True

    def makeYourGame(self): 
        account = self.Account
        username = self.currentUsername
        color = self.yourCarColor
        level = "Your Game"
        levelList = self.drawYourGameBoard()
        self.onInit(account, "Game", self.score, level, username, 
                    self.saved, color, levelList, None, self.scoreRecord)
        self.drawYourGameBoard()

    def drawYourGameBoard(self):
        levelList = []
        rows, cols = int(self.customize.rows), int(self.customize.cols)
        motorRow = int(self.customize.motorRow) - 1
        motorCol = int(self.customize.motorCol) - 1
        wheelRow = int(self.customize.wheelRow) - 1
        wheelCol = int(self.customize.wheelCol) - 1
        # Board
        levelList += [(rows, cols)]
        # Motor
        levelList += ([[(motorRow, motorCol), int(self.customize.motorSpeed),
                        self.customize.motorDirection.lower()]])
        # Wheel
        levelList += ([[(wheelRow, wheelCol), int(self.customize.wheelSpeed),
                        self.customize.wheelDirection.lower()]])
        # Axles
        levelList += [int(self.customize.axles)]
        # Wheel Radius
        levelList += [int(self.customize.wheelR)]
        return levelList

############################# Mouse Move Functions #############################

    def onMouseMove(self, event):
        if (self.choice == "Menu"):
            self.menuMouseMove(event)
        elif (self.choice == "Customize"):
            self.customizeMouseMove(event)
        elif (self.choice == "Instruction"):
            self.instructionMouseMove(event)
        elif (self.choice == "Game"):
            if (self.doneSelected == False):
                self.gameMouseMove(event)
            elif (self.raceOver == True):
                self.resultMouseMove(event)

############
### Menu ###
############

    def menuMouseMove(self, event):
        (x, y) = (event.x, event.y)
        button = self.menu.contain(x,y)
        if (button != None):
            if (repr(self.menu) == "LevelMenu()"): 
                self.menu.row, self.menu.col = button
            else:
                self.menu.i = self.menu.buttonList.index(button)
                if (repr(self.menu) == "ChooseColor()"):
                    self.menu.highlight = True
        else:
            if (repr(self.menu) == "LevelMenu()"):
                self.levelMenuMouseMove(x, y)
            else:
                self.menu.i = None
                if (repr(self.menu) == "ChooseColor()"):
                    self.menu.highlight = False

    def levelMenuMouseMove(self, x, y):
        self.menu.row, self.menu.col = None, None
        button = self.menu.containLogOutOrViewScoreButton(x, y)
        if (button == "View Score"):
            self.viewScoreRecord()
        elif (button == "Log Out"):
            self.menu.logOutButtonSelected = True
            self.menu.viewScoreButtonSelected = False
            self.menu.makeYourGameButtonSelected = False
            self.result.scoreRecordSelected = False
        elif self.menu.containMakeYourGameButton(x, y):
            self.menu.makeYourGameButtonSelected = True
            self.menu.logOutButtonSelected = False
            self.menu.viewScoreButtonSelected = False
            self.result.scoreRecordSelected = False
        else:
            self.menu.makeYourGameButtonSelected = False
            self.menu.logOutButtonSelected = False
            self.menu.viewScoreButtonSelected = False
            self.result.scoreRecordSelected = False

    def viewScoreRecord(self):
        self.menu.viewScoreButtonSelected = True
        self.menu.logOutButtonSelected = False
        self.menu.makeYourGameButtonSelected = False
        self.result.scoreRecord = self.scoreRecord                      
        self.result.scoreRecordSelected = True

###################
### Instruction ###
###################

    def instructionMouseMove(self, event):
        (x, y) = (event.x, event.y)
        button = self.instruction.contain(x, y)
        if (button == "Back"):
            self.instruction.highlightBackButton = True
            self.instruction.highlightNextOrMenuButton = False
        elif (button == "Next") or (button == "Menu"):
            self.instruction.highlightNextOrMenuButton = True
            self.instruction.highlightBackButton = False
        else: 
            self.instruction.highlightNextOrMenuButton = False
            self.instruction.highlightBackButton = False


############
### Game ###
############

    def gameMouseMove(self, event):
        (x, y) = (event.x, event.y)
        # Axles from preview
        if (self.axlePreviewSelected == True):
            if (self.board.contain(x, y) != None):
                self.row, self.col, cx, cy = self.board.contain(x, y)
                self.highlightHole = True
        # Buttons
        self.mouseMoveExitButtons(x, y)
        self.mouseMoveGameButtons(x, y)
        self.mouseMoveSolutionButtons(x, y)
        self.mouseMoveShowTag(x, y)

    def resultMouseMove(self, event):
        (x,y) = (event.x, event.y)
        button = self.result.contain(x,y)
        if (button != None):
            self.highlightResult = True
            self.result.i = self.result.buttonList.index(button)
            if (button == "View Score"):
                self.result.scoreRecord = self.scoreRecord                      
                self.result.scoreRecordSelected = True
        else:
            self.highlightResult = False
            self.result.scoreRecordSelected = False

    def mouseMoveExitButtons(self, x, y):
        self.mouseMoveGameButtons(x, y)
        button = self.preview.containExitButton(x, y)
        if (button != None):
            if (button == "Clear"): self.clearButtonSelected = True
            else: self.clearButtonSelected = False
            self.highlightExitButton = button
        else: self.highlightExitButton = None

    def mouseMoveGameButtons(self, x, y):
        button = self.preview.containGameButton(x, y)
        if (button != None):
            if (button == "Hint"): self.hintButtonSelected = True
            else: self.hintButtonSelected = False
            self.highlightGameButton = button
        else: 
            self.highlightGameButton = None
            self.hintButtonSelected = False

    def mouseMoveSolutionButtons(self, x, y):
        button = self.preview.containSolutionButton(x, y)
        if (button != None):
            self.highlightSolutionButton = button
        else: 
            self.highlightSolutionButton = None

    def mouseMoveShowTag(self, x, y):
        if self.preview.tagButtonSelected:
            if (self.board.contain(x, y) != None):
                self.tagLocation = self.board.contain(x, y)
            else: 
                self.tagLocation = None

#################
### Customize ###
#################

    def customizeMouseMove(self, event):
        (x, y) = (event.x, event.y)
        contain = self.customize.contain(x, y)
        if (contain == "Submit"):
            if (self.customize.submitSelected == False): 
                self.customize.submitSelected = True
                self.customize.backSelected = False
        elif (contain == "Back"):
            if (self.customize.backSelected == False): 
                self.customize.backSelected = True
                self.customize.submitSelected = False
        else:
            self.customize.submitSelected = False
            self.customize.backSelected = False

############################# Mouse Drag Functions #############################

############
### Game ###
############

    def onMouseDrag(self, event):
        if (self.choice == "Game"):
            if (self.doneSelected == False):
                self.gameMouseDrag(event)

    def gameMouseDrag(self, event):                                        
        (x, y) = (event.x, event.y)
        if (self.highlightHole == True):
            self.highlightHole = False
            self.axleBoardSelected = False
        # Moving gear from preview
        if (self.preview.contain(x, y) == "Gear"):
            self.gearPreviewSelected = True
            (self.preview.gear.cx, self.preview.gear.cy) = (x, y) 
        if (self.board.contain(x, y) == None): self.highlightHole = False 
        else:
            self.row, self.col, cx, cy = self.board.contain(x, y)
            if (self.gearPreviewSelected == True): self.highlightHole = True
            # Moving gear on board
            elif ((self.board.containGear(x, y, self.row, self.col) != None) and
                (self.gearBoardSelected == False)):
                self.changeGearPosition(x, y)
            elif (self.gearBoardSelected == True) or (self.gear != None):
                self.row, self.col, cx, cy = self.board.contain(x, y)
        if (self.gear != None): 
            self.gear.cx, self.gear.cy = x, y
            self.gearBoardSelected = True

    def changeGearPosition(self, x, y):
        self.gearBoardSelected = True
        row,col,depth = self.board.containGear(x, y, self.row, self.col)
        gear = self.board.board[row][col][depth]
        self.gear = Gear(x, y, gear.teeth, self.level)
        self.gear.holeColor = "grey"
        self.board.board[row][col][depth] = None

########################### Mouse Release Functions ############################

############
### Game ###
############

    def onMouseRelease(self, event):
        if (self.choice == "Game"):
            if (self.doneSelected == False):
                self.gameMouseRelease(event)

    def gameMouseRelease(self, event):                              
        (x, y) = (event.x, event.y)
        if (self.board.contain(x, y) != None):
            (row, col, cx, cy) = self.board.contain(x, y)
            # Moving gear on board
            if ((self.gearBoardSelected == True) or 
                (self.gearPreviewSelected == True)):
                if (self.board.holes[row-1][col-1] != "white"):
                    self.placeGear(cx, cy, row, col)
        # Trashing gear
        elif ((self.gearPreviewSelected == True) or 
            (self.gearBoardSelected == True)):
            self.trashGear(event)

    def placeGear(self, cx, cy, row, col):
        if (self.gearPreviewSelected == True):
            teeth = self.preview.gear.teeth
        elif (self.gearBoardSelected == True):
            teeth = self.gear.teeth
        try: gear = Gear(cx, cy, teeth, self.level, 0, self.yourgame)
        except: gear = self.gear
        if ((gear != None) and 
            self.board.isLegal(row-1, col-1, gear.depth, gear.r) and
            (self.board.board[row-1][col-1][0] == None)):
            gear.holeColor = self.board.holes[row-1][col-1]
            self.board.board[row-1][col-1][gear.depth] = gear
            (gear.cx, gear.cy) = cx, cy
            self.preview.gear = None
            self.gear = None
            self.gearBoardSelected = False
            self.gearPreviewSelected = False
            self.highlightHole = False

    def trashGear(self, event):
        (x, y) = (event.x, event.y)
        if self.preview.containTrash(x, y):
            self.preview.gear = None
            self.gear = None
            self.gearPreviewSelected = False
            self.gearBoardSelected = False
        else: 
            self.highlightHole = False
            self.gearBoardSelected = False


################################ Key Functions #################################

    def onKey(self, event):
        if (self.choice == "Menu"):
            self.menuKey(event)
        elif (self.choice == "Customize"):
            self.customizeKey(event)
        elif (self.choice == "Game"):
            self.gameKey(event)

############
### Menu ###
############

    def menuKey(self, event):
        if ((repr(self.menu) == "NewGameMenu()") or 
            (repr(self.menu) == "LogInMenu()")):
            if (self.menu.I == 0) or (self.menu.I == 1):
                # only one character symbols allowed
                if (len(event.keysym) == 1): 
                    self.menu.errorI = None
                    if ((self.menu.I == 0) and # index of username
                        (len(self.menu.username) <= self.maxEntryChar)):
                        self.typeUsername(event) 
                    elif ((self.menu.I == 1) and # index of password
                          (len(self.menu.password) <= self.maxEntryChar)):
                        self.typePassword(event)
                elif (event.keysym == "BackSpace"):
                    self.menu.errorI = None
                    self.erase(event)
                # error if key is not alphabet or number
                elif (event.keysym != "??"): self.menu.errorI = 0
                # error if exceed max characters
                if ((len(self.menu.username) > self.maxEntryChar) or
                    (len(self.menu.password) > self.maxEntryChar)): 
                    self.menu.errorI = 1

    def typeUsername(self, event):
        if (len(self.menu.username) == self.maxEntryChar):
            self.menu.username += " "
        else: self.menu.username += event.keysym

    def typePassword(self, event):
        if (len(self.menu.password) == self.maxEntryChar):
            self.menu.password += " "
        else:
            self.menu.password += event.keysym
            self.menu.encode += "*"

    def erase(self, event):
        if (self.menu.I == 0): 
            self.menu.username = self.menu.username[:-1]
        elif (self.menu.I == 1): 
            self.menu.password = self.menu.password[:-1]
            self.menu.encode = self.menu.encode[:-1]

############
### Game ###
############

    def gameKey(self, event):
        if (self.highlightEntry == True):
            if event.keysym.isdigit():
                maxChar = 4
                if (len(self.preview.entryText) < 4):
                    self.preview.entryText += event.keysym
            elif (event.keysym == "BackSpace"):
                self.preview.entryText = self.preview.entryText[:-1]
            elif (event.keysym == "Return"): 
                if self.preview.entryText.isdigit():
                    if ((int(self.preview.entryText) > 24) or 
                        (int(self.preview.entryText) < 6)):
                        message="The number of teeth must be between 6 and 24!"
                        tkMessageBox.showerror("Error", message)
                    else:
                        (cx, cy) = (self.preview.cx, self.preview.cy)
                        teeth = int(self.preview.entryText)
                        self.preview.gear = Gear(cx, cy, teeth, self.level, 
                                                 None, self.yourgame)
        # Change gear depth
        else: self.changeDepth(event)

    def changeDepth(self, event):
        if (self.selectedGear != None):
            row, col, r = self.row-1, self.col-1, self.selectedGear.r
            if (event.keysym == "Up"):
                if (self.selectedGear.depth > 0):                    
                    self.selectedGear.depth -= 1
                    if ((self.relocateGearOnList() == False) or not
                        self.board.isLegal(row,col,self.selectedGear.depth,r)):
                        self.selectedGear.depth += 1
                    elif self.board.isLegal(row,col,self.selectedGear.depth,r): 
                        self.relocateGearOnList()
            elif (event.keysym == "Down"):
                if (self.selectedGear.depth < 3):
                    self.selectedGear.depth += 1
                    if ((self.relocateGearOnList() == False) or not
                        self.board.isLegal(row,col,self.selectedGear.depth,r)):
                        self.selectedGear.depth -= 1
                    elif self.board.isLegal(row,col,self.selectedGear.depth,r): 
                        self.relocateGearOnList()

    def relocateGearOnList(self):
        for row in xrange(self.board.rows):
            for col in xrange(self.board.cols):
                for depth in xrange(self.board.depths):
                    gear = self.board.board[row][col][depth]
                    if (gear != None):
                        if (gear.depth != depth):
                            if (self.board.board[row][col][gear.depth] != None):
                                return False # if a gear is already there
                            elif self.board.isLegal(row,col,gear.depth,gear.r): 
                                self.board.board[row][col][gear.depth] = gear
                                self.board.board[row][col][depth] = None

#################
### Customize ###
#################

    def customizeKey(self, event):
        self.boardKey(event)
        self.motorKey(event)
        self.wheelKey(event) 
        self.motorAxleKey(event)
        self.wheelAxleKey(event)

    def boardKey(self, event):
        if (self.customize.rowsSelected == True): 
            if event.keysym.isdigit():
                if (len(self.customize.rows) == 0):
                    self.customize.rows += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.rows = self.customize.rows[:-1]
        elif (self.customize.colsSelected == True):
            if event.keysym.isdigit():
                if (len(self.customize.cols) == 0):
                    self.customize.cols += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.cols = self.customize.cols[:-1]
        elif (self.customize.axlesSelected == True):
            if event.keysym.isdigit(): 
                if (len(self.customize.axles) == 0):
                    self.customize.axles += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.axles = self.customize.axles[:-1]

    def motorKey(self, event):
        maxChrs = 16 
        if (self.customize.motorSpeedSelected == True): 
            if event.keysym.isdigit():
                if (len(self.customize.motorSpeed) == 0):
                    self.customize.motorSpeed += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.motorSpeed = self.customize.motorSpeed[:-1]
        elif (self.customize.motorDirSelected == True):
            if (len(event.keysym) == 1) and not event.keysym.isdigit():
                if (len(self.customize.motorDirection) < maxChrs):
                    self.customize.motorDirection += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.motorDirection=self.customize.motorDirection[:-1]

    def wheelKey(self, event):
        maxChrs = 16 
        if (self.customize.wheelSpeedSelected == True): 
            if event.keysym.isdigit():
                if (len(self.customize.wheelSpeed) == 0):
                    self.customize.wheelSpeed += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.wheelSpeed = self.customize.wheelSpeed[:-1]
        elif (self.customize.wheelDirSelected == True): 
            if (len(event.keysym) == 1) and not event.keysym.isdigit():
                if (len(self.customize.wheelDirection) < maxChrs):
                    self.customize.wheelDirection += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.wheelDirection=self.customize.wheelDirection[:-1]
        elif (self.customize.wheelRadiusSelected == True):
            if event.keysym.isdigit():
                if (len(self.customize.wheelR) == 0):
                    self.customize.wheelR += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.wheelR = self.customize.wheelR[:-1]

    def motorAxleKey(self, event):
        if (self.customize.motorRowSelected == True): 
            if event.keysym.isdigit():
                if (len(self.customize.motorRow) == 0):
                    self.customize.motorRow += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.motorRow = self.customize.motorRow[:-1]
        elif (self.customize.motorColSelected == True):
            if event.keysym.isdigit():
                if (len(self.customize.motorCol) == 0):
                    self.customize.motorCol += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.motorCol = self.customize.motorCol[:-1]

    def wheelAxleKey(self, event):
        if (self.customize.wheelRowSelected == True): 
            if event.keysym.isdigit():
                if (len(self.customize.wheelRow) == 0):
                    self.customize.wheelRow += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.wheelRow = self.customize.wheelRow[:-1]
        elif (self.customize.wheelColSelected == True):
            if event.keysym.isdigit():
                if (len(self.customize.wheelCol) == 0):
                    self.customize.wheelCol += event.keysym
            elif (event.keysym == "BackSpace"):
                self.customize.wheelCol = self.customize.wheelCol[:-1]


################################ Step Functions ################################

############
### Game ###
############

    def onStep(self):
        if (self.choice == "Game"):
            if (self.doneSelected == False):
                self.gameStep()
            elif (self.doneSelected == True):
                if (self.raceOver == False): 
                    self.raceStep()

    def gameStep(self):
        if (self.time >= 0):
            tenSecond = 100
            score = 100
            # Score
            if (self.step%tenSecond == 0):
                self.score -= score
                self.levelScore -= score
            # Time
            second = 10
            if (self.step%second == 0): self.time -= 1
        if (self.time == 0):
            message = "Time Over!"
            title = "Warning"
            tkMessageBox.showwarning(title, message) 
            score = self.startingScore
            account = self.Account
            username = self.currentUsername
            color = self.yourCarColor
            self.onInit(account,"Game",score,self.level,username,None,color,
                        self.yourgame, self.savedYourGame, self.scoreRecord)
        # Run gears
        self.runGears()

    # "Run" button plays the gears running
    def runGears(self):                                                    
        angle = 300.0
        angleIncre = math.pi/angle
        if (self.clickedButton == "Run"):
            gearList = self.board.findGears() 
            gearDict = self.board.makeDict(gearList)                                                                        
            if (self.board.isLegalRun() and  
                (self.board.moreThanOneInputGear() == False)):     
                for gear in gearDict:
                    speed, direction = gearDict[gear][0], gearDict[gear][1]
                    if (direction == "clockwise"):
                        gear.step -= angleIncre*speed
                    elif (direction == "counterclockwise"):
                        gear.step += angleIncre*speed 

    def raceStep(self):                                                  
        if (self.step%10 == 0):
            if (type(self.main.countdownText) == int): 
                if (self.main.countdownText > 1): self.main.countdownText -= 1   
                elif (self.main.countdownText == 1):
                    self.main.countdownText = "Go!"
        if (self.main.countdownText=="Go!") or (self.main.countdownText==""): 
            moment = 9
            if (self.step%10 == moment):
                self.main.countdownText = ""
                if (self.main.time > 0): self.main.time -= 1 
                elif (self.main.time == 0): self.raceOver = True
            self.moveCars()
        if (self.raceOver == True):
            self.resultMsg()

    def moveCars(self):
        start = self.main.startX
        end = self.main.lineX
        distance = end - start
        stepsInTenSec = 100
        stepSize1 = distance/stepsInTenSec
        # Demo Car
        if (self.main.demoX < end):
            # demoX is coordinate of leftend of demo car
            self.main.demoX += stepSize1
        # Your Car
        self.moveYourCar(stepSize1, end)

    def moveYourCar(self, stepSize1, end):
        wheelRow = self.board.levelDetails[2][0][0]
        wheelCol = self.board.levelDetails[2][0][1]
        wheelSpeed = self.board.levelDetails[2][1] # expected speed
        wheelDir = self.board.levelDetails[2][2] # expected direction
        gearList = self.board.findGears()                              
        rowI, colI = 3, 4 # indices
        for gear in gearList:
            row, col = gear[rowI], gear[colI]
            if (row == wheelRow) and (col == wheelCol):
                yourSpeed = gear[1]
                yourDir = gear[2]
                break
        stepSize2 = stepSize1*yourSpeed/wheelSpeed
        dx = 20
        if (self.main.yourX < end+dx):
            if (yourDir == wheelDir):
                self.main.yourX += stepSize2
            else:
                self.main.yourX -= stepSize2

    def resultMsg(self):
        exceptableDistance, maxLevel = 10, 10
        if (abs(self.main.yourX-self.main.demoX) <= exceptableDistance): 
            self.win = True
            if ((self.currentLevel == maxLevel) or 
                (self.currentLevel == "Your Game")):
                self.result.buttonList = ["Menu", "View Score"]
                self.result.text = "You made it!"
            else:
                self.result.buttonList = ["Menu", "Next Level"]
                self.result.text = "Well Done!"
            self.result.score = self.score
            if (self.currentLevel != "Your Game"):
                self.scoreRecord[self.currentLevel] = self.score
        else: 
            self.win = False
            self.result.buttonList = ["Menu", "Play Again"]
            self.result.text = "Nice try!" 
            self.result.score = 0
            self.scoreRecord[self.currentLevel] = 0
            
###############################################################################
###############################################################################
def PlayGeaRace():
    GeaRace(width=900, height=700, timerDelay=100).run()

PlayGeaRace()
            