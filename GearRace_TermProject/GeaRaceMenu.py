# By Jae-Eun (Esther) Lim 
# jaeeunl
# Section R
############################################################################### 
from Tkinter import *
from GeaRaceManage import *
from GeaRaceGame import *
###############################################################################
###############################################################################
### Main Menu ###

class MainMenu(Button):
    def __init__(self):
        Button.__init__(self)
        self.buttons = 3
        self.y = self.height/2 # top of first button
        self.buttonColor = "light blue"
        self.buttonList = ["Play","Instruction", "Quit"]
        self.i = None # index of button in buttonList

    def draw(self, canvas):
        # Title
        #(CITATION: scaling image from this website:
        # http://stackoverflow.com/questions/18316328/
        # cannot-resize-image-with-tkinter)
        title = PhotoImage(file="GeaRace.gif").subsample(2,2)                   
        label = Label(image=title)
        label.image = title
        canvas.create_image(self.width/2, self.width/3, anchor="s", image=title)
        # Buttons
        dy = self.dy
        size = self.textSize
        for i in xrange(self.buttons):
            (x, y) = (self.x, self.y + (self.buttonH+dy)*i)
            canvas.create_rectangle(x, y, x+self.buttonW, y+self.buttonH,
                                    fill=self.buttonColor)
            text = self.buttonList[i]
            canvas.create_text( self.width/2, y+dy, 
                            text=text, anchor="n", font="Courier "+size+" bold")

    def contain(self, x, y):
        for i in xrange(self.buttons):
            (x0, y0) = (self.x, self.y + (self.buttonH+self.dy)*i)
            if ((x0 < x < x0+self.buttonW) and
                (y0 < y < y0+self.buttonH)):
                return self.buttonList[i]
        return None


###############################################################################
###############################################################################
### Play Menu ###

class PlayMenu(MainMenu):
    def __init__(self):
        MainMenu.__init__(self)
        self.buttons = 3
        self.y = self.height/3 # top of first button
        self.buttonColor = "pink"
        self.buttonList = ["New Game","Log In", "Menu"]
        self.i = None # index of button in buttonList

    def draw(self, canvas): 
        dy = self.dy
        size = self.textSize
        for i in xrange(self.buttons):
            (x, y) = (self.x, self.y + (self.buttonH+dy)*i)
            canvas.create_rectangle(x, y, x+self.buttonW, y+self.buttonH,
                                    fill=self.buttonColor)
            text = self.buttonList[i]
            canvas.create_text( self.width/2, y+dy, 
                            text=text, anchor="n", font="Courier "+size+" bold")

###############################################################################
###############################################################################
### New Game Menu ###

class NewGameMenu(Button):
    def __init__(self):
        Button.__init__(self)
        self.title = "Create New Game"
        self.titleColor = "green"
        # Button
        self.buttonInit()
        # Entry
        self.entryInit()

    def buttonInit(self):
        self.buttons = 2
        verticalDivision = 1.0/3.0
        horizontalDivision = 3.0/5.0
        proportion = 1.0/7.0
        self.x = self.width*verticalDivision # left side of button
        self.y = self.height*horizontalDivision # top of button
        self.buttonW = self.width*proportion
        self.buttonColor = "light green"
        self.buttonList = ["Back", "Create"]
        self.i = None # index of buttonList

    def entryInit(self):
        proportion = 1.0/12.0
        self.entries = 2
        self.entryHeight = self.height*proportion
        self.rowWidth = self.height/10
        self.entryList = ["Username", "Password"]
        self.I = None # index of entryList
        self.username = ""
        self.password = ""
        self.encode = ""
        self.errorI = None

################################ Draw Functions ################################

    def draw(self, canvas):
        # Contents
        self.drawContent(canvas)
        # Write Entry
        self.writeEntry(canvas)
        # Error 
        if (self.errorI != None):
            self.errorMessage(canvas)

    def drawTitle(self, canvas):
        # Title
        title = self.title
        size = "50"
        color = self.titleColor
        canvas.create_text( self.width/2, self.y/2, text=title,
                            font="Courier "+size+" bold", fill=color   )

    def drawContent(self, canvas):
        # Title
        self.drawTitle(canvas)
        # Entry Label
        size = "15"
        for i in xrange(self.entries):
            text = self.entryList[i]
            canvas.create_text( self.x, self.y-(2-i)*self.rowWidth, text=text, 
                                anchor="w", font="Courier "+size+" bold" )
        # Entry
        self.drawEntry(canvas)
        # Buttons
        size = self.textSize
        dx = self.dy
        for i in xrange(self.buttons):
            (x, y) = (self.x + (self.buttonW+dx)*i, self.y)
            canvas.create_rectangle(x, y, x+self.buttonW, y+self.buttonH,
                                    fill=self.buttonColor)
            text = self.buttonList[i]
            canvas.create_text( x+self.buttonW/2, y+self.buttonH/2, 
                                text=text, font="Courier "+size+" bold")

    def drawEntry(self, canvas):
        for i in xrange(self.entries):
            (x, y) = (self.width/2, self.y-(2-i)*self.entryHeight)
            canvas.create_rectangle(x, y, x+self.buttonW, y-self.rowWidth/2,
                                    outline="grey", width=2)

    def writeEntry(self, canvas):
        size = "15"
        delta = self.dy
        # Username
        i = 0
        text = self.username
        (x, y) = (self.width/2+delta/2, self.y-(2-i)*self.entryHeight-delta/2)
        canvas.create_text( x, y, text=text, anchor="sw", 
                            font="Arial "+size)
        # Password
        i = 1
        text = self.encode
        (x, y) = (self.width/2+delta/2, self.y-(2-i)*self.entryHeight-delta/2)
        canvas.create_text( x, y, text=text, anchor="sw", 
                            font="Arial "+size)

    def errorMessage(self, canvas):
        errors = ([ "Only alphabetical or numerical characters",
                    "May not exceed 12 characters"])
        size = "12"
        color = "red"
        text = errors[self.errorI]
        canvas.create_text( self.width/3, self.y-self.entryHeight/2,
                            text=text, anchor="nw", fill=color,
                            font="Courier "+size+" bold")

############################### Contain Functions #############################
    
    # For buttons
    def contain(self, x, y):
        dx = self.dy
        for i in xrange(self.buttons):
            (x0, y0) = (self.x + (self.buttonW+dx)*i, self.y)
            if ((x0 < x < x0+self.buttonW) and
                (y0 < y < y0+self.buttonH)):
                return self.buttonList[i]
        return None

    # For entry
    def containEntry(self, x, y):
        for i in xrange(self.entries):
            (x0, y0) = (self.width/2, self.y-(2-i)*self.entryHeight)
            if (x0 < x < x0+self.buttonW) and (y0-self.rowWidth/2 < y < y0):
                return i
        return None

###############################################################################
###############################################################################
### Log In Menu ###

class LogInMenu(NewGameMenu):
    def __init__(self):
        NewGameMenu.__init__(self)
        self.title = "Log In"
        self.titleColor = "orange"
        self.buttonColor = "yellow"
        self.buttonList = ["Back", "Go"]

    def draw(self, canvas):
        # Contents
        self.drawContent(canvas)
        # Write Entry
        self.writeEntry(canvas)

###############################################################################
###############################################################################
### Levels Menu ###

class LevelMenu(Button):
    def __init__(self, username, color="purple"):
        Button.__init__(self)
        self.levels = 10
        self.lock = [True] * self.levels
        self.rows = 5
        self.cols = 2
        self.row = None
        self.col = None
        verticalDivision = 1.0/5.0
        horizontalDivision = 1.0/4.0
        self.x = self.width*verticalDivision # left side of buttons in 1st col
        self.y = self.height*horizontalDivision # top of first button
        self.dx = self.buttonW # horizontal distance between buttons
        self.buttonColor = "grey"
        self.logOutButtonSelected = False
        self.viewScoreButtonSelected = False
        self.makeYourGameButtonSelected = False
        self.username = username
        self.yourCarColor = color

################################ Draw Functions ################################

    def draw(self, canvas):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                x = self.x + col*(2*self.dx)
                y = self.y + row*(self.buttonH+self.dy)
                # Draw Box
                canvas.create_rectangle(x, y, x+self.buttonW, y+self.buttonH,
                                        fill=self.buttonColor)
                # Write Text
                size = self.textSize
                if (col == 0):
                    text = "Level "+str(row+1)
                elif (col == 1):
                    startingLevel = 6
                    text = "Level "+str(row+startingLevel)
                canvas.create_text( x+self.buttonW/2, y+self.buttonH/2,
                                    text=text, font="Courier "+size+" bold" )
        # Log Out button
        self.drawLogOutAndViewScoreButton(canvas)
        if (self.logOutButtonSelected == True):
            self.highlightLogOutOrViewScoreButton(canvas, 0)
        elif (self.viewScoreButtonSelected == True):
            self.highlightLogOutOrViewScoreButton(canvas, 1)
        # Make Your Game Button
        self.drawMakeYourGameButton(canvas)
        if (self.makeYourGameButtonSelected == True):
            self.highlightMakeYourGameButton(canvas)
        # Player
        y = 20
        Player(self.username, self.yourCarColor, y).draw(canvas)

    def drawLogOutAndViewScoreButton(self, canvas):
        (buttonW, buttonH) = (self.buttonW/2, self.buttonH/2)
        colors = ["pink", "orange"]
        buttons = ["Log Out", "View Score"]
        # Box
        margin = 10
        for i in xrange(len(buttons)):
            button = buttons[i]
            color = colors[i]
            (x, y) = (margin+i*(buttonW+margin), self.height - margin)
            canvas.create_rectangle(x, y-buttonH, x+buttonW, y, fill=color)
            # Text
            text = button
            if (button == "Log Out"): size = "18"
            else: size = "13"
            canvas.create_text( x+buttonW/2, y-buttonH/2, 
                            text=text, font="Courier "+size+" bold")

    def drawMakeYourGameButton(self, canvas):
        # Box
        margin = 10
        color = "light blue"
        (x, y) = (self.width - margin, self.height - margin)
        (buttonW, buttonH) = (self.buttonW, self.buttonH/2)
        canvas.create_rectangle(x-buttonW, y-buttonH, x, y, fill=color)
        # Text
        text = "Make Your Game"
        size = "18"
        canvas.create_text( x-buttonW+buttonW/2, y-buttonH+buttonH/2, 
                            text=text, font="Courier "+size+" bold")

#### Highlight ####

    def highlightLogOutOrViewScoreButton(self, canvas, i):
        (buttonW, buttonH) = (self.buttonW/2, self.buttonH/2)
        color = "red"
        # Box
        margin = 10
        (x, y) = (margin+i*(buttonW+margin), self.height - margin)
        canvas.create_rectangle(x, y-buttonH, x+buttonW, y, 
                                outline=color, width=2)

    def highlightMakeYourGameButton(self, canvas):
        margin = 10
        color = "cyan"
        (x, y) = (self.width - margin, self.height - margin)
        (buttonW, buttonH) = (self.buttonW, self.buttonH/2)
        canvas.create_rectangle(x-buttonW, y-buttonH, x, y, 
                                outline=color, width=2)

############################### Contain Functions #############################

    # For level buttons
    def contain(self, x, y):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                x0 = self.x + col*(2*self.dx)
                y0 = self.y + row*(self.buttonH+self.dy)
                if (x0 < x < x0+self.buttonW) and (y0 < y < y0+self.buttonH):
                    return row, col

    # For "Log Out" button
    def containLogOutOrViewScoreButton(self, x, y):
        (buttonW, buttonH) = (self.buttonW/2, self.buttonH/2)
        colors = ["pink", "orange"]
        buttons = ["Log Out", "View Score"]

        margin = 10
        (x0, y0) = (margin, self.height - margin)
        (buttonW, buttonH) = (self.buttonW/2, self.buttonH/2)
        for i in xrange(len(buttons)):
            button = buttons[i]
            color = colors[i]
            (x0, y0) = (margin+i*(buttonW+margin), self.height - margin)
            if (x0 < x < x0+buttonW) and (y0-buttonH < y < y0):
                return buttons[i]

    def containMakeYourGameButton(self, x, y):
        margin = 10
        (x0, y0) = (self.width - margin, self.height - margin)
        (buttonW, buttonH) = (self.buttonW, self.buttonH/2)
        if (x0-buttonW < x < x0) and (y0-buttonH < y < y0):
            return True
        return False

###############################################################################
###############################################################################
### Instruction ###

class Instruction(Button):
    def __init__(self):
        Button.__init__(self)
        self.firstPage = True
        self.secondPage = False
        self.thirdPage = False
        self.lastPage = False
        self.highlightBackButton = False
        self.highlightNextOrMenuButton = False

############################# Draw Functions ###################################

    def draw(self, canvas):
        # Title
        self.drawTitle(canvas)
        # Buttons
        self.drawButtons(canvas)
        # Write Contents
        if (self.firstPage == True): self.drawFirstPage(canvas)
        elif (self.secondPage == True): self.drawSecondPage(canvas)
        elif (self.thirdPage == True): self.drawThirdPage(canvas)
        elif(self.lastPage == True): self.drawLastPage(canvas)

    def drawTitle(self, canvas):
        text = "Instruction"
        size = "50"
        margin = 50
        color = "blue"
        canvas.create_text( self.width/2, margin, text=text, fill=color,
                            font="Courier "+size+" bold")

    def drawButtons(self, canvas):
        if (self.lastPage == True): buttons = ["Back", "Menu"]
        else: buttons = ["Back", "Next"]
        (buttonW, buttonH) = (self.buttonW/2, self.buttonH/2)
        margin = 10
        size = "20"
        for i in xrange(len(buttons)):
            button = buttons[i]
            color = "light green"
            x = margin + i*(self.width-2*margin-buttonW)
            y = self.height-margin-buttonH
            # Button Boxes
            canvas.create_rectangle(x, y, x+buttonW, y+buttonH, fill=color)
            # Highlight
            highlight = "dark green"
            if (i == 0):
                if (self.highlightBackButton == True):
                    canvas.create_rectangle(x, y, x+buttonW, y+buttonH, 
                                            outline=highlight, width=2)
            elif (self.highlightNextOrMenuButton == True):
                canvas.create_rectangle(x, y, x+buttonW, y+buttonH, 
                                        outline=highlight, width=2)
            # Text
            canvas.create_text(x+buttonW/2, y+buttonH/2, text=button,
                               font="Courier "+size+" bold")

    def drawFirstPage(self, canvas): 
        text = """Your goal is to make a gear train for a toy car.\n\n\n
You will be given the following:\n\n
1. Input motor speed, direction, and location\n
2. Output wheel speed, direction, and location\n
3. Number of axles to be used\n\n
Your task is to build a gear train that satisfies the requirements in 5 minutes.
"""
        size = "15"
        (x, y) = (self.width/2, self.height/2)
        canvas.create_text(x, y, text=text, font="Courier "+size)
        # Car Picture
        self.drawCar(canvas)

    def drawCar(self, canvas):
        car = Car()
        proportion = 1.0/4.0
        margin = self.height*proportion
        x, y = self.width-margin, margin
        color = "red"
        margin = car.carW/3
        dy = margin/2
        canvas.create_rectangle(x+margin, y, x+2*margin, y+dy, fill=color)
        canvas.create_rectangle(x, y+dy, x+car.carW, y+2*dy, fill=color)
        # wheels:
        for i in xrange(2):
            (cx, cy, r) = (x+(1+i)*margin, y+2*dy, car.wheelR)
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="black")

    def drawSecondPage(self, canvas): 
        text = """Placing an axle on the board:\n\n
\tFirst, click on the axle display.
\tThen, click on any empty hole on the board.\n\n\n
Changing the location of an axle:\n\n
\tFirst, click on the axle on the board.
\tThen, click on any empty hole on the board.\n\n\n
(NOTE: The location of the motor and wheel axles are fixed.)"""
        size = "15"
        (x, y) = (self.width/2, self.height/2)
        canvas.create_text(x, y, text=text, font="Courier "+size)
        # Axle picture
        self.drawAxle(canvas)

    def drawAxle(self, canvas):
        axle = Preview()
        proportion = 1.0/5.0
        margin = self.height*proportion
        x, y = self.width-margin, margin
        axle.drawAxle(canvas, x, y)

    def drawThirdPage(self, canvas): 
        text = """Getting a gear:\n\n
\tType the number of teeth in the N-entry.
\tThe minimum number of teeth is 6 and maximum is 24.
\tYou can drag the gear to the trashcan if you do not want to use it.\n\n\n
Placing a gear on the board:\n\n
\tAfter specifying the number of teeth, you can drag the gear 
\tto the axle in which you want to insert the gear.\n\n\n
Changing gear depth:\n\n
\tOnce you have your gear on an axle, you can use the "up" and "down"
\tkeys to change the depth of the gear.
\tThere are 4 depths. 1 is the highest and 4 is the lowest.
\tThis allows you to place up to 4 gears in each axle.
\t(RULE: However, the input motor axle cannot hold more than one gear.)"""
        size = "15"
        (x, y) = (self.width/2, self.height/2)
        canvas.create_text(x, y, text=text, font="Courier "+size)
        # N-entry picture
        entry = Preview()
        entry.drawEntry(canvas)

    def drawLastPage(self, canvas): 
        text = """Helpful features:\n\n
\tHINT - (For levels 1 to 8) You can use Hint to see the equation for the 
\trelationship between the number of teeth, radius and speed of a gear.\n
\tTAG - (For levels 1 to 8) You can use the Tag feature to hover the mouse over 
\tthe gears to see their speed and direction.\n
\tRUN - You can see the gears running on the board.\n
\tPLACE AXLES - You can use this feature to have the axles automatically placed 
\tfor you.\n
\tSOLUTION - This feature automatically solves the game. 
\t(RESPONSIBILITY: You should only use it when you are struggling.
\tAnd you should clear it after viewing.)"""
        size = "15"
        (x, y) = (self.width/2, self.height/2)
        canvas.create_text(x, y, text=text, font="Courier "+size)
        # Gear picture
        self.drawGear(canvas)

    def drawGear(self, canvas):
        proportion = 1.0/5.0
        margin = self.height*proportion
        cx, cy = self.width-margin, margin
        teeth = 12
        gear = Gear(cx, cy, teeth)
        gear.draw(canvas)

############################# Contain Functions ################################

    def contain(self, x, y):
        if (self.lastPage == True): buttons = ["Back", "Menu"]
        else: buttons = ["Back", "Next"]
        (buttonW, buttonH) = (self.buttonW/2, self.buttonH/2)
        margin = 10
        for i in xrange(len(buttons)):
            button = buttons[i]
            x0 = margin + i*(self.width-2*margin-buttonW)
            y0 = self.height-margin-buttonH
            if (x0 < x < x0+buttonW) and (y0 < y < y0+buttonH):
                return button 

###############################################################################
###############################################################################
#### Choose Color Menu ####

class ChooseColor(Car):
    def __init__(self):
        Car.__init__(self)
        self.buttonList = (["Red", "Yellow", "Orange", "dark green", 
                            "Blue", "Purple"])
        self.title = "Choose Your Car Color"
        self.titleSize = "40"
        proportion = 1.0/5.0
        self.y = self.height*proportion
        self.i = None
        self.highlight = False

    def draw(self, canvas): 
        # Title
        text = self.title
        size = self.titleSize
        (x, y) = (self.width/2, self.y)
        canvas.create_text(x, y, text=text, font="Courier "+size+" bold")
        # Car Buttons
        self.drawCarButtons(canvas)
        # Highlight Button
        if (self.highlight == True):
            self.highlightCarButton(canvas, self.i)

    def drawCarButtons(self, canvas):
        space = 50 # between first car button and the title
        margin = self.carW/3
        carH = margin/2
        dy = 50
        for i in xrange(len(self.buttonList)):
            (x, y) = (self.width/2 - self.carW/2, self.y + space + i*(carH+dy))
            color = self.buttonList[i]
            canvas.create_rectangle(x+margin, y, x+2*margin, y+carH,
                                    fill=color)
            canvas.create_rectangle(x, y+carH, x+self.carW, y+2*carH, 
                                    fill=color)
            ## wheels:
            wheelColor = "black"
            for j in xrange(2):
                (cx, cy, r) = (x+(1+j)*margin, y+2*carH, self.wheelR)
                canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=wheelColor)

    def highlightCarButton(self, canvas, i):
        space = 50 # between first car button and the title
        margin = self.carW/3
        carH = margin/2
        dy = 50
        (x, y) = (self.width/2 - self.carW/2, self.y + space + i*(carH+dy))
        color = "cyan"
        for j in xrange(2):
            (cx, cy, r) = (x+(1+j)*margin, y+2*carH, self.wheelR)
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color, width=2)        

    def contain(self, x, y): 
        space = 50 # between first car button and the title
        margin = self.carW/3
        carH = margin/2
        dy = 50
        for i in xrange(len(self.buttonList)):
            (x0, y0) = (self.width/2-self.carW/2, self.y+space+i*(carH+dy))
            if (x0 < x < x0+self.carW) and (y0 < y < y0+2*carH):
                return self.buttonList[i]

###############################################################################
###############################################################################
### You Lose or Win! Screen ###

class Result(NewGameMenu):
    def __init__(self):
        NewGameMenu.__init__(self)
        self.score = 0
        self.buttonList = []
        self.buttonColor = "pink"
        self.text = None
        self.scoreRecord = None 
        self.scoreRecordSelected = False

################################ Draw Functions ################################

    def draw(self, canvas):
        (x, y) = (self.width/2, self.height/2)
        # Background
        self.drawBackground(canvas)
        # Result Message
        margin = 50
        text1 = self.text
        size1 = "70"
        color = "red"
        canvas.create_text( x, y-margin, text=text1, anchor="s", fill=color,
                            font="Courier "+size1+" bold")
        # Score
        text2 = "Score: "+str(self.score)
        size2 = "25"
        color = "blue"
        canvas.create_text( x, y, text=text2, anchor="s", fill=color,
                            font="Courier "+size2+" bold")
        # Buttons
        self.drawButtons(canvas)
        if (self.scoreRecordSelected == True):
            self.drawScoreRecord(canvas)

    def drawBackground(self, canvas):
        proportion = 1.0/5.0
        margin = self.height*proportion
        color = "white"
        canvas.create_rectangle(margin, margin, 
                                self.width-margin, self.height-margin,
                                fill=color)

    def drawButtons(self, canvas):
        size = self.textSize
        dx = self.dy
        for i in xrange(len(self.buttonList)):
            (x, y) = (self.x + (self.buttonW+dx)*i, self.y)
            canvas.create_rectangle(x, y, x+self.buttonW, y+self.buttonH,
                                    fill=self.buttonColor)
            text = self.buttonList[i]
            if (i == 1): size = "18"
            canvas.create_text( x+self.buttonW/2, y+self.buttonH/2, 
                                text=text, font="Courier "+size+" bold")

    def drawScoreRecord(self, canvas):
        # Background
        proportion, dy = 1.0/4.0, 50
        (x0, y0) = (self.height/2, self.height*proportion-dy/2)
        (x1, y1) = (self.width-x0, 2*(y0+dy))
        color = "light blue"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        # Contents
        vertDiv, horiDiv = 1.0/8.0, 1.0/10.0
        dx, dy = (x1 - x0)*vertDiv, (y1 - y0)*horiDiv
        verSpace, horSpace = 100, 20 # between columns and rows
        totalScore = 0
        i = 0
        for level in self.scoreRecord:
            score = self.scoreRecord[level]
            totalScore += score
            (x, y) = (x0+dx, y0+dy+i*horSpace)
            size = "15"
            text1 = "Level "+str(level)
            canvas.create_text(x,y,text=text1,anchor="w",font="Courier "+size)
            text2 = str(score)
            canvas.create_text(x+verSpace, y, text=text2, anchor="w", 
                                font="Courier "+size)
            i += 1
        # Total Score
        text4 = "Total Score: "+str(totalScore)
        canvas.create_text(x0+dx, y+verSpace/3, text=text4, anchor="w", 
                            font="Courier "+size+" bold")

############################### Contain Function ###############################

    def contain(self, x, y):
        # Buttons
        dx = self.dy
        for i in xrange(len(self.buttonList)):
            (x0, y0) = (self.x + (self.buttonW+dx)*i, self.y)
            if (x0 < x < x0+self.buttonW) and (y0 < y < y0+self.buttonH):
                return self.buttonList[i]
        return None