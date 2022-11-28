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
    def __init__(self, app, tileRow, tileCol, color, facingRight):
        super().__init__(app, tileRow, tileCol)
        self.color = color
        self.facingRight = facingRight
    
    def __eq__(self, other):
        if(self.color == other.color):
            return True
        return False

    def redraw(self, app, canvas):
        if(self.color == 'red'):
            if(app.turn == self):
                sprite = app.redJumpSprites[app.SpriteCounterFast % 8]
                canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(app.redCircleSprite))
            else:
                sprite = app.redIdleSprites[app.SpriteCounterSlow % 2]
        if(self.color == 'green'):
            if(app.turn == self):
                sprite = app.greenJumpSprites[app.SpriteCounterFast % 8]
                canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(app.greenCircleSprite))
            else:
                sprite = app.greenIdleSprites[app.SpriteCounterSlow % 2]

        if(self.facingRight == False):
            sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        canvas.create_image(self.x, self.y-14, image=ImageTk.PhotoImage(sprite))
        
    def getColor(self):
        return self.color
    
    def faceRight(self, facingRight):
        self.facingRight = facingRight
    
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
        if(self.color == 'red'):
            treasures = app.redTreasuresLeft
        elif(self.color == 'green'):
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
        self.image = app.batSprites

    def getName(self):
        return self.name

    def updateTreasure(self):
        self.tileRow = self.tile.getTileRow()
        self.tileCol = self.tile.getTileCol()
        self.x, self.y = self.tile.getCoords()

    def getSprite(self, app):
        sprite = app.triangleSpriteUp
        if(self.name == 'Bat'):
            sprite = app.batSprites[app.SpriteCounterFast % 10]
        elif(self.name == 'Rat'):
            sprite = app.ratSprites[app.SpriteCounterFast % 10]
        elif(self.name == 'Snae'):
            sprite = app.snakeSprites[app.SpriteCounterFast % 10]
        elif(self.name == 'Slime'):
            sprite = app.slimeSprites[app.SpriteCounterFast % 10]
        elif(self.name == 'Cat'):
            sprite = app.catSprites[app.SpriteCounterFast % 15]
        elif(self.name == 'Gem'):
            sprite = app.gemSprite
        elif(self.name == 'Chest'):
           sprite = app.chestSprite
        elif(self.name == 'Key'):
            sprite = app.keySprite
        elif(self.name == 'Ring'):
            sprite = app.ringSprite
        elif(self.name == 'Map'):
            sprite = app.mapSprite
        elif(self.name == 'Book'):
            sprite = app.bookSprite
        return sprite
    def redraw(self, app, canvas):
        sprite = self.getSprite(app)
        if(sprite != None):
            canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite))
        else:
            canvas.create_text(self.x, self.y, text = self.name[:2],
                                fill='black', font = 'Georgia 12')