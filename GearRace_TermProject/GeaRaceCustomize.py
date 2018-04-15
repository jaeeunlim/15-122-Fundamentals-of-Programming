# By Jae-Eun (Esther) Lim 
# jaeeunl
# Section R
###############################################################################
from Tkinter import *
from GeaRaceManage import *
from GeaRaceGame import *
###############################################################################
###############################################################################
### Make Your Game ###

class Customize(Window):
    def __init__(self, username, color="purple"):
        Window.__init__(self)
        self.preview = Preview()
        self.board = Board()
        self.player = Player(username, color)
        self.dx = self.dy = 5
        vertDiv = 3.0/4.0
        horiDiv = 1.0/3.0
        margin = 15
        self.x = self.width*vertDiv # left side of all entry
        self.y = self.height*horiDiv+margin # top of entry
        self.entryW = self.entryH = 20
        # Entries
        self.entryInit()
        # Highlight
        self.highlightInit()

    def entryInit(self):
        self.rows = ""
        self.cols = ""
        self.axles = ""
        self.motorSpeed = ""
        self.motorDirection = ""
        self.wheelSpeed = ""
        self.wheelDirection = ""
        self.wheelR = ""
        self.motorRow = ""
        self.motorCol = ""
        self.wheelRow = ""
        self.wheelCol = ""

    def highlightInit(self):
        self.color = "cyan"
        self.rowsSelected = False
        self.colsSelected = False
        self.axlesSelected = False
        self.motorSpeedSelected = False
        self.motorDirSelected = False
        self.wheelSpeedSelected = False
        self.wheelDirSelected = False
        self.wheelRadiusSelected = False
        self.motorRowSelected = False
        self.motorColSelected = False
        self.wheelRowSelected = False
        self.wheelColSelected = False
        self.submitSelected = False
        self.backSelected = False

################################## Draw Function ###############################

    def draw(self, canvas):
        self.preview.drawBackground(canvas)
        self.player.writeUsername(canvas)
        # Board
        (x, y) = (self.board.x0, self.board.y0)
        canvas.create_rectangle(x, y, x+self.board.boardW, y+self.board.boardH,
                                fill=self.board.color)
        # Title
        text = "Your Game"
        size = "25"
        margin = 10
        canvas.create_text( margin, margin, text=text, anchor="nw", 
                            font="Courier "+size+" bold underline" )
        self.drawCustomizeInfo(canvas)

    def drawCustomizeInfo(self, canvas):
        # Board Size
        self.drawBoardSize(canvas)
        self.drawBoardEntry(canvas)
        # Required Number of Axles
        self.drawNumberOfAxles(canvas)
        # Motor Info
        self.drawMotorInfo(canvas)
        self.drawMotorSpeedEntry(canvas)
        self.drawMotorDirEntry(canvas)
        # Wheel Info
        self.drawWheelInfo(canvas)
        self.drawWheelSpeedEntry(canvas)
        self.drawWheelDirEntry(canvas)
        self.drawWheelRadiusEntry(canvas)
        # Buttons (place motor/wheel/submit axle)
        self.drawMotorAxle(canvas)
        self.drawMotorAxleEntry(canvas)
        self.drawWheelAxle(canvas)
        self.drawWheelAxleEntry(canvas)
        self.drawSubmit(canvas)
        self.drawBack(canvas)

    def drawBoardSize(self, canvas):
        (x, y) = (self.x, self.y)
        text1 = "Board Size:"
        size = "11"
        canvas.create_text(x, y, text=text1, anchor="sw", font="Courier "+size)
        text3 = "Rows"
        size = "10"
        canvas.create_text( x+self.dx, y+self.dy, text=text3, anchor="nw", 
                            font="Courier "+size)
        text4 = "Columns"
        margin = 100
        canvas.create_text( x+margin, y+self.dy, text=text4, anchor="nw", 
                            font="Courier "+size)

    def drawBoardEntry(self, canvas):
        (x, y) = (self.x, self.y)
        size = "13"
        # Rows
        margin = 40
        canvas.create_rectangle(x+margin,y,x+margin+self.entryW,y+self.entryH)
        if (self.rowsSelected == True): # highlight
            canvas.create_rectangle(x+margin, y, x+margin+self.entryW,
                                    y+self.entryH, outline=self.color, width=2)
        text1 = self.rows
        canvas.create_text( x+margin+self.entryW/2, y+self.entryH/2, 
                            text=text1, font="Courier "+size)
        margin = 150
        canvas.create_rectangle(x+margin, y, 
                                x+margin+self.entryW, y+self.entryH)
        if (self.colsSelected == True): # highlight
            canvas.create_rectangle(x+margin, y, x+margin+self.entryW,
                                    y+self.entryH, outline=self.color, width=2)
        text2 = self.cols
        canvas.create_text( x+margin+self.entryW/2, y+self.entryH/2, 
                            text=text2, font="Courier "+size)

    def drawNumberOfAxles(self, canvas):
        margin = 45
        (x, y) = (self.x, self.y+margin)
        text1 = "Number of Axles:"
        size = "11"
        canvas.create_text(x, y, text=text1, anchor="sw", font="Courier "+size)
        # Entry Box
        margin = 130
        canvas.create_rectangle(x+margin, y-self.entryH+self.dy, 
                                x+margin+self.entryW, y+self.dy)
        if (self.axlesSelected == True):
            canvas.create_rectangle(x+margin, y-self.entryH+self.dy, 
                                    x+margin+self.entryW, y+self.dy,
                                    outline=self.color, width=2)
        text2 = self.axles
        size = "13"
        canvas.create_text( x+margin+self.entryW/2, 
                            y-self.entryH+self.dy+self.entryH/2, 
                            text=text2, font="Courier "+size)

    def drawMotorInfo(self, canvas):
        margin = 75
        (x, y) = (self.x, self.y+margin)
        size = "11"
        text1 = "Motor Speed:"
        canvas.create_text(x, y, text=text1, anchor="sw", font="Courier "+size)
        text2 = "rpm"
        dx = 130
        canvas.create_text( x+dx, y, text=text2, anchor="sw", 
                            font="Courier "+size)
        text3 = "Motor Direction:"
        dy = 30
        canvas.create_text( x, y+dy, text=text3, anchor="sw", 
                            font="Courier "+size)

    def drawMotorSpeedEntry(self, canvas):
        margin = 75
        (x, y) = (self.x, self.y+margin)
        margin = 100
        canvas.create_rectangle(x+margin, y-self.entryH+self.dy, 
                                x+margin+self.entryW, y+self.dy) 
        if (self.motorSpeedSelected == True):
            canvas.create_rectangle(x+margin, y-self.entryH+self.dy,
                                    x+margin+self.entryW, y+self.dy, 
                                    outline=self.color, width=2) 
        text1 = self.motorSpeed
        size = "13"
        canvas.create_text( x+margin+self.entryW/2, 
                            y-self.entryH+self.dy+self.entryH/2, 
                            text=text1, font="Courier "+size)

    def drawMotorDirEntry(self, canvas):
        margin = 75
        (x, y) = (self.x, self.y+margin)
        proportion = 11.0/2.0
        margin = 110
        dy = 35
        entryW = self.entryW*proportion
        canvas.create_rectangle(x+margin,y-self.entryH+dy,x+margin+entryW,y+dy)
        if (self.motorDirSelected == True):
            canvas.create_rectangle(x+margin, y-self.entryH+dy, x+margin+entryW, 
                                    y+dy, outline=self.color, width=2)
        text2 = self.motorDirection
        size = "10"
        canvas.create_text( x+margin+self.dx, y-self.entryH+dy+self.entryH/2, 
                            text=text2, anchor="w", font="Courier "+size)

    def drawWheelInfo(self, canvas):
        margin = 135
        (x, y) = (self.x, self.y+margin)
        size = "11"
        text1 = "Wheel Speed:"
        canvas.create_text(x, y, text=text1, anchor="sw", font="Courier "+size)
        text2 = "rpm"
        dx = 130
        canvas.create_text(x+dx, y,text=text2,anchor="sw",font="Courier "+size)
        text3 = "Wheel Direction:"
        dy = 30
        canvas.create_text(x,y+dy,text=text3,anchor="sw",font="Courier "+size)
        text4 = "Wheel Radius:"
        margin = 60
        y0 = y+margin
        canvas.create_text(x,y0,text=text4,anchor="sw",font="Courier "+size)
        text5 = "cm"
        dx = 130
        canvas.create_text(x+dx,y0,text=text5,anchor="sw",font="Courier "+size)
        
    def drawWheelDirEntry(self, canvas):
        margin = 135
        (x, y) = (self.x, self.y+margin) 
        proportion = 11.0/2.0
        dx, dy = 110, 35
        entryW = self.entryW*proportion
        canvas.create_rectangle(x+dx,y-self.entryH+dy,x+dx+entryW,y+dy)
        if (self.wheelDirSelected == True):
            canvas.create_rectangle(x+dx,y-self.entryH+dy,x+dx+entryW,y+dy,
                                    outline=self.color, width=2)
        text1 = self.wheelDirection
        size = "10"
        canvas.create_text( x+dx+self.dx, y-self.entryH+dy+self.entryH/2, 
                            text=text1, anchor="w", font="Courier "+size)

    def drawWheelSpeedEntry(self, canvas):
        margin = 135
        (x, y) = (self.x, self.y+margin) 
        margin = 100
        canvas.create_rectangle(x+margin, y-self.entryH+self.dy, 
                                x+margin+self.entryW, y+self.dy)
        if (self.wheelSpeedSelected == True):
            canvas.create_rectangle(x+margin, y-self.entryH+self.dy, 
                                    x+margin+self.entryW, y+self.dy,
                                    outline=self.color, width=2)
        text2 = self.wheelSpeed
        size = "13"
        canvas.create_text( x+margin+self.entryW/2, 
                            y-self.entryH+self.dy+self.entryH/2, 
                            text=text2, font="Courier "+size)

    def drawWheelRadiusEntry(self, canvas):
        margin = 135
        (x, y) = (self.x, self.y+margin) 
        ## Radius
        margin = 100
        dy = 55
        y0 = y+dy
        canvas.create_rectangle(x+margin, y0-self.entryH+self.dy, 
                                x+margin+self.entryW, y0+self.dy)
        if (self.wheelRadiusSelected == True):
            canvas.create_rectangle(x+margin, y0-self.entryH+self.dy, 
                                    x+margin+self.entryW, y0+self.dy,
                                    outline=self.color, width=2)  
        text3 = self.wheelR
        size = "13"
        canvas.create_text( x+margin+self.entryW/2, 
                            y0-self.entryH+self.dy+self.entryH/2, 
                            text=text3, font="Courier "+size)

    def drawMotorAxle(self, canvas):
        margin = 225
        (x, y) = (self.x, self.y+margin)
        text1 = "Motor Axle:"
        size = "11"
        canvas.create_text(x, y, text=text1, anchor="sw", font="Courier "+size)
        text3 = "Row"
        size = "10"
        canvas.create_text( x+self.dx, y+self.dy, text=text3, anchor="nw", 
                            font="Courier "+size)
        text4 = "Column"
        margin = 100
        canvas.create_text( x+margin, y+self.dy, text=text4, anchor="nw", 
                            font="Courier "+size)

    def drawMotorAxleEntry(self, canvas):
        margin = 225
        (x, y) = (self.x, self.y+margin)
        size = "13"
        # Rows
        margin = 40
        canvas.create_rectangle(x+margin,y,x+margin+self.entryW,y+self.entryH)
        if (self.motorRowSelected == True): # highlight
            canvas.create_rectangle(x+margin, y, x+margin+self.entryW,
                                    y+self.entryH, outline=self.color, width=2)
        text1 = self.motorRow
        canvas.create_text( x+margin+self.entryW/2, y+self.entryH/2, 
                            text=text1, font="Courier "+size)
        margin = 150
        canvas.create_rectangle(x+margin, y, 
                                x+margin+self.entryW, y+self.entryH)
        if (self.motorColSelected == True): # highlight
            canvas.create_rectangle(x+margin, y, x+margin+self.entryW,
                                    y+self.entryH, outline=self.color, width=2)
        text2 = self.motorCol
        canvas.create_text( x+margin+self.entryW/2, y+self.entryH/2, 
                            text=text2, font="Courier "+size)

    def drawWheelAxle(self, canvas):
        margin = 20
        (x, y) = (self.x, self.y*2+margin)
        text1 = "Wheel Axle:"
        size = "11"
        canvas.create_text(x, y, text=text1, anchor="sw", font="Courier "+size)
        text3 = "Row"
        size = "10"
        canvas.create_text( x+self.dx, y+self.dy, text=text3, anchor="nw", 
                            font="Courier "+size)
        text4 = "Column"
        margin = 100
        canvas.create_text( x+margin, y+self.dy, text=text4, anchor="nw", 
                            font="Courier "+size)

    def drawWheelAxleEntry(self, canvas):
        margin = 20
        (x, y) = (self.x, self.y*2+margin)
        size = "13"
        # Rows
        margin = 40
        canvas.create_rectangle(x+margin,y,x+margin+self.entryW,y+self.entryH)
        if (self.wheelRowSelected == True): # highlight
            canvas.create_rectangle(x+margin, y, x+margin+self.entryW,
                                    y+self.entryH, outline=self.color, width=2)
        text1 = self.wheelRow
        canvas.create_text( x+margin+self.entryW/2, y+self.entryH/2, 
                            text=text1, font="Courier "+size)
        margin = 150
        canvas.create_rectangle(x+margin, y, 
                                x+margin+self.entryW, y+self.entryH)
        if (self.wheelColSelected == True): # highlight
            canvas.create_rectangle(x+margin, y, x+margin+self.entryW,
                                    y+self.entryH, outline=self.color, width=2)
        text2 = self.wheelCol
        canvas.create_text( x+margin+self.entryW/2, y+self.entryH/2, 
                            text=text2, font="Courier "+size)

    def drawSubmit(self, canvas):
        proportion = 4
        (entryW, entryH) = (self.entryW*proportion, self.entryH)
        size = "13"
        dy = 310
        (x, y) = (self.x, self.y+dy) 
        color = "green"
        canvas.create_rectangle(x, y, x+entryW, y+entryH, fill=color)
        if (self.submitSelected == True):
            canvas.create_rectangle(x, y, x+entryW, y+entryH,
                                    outline=self.color, width=2)
        text = "Submit"
        canvas.create_text(x+entryW/2, y+entryH/2, text=text,
                           font="Courier "+size+" bold")

    def drawBack(self, canvas):
        proportion = 4
        (entryW, entryH) = (self.entryW*proportion, self.entryH)
        size = "13"
        dy = 340
        (x, y) = (self.x, self.y+dy) 
        color = "pink"
        canvas.create_rectangle(x, y, x+entryW, y+entryH, fill=color)
        if (self.backSelected == True):
            canvas.create_rectangle(x, y, x+entryW, y+entryH,
                                    outline=self.color, width=2)
        text = "Back"
        canvas.create_text(x+entryW/2, y+entryH/2, text=text,
                           font="Courier "+size+" bold")

############################### Contain Function ###############################
    
    def contain(self, x, y):
        if (self.containBoardSizeOrAxle(x, y) != None):
            return self.containBoardSizeOrAxle(x, y)
        elif (self.containMotorInfo(x, y) != None):
            return self.containMotorInfo(x, y)
        elif (self.containWheelInfo(x, y) != None):
            return self.containWheelInfo(x, y)
        elif (self.containMotorWheelAxle(x, y) != None):
            return self.containMotorWheelAxle(x, y)
        elif (self.containButtons(x, y) != None):
            return self.containButtons(x, y)

    def containBoardSizeOrAxle(self, x, y):
        # Rows
        (x0, y0) = (self.x, self.y)
        margin = 40
        if ((x0+margin < x < x0+margin+self.entryW) and 
            (y0 < y < y0+self.entryH)): return "Rows"
        # Cols
        margin = 150
        if ((x0+margin < x < x0+margin+self.entryW) and 
            (y0 < y < y0+self.entryH)): return "Cols"
        # Axles
        margin = 45
        (x0, y0) = (self.x, self.y+margin)
        margin = 130
        if ((x0+margin < x < x0+margin+self.entryW) and 
            (y0-self.entryH+self.dy < y < y0+self.dy)): return "Axles"

    def containMotorInfo(self, x, y):
        margin = 75
        (x0, y0) = (self.x, self.y+margin)
        ## Speed
        margin = 100
        if ((x0+margin < x < x0+margin+self.entryW) and 
            (y0-self.entryH+self.dy < y < y0+self.dy)): return "Motor Speed"
        ## Direction
        proportion = 11.0/2.0
        margin = 110
        dy = 35
        entryW = self.entryW*proportion
        if ((x0+margin < x < x0+margin+entryW) and 
            (y0-self.entryH+dy < y < y0+dy)): return "Motor Direction"

    def containWheelInfo(self, x, y):
        margin = 135
        (x0, y0) = (self.x, self.y+margin) 
        ## Direction
        proportion = 11.0/2.0
        dx, dy = 110, 35
        entryW = self.entryW*proportion
        if ((x0+dx < x < x0+dx+entryW) and 
            (y0-self.entryH+dy < y < y0+dy)): return "Wheel Direction"
        ## Speed
        margin = 100
        if ((x0+margin < x < x0+margin+entryW) and 
            (y0-self.entryH+self.dy < y < y0+self.dy)): return "Wheel Speed"
        ## Radius
        margin = 100
        dy = 55
        y0 = y0+dy
        if ((x0+margin < x < x0+margin+entryW) and 
            (y0-self.entryH+self.dy < y < y0+self.dy)): return "Wheel Radius" 

    def containMotorWheelAxle(self, x, y):
        # Motor Axle Row
        margin = 225
        (x0, y0) = (self.x, self.y+margin)
        margin = 40
        if ((x0+margin < x < x0+margin+self.entryW) and 
            (y0 < y < y0+self.entryH)): return "Motor Row"
        # Motor Axle Col
        margin = 150
        if ((x0+margin < x < x0+margin+self.entryW) and 
            (y0 < y < y0+self.entryH)): return "Motor Col"
        # Wheel Axle Row
        margin = 20
        (x0, y0) = (self.x, self.y*2+margin)
        margin = 40
        if ((x0+margin < x < x0+margin+self.entryW) and 
            (y0 < y < y0+self.entryH)): return "Wheel Row"
        # Wheel Axle Col
        margin = 150
        if ((x0+margin < x < x0+margin+self.entryW) and 
            (y0 < y < y0+self.entryH)): return "Wheel Col"

    def containButtons(self, x, y):
        # Submit Button
        proportion = 4
        (entryW, entryH) = (self.entryW*proportion, self.entryH)
        dy = 310
        (x0, y0) = (self.x, self.y+dy) 
        if (x0 < x < x0+entryW) and (y0 < y < y0+entryH): return "Submit" 
        # Back Button
        dy = 340
        (x0, y0) = (self.x, self.y+dy) 
        if (x0 < x < x0+entryW) and (y0 < y < y0+entryH): return "Back" 

###############################################################################
###############################################################################
### Make Your Game ###

class MakeYourGame(Window):
    def __init__(self, username, color="purple"):
        Window.__init__(self)
        self.preview = Preview()
        self.board = Board()
        self.player = Player(username, color)
        self.customize = Customize()

    def draw(self, canvas):
        self.preview.drawBackground(canvas)
        self.preview.drawExitButtons(canvas)
        self.player.writeUsername(canvas)
        self.customize.draw(canvas)
        # Board
        (x, y) = (self.board.x0, self.board.y0)
        canvas.create_rectangle(x, y, x+self.boardW, y+self.boardH,
                                fill=self.board.color)
        # Title
        text = "Your Game"
        size = "25"
        margin = 10
        canvas.create_text( margin, margin, text=text, anchor="nw", 
                            font="Courier "+size+" bold underline" )