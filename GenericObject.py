import math, copy, random

from Board import *

class GenericObject:
    def __init__(self, app, tileRow, tileCol):
        self.tileRow = tileRow
        self.tileCol = tileCol
        self.x, self.y = getTileCenter(app, tileRow, tileCol)
    
    def getTileRow(self):
        return self.tileRow
    
    def getTileCol(self):
        return self.tileCol
    
    def shift(self, app, tileRowShift, tileColShift):
        self.tileRow += tileRowShift
        self.tileCol += tileColShift

        if(self.tileRow > 7):
            self.tileRow = 1
        elif(self.tileCol > 7):
            self.tileCol = 1
        elif(self.tileRow < 1):
            self.tileRow = 7
        elif(self.tileCol < 1):
            self.tileCol = 7
        
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
    
    def getColor(self):
        return self.color
    
    def move(self, app, tileRowShift, tileColShift):
        newTileRow = self.tileRow+tileRowShift
        newTileCol = self.tileCol+tileColShift
        if(newTileRow < 1 or newTileRow > 7 or newTileCol < 1 or newTileCol > 7):
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
            self.checkTreasures(app)
        
    def checkTreasures(self, app):
        if(self.color == 'tomato'):
            treasures = app.redTreasuresLeft
        else:
            treasures = app.greenTreasuresLeft
        treasure = treasures[0]
        if(treasure.getTileRow() == self.tileRow and
            treasure.getTileCol() == self.tileCol):
            treasures.pop(0)

class Treasure(GenericObject):
    def __init__(self, app, tileRow, tileCol, name):
        super().__init__(app, tileRow, tileCol)
        self.name = name
        self.tile = app.board[tileRow][tileCol]

    def getName(self):
        return self.name

    def updateTreasure(self):
        self.tileRow = self.tile.getTileRow()
        self.tileCol = self.tile.getTileCol()
        self.x, self.y = self.tile.getCoords()

    # def shift(self, app, tileRowShift, tileColShift):
    #     self.tileRow += tileRowShift
    #     self.tileCol += tileColShift

    #     if(self.tileRow == 0 or self.tileRow == 8 or self.tileCol == 0
    #         or self.tileCol == 8):
    #         self.tileRow = 1
    #         self.tileCol = 10

    #     self.x, self.y = getTileCenter(app, self.tileRow, self.tileCol)
    
    def redraw(self, canvas):
        canvas.create_text(self.x, self.y, text = self.name[:2],
                            fill='black', font = 'Georgia 12')