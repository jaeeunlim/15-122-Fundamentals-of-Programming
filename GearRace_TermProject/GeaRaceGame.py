# By Jae-Eun (Esther) Lim 
# jaeeunl
# Section R
###############################################################################
import math
import copy

from Tkinter import *
from GeaRaceManage import *
###############################################################################
###############################################################################
### Board ###

class Board(Window):
    def __init__(self, level=1, yourgame=None):                             
        Window.__init__(self, level, yourgame)
        # Grid of holes
        self.rows, self.cols = self.levelDetails[0]
        # Board represented by dictionary
        self.depths = 4 # depths to which gear can be inserted in axle
        L = [[None, None, None, None] for i in xrange(self.cols)]
        self.board = dict()
        for i in xrange(self.rows): 
            self.board[i] = copy.deepcopy(L)
        # List of hole colors 
        self.holeColorsInit()
        # (x0, y0) are coordinate for left top corner of the board
        verticalDiv = 1.0/12.0
        horizontalDiv = 1.0/4.5
        proportion = 4.0/6.0
        self.x0, self.y0 = self.height*verticalDiv, self.width*horizontalDiv
        self.boardW, self.boardH = self.width*proportion, self.height*proportion
        self.color = "black" # color of board
        self.R = 9 # radius of holes

    def holeColorsInit(self):
        self.holes = [["white"]*self.cols for i in xrange(self.rows)]
        motorRow = self.levelDetails[1][0][0]
        motorCol = self.levelDetails[1][0][1]
        wheelRow = self.levelDetails[2][0][0]
        wheelCol = self.levelDetails[2][0][1]
        self.holes[motorRow][motorCol] = "blue"
        self.holes[wheelRow][wheelCol] = "red"                       

################################ Draw Functions ################################

    def draw(self, canvas):
        (x, y, R) = (self.x0, self.y0, self.R)
        # Board
        canvas.create_rectangle(x, y, x+self.boardW, y+self.boardH,
                                fill=self.color )
        # Holes
        for row in xrange(1, self.rows+1):
            for col in xrange(1, self.cols+1):
                color = self.holes[row-1][col-1]
                dx = self.boardW / (self.cols+1)
                dy = self.boardH / (self.rows+1)
                (x0, y0) = (x + dx*col - self.R, y + dy*row - self.R)
                (x1, y1) = (x + dx*col + self.R, y + dy*row + self.R)
                canvas.create_oval(x0, y0, x1, y1, fill=color)
        # Gears
        self.drawGears(canvas)

    # draw gears on board
    def drawGears(self, canvas):
        for depth in xrange(self.depths):
            for row in xrange(self.rows):
                for col in xrange(self.cols):
                    gear = self.board[row][col][self.depths-1-depth]
                    if (gear != None):
                        gear.draw(canvas)

############################### Contain Functions #############################

    # check if player is trying to insert axle/gear to a hole
    def contain(self, x, y):
        for row in xrange(1, self.rows+1):
            for col in xrange(1, self.cols+1):
                dx = self.boardW / (self.cols+1)
                dy = self.boardH / (self.rows+1)
                (cx, cy) = (self.x0 + dx*col, self.y0 + dy*row)
                # multiply radius by 3 for wider range of sensing
                if (math.sqrt((cx-x)**2 + (cy-y)**2) <= 3*self.R):
                    return row, col, cx, cy

    # check if gear on the board is clicked
    def containGear(self, x, y, row, col):
        for depth in xrange(self.depths):
            gear = self.board[row-1][col-1][depth]
            if (gear != None):
                return row-1, col-1, depth
        else: return None

############################### Legal Functions ################################

    # check if gears overlap
    def isLegal(self, row, col, depth, r1):
        # vertical and horizontal directions
        directions1 = [(0,-1),(0,+1),(+1,0),(-1,0)]
        # diagonal directions
        directions2 = [(-1,-1),(+1,-1),(+1,+1),(-1,+1)]
        # all directions
        directions = [directions1, directions2]
        for i in xrange(len(directions)):
            direction = directions[i]
            for j in xrange(len(direction)):
                (drow, dcol) = direction[j]
                try: gear2 = self.board[row+drow][col+dcol][depth]
                except: gear2 = None
                if (gear2 != None):
                    r2 = gear2.r
                    if (i == 0):
                        if (self.checkCollision(r1, r2, row, row+drow) == True): 
                            return False
                    elif (i == 1):
                        if (self.checkDiagonalCollision(r1, r2) == True):
                            return False
        return True

    # checks collision of horizontally and vertically adjacent gears
    def checkCollision(self, r1, r2, row1, row2):
        # centers of the first hole and 
        # the one on the right and bottom of the first hole
        cx1 = self.x0 + (self.boardW/(self.cols+1))
        cy1 = self.y0 + (self.boardH/(self.rows+1))
        cx2 = self.x0 + (self.boardW/(self.cols+1))*2
        cy2 = self.y0 + (self.boardH/(self.rows+1))
        cx3 = self.x0 + (self.boardW/(self.cols+1))
        cy3 = self.y0 + (self.boardH/(self.rows+1))*2
        # distance between holes in a row
        d1 = math.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
        # distance between holes in a column
        d2 = math.sqrt((cx1-cx3)**2 + (cy1-cy3)**2)
        row = self.levelDetails[0][0]
        minRows = 3
        minDistance = 10
        minDistance = minDistance - (row - minRows) # allowed between gears
        if (row1 == row2): # same row
            if ((r1+r2+minDistance) > d1): return True
        elif (row1 != row2): # same col
            if ((r1+r2+minDistance) > d2): return True
        return False

    # checks collision of diagonally adjacent gears
    def checkDiagonalCollision(self, r1, r2):
        # centers of the first hole and one diagonal to it
        cx1 = self.x0 + (self.boardW/(self.cols+1))
        cy1 = self.y0 + (self.boardH/(self.rows+1))
        cx2 = self.x0 + (self.boardW/(self.cols+1))*2
        cy2 = self.y0 + (self.boardH/(self.rows+1))*2
        # distance between the holes
        d = math.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
        row = self.levelDetails[0][0]
        minRows = 3
        minDistance = 10
        minDistance = minDistance - (row - minRows) # allowed between gears
        if ((r1+r2+minDistance) > d): return True
        else: return False

    # checks if gear1 and gear2 are in contact
    def isLegalGear(self, gear1, gear2):
        if (gear2 == None): return False
        elif (gear1 == None): return True
        else: 
            row = self.levelDetails[0][0]
            minRows = 3
            maxDistance = 20
            maxDistance = maxDistance - 2*(row - minRows) # between gears
            r1, r2 = gear1.r, gear2.r
            cx1, cy1 = gear1.cx, gear1.cy
            cx2, cy2 = gear2.cx, gear2.cy
            d = math.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
            if (d-maxDistance <= r1+r2 <= d):
                return True
        return False

    # check if no two adjacent axles contain 
    # more than one gear in the same depths
    def isLegalRun(self):                                                   
        # 8 directions
        directs = [(0,-1),(+1,0),(0,+1),(-1,0),(-1,-1),(+1,-1),(+1,+1),(-1,+1)]
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                gearCount1 = 0
                for depth in xrange(self.depths):
                    if (self.board[row][col][depth] != None): gearCount1 += 1
                if (gearCount1 > 1):
                    for direct in directs:
                        (drow, dcol) = direct
                        gearCount2 = 0
                        for depth in xrange(self.depths):
                            try: gear = self.board[row+drow][col+dcol][depth]
                            except: gear = None
                            if (gear != None): gearCount2 += 1
                        if (gearCount2 > 1):
                            result=self.noSameDepths(row,col,row+drow,col+dcol)
                            if (result == False): return False
        return True

    # checks how many adjacent gears are in same depth
    def noSameDepths(self, row1, col1, row2, col2):
        gears1 = self.board[row1][col1]
        gears2 = self.board[row2][col2]
        sameCount = 0
        for depth in xrange(self.depths):
            if (gears1[depth] != None) and (gears2[depth] != None):
                if self.isLegalGear(gears1[depth], gears2[depth]):
                    if (gears1[depth].r != gears2[depth].r):
                        sameCount += 1
        if (sameCount <= 1):
            return True
        else: return False

    # returns True if there is more than one input gear
    def moreThanOneInputGear(self):
        # row and col of motor axle
        row = self.levelDetails[1][0][0]
        col = self.levelDetails[1][0][1]
        gearCount = 0
        for depth in xrange(self.depths):
            if (self.board[row][col][depth] != None):
                gearCount += 1
        if (gearCount > 1):
            return True
        else: return False

    # returns True if there is no input gear
    def noInputGear(self):
        # row and col of motor axle
        row = self.levelDetails[1][0][0]
        col = self.levelDetails[1][0][1]
        gearCount = 0
        for depth in xrange(self.depths):
            if (self.board[row][col][depth] != None):
                gearCount += 1
        if (gearCount == 0):
            return True
        else: return False

    # checks if there is any axles on board without gear
    def noEmptyAxles(self):                                              
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if (self.holes[row][col] != "white"): # there is an axle
                    gearCount = 0
                    for depth in xrange(self.depths):
                        if (self.board[row][col][depth] != None):
                            gearCount += 1
                    if (gearCount == 0): return False
        return True   

    # checks if there is no gear on board
    def noGearOnBoard(self):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                for depth in xrange(self.depths):
                    if (self.board[row][col][depth] != None): return False
        return True

    # checks if any axle is isolated and return True if yes
    def checkIsolation(self):
        # 8 directions
        directs = [(0,-1),(+1,0),(0,+1),(-1,0),(-1,-1),(+1,-1),(+1,+1),(-1,+1)]
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                for depth in xrange(self.depths):
                    gear = self.board[row][col][depth]
                    if (gear != None):
                        for direct in directs:
                            (drow, dcol) = direct
                            try: gear = self.board[row+drow][col+dcol][depth]
                            except: gear == None
                            if (gear != None): break
                            elif (drow == -1) and (dcol == +1): # the last dir
                                return True
        return False

    # checks if every gear is working
    def checkAllGearWork(self):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                for depth in xrange(self.depths):
                    gear = self.board[row][col][depth]
                    if (gear != None):
                        found = 0
                        gearList = self.findGears()
                        gearDict = self.makeDict(gearList)
                        for gear in gearDict:
                            row2, col2 = gearDict[gear][2], gearDict[gear][3]
                            if (row == row2) and (col == col2):
                                found += 1
                                break
                        if (found == 0): return False
        return True

############################### Other Functions ################################

    # find gears on board that can rotate 
    def findGears(self):
        gearList = []
        rotations = ["clockwise", "counterclockwise"]
        # 8 directions
        direct = [(0,-1),(+1,0),(0,+1),(-1,0),(-1,-1),(+1,-1),(+1,+1),(-1,+1)]
        # speed and direction of motor
        motorS, motorD = self.levelDetails[1][1], self.levelDetails[1][2]
        row, col = self.levelDetails[1][0][0], self.levelDetails[1][0][1]
        for depth in xrange(self.depths):
            gear = self.board[row][col][depth]
            if (gear != None):
                gearList += [[gear, motorS, motorD, row, col]]
                gearList += self.makeGearList1(rotations, direct, motorS, 
                                                motorD, depth, row, col)
        maxCols = 7
        for i in xrange(maxCols):
            spDict = self.getAxleSpeed(gearList)
            gearList += self.makeGearList2(spDict, depth)  
        return gearList

    # for gears on the same depth as input gear
    def makeGearList1(self, rotations, directions, speed, rotation, depth, 
                      row1, col1, row2=None, col2=None, count=1):                         
        # row1, col1 is current and row2, col2 is previous
        gear1 = self.board[row1][col1][depth]
        gearList = []
        for i in xrange(len(directions)):
            (drow, dcol) = directions[i]
            try: gear2 = self.board[row1+drow][col1+dcol][depth]
            except: gear2 = None
            if self.isLegalGear(gear1, gear2):
                i1 = rotations.index(rotation)
                if (i1==0): i2 = 1
                elif (i1==1): i2 = 0
                rot, sp = rotations[i2], self.getSpeed(gear1, gear2, speed)
                gearList += [[gear2, sp, rot, row1+drow, col1+dcol]]
                ro1, co1, ro2, co2 = row1+drow, col1+dcol, row1, col1
                # No need to check the previous gear
                if (ro1 == row2) and (co1 == col2): continue
                maxCols = 7
                if (count == maxCols): return gearList
                gearList += self.makeGearList1(rotations, directions, sp, rot, 
                                            depth, ro1, co1, ro2, co2, count+1)
        return gearList

    # for gears more than one gear away from the input gear
    def makeGearList2(self, spDict, depth, count=0):
        gearList = []
        rotations = ["clockwise", "counterclockwise"]
        # 8 directions
        direct = [(0,-1),(+1,0),(0,+1),(-1,0),(-1,-1),(+1,-1),(+1,+1),(-1,+1)]
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                for depth in xrange(self.depths):
                    gear = self.board[row][col][depth]
                    if (gear != None):
                        try: (sp, rot) = spDict[(row, col)]
                        except: (sp, rot) = (None, None)
                        if (sp != None):
                            gearList += [[gear,sp,rot,row,col]]
                            gearList += self.makeGearList1(rotations, direct, 
                                                        sp,rot,depth,row,col)
        return gearList

    # makes gearList into dictionary
    def makeDict(self, gearList):
        # indices
        speedI = 1
        dirI = 2
        rowI = 3
        colI= 4
        gearDict = dict()
        for gear in gearList:
            gearDict[gear[0]] = (gear[speedI],gear[dirI],gear[rowI],gear[colI])
        return gearDict

    def getAxleSpeed(self, gearList):
        # indices
        rowIndex = 3
        colIndex = 4
        speedI = 1
        dirI = 2
        speedDict = dict()
        # first make a dictionary of speed for each axle with gears
        for i in xrange(len(gearList)):
            (row, col) = (gearList[i][rowIndex], gearList[i][colIndex])
            speedDict[(row, col)] = (gearList[i][speedI], gearList[i][dirI])
        return speedDict

    # calculates speed of gear2
    def getSpeed(self, gear1, gear2, speed):
        if (gear1 == None): return None
        teeth1 = gear1.teeth
        teeth2 = gear2.teeth
        ratio = float(teeth1)/float(teeth2)
        speed2 = speed*ratio
        return speed2

###############################################################################
###############################################################################
### Gear ###

class Gear(Window):
    def __init__(self, cx, cy, teeth, level=1, depth=None, yourgame=None):
        Window.__init__(self, level, yourgame)
        self.cx = cx
        self.cy = cy
        self.teeth = teeth # number of teeth
        # distance between two teeth
        maxSpacing = 30.0
        scale = 4.0
        minRows = 3.0
        rows = self.levelDetails[0][0]
        self.toothSpacing = maxSpacing - scale*(rows - minRows)
        self.toothThickness = self.toothSpacing/2
        self.r = (self.toothSpacing*self.teeth)/(2*math.pi) # radius of gear
        self.R = 9 # radius of hole
        self.depth = depth
        # arc angle of a tooth
        self.arcAngle = float(math.acos(1-((self.toothThickness/self.r)**2)/2)) 
        self.color = "dark grey" # color of gear
        self.holeColor = "grey"
        self.straightAngle = 180.0
        self.rightAngle = 90.0
        self.step = 0
        
    def draw(self, canvas):
        # r is radius of gear and R is radius of hole
        (cx, cy, r, R) = (self.cx, self.cy, self.r, self.R)
        tT = self.toothThickness
        # Body (circle)
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=self.color)
        # Teeth (square)
        for i in xrange(self.teeth):
            # x, y values are coordinates for each corner of a square tooth
            # angle is the location of the coordinate            
            # 1: bottom right corner
            angle1 = i * (2*math.pi / float(self.teeth)) + self.step
            x1 = cx + (r * math.cos(angle1))
            y1 = cy - (r * math.sin(angle1))            
            # 2: bottom left corner
            angle2 = angle1 + self.arcAngle
            x2 = cx + (r * math.cos(angle2))
            y2 = cy - (r * math.sin(angle2))            
            # 3: top left corner
            # "length" is measured from the center of circular body to (x3, y3)
            #   (use law of cosine to find length)
            # "angle" is made by 2 lines: 
            #   one from the center of circle to (x1, y1)
            #   another from (x1, y1) to (x3, y3)
            angle = ((self.straightAngle - self.arcAngle)/2 + self.rightAngle)
            length = math.sqrt(r**2 + tT**2 - 2*r*tT*math.cos(angle))
            # arc angle of tooth with respect to the circle around the outer 
            #   edge of teeth
            arcAngle = float(math.acos(1-((tT/length)**2)/2)) 
            angle3 = angle2 - (self.arcAngle - arcAngle)/2
            x3 = cx + (length * math.cos(angle3))
            y3 = cy - (length * math.sin(angle3))
            # 4: top right corner
            angle4 = angle1 + (self.arcAngle - arcAngle)/2
            x4 = cx + (length * math.cos(angle4))
            y4 = cy - (length * math.sin(angle4))
            outlineColor = "black"
            canvas.create_polygon(  (x1, y1), (x2, y2), (x3, y3), (x4, y4),
                                    fill=self.color, outline=outlineColor )
            # hole
            canvas.create_oval( cx-R, cy-R, cx+R, cy+R, fill=self.holeColor)
            # write depth
            self.writeDepth(canvas, cx, cy)

    def writeDepth(self, canvas, cx, cy):
        size = "15"
        if (self.depth != None):
            canvas.create_text(cx, cy, text=self.depth+1, font="Arial "+size)

    def contain(self, x, y):
        (cx, cy) = (self.cx, self.cy)
        if (math.sqrt((cx-x)**2 + (cy-y)**2) <= self.r):
            return True
        return False

###############################################################################
###############################################################################
### Preview ###

# Displays of gear and axle
class Preview(Window):
    def __init__(self, level=1, yourgame=None):
        Window.__init__(self, level, yourgame)
        proportion = 1.0/4.0
        self.size = self.height*proportion # size of preview boxes
        self.backgroundColors = ["light green", "orange", "light grey"]
        self.backgrounds = 3
        # coordinate of center of gear
        self.cx, self.cy = self.width-self.size/2, self.size/2
        self.gear = None
        # coordinate of axle
        self.x = self.width-self.size*(1+proportion)
        self.y = self.size*proportion
        self.axles = self.levelDetails[3] # number of required axles
        self.axleColor = "yellow"
        self.axleR = 9
        self.dy = 7 # space between the entry box and preview box
        self.entryText = "" # what player enters
        self.gameButtonInfo()
        self.exitButtonInfo()
        self.solutionButtonInfo()
        self.tagButtonSelected = False

    def gameButtonInfo(self):
        self.buttons = 3
        self.gameButtons = ["Run", "Hint", "Done"]
        self.gameButtonColors = ["red", "pink", "blue"]
        vertDiv = 9.0/10.0
        horiDiv = 4.0/5.0
        # coordinate of top left of first button
        self.gameButtonX = self.width*vertDiv
        self.gameButtonY = self.height*horiDiv
        self.gameButtonW = self.size/self.buttons
        self.gameButtonH = self.gameButtonW/self.buttons

    def exitButtonInfo(self):
        self.exitButtons = ["Save and Exit", "Quit", "Clear"]
        self.exitButtonColors = ["pink", "light grey", "yellow"]
        # coordinate of top left of first button
        margin = 5
        self.exitButtonW = self.size/self.buttons
        self.exitButtonH = self.exitButtonW/self.buttons
        self.exitButtonX = margin
        self.exitButtonY = self.height-margin-self.exitButtonH

    def solutionButtonInfo(self):
        proportion = 1.0/3.0
        self.solutionButtons = ["Place Axles", "Solution"]
        self.solutionButtonColors = ["pink", "light green"]
        # coordinate of top left of first button
        marginY = 5
        marginX = 350
        self.solButtonW = 2*self.size*proportion
        self.solButtonH = self.size*proportion**2
        self.solButtonX = marginX
        self.solButtonY = self.height-marginY-self.solButtonH

################################ Draw Functions ################################

    def draw(self, canvas):
        # Trashcan
        self.drawTrashcan(canvas)
        # Buttons
        self.drawGameButtons(canvas)
        self.drawExitButtons(canvas)
        self.drawSolutionButtons(canvas)
        minHighLevel = 9                                
        if (self.level < minHighLevel):
            self.drawTagButton(canvas)
            if self.tagButtonSelected:
                self.highlightTagButton(canvas)
        # Background
        self.drawBackground(canvas)
        # Motor and Wheel Information
        self.writeMotorWheelInfo(canvas)
        # Entry for number of teeth
        self.drawEntry(canvas)
        # Gear
        if (self.gear != None):
            self.gear.draw(canvas)
        # Axle
        if (self.axles > 0):
            (x, y) = (self.x, self.y)
            self.drawAxle(canvas, x, y)
        # Write number of axles available
        self.writeAxles(canvas)

    def drawBackground(self, canvas):
        for i in xrange(self.backgrounds):
            color = self.backgroundColors[i]
            (x, y) = (self.width-(1+i)*self.size, 0)
            canvas.create_rectangle(x, y, x+self.size, y+self.size,
                                    fill=color, width=0)

    # Draw Run, Hint, and Done buttons
    def drawGameButtons(self, canvas):
        (x, y) = (self.gameButtonX, self.gameButtonY)
        buttonW, buttonH = (self.gameButtonW, self.gameButtonH)
        dy = 10
        for i in xrange(self.buttons):
            y0 = y+(i*(dy+buttonH))
            # Box
            color = self.gameButtonColors[i]
            canvas.create_rectangle(x, y0, x+buttonW, y0+buttonH, fill=color)
            # Text
            text = self.gameButtons[i]
            size = "20"
            canvas.create_text( x+buttonW/2, y0+buttonH/2, text=text, 
                                font="Courier "+size+" bold")

    # Save and Exit, Quit, and Clear buttons
    def drawExitButtons(self, canvas):
        (x, y) = (self.exitButtonX, self.exitButtonY)
        buttonH = self.exitButtonH
        dx = 10
        for i in xrange(self.buttons):
            proportion = 5.0/2.0
            if (i == 0): # a little longer button
                buttonW = self.exitButtonW*proportion
                x0 = x
            elif (i == 1):
                x0 = x + dx + buttonW
                buttonW = self.exitButtonW
            elif (i == 2):
                buttonW = self.exitButtonW
                x0 = x + i*dx + buttonW + buttonW*proportion
            # Box
            color = self.exitButtonColors[i]
            canvas.create_rectangle(x0, y, x0+buttonW, y+buttonH, 
                                    fill=color)
            # Text
            text = self.exitButtons[i]
            size = "15"
            canvas.create_text( x0+buttonW/2, y+buttonH/2, text=text,
                                font="Courier "+size+" bold") 

    def drawSolutionButtons(self, canvas):
        (x, y) = (self.solButtonX, self.solButtonY)
        buttonW, buttonH = (self.solButtonW, self.solButtonH)
        dx = 10
        for i in xrange(2):
            x0 = x+(i*(dx+buttonW))
            # Box
            color = self.solutionButtonColors[i]
            canvas.create_rectangle(x0, y, x0+buttonW, y+buttonH, fill=color)
            # Text
            text = self.solutionButtons[i]
            size = "15"
            canvas.create_text( x0+buttonW/2, y+buttonH/2, text=text, 
                                font="Courier "+size+" bold")

    # Draw tag that shows the speed and direction of gear
    def drawTagButton(self, canvas):
        margin = 10
        buttonW, buttonH = (self.gameButtonW, self.gameButtonH)
        x = self.gameButtonX
        y = self.height - margin - buttonH
        # Box
        color = "light blue"
        canvas.create_rectangle(x, y, x+buttonW, y+buttonH, fill=color)
        # Text
        text = "Tag"
        size = "20"
        canvas.create_text( x+buttonW/2, y+buttonH/2, text=text, 
                            font="Courier "+size+" bold") 

    def drawEntry(self, canvas):
        # Entry Box
        (x, y) = (self.width-self.size/2, self.size+self.dy)
        (entryH, entryW) = (self.size/self.dy, self.size/3)
        canvas.create_rectangle(x, y, x+entryW, y+entryH)
        # Entry label
        text = "N = "
        size = "20"
        canvas.create_text(  x, y, text=text, anchor="ne", 
                            font="Courier "+size+" bold")
        # Write entry
        text = self.entryText
        size = "15"
        dx, dy = 10, 5
        canvas.create_text( x+dx, y+dy, text=text, anchor="nw",
                            font="Arial "+size+" bold")

    def drawAxle(self, canvas, x, y):
        color = self.axleColor
        width = 2*self.axleR
        # Body
        canvas.create_line( x, y, x-self.size/2, y+self.size/2, 
                            fill=color, width=width )
        # Edges
        for i in xrange(2):
            (x0, y0) = (x - i*self.size/2, y + i*self.size/2)
            r = self.axleR
            outlineColor = "grey"
            if (i == 0): # backside
                width = 0
            elif (i ==1): # frontside
                width = 1
            canvas.create_oval( x0-r, y0-r, x0+r, y0+r, 
                                fill=color, outline=outlineColor, width=width)      

    # Write how many axles are available
    def writeAxles(self, canvas):
        text = str(self.axles)
        color = "red"
        size = "20"
        horizontalDiv = 1.0/4.0
        verticalDiv = 7.0/4.0
        (x, y) = (self.width-self.size*verticalDiv, self.size*horizontalDiv)
        canvas.create_text( x, y, text=text, fill=color, 
                            font="Arial "+size+" bold" )

    def writeMotorWheelInfo(self, canvas):
        motorSpeed = self.levelDetails[1][1]
        motorDirection = self.levelDetails[1][2]
        wheelSpeed = self.levelDetails[2][1]
        wheelDirection = self.levelDetails[2][2]
        margin = 18
        (x, y) = (self.width - 3*self.size + margin, margin)
        size = "13"
        text = ("Motor: (Blue) \n%d rpm %s \n\n\nWheel: (Red)\n%d rpm %s" 
                % (motorSpeed, motorDirection, wheelSpeed, wheelDirection))
        canvas.create_text( x, y, text=text, anchor="nw",
                            font="Arial "+size)
        # Wheel Radius Info
        wheelRadiusIndex = 4
        wheelR = self.levelDetails[wheelRadiusIndex]
        text = "Wheel Radius = "+str(wheelR)+" cm"
        margin = 140
        canvas.create_text( x, margin, text=text, anchor="nw", 
                            font="Arial "+size)

    def drawTrashcan(self, canvas):
        title = PhotoImage(file="trashcan.gif").subsample(2,2)                   
        label = Label(image=title)
        label.image = title
        vertDiv = 9.0/10.0
        horiDiv = 2.0/3.0
        canvas.create_image(self.width*vertDiv, self.height*horiDiv, 
                            anchor="nw", image=title)  

###### Highlight ######      

    def highlightGameButton(self, canvas, button):
        i = self.gameButtons.index(button)
        dy = 10
        (x, y) = (self.gameButtonX, self.gameButtonY+(i*(dy+self.gameButtonH)))
        buttonW, buttonH = (self.gameButtonW, self.gameButtonH)
        color = "green"
        canvas.create_rectangle(x, y, x+buttonW, y+buttonH, 
                                outline=color, width=2)

    def highlightExitButton(self, canvas, button):
        i = self.exitButtons.index(button)
        (x, y) = (self.exitButtonX, self.exitButtonY)
        buttonH = self.exitButtonH
        dx = 10
        proportion = 5.0/2.0
        if (i == 0): # a little longer button
            buttonW = self.exitButtonW*proportion
            x0 = x
        elif (i == 1):
            buttonW = self.exitButtonW
            x0 = x + dx + self.exitButtonW*proportion
        elif (i == 2):
            buttonW = self.exitButtonW
            x0 = x + i*dx + buttonW + buttonW*proportion
        color = "green"
        canvas.create_rectangle(x0, y, x0+buttonW, y+buttonH, 
                                outline=color, width=2)  

    def highlightSolutionButton(self, canvas, button):
        i = self.solutionButtons.index(button)
        (x, y) = (self.solButtonX, self.solButtonY)
        buttonW, buttonH = (self.solButtonW, self.solButtonH)
        dx = 10
        x0 = x+(i*(dx+buttonW))
        color = "green"
        canvas.create_rectangle(x0, y, x0+buttonW, y+buttonH, 
                                outline=color, width=2)

    def highlightTagButton(self, canvas):
        margin = 10
        buttonW, buttonH = (self.gameButtonW, self.gameButtonH)
        x = self.gameButtonX
        y = self.height - margin - buttonH
        color = "green"
        canvas.create_rectangle(x, y, x+buttonW, y+buttonH, 
                                outline=color, width=2) 

    def highlightAxleBox(self, canvas):
        color = "red"
        width = 10
        (x, y) = (self.width-2*self.size, 0)
        canvas.create_rectangle(x, y, x+self.size, y+self.size,
                                outline=color, width=width)

############################### Contain Functions ##############################
    
    # checks if mouse is on axle or gear display
    def contain(self, x, y):
        (x0, y0) = (self.x, self.y)
        if (x0-self.size/2 < x < x0) and (y0 < y < y0+self.size/2):
            return "Axle"
        elif (self.gear != None) and self.gear.contain(x, y):
            return "Gear"

    def containEntry(self, x, y):
        (x0, y0) = (self.width-self.size/2, self.size+self.dy)
        (entryH, entryW) = (self.size/self.dy, self.size/3)
        if (x0 < x < x0+entryW) and (y0 < y < y0+entryH):
            return True
        return False

    def containTrash(self, x, y):
        vertDiv = 10.0/11.0
        horiDiv = 2.0/3.0
        proportion = 1.0/4.0
        (x0, y0) = (self.width*vertDiv, self.height*horiDiv)
        size = self.size*proportion
        if (x0 < x < x0+size) and (y0 < y < y0+size):
            return True
        return False

    def containGameButton(self, x, y):
        buttonW, buttonH = (self.gameButtonW, self.gameButtonH)
        dy = 10
        for i in xrange(self.buttons):
            (x0, y0) = (self.gameButtonX, self.gameButtonY+(i*(dy+buttonH)))
            if (x0 < x < x0+buttonW) and (y0 < y < y0+buttonH):
                return self.gameButtons[i]

    def containExitButton(self, x, y):
        (x0, y0) = (self.exitButtonX, self.exitButtonY)
        buttonH = self.exitButtonH
        dx = 10
        for i in xrange(self.buttons):
            proportion = 5.0/2.0
            if (i == 0): # a little longer button
                buttonW = self.exitButtonW*proportion
                x1 = x0
            elif (i == 1):
                buttonW = self.exitButtonW
                x1 = x0 + dx + self.exitButtonW*proportion
            elif (i == 2):
                buttonW = self.exitButtonW
                x1 = x0 + i*dx + buttonW + buttonW*proportion
            if (x1 < x < x1+buttonW) and (y0 < y < y0+buttonH):
                return self.exitButtons[i]

    def containSolutionButton(self, x, y):
        (x0, y0) = (self.solButtonX, self.solButtonY)
        buttonW, buttonH = (self.solButtonW, self.solButtonH)
        dx = 10
        for i in xrange(2):
            x1 = x0+(i*(dx+buttonW))
            if (x1 < x < x1+buttonW) and (y0 < y < y0+buttonH):
                return self.solutionButtons[i]

    def containTagButton(self, x, y):
        margin = 10
        buttonW, buttonH = (self.gameButtonW, self.gameButtonH)
        x0 = self.gameButtonX
        y0 = self.height - margin - buttonH
        if (x0 < x < x0+buttonW) and (y0 < y < y+buttonH):
            return True
        return False 

###############################################################################
###############################################################################
### Car Traveling Scene ###

class Car(Window):
    def __init__(self, color="purple"):
        Window.__init__(self)
        # Background
        self.backgroundColor = "green"
        # Road
        self.roadColor = "light grey"
        self.roadW = self.height/2
        self.roadX, self.roadY = 0, self.height/3
        # Start Line
        self.startX = 100
        # Finish Line
        margin = 150
        self.lineX, self.lineY = self.width-margin, self.height/3
        self.lineColor = "red"
        # Time
        self.time = 10 # seconds
        # Countdown
        self.countdownText = 5 # seconds
        # Distance
        self.distance = 0
        # Car
        ## Your Car 
        self.yourCarColor = color
        proportion = 1.0/10.0
        self.carW = self.width*proportion
        self.wheelR = self.carW*proportion
        margin = 200
        self.yourX, self.yourY = margin/2, self.roadY+margin
        ## Demo Car
        self.demoX, self.demoY = margin/2, self.roadY+margin/2

################################ Draw Functions ################################

    def draw(self, canvas):
        # Background 
        canvas.create_rectangle(0, 0, self.width, self.height, 
                                fill=self.backgroundColor)
        # Road
        (x, y) = (self.roadX, self.roadY)
        canvas.create_rectangle(x, y, self.width, y+self.roadW,
                                fill=self.roadColor)
        # Finish Line
        width = 10
        (x, y) = (self.lineX, self.lineY)
        canvas.create_line( x, y, x, y+self.roadW, 
                            fill=self.lineColor, width=width )
        # Your Car
        self.drawCar(canvas,"Your Car")
        # Demo Car
        self.drawCar(canvas, "Demo Car")
        # Info: Time, Distance, Demo Car Color, You Car Color
        self.writeInfo(canvas)
        # Countdown
        self.countdown(canvas)

    def drawCar(self, canvas, car): 
        if (car == "Your Car"):
            (x, y) = (self.yourX, self.yourY) 
            color = self.yourCarColor
        elif (car == "Demo Car"):
            (x, y) = (self.demoX, self.demoY)
            color = "brown"
        ## body:
        margin = self.carW/3
        dy = margin/2
        canvas.create_rectangle(x+margin, y, x+2*margin, y+dy, fill=color)
        canvas.create_rectangle(x, y+dy, x+self.carW, y+2*dy, fill=color)
        ## wheels:
        wheelColor = "black"
        for i in xrange(2):
            (cx, cy, r) = (x+(1+i)*margin, y+2*dy, self.wheelR)
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=wheelColor)

    def writeInfo(self, canvas):
        # Time
        margin0 = 50
        text = "Time: "+str(self.time)+" s"
        size = "40"
        canvas.create_text( margin0, margin0, anchor="nw",
                            text=text, font="Courier "+size+" bold")
        # Distance
        size = "25"
        text = "Distance: "+str(self.distance)+" m"
        margin = 100
        canvas.create_text( margin0, margin, anchor="nw",
                            text=text, font="Courier "+size+" bold")
        # Demo Car Color
        text = "Demo Car: Brown"
        color = "brown"
        margin = 130
        canvas.create_text( margin0, margin, text=text, anchor="nw",
                            fill=color, font="Courier "+size)
        # Your Car Color
        color = self.yourCarColor
        if (color == "dark green"): color = "Green"
        text = "Your Car: "+color[0].upper()+color[1:len(color)]
        color = self.yourCarColor
        margin = 160
        canvas.create_text( margin0, margin, text=text, anchor="nw",
                            fill=color, font="Courier "+size)

    def countdown(self, canvas):
        text = str(self.countdownText)
        size = "100"
        margin = 50
        color = "blue"
        canvas.create_text( self.width-margin, margin, anchor="ne", fill=color,
                            text=text, font="Courier "+size+" bold")

###############################################################################
###############################################################################
#### Username and Car ####

class Player(Car):
    def __init__(self, username, color="purple", dy = 50):
        Car.__init__(self)
        self.username = username
        self.yourCarColor = color
        self.dy = dy

    def draw(self, canvas):
        self.writeUsername(canvas)

    def writeUsername(self, canvas):
        text = "Player: "+self.username
        size = "15"
        dx = 10
        dy = self.dy
        canvas.create_text( dx, dy, text=text, anchor="nw", 
                            font="Courier "+size)
        self.drawUserCar(canvas)

    def drawUserCar(self, canvas):
        proportion = 1.0/4.0
        x = self.width*proportion
        y = self.dy
        color = self.yourCarColor
        margin = self.carW/3
        dy = margin/2
        canvas.create_rectangle(x+margin, y, x+2*margin, y+dy, fill=color)
        canvas.create_rectangle(x, y+dy, x+self.carW, y+2*dy, fill=color)
        ## wheels:
        wheelColor = "black"
        for i in xrange(2):
            (cx, cy, r) = (x+(1+i)*margin, y+2*dy, self.wheelR)
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=wheelColor)

