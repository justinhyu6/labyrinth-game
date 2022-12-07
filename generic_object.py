#################################################
# Treasures and Wizards
#################################################

import math, copy, random

from board import *
from helper_functions import *

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

    def setPos(self, app, tileRow, tileCol):
        self.tileRow = tileRow
        self.tileCol = tileCol
        self.x, self.y = getTileCenter(app, tileRow, tileCol)

    def redraw(self, app, canvas):
        # canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(app.redCircleSprite))
        if(self.color == 'red'):
            sprite = app.redIdleSprites[app.SpriteCounterSlow % 2]
            if(app.turn == self and app.moveMode == True):
                    sprite = app.redJumpSprites[app.SpriteCounterFast % 8]
        elif(self.color == 'yellow'):
            sprite = app.yellowIdleSprites[app.SpriteCounterSlow % 2]
            if(app.turn == self and app.moveMode == True):
                sprite = app.yellowJumpSprites[app.SpriteCounterFast % 8]
        elif(self.color == 'green'):
            sprite = app.greenIdleSprites[app.SpriteCounterSlow % 2]
            if(app.turn == self and app.moveMode == True):
                sprite = app.greenJumpSprites[app.SpriteCounterFast % 8]
        elif(self.color == 'blue'):
            sprite = app.blueIdleSprites[app.SpriteCounterSlow % 2]
            if(app.turn == self and app.moveMode == True):
                sprite = app.blueJumpSprites[app.SpriteCounterFast % 8]

        if(self.facingRight == False):
            sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        canvas.create_image(self.x, self.y-12, image=ImageTk.PhotoImage(sprite))
        
    def getColor(self):
        return self.color
    
    def faceRight(self, facingRight):
        self.facingRight = facingRight
    
    def move(self, app, tileRowShift, tileColShift, checkForTreasures):
        if(isValidMove(app, self.tileRow, self.tileCol, (tileRowShift, tileColShift))):
            self.shift(app, tileRowShift, tileColShift)
        if(checkForTreasures):
            self.checkTreasures(app, True)
        app.boop.playSound()
        
    def checkTreasures(self, app, changeTurnIfFound):
        treasures = self.getTreasures(app)

        treasure = treasures[0]
        if(treasure.getTileRow() == self.tileRow and
            treasure.getTileCol() == self.tileCol):
            treasures.pop(0)
            app.confirm1.playSound()
            if(treasures == []):
                app.gameOver = True
            elif(changeTurnIfFound):
                changeTurn(app)
            return True
        return False
    
    def getTreasures(self, app):
        if(self.color == 'red'):
            return app.redTreasuresLeft
        elif(self.color == 'green'):
            return app.greenTreasuresLeft
        elif(self.color == 'blue'):
            return app.blueTreasuresLeft
        elif(self.color == 'yellow'):
            return app.yellowTreasuresLeft

class Treasure(GenericObject):
    def __init__(self, app, tileRow, tileCol, name):
        super().__init__(app, tileRow, tileCol)
        self.name = name

    def getName(self):
        return self.name

    def updateTreasure(self, tileRow, tileCol, x, y):
        self.tileRow = tileRow
        self.tileCol = tileCol
        self.x, self.y = x, y

    def getSprite(self, app):
        sprite = app.triangleSpriteUp
        if(self.name == 'Bat'):
            sprite = app.batSprites[app.SpriteCounterFast % 10]
        elif(self.name == 'Rat'):
            sprite = app.ratSprites[app.SpriteCounterFast % 10]
        elif(self.name == 'Snake'):
            sprite = app.snakeSprites[app.SpriteCounterFast % 10]
        elif(self.name == 'Slime'):
            sprite = app.slimeSprites[app.SpriteCounterFast % 10]
        elif(self.name == 'Cat'):
            sprite = app.catSprites[app.SpriteCounterFast % 15]
        elif(self.name == 'Ghost'):
            sprite = app.ghostSprites[app.SpriteCounterFast//2 % 4]
        elif(self.name == 'Butterfly'):
            sprite = app.butterflySprites[app.SpriteCounterFast//2 % 4]
        elif(self.name == 'Mushroom'):
            sprite = app.mushroomSprites[app.SpriteCounterFast//2 % 5]
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
        elif(self.name == 'Vase'):
            sprite = app.vaseSprite
        elif(self.name == 'Crown'):
            sprite = app.crownSprite
        elif(self.name == 'Potion'):
            sprite = app.potionSprite
        elif(self.name == 'Skull'):
            sprite = app.skullSprite
        elif(self.name == 'Dagger'):
            sprite = app.daggerSprite
        elif(self.name == 'Robe'):
            sprite = app.robeSprite
        return sprite
        
    def redraw(self, app, canvas):
        sprite = self.getSprite(app)
        if(sprite != None):
            canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite))
        else:
            canvas.create_text(self.x, self.y, text = self.name[:2],
                                fill='black', font = 'Georgia 12')

class Home(Treasure):
    def __init__(self, app, tileRow, tileCol, name):
        super().__init__(app, tileRow, tileCol, name)

    def getSprite(self, app):
        if(self.name == 'Red'):
            sprite = app.redCircleSprite
        elif(self.name == 'Blue'):
            sprite = app.blueCircleSprite
        elif(self.name == 'Green'):
            sprite = app.greenCircleSprite
        elif(self.name == 'Yellow'):
            sprite = app.yellowCircleSprite
        return sprite