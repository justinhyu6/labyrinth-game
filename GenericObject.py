import math, copy, random

from Board import *

class GenericObject:
    def __init__(self, app, tileRow, tileCol):
        self.tileRow = tileRow
        self.tileCol = tileCol
        x, y = getTileCenter(app, tileRow, tileCol)
        self.x = x
        self.y = y
    
    def getTileRow(self):
        return self.tileRow
    
    def getTileCol(self):
        return self.tileCol
    
    def shift(self, app, tileRowShift, tileColShift):
        self.tileRow += tileRowShift
        self.tileCol += tileColShift

        if(self.tileRow >= 7):
            self.tileRow = 0
        elif(self.tileCol >= 7):
            self.tileCol = 0
        elif(self.tileRow < 0):
            self.tileRow = 6
        elif(self.tileCol < 0):
            self.tileCol = 6
        
        self.x, self.y = getTileCenter(app, self.tileRow, self.tileCol)

class Wizard(GenericObject):
    def __init__(self, app, tileRow, tileCol, color):
        super().__init__(app, tileRow, tileCol)
        self.color = color
    
    def redraw(self, canvas):
        radius = 12
        x0 = self.x - radius
        y0 = self.y - radius
        x1 = self.x + radius
        y1 = self.y + radius
        canvas.create_oval(x0, y0, x1, y1,
                            fill=self.color, outline='black', width=0)
    
    def move(self, app, tileRowShift, tileColShift):
        newTileRow = self.tileRow+tileRowShift
        newTileCol = self.tileCol+tileColShift
        if(tileRowShift == 0 and tileColShift == 0):
            return None
        elif(newTileRow < 0 or newTileRow >= app.tileRows or
            newTileCol < 0 or newTileCol >= app.tileCols):
            return None

        tileToCheck = app.board[newTileRow][newTileCol]
        hasPath = False
        if(tileColShift == -1):
            hasPath = tileToCheck.getList()[1][2]
        elif(tileColShift == 1):
            hasPath = tileToCheck.getList()[1][0]
        elif(tileRowShift == -1):
            hasPath = tileToCheck.getList()[2][1]
        elif(tileRowShift == 1):
            hasPath = tileToCheck.getList()[0][1]
        
        currentTile = app.board[self.tileRow][self.tileCol]
        hasPathCurrent = currentTile.getList()[1+tileRowShift][1+tileColShift]

        if(hasPath and hasPathCurrent):
            self.shift(app, tileRowShift, tileColShift)

class Treasure(GenericObject):
    def __init__(self, app, tileRow, tileCol, name):
        super().__init__(app, tileRow, tileCol)
        self.name = name
    
    def redraw(self, canvas):
        canvas.create_text(self.x, self.y, text = self.name[:2],
                            fill='black', font = 'Georgia 12')