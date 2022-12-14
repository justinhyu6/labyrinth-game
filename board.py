#################################################
# Board.py
#
# Your name: Justin Yu
# Your andrew id: justinyu
#################################################

import math, copy, random

from cmu_112_graphics import *
import pygame
from generic_object import *
from helper_functions import *
from interface import *

#################################################
# Labyrinth
#################################################

# Win condition
# Automatic AI?
# Select AI mode

def gameDimensions():
    rows = 27
    cols = 27
    cellSize = 19
    margin = 50
    return (rows, cols, cellSize, margin)

def appStarted(app):
    app.titleScreen = True
    app.mainMenu = False
    app.numAI = 0
    app.helperMessages = True
    app.menuIndex = 0

    app.gameStarted = False
    app.boardCreated = False
    app.gameOver = False
    app.treasuresAdded = False
    app.diagonalsDrawn = 0
    app.rotateShiftMode = True
    app.moveMode = False
    app.currentTileSelected = False
    app.turn = None

    (rows, cols, cellSize, margin) = gameDimensions()
    app.rows = cols
    app.cols = rows
    app.cellSize = cellSize
    app.margin = margin
    app.tileRows = 9
    app.tileCols = 9
    app.tileSize = app.cellSize * 3
    app.labyrinthWidth = app.cols * app.cellSize + 2 * app.margin
    app.labyrinthHeight = app.rows * app.cellSize + 2 * app.margin
    app.gridWidth = app.labyrinthWidth - 2 * app.margin
    app.gridHeight = app.labyrinthHeight - 2 * app.margin

    # Shifting
    app.shiftCurrentTile = False
    app.shiftCounter = 0
    app.shifting = False

    # AI/Players
    app.moves = [(0, 2), (0, 4), (0, 6), (8, 2), (8, 4), (8, 6),
                (2, 0), (4, 0), (6, 0), (2, 8), (4, 8), (6, 8)]
    app.undoMoves = [(8, 2), (8, 4), (8, 6), (0, 2), (0, 4), (0, 6),
                    (2, 8), (4, 8), (6, 8), (2, 0), (4, 0), (6, 0)]
    app.drawPath = False
    app.path = []
    app.pathLength = 0
    app.redAI = False
    app.yellowAI = False
    app.greenAI = False
    app.blueAI = False
    app.previousMove = (-1, -1)

    # Sprites

    # Board
    app.tSprite = app.loadImage('t_tile.png')
    app.tSprite = app.scaleImage(app.tSprite, 2)
    app.iSprite = app.loadImage('i_tile.png')
    app.iSprite = app.scaleImage(app.iSprite, 2)
    app.lSprite = app.loadImage('l_tile.png')
    app.lSprite = app.scaleImage(app.lSprite, 2)
    app.emptySprite = app.loadImage('empty_tile.png')
    app.emptySprite = app.scaleImage(app.emptySprite, 2)
    app.emptyFadedSprite = app.loadImage('empty_tile_faded.png')
    app.emptyFadedSprite = app.scaleImage(app.emptyFadedSprite, 2)

    # UI
    app.emptyRedSprite = app.loadImage('empty_red_tile.png')
    app.emptyRedSprite = app.scaleImage(app.emptyRedSprite, 2)
    app.emptyGreenSprite = app.loadImage('empty_green_tile.png')
    app.emptyGreenSprite = app.scaleImage(app.emptyGreenSprite, 2)
    app.emptyBlueSprite = app.loadImage('empty_blue_tile.png')
    app.emptyBlueSprite = app.scaleImage(app.emptyBlueSprite, 2)
    app.emptyYellowSprite = app.loadImage('empty_yellow_tile.png')
    app.emptyYellowSprite = app.scaleImage(app.emptyYellowSprite, 2)

    app.triangleSpriteUp = app.loadImage('triangle.png')
    app.triangleSpriteUp = app.scaleImage(app.triangleSpriteUp, 2)
    app.triangleSpriteLeft = app.triangleSpriteUp.transpose(Image.ROTATE_90)
    app.triangleSpriteDown = app.triangleSpriteUp.transpose(Image.ROTATE_180)
    app.triangleSpriteRight = app.triangleSpriteUp.transpose(Image.ROTATE_270)

    # https://kyrise.itch.io/kyrises-free-16x16-rpg-icon-pack
    
    app.shiftSprite = app.loadImage('shift.png')
    app.shiftSprite = app.scaleImage(app.shiftSprite, 2)
    app.moveSprite = app.loadImage('move.png')
    app.moveSprite = app.scaleImage(app.moveSprite, 2)
    app.questionSprite = app.loadImage('question.png')
    app.questionSprite = app.scaleImage(app.questionSprite, 2)

    app.redCapSprite = app.loadImage('red_cap.png')
    app.redCapSprite = app.scaleImage(app.redCapSprite, 2)
    app.greenCapSprite = app.loadImage('green_cap.png')
    app.greenCapSprite = app.scaleImage(app.greenCapSprite, 2)
    app.blueCapSprite = app.loadImage('blue_cap.png')
    app.blueCapSprite = app.scaleImage(app.blueCapSprite, 2)
    app.yellowCapSprite = app.loadImage('yellow_cap.png')
    app.yellowCapSprite = app.scaleImage(app.yellowCapSprite, 2)
    
    app.redCircleSprite = app.loadImage('red_circle.png')
    app.redCircleSprite = app.scaleImage(app.redCircleSprite, 2)
    app.greenCircleSprite = app.loadImage('green_circle.png')
    app.greenCircleSprite = app.scaleImage(app.greenCircleSprite, 2)
    app.blueCircleSprite = app.loadImage('blue_circle.png')
    app.blueCircleSprite = app.scaleImage(app.blueCircleSprite, 2)
    app.yellowCircleSprite = app.loadImage('yellow_circle.png')
    app.yellowCircleSprite = app.scaleImage(app.yellowCircleSprite, 2)
 
    # Wizards https://penzilla.itch.io/hooded-protagonist
    app.redJumpSprites = loadSprites(app, 'red.png', 0, 160, 32, 1.5, 8)
    app.redIdleSprites = loadSprites(app, 'red.png', 0, 0, 32, 1.5, 8)
    app.yellowJumpSprites = loadSprites(app, 'yellow.png', 0, 160, 32, 1.5, 8)
    app.yellowIdleSprites = loadSprites(app, 'yellow.png', 0, 0, 32, 1.5, 8)
    app.greenJumpSprites = loadSprites(app, 'green.png', 0, 160, 32, 1.5, 8)
    app.greenIdleSprites = loadSprites(app, 'green.png', 0, 0, 32, 1.5, 8)
    app.blueJumpSprites = loadSprites(app, 'blue.png', 0, 160, 32, 1.5, 8)
    app.blueIdleSprites = loadSprites(app, 'blue.png', 0, 0, 32, 1.5, 8)

    app.SpriteCounterFast = 0
    app.SpriteCounterSlow = 0

    # Treasures

    # Animated Sprites https://opengameart.org/content/animated-slime
    app.batSprites = loadSprites(app, 'rat_bat.png', 0, 160, 32, 2, 10)
    app.ratSprites = loadSprites(app, 'rat_bat.png', 0, 10, 32, 2, 10)
    app.snakeSprites = loadSprites(app, 'snake.png', 0, 10, 32, 2, 10)
    app.slimeSprites = loadSprites(app, 'slime.png', 0, 74, 32, 2, 10)
    app.catSprites = loadSprites(app, 'cat.png', 0, 0, 16, 2, 15)
    #https://yvodlynpaul.itch.io/tiny-butterfly-character
    app.butterflySprites = loadSprites(app, 'butterfly.png', 0, 0, 16, 2, 4)
    app.ghostSprites = loadSprites(app, 'ghost.png', 0, 0, 16, 2, 4)
    # https://caz-creates-games.itch.io/cute-shroom-4
    app.mushroomSprites = loadSprites(app, 'mushroom.png', 0, 16, 16, 2, 5)   

    # https://free-game-assets.itch.io/free-icons-for-mine-location-pixel-art
    # https://opengameart.org/content/roguelikerpg-items
    app.gemSprite = app.loadImage('gem.png')
    app.gemSprite = app.scaleImage(app.gemSprite, 2)
    app.chestSprite = app.loadImage('chest.png')
    app.chestSprite = app.scaleImage(app.chestSprite, 2)
    app.keySprite = app.loadImage('key.png')
    app.keySprite = app.scaleImage(app.keySprite, 2)
    app.ringSprite = app.loadImage('ring.png')
    app.ringSprite = app.scaleImage(app.ringSprite, 2)
    app.mapSprite = app.loadImage('map.png')
    app.mapSprite = app.scaleImage(app.mapSprite, 2)
    app.bookSprite = app.loadImage('book.png')
    app.bookSprite = app.scaleImage(app.bookSprite, 2)

    # New Sprites for 3-4 players
    # https://valletyh.itch.io/icon-pack
    # https://bluwhit.itch.io/pirate-booty-asset-pack
    app.crownSprite = app.loadImage('crown.png')
    app.crownSprite = app.scaleImage(app.crownSprite, 2)
    app.vaseSprite = app.loadImage('vase.png')
    app.vaseSprite = app.scaleImage(app.vaseSprite, 2)
    app.potionSprite = app.loadImage('potion.png')
    app.potionSprite = app.scaleImage(app.potionSprite, 2)
    app.skullSprite = app.loadImage('skull.png')
    app.skullSprite = app.scaleImage(app.skullSprite, 2)
    app.daggerSprite = app.loadImage('dagger.png')
    app.daggerSprite = app.scaleImage(app.daggerSprite, 2)
    app.robeSprite = app.loadImage('robe.png')
    app.robeSprite = app.scaleImage(app.robeSprite, 2)

    # Title and Menu Sprites
    app.background1Sprite = app.loadImage('background1.png')
    app.borderSprite = app.loadImage('gothic_border.png')
    app.titleSprite = app.loadImage('title.png')
    app.line = loadAnimatedGif('line.gif')
    app.fire = loadAnimatedGif('fire.gif')

    # Game State
    result = []
    for row in range(app.tileRows):
        result += [[False] * app.tileCols]
    app.board = result
    app.labyrinthTiles = getTiles()
    app.immovableTiles = getImmovableTiles(app)
    app.currentTile = Tile(app, 0, 11, app.labyrinthTiles[0], 0)
    generateLabyrinth(app)
    
    app.buttons = []
    x, y = getTileCenter(app, 6, 10)
    app.buttons.append(Button(x, y, app.questionSprite, 'help'))

    app.wizards = []
    app.blueWizard = Wizard(app, 1, 1,'blue', True)
    app.redWizard = Wizard(app, 7, 1,'red', True)
    app.yellowWizard = Wizard(app, 7, 7,'yellow', False)
    app.greenWizard = Wizard(app, 1, 7,'green', False)
    app.treasuresLeft = []
    app.redTreasuresLeft = []
    app.yellowTreasuresLeft = []
    app.greenTreasuresLeft = []
    app.blueTreasuresLeft = []
    app.numWizards = 4
    app.turnCount = 0
    
    # Timer
    app.mouseMovedDelay = 1
    app.timerDelay = 1
    app.timePassed = 0
    app.messageLength = 0

    # Sounds
    pygame.mixer.init(44100, -16, 2, 512)
    app.confirm1 = Sound("abs-confirm-1.mp3")
    app.confirm1.set_volume(0.1)
    app.confirm2 = Sound("abs-confirm-2.mp3")
    app.confirm2.set_volume(0.1)
    app.pointer2 = Sound("abs-pointer-2.mp3")
    app.pointer2.set_volume(0.1)
    app.place = Sound("shoot02.ogg")
    app.boop = Sound("boop 1.ogg")
    app.slide = Sound("slide.mp3")
    app.slide.set_volume(0.2)

    pygame.mixer.music.load("Echoes.mp3")

def appStopped(app):
    pass


#--------Labyrinth generator-------------------------------------------------

def loadSprites(app, file, x0, y0, size, scale, spriteLength):
    name = file
    spritestrip = app.loadImage(name)
    sprites = [ ]
    for i in range(spriteLength):
        sprite = spritestrip.crop((size*i, y0, x0+size*(1+i), y0+size))
        sprite = app.scaleImage(sprite, scale)
        sprites.append(sprite)
    return sprites

def addWizards(app):
    if(app.numWizards >= 3):
        app.wizards.append(app.blueWizard)
    app.wizards.append(app.redWizard)
    if(app.numWizards == 4):
        app.wizards.append(app.yellowWizard)
    app.wizards.append(app.greenWizard)

    app.turn = app.wizards[0]

def addTreasuresToPlayer(app):
    random.shuffle(app.treasuresLeft)
    index = 5
    app.redTreasuresLeft += app.treasuresLeft[0:index]
    app.greenTreasuresLeft += app.treasuresLeft[index:index*2]
    if(app.numWizards >= 3):
        app.blueTreasuresLeft += app.treasuresLeft[index*2:index*3]
    if(app.numWizards == 4):
        app.yellowTreasuresLeft += app.treasuresLeft[index*3:]

    app.redTreasuresLeft.append(Home(app, 7, 1, 'Red'))
    if(app.numWizards == 4):
        app.yellowTreasuresLeft.append(Home(app, 7, 7, 'Yellow'))
    app.greenTreasuresLeft.append(Home(app, 1, 7, 'Green'))
    if(app.numWizards >= 3):
        app.blueTreasuresLeft.append(Home(app, 1, 1, 'Blue'))

def addImmovableTreasures(app):
    app.treasuresLeft.append(Treasure(app, 7, 3, 'Map'))
    app.treasuresLeft.append(Treasure(app, 5, 1, 'Book'))
    app.treasuresLeft.append(Treasure(app, 5, 3, 'Key'))

    app.treasuresLeft.append(Treasure(app, 3, 5, 'Chest'))
    app.treasuresLeft.append(Treasure(app, 3, 7, 'Ring'))
    app.treasuresLeft.append(Treasure(app, 1, 5, 'Gem'))

    app.treasuresLeft.append(Treasure(app, 3, 1, 'Crown'))
    app.treasuresLeft.append(Treasure(app, 1, 3, 'Potion'))
    app.treasuresLeft.append(Treasure(app, 3, 3, 'Vase'))

    app.treasuresLeft.append(Treasure(app, 7, 5, 'Skull'))
    app.treasuresLeft.append(Treasure(app, 5, 5, 'Dagger'))
    app.treasuresLeft.append(Treasure(app, 5, 7, 'Robe'))

    

    for treasure in app.treasuresLeft:
        app.board[treasure.getTileRow()][treasure.getTileCol()].addTreasure(treasure)


def addMovableTreasures(app):
    tNames = ['Snake', 'Cat', 'Bat', 'Ghost'] 
    tIndex = 0
    lNames = ['Slime', 'Mushroom', 'Rat', 'Butterfly']
    lIndex = 0
    while(tIndex < 4 or lIndex < 4):
        tileRow = 1
        tileCol = 1
        while(tileRow % 2 == 1 and tileCol % 2 == 1):
            tileRow = random.randint(1, 7)
            tileCol = random.randint(1, 7)

        emptyTile = False
        if(app.board[tileRow][tileCol].getTreasure() == None):
            emptyTile = True
        if(tIndex < 4 and app.board[tileRow][tileCol].getPathCount() == 4 and emptyTile == True):
            treasure = Treasure(app, tileRow, tileCol, tNames[tIndex])
            app.board[tileRow][tileCol].addTreasure(treasure)
            app.treasuresLeft.append(treasure)
            tIndex += 1
        elif(lIndex < 4 and app.board[tileRow][tileCol].getPathCount() == 3 and emptyTile == True):
            treasure = Treasure(app, tileRow, tileCol, lNames[lIndex])
            app.board[tileRow][tileCol].addTreasure(treasure)
            app.treasuresLeft.append(treasure)
            lIndex += 1

def getImmovableTiles(app):
    # T-tile 0, I-tile 1, L-tile 2, rotates clockwise 
    tiles = app.labyrinthTiles
    tile1 = Tile(app, 1, 1, tiles[2], 1)
    tile2 = Tile(app, 1, 3, tiles[0], 0)
    tile3 = Tile(app, 1, 5, tiles[0], 0)
    tile4 = Tile(app, 1, 7, tiles[2], 2)
    tile5 = Tile(app, 3, 1, tiles[0], 3)
    tile6 = Tile(app, 3, 3, tiles[0], 3)
    tile7 = Tile(app, 3, 5, tiles[0], 0)
    tile8 = Tile(app, 3, 7, tiles[0], 1)
    tile9 = Tile(app, 5, 1, tiles[0], 3)
    tile10 = Tile(app, 5, 3, tiles[0], 2)
    tile11 = Tile(app, 5, 5, tiles[0], 1)
    tile12 = Tile(app, 5, 7, tiles[0], 1)
    tile13 = Tile(app, 7, 1, tiles[2], 0)
    tile14 = Tile(app, 7, 3, tiles[0], 2)
    tile15 = Tile(app, 7, 5, tiles[0], 2)
    tile16 = Tile(app, 7, 7, tiles[2], 3)
    return [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8,
            tile9, tile10, tile11, tile12, tile13, tile14, tile15, tile16]

def generateLabyrinth(app):
    tileCounts = [11, 11, 11]
    immovableTileIndex = 0
    for tileRow in range(1, 8):
        for tileCol in range(1, 8):
            if(tileRow % 2 != 1 or tileCol % 2 != 1): # moveable tile
                chooseTile(app, tileRow, tileCol, 
                            tileCounts, immovableTileIndex, True)
            else:
                chooseTile(app, tileRow, tileCol, 
                            tileCounts, immovableTileIndex, False)
                immovableTileIndex += 1
    app.currentTile = Tile(app, 1, 10, app.labyrinthTiles[0], 0)

    turnOverTiles(app)

def turnOverTiles(app):
    for tileRow in range(1, 8):
        for tileCol in range(1, 8):
            if(tileRow % 2 == 1 and tileCol % 2 == 1):
                app.board[tileRow][tileCol].displayOnScreen()


def chooseTile(app, tileRow, tileCol, tileCounts, index, moveableTile):
    if(moveableTile):
        index = random.randint(0, 2)
        while(tileCounts[index] == 0):
            index = (index + 1) % 3
        tileCounts[index] -= 1
        times = random.randint(0, 3)
        L = app.labyrinthTiles[index]
        app.currentTile = Tile(app, tileRow, tileCol, L, times)
    else:
        app.currentTile = app.immovableTiles[index]
    app.board[tileRow][tileCol] = app.currentTile

#--------Player controls-------------------------------------------------

def mousePressed(app, event):
    if(app.currentTile != None):
        x, y = app.currentTile.getCoords()
        app.currentTileSelected = checkInSquare(event.x, event.y, x, y, app.tileSize)
    
    for button in app.buttons:
        if(button.containsPoint(event.x, event.y)):
            function = button.mousePressed(event)
            buttonPressed(app, function)

def buttonPressed(app, function):
    if('help' in function): 
        app.confirm2.playSound()
        app.helperMessages = not app.helperMessages

def mouseDragged(app, event):
    if(app.currentTileSelected):
        app.currentTile.setCoords(event.x, event.y)
    if(app.currentTile.getTreasure() != None):
        app.currentTile.updateTreasure()

def mouseReleased(app, event):
    if(app.currentTileSelected):
        tileRow, tileCol = placeCurrentTile(app, event.x, event.y)
        if(isValidMove2(app, (tileRow, tileCol))):
            app.currentTile.setTile(app, tileRow, tileCol)
            if(app.currentTile.getTreasure() != None):
                app.currentTile.updateTreasure()
            app.previousMove = (tileRow, tileCol)
            app.board[tileRow][tileCol] = app.currentTile
            app.currentTile = None
            app.shiftCurrentTile = True
        else:
            app.place.playSound()
            app.currentTile.setTile(app, 1, 10)
            if(app.currentTile.getTreasure() != None):
                app.currentTile.updateTreasure()

        app.currentTileSelected = False

def placeCurrentTile(app, x, y):
    for tileRow in [2, 4, 6]:
        for tileCol in [0, 8]:
            centerX, centerY = getTileCenter(app, tileRow, tileCol)
            if(checkInSquare(centerX, centerY, x, y, app.tileSize)):
                return tileRow, tileCol
            if(checkInSquare(centerY, centerX, x, y, app.tileSize)):
                return tileCol, tileRow
    return app.currentTile.getTileRow(), app.currentTile.getTileCol()
    
def isValidMove2(app, move):
    if(move in app.moves):
        index = app.moves.index(move)
    else:
        return False

    if(index != -1):
        if(app.previousMove not in app.undoMoves):
            return True
        elif(app.undoMoves.index(app.previousMove) != index):
            return True
    return False

def shiftBoard(app, currentTileRow, currentTileCol):
    # For the AI
    if(app.currentTile != None):
        tileRow = currentTileRow
        tileCol = currentTileCol
        app.currentTile.setTile(app, tileRow, tileCol)
        if(app.currentTile.getTreasure() != None):
            app.currentTile.updateTreasure()
        app.previousMove = (tileRow, tileCol)
        app.board[tileRow][tileCol] = app.currentTile
        app.currentTile = None

    shift = 0
    if(currentTileRow == 0 or currentTileRow == 8):
        if(currentTileRow == 0):
            shift = 1
            pushingRow = 1
            pushedRow = 8
            shiftBoardCol(app, currentTileRow, currentTileCol, shift)
        elif(currentTileRow == 8):
            shift = -1
            pushingRow = 7
            pushedRow = 0
            shiftBoardCol(app, currentTileRow, currentTileCol, shift) 
        
        app.board[app.previousMove[0]][app.previousMove[1]] = False
        app.currentTile = app.board[pushedRow][currentTileCol]
        app.board[pushedRow][currentTileCol] = False
    
    if(currentTileCol == 0 or currentTileCol == 8):
        if(currentTileCol == 0):
            shift = 1
            pushingCol = 1
            pushedCol = 8
            shiftBoardRow(app, currentTileRow, currentTileCol, shift)
        elif(currentTileCol == 8):
            shift = -1
            pushingCol = 7
            pushedCol = 0
            shiftBoardRow(app, currentTileRow, currentTileCol, shift)
        
        app.board[app.previousMove[0]][app.previousMove[1]] = False
        app.currentTile = app.board[currentTileRow][pushedCol]
        app.board[currentTileRow][pushedCol] = False
    
    moveWizards(app, currentTileRow, currentTileCol, shift)
    moveTreasures(app)

def shiftBoardRow(app, currentTileRow, currentTileCol, shift):
    if(shift == -1):
        start = 1
        end = 9
    elif(shift == 1):
        start = 0
        end = 8
    for tileCol in range(start, end):
        if(shift == -1):
            oldTileCol = tileCol
            newTileCol = tileCol + shift
        elif(shift == 1):
            oldTileCol = end - tileCol - shift
            newTileCol = end - tileCol
        tile = app.board[currentTileRow][oldTileCol]
        if(isinstance(tile, Tile)):
            tile.setTile(app, currentTileRow, newTileCol)
        # print((currentTileRow, oldTileCol), (currentTileRow, newTileCol))
        app.board[currentTileRow][newTileCol] = tile

def shiftBoardCol(app, currentTileRow, currentTileCol, shift):
    if(shift == -1):
        start = 1
        end = 9
    elif(shift == 1):
        start = 0
        end = 8
    for tileRow in range(start, end):
        if(shift == -1):
            oldTileRow = tileRow
            newTileRow = tileRow + shift
        elif(shift == 1):
            oldTileRow = end - tileRow - shift
            newTileRow = end - tileRow
        tile = app.board[oldTileRow][currentTileCol]
        if(isinstance(tile, Tile)):
            tile.setTile(app, newTileRow, currentTileCol)
        # print((oldTileRow, currentTileCol), (newTileRow, currentTileCol))
        app.board[newTileRow][currentTileCol] = tile

def shiftCurrentTile(app):
    app.currentTile.setTile(app, 1, 10)
    moveTreasures(app)

    app.shiftCurrentTile = False
    app.rotateShiftMode = False
    app.moveMode = True
    app.messageLength = 0
    app.shiftCounter = 0
    
def moveTreasures(app):
    for tileRow in range(1, 8):
        for tileCol in range(1, 8):
            if(app.board[tileRow][tileCol].getTreasure() != None):
                app.board[tileRow][tileCol].updateTreasure()

    if(app.currentTile.getTreasure() != None):
        app.currentTile.updateTreasure()

def moveWizards(app, currentTileRow, currentTileCol, shift):
    for wizard in app.wizards:
        tileRowShift = 0
        tileColShift = 0
        if(wizard.getTileRow() == currentTileRow):
            tileColShift = shift
        if(wizard.getTileCol() == currentTileCol):
            tileRowShift = shift
        wizard.shift(app, tileRowShift, tileColShift)

def keyPressed(app, event):
    if(event.key == '0'):
        appStarted(app)

    if(event.key == '3'):
        appStarted(app)
        app.titleScreen = False
        app.mainMenu = False
        app.gameStarted = True
        app.helperMessages = False
        app.messageLength = 0
        pygame.mixer.music.stop()

    if(app.gameOver):
        return

    if(app.titleScreen == True):
        app.titleScreen = False
        app.mainMenu = True
    
    if(app.mainMenu == True):
        if(event.key == 'Space'):
            app.confirm2.playSound()
            if(app.menuIndex == 0):
                app.numAI = app.numAI + 1
                if(app.numAI > app.numWizards):
                    app.numAI = 0
                updateNumAI(app)
            elif(app.menuIndex == 1):
                app.numWizards += 1
                if(app.numWizards > 4):
                    app.numWizards = 2
            elif(app.menuIndex == 2):
                app.mainMenu = False
                app.gameStarted = True
                app.helperMessages = False
                app.messageLength = 0
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("Metropolis_cut.mp3")
                pygame.mixer.music.play(0)

        elif(event.key == 'Up'):
            app.pointer2.playSound()
            app.messageLength = 0
            app.menuIndex -= 1
            app.SpriteCounterSlow = 4
            if(app.menuIndex < 0):
                app.menuIndex = 2
        elif(event.key == 'Down'):
            app.pointer2.playSound()
            app.messageLength = 0
            app.menuIndex += 1
            app.SpriteCounterSlow = 4
            if(app.menuIndex > 2):
                app.menuIndex = 0
            
    if(app.gameStarted == True):
        if(event.key == '1'):
            app.redTreasuresLeft.pop(0)
            app.confirm1.playSound()
        if(event.key == '2'):
            bestMove2(app, app.wizards[app.turnCount],
                        app.wizards[(app.turnCount+1)%2])
        if(event.key == '4' and app.rotateShiftMode):
            bestMove4(app, app.wizards[app.turnCount])
        if(event.key == 'r'):
            app.currentTile.rotate(1)
            app.boop.playSound()
        elif(event.key == 'Space' and app.moveMode == True):
            app.confirm2.playSound()
            changeTurn(app)
            app.messageLength = 0
        for wizard in app.wizards:
            if(app.moveMode == True and app.turn == wizard):
                if(event.key == 'Up'):
                    wizard.move(app, -1, 0, True)
                elif(event.key == 'Down'):
                    wizard.move(app, 1, 0, True)
                elif(event.key == 'Left'):
                    wizard.move(app, 0, -1, True)
                    wizard.faceRight(False)
                elif(event.key == 'Right'):
                    wizard.move(app, 0, 1, True)
                    wizard.faceRight(True)

def updateNumAI(app):
    app.redAI = False
    app.yellowAI = False
    app.greenAI = False
    app.blueAI = False

    if(app.numAI >= 1):
        app.redAI = True
    if(app.numAI >= 2):
        app.greenAI = True
    if(app.numAI >= 3):
        app.blueAI = True
    if(app.numAI >= 4):
        app.yellowAI = True

def changeTurn(app):
    app.turnCount = (app.turnCount+1)%app.numWizards

    app.turn = app.wizards[app.turnCount]
    app.moveMode = False
    app.rotateShiftMode = True

def timerFired(app):
    app.timePassed += 1
    if(app.timePassed == 3):
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0, 1500)
    if(app.timePassed % 2):
        app.SpriteCounterFast += 1
    if(app.timePassed % 6 == 0):
        app.SpriteCounterSlow += 1

    if(app.mainMenu == True):
        app.messageLength += 2

    if(app.gameStarted == True):
        if(app.helperMessages == True):
            app.messageLength += 2
        else:
            app.messageLength = 0
        if(app.boardCreated == False and app.timePassed % 1 == 0): #5
            boardCreationAnimation(app)
        if(app.boardCreated == True):
            if(app.treasuresAdded == False):
                addWizards(app)
                addImmovableTreasures(app)
                addMovableTreasures(app)
                addTreasuresToPlayer(app)
                app.treasuresAdded = True

            if(app.timePassed % 3 == 0 and app.drawPath == True and app.shiftCurrentTile == False):
                if(app.pathLength == len(app.path)):
                    app.pathLength = 0
                    app.drawPath = False
                    app.boop.playSound()
                    if(app.turn.checkTreasures(app, True) == False):
                        changeTurn(app)
                else:
                    app.pathLength += 1
                    newPos = app.path[app.pathLength - 1]
                    if(newPos[1] > app.turn.getTileCol()):
                        app.turn.move(app, 0, 1, False)
                        app.turn.faceRight(True)
                    elif(newPos[1] < app.turn.getTileCol()):
                        app.turn.move(app, 0, -1, False)
                        app.turn.faceRight(False)
                    elif(newPos[0] > app.turn.getTileRow()):
                        app.turn.move(app, 1, 0, False)
                    elif(newPos[0] < app.turn.getTileRow()):
                        app.turn.move(app, -1, 0, False)
                    # app.turn.setPos(app, newPos[0], newPos[1])

            if(app.shiftCurrentTile == True):
                if(app.shiftCounter == 0):
                    app.place.playSound()
                    app.slide.playSound()
                    app.shifting = True

                if(app.shifting):
                    shiftingAnimation(app)
                
                app.shiftCounter += 1
                if(app.shifting == False and app.shiftCounter == 5):
                    pygame.mixer.fadeout(1000)
                    shiftBoard(app, app.previousMove[0], app.previousMove[1])
                    shiftCurrentTile(app)
                    app.place.playSound()

def shiftingAnimation(app):

    move = app.previousMove
    if(move[0] == 0 or move[1] == 0):
        shift = 1
    elif(move[0] == 8 or move[1] == 8):
        shift = -1

    speed = 9 # app.shiftCounter + 12
    if(move[0] == 0 or move[0] == 8):
        for tileRow in range(app.tileRows):
            tile = app.board[tileRow][move[1]]
            if(isinstance(tile, Tile)):
                # print((tileRow, move[1]))
                x0, y0 = tile.getCoords()
                x1, y1 = getTileCenter(app, tileRow + shift, move[1])
                y0 += shift*speed
                if(abs(y0 - y1) < abs(shift*speed)):
                    y0 = y1
                    app.shifting = False
                    app.shiftCounter = 0

                tile.setCoords(x0, y0)
                for wizard in app.wizards:
                    if(wizard.getTileRow() == tileRow and wizard.getTileCol() == move[1]):
                        wizard.updateWizard(x0, y0)
                if(app.board[tileRow][move[1]].getTreasure() != None):
                    app.board[tileRow][move[1]].updateTreasure()
    
    elif(move[1] == 0 or move[1] == 8):
        for tileCol in range(app.tileCols):
            tile = app.board[move[0]][tileCol]
            if(isinstance(tile, Tile)):
                x0, y0 = tile.getCoords()
                x1, y1 = getTileCenter(app,  move[0], tileCol + shift)
                x0 += shift*speed
                if(abs(x0 - x1) < abs(shift*speed)):
                    x0 = x1
                    app.shifting = False
                    app.shiftCounter = 0

                tile.setCoords(x0, y0)
                for wizard in app.wizards:
                    if(wizard.getTileRow() == move[0] and wizard.getTileCol() == tileCol):
                        wizard.updateWizard(x0, y0)
                if(app.board[move[0]][tileCol].getTreasure() != None):
                    app.board[move[0]][tileCol].updateTreasure()
                
            
def boardCreationAnimation(app):
    for tileRow in range(1, 8):
        for tileCol in range(1, 8):
            if(tileRow + tileCol - 2 <= app.diagonalsDrawn):
                app.board[tileRow][tileCol].displayOnScreen()
    app.diagonalsDrawn += 1
    if(app.diagonalsDrawn == 13):
        app.currentTile.displayOnScreen()
        app.boardCreated = True
    else:
        app.place.playSound()

#--------View / redrawAll-------------------------------------------------
def redrawAll(app, canvas):
    bg = rgbString(36, 29, 45)
    canvas.create_rectangle(0, 0, app.width, app.height, fill=bg, width=0)
    # canvas.create_rectangle(0, 0, app.width, app.height, fill='dark slate blue', width=0)
    # if(app.mainMenu or app.titleScreen):
    canvas.create_image(784/2, 632/2, image=ImageTk.PhotoImage(app.background1Sprite))
    canvas.create_image(784/2, 632/2, image=ImageTk.PhotoImage(app.borderSprite))
    if(app.titleScreen == True):
        drawTitleScreen(app, canvas)
    elif(app.mainMenu == True):
        drawMainMenu(app, canvas)
        if(app.helperMessages):
            drawHelpMessage(app, canvas)

    if(app.gameStarted and app.boardCreated):
        drawSymbols(app, canvas)
        drawTileOptions(app, canvas)
        drawHelpMessage(app, canvas)

    if(app.gameStarted == True):
        drawBoard(app, canvas)

    if(app.gameStarted == True and app.treasuresAdded == True):
        for button in app.buttons:
            button.redraw(canvas)
        for treasure in app.redTreasuresLeft + app.greenTreasuresLeft + app.blueTreasuresLeft + app.yellowTreasuresLeft:
            treasure.redraw(app, canvas)    
        if(app.drawPath == True):
            drawPath(app, canvas)
        for wizard in app.wizards:
            wizard.redraw(app, canvas)

        drawTreasuresLeft(app, canvas)
        if(app.currentTile != None):
            app.currentTile.drawTile(app, canvas)
            if(app.currentTile.getTreasure() != None):
                app.currentTile.getTreasure().redraw(app, canvas)
    
    if(app.gameOver == True):
        drawGameOver(app, canvas)

# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping

def loadAnimatedGif(path):
    # load first sprite outside of try/except to raise file-related exceptions
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return spritePhotoImages

def drawTileOptions(app, canvas):
    x0, y0 = getTileCenter(app, 1, 10)
    canvas.create_image(x0, y0, image=ImageTk.PhotoImage(app.emptyFadedSprite))
    for tileRow in [2, 4, 6]:
        for tileCol in [0, 8]:
            x0, y0 = getTileCenter(app, tileRow, tileCol)
            x1, y1 = getTileCenter(app, tileCol, tileRow)
            
            if(app.currentTileSelected):
                if(isValidMove2(app, (tileRow, tileCol))):
                    canvas.create_image(x0, y0, image=ImageTk.PhotoImage(app.emptyFadedSprite))
                if(isValidMove2(app, (tileCol, tileRow))):
                    canvas.create_image(x1, y1, image=ImageTk.PhotoImage(app.emptyFadedSprite))

            if(tileCol == 0):
                topBottomSprite = app.triangleSpriteDown
                leftRightSprite = app.triangleSpriteRight
                x0 += 10
                y1 += 10
            if(tileCol == 8):
                topBottomSprite = app.triangleSpriteUp
                leftRightSprite = app.triangleSpriteLeft
                x0 -= 10
                y1 -= 10
            
            canvas.create_image(x0, y0, image=ImageTk.PhotoImage(leftRightSprite))
            canvas.create_image(x1, y1, image=ImageTk.PhotoImage(topBottomSprite))
            
def drawTreasuresLeft(app, canvas):
    x0, y0 = getTileCenter(app, 5, 9.5)
    x1, y1, x2, y2 = getTileBounds(app, 5, 9.5)
    canvas.create_image(x0, y0, image=ImageTk.PhotoImage(app.emptyRedSprite))
    canvas.create_text(x2-10, y1+10, text = f'{len(app.redTreasuresLeft)}',
                            fill='white', font = 'm3x6 16')
    if(app.redTreasuresLeft != []):
        sprite1 = app.redTreasuresLeft[0].getSprite(app)
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(sprite1))
        
    
    x0, y0 = getTileCenter(app, 4, 10.5)
    x1, y1, x2, y2 = getTileBounds(app, 4, 10.5)
    canvas.create_image(x0, y0, image=ImageTk.PhotoImage(app.emptyGreenSprite))
    canvas.create_text(x2-10, y1+10, text = f'{len(app.greenTreasuresLeft)}',
                            fill='white', font = 'm3x6 16')
    if(app.greenTreasuresLeft != []):
        sprite = app.greenTreasuresLeft[0].getSprite(app)
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(sprite))

    if(app.numWizards >= 3):
        x0, y0 = getTileCenter(app, 4, 9.5)
        x1, y1, x2, y2 = getTileBounds(app, 4, 9.5)
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(app.emptyBlueSprite))
        canvas.create_text(x2-10, y1+10, text = f'{len(app.blueTreasuresLeft)}',
                                fill='white', font = 'm3x6 16')
        if(app.blueTreasuresLeft != []):
            sprite = app.blueTreasuresLeft[0].getSprite(app)
            canvas.create_image(x0, y0, image=ImageTk.PhotoImage(sprite))
    
    if(app.numWizards == 4):
        x0, y0 = getTileCenter(app, 5, 10.5)
        x1, y1, x2, y2 = getTileBounds(app, 5, 10.5)
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(app.emptyYellowSprite))
        canvas.create_text(x2-10, y1+10, text = f'{len(app.yellowTreasuresLeft)}',
                                fill='white', font = 'm3x6 16')
        if(app.yellowTreasuresLeft != []):
            sprite = app.yellowTreasuresLeft[0].getSprite(app)
            canvas.create_image(x0, y0, image=ImageTk.PhotoImage(sprite))

def drawSymbols(app, canvas):
    if(app.turnCount % 4 == 1):
        sprite1 = app.redCapSprite
    elif(app.turnCount % 4 == 2):
        sprite1 = app.yellowCapSprite
    elif(app.turnCount % 4 == 3):
        sprite1 = app.greenCapSprite
    elif(app.turnCount % 4 == 0):
        sprite1 = app.blueCapSprite

    x0, y0 = getTileCenter(app, 3, 9.5)
    canvas.create_image(x0, y0, image=ImageTk.PhotoImage(sprite1))

    if(app.rotateShiftMode):
        sprite2 = app.shiftSprite
    elif(app.moveMode):
            sprite2 = app.moveSprite
    x0, y0 = getTileCenter(app, 3, 10.5)
    canvas.create_image(x0, y0, image=ImageTk.PhotoImage(sprite2))
    
        
def drawTitleScreen(app, canvas):
    
    canvas.create_image(app.width/2 + 75, app.height/2 - 65, image=app.fire[app.SpriteCounterFast % 6])
    # canvas.create_image(app.width/2, app.height/2 + 45, image=app.line[app.SpriteCounterFast % 6])
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.titleSprite))
    message = 'press any key'
    if(app.SpriteCounterSlow % 4 != 1):
        message = '> ' + message
    canvas.create_text(app.width/2 + 75, app.height/2 + 80, 
                            text = message,
                            fill='white', font = 'm3x6 36', anchor = 'e')

def drawHelpMessage(app, canvas):
    message = getHelpMessage(app)
    canvas.create_text(130, app.height - 70, text = message,
                            fill='white', font = 'm3x6 24', anchor = 'w')

def drawMainMenu(app, canvas):
    
    modeText = f'  number of AI: {app.numAI}'
    numText = f'  number of players: {app.numWizards}'
    startText = '  start game'
    spacing = 50

    if(app.menuIndex == 0):
        modeText = '>' + modeText[1:]
    elif(app.menuIndex == 1):
        numText = '>' + numText[1:]
    elif(app.menuIndex == 2):
        startText = '>' + startText[1:]
    canvas.create_text(app.width/3, app.height/2-spacing,
                                text = modeText, anchor='w',
                                fill='white', font='m3x6 32')
    canvas.create_text(app.width/3, app.height/2,
                                text = numText, anchor='w',
                                fill='white', font='m3x6 32')
    canvas.create_text(app.width/3, app.height/2 + spacing,
                                text = startText, anchor='w',
                                fill='white', font='m3x6 32')

def drawGameOver(app, canvas):
    message = f'{app.turn.getColor()} wins!'
    canvas.create_text(app.width - 140, app.height/2 + 140, text = message,
                            fill='white', font = 'm3x6 48')
    message2 = 'Press 0 to restart'
    canvas.create_text(app.width - 140, app.height/2 + 40 + 140, text = message2,
                            fill='white', font = 'm3x6 32')

def drawBoard(app, canvas):
    for tileRow in range(app.tileRows):
        for tileCol in range(app.tileCols):
            if(isinstance(app.board[tileRow][tileCol], Tile)):
                app.board[tileRow][tileCol].drawTile(app, canvas)

def drawCell(app, canvas, row, col, isPath):
    if(isPath == False):
        color = 'sienna1'
    elif(isPath == True):
        color = 'burlywood1'

    if(isinstance(isPath, bool)):
        x0, y0, x1, y1 = getCellBounds(app, row, col, True, True)
        canvas.create_rectangle(x0, y0, x1, y1,
                                fill=color, width = 0)

def drawPath(app, canvas):
    color = app.turn.getColor()
    for index in range(1, app.pathLength):
        currentPos = app.path[index - 1]
        nextPos = app.path[index]

        x0, y0 = getTileCenter(app, currentPos[0], currentPos[1])
        x1, y1 = getTileCenter(app, nextPos[0], nextPos[1])
        canvas.create_line(x0, y0, x1, y1, fill=color, width=2)

def rotateImage(image, times):
    result = image
    for i in range(times):
        result = result.transpose(Image.ROTATE_270)
    return result

#--------Recursive solver--------------------------------------------

# For 2 - 4 Players
def bestMove4(app, wizard):
    bestScore = 99
    bestMove = (-1, -1)
    rotations = 0

    for j in range(1, 5):
        app.currentTile.rotate(1)
        for i in range(len(app.moves)):
            if(isValidMove2(app, app.moves[i])):
                position = (wizard.getTileRow(), wizard.getTileCol())
                path = doMove2(app, wizard, app.moves[i])
                score = evaluate(app, wizard, 1)
                if(score < bestScore):
                    bestScore = score
                    bestMove = app.moves[i]
                    app.path = path
                    rotations = j
                    # print(bestScore)

                undoMove(app, wizard, app.undoMoves[i], position)
    
    # Print and perform the move
    print(f'BEST MOVE: {rotations}, {bestMove}, {app.path}, {bestScore}')
    app.previousMove = bestMove
    app.currentTile.rotate(rotations)

    app.currentTile.setTile(app, bestMove[0], bestMove[1])
    if(app.currentTile.getTreasure() != None):
        app.currentTile.updateTreasure()
    app.board[bestMove[0]][bestMove[1]] = app.currentTile
    app.currentTile = None
    app.shiftCurrentTile = True
    app.drawPath = True

def evaluate(app, wizard, maxDepth, depth=0):
    target = wizard.getTreasures(app)
    target = target[0]
    if(depth == maxDepth):
        return closestPath(app, wizard)[2]
    elif(target.getTileRow() == wizard.getTileRow() and 
        target.getTileCol() == wizard.getTileCol()):
        # print('found')
        return -99

    bestScore = 99
    for i in range(len(app.moves)):
        position = (wizard.getTileRow(), wizard.getTileCol())
        
        doMove2(app, wizard, app.moves[i])
        result = evaluate(app, wizard, maxDepth, depth+1)

        # Undo moves
        undoMove(app, wizard, app.undoMoves[i], position)

        if(result < bestScore):
            bestScore = result
    return bestScore

def doMove2(app, wizard, move):
    shiftBoard(app, move[0], move[1])
    shiftCurrentTile(app)
    path = closestPath(app, wizard)[1]
    newPos = path[-1]
    wizard.setPos(app, newPos[0], newPos[1])
    # wizard.checkTreasures(app, False)
    return path

#--------Minimax solver--------------------------------------------

# For 2 Players
def bestMove2(app, wizard, otherWizard):
    bestScore = -1000
    bestPath = []
    bestMove = (-1, -1)
    rotations = 0

    for j in range(1, 5):
        app.currentTile.rotate(1)
        for i in range(len(app.moves)):
            position = (wizard.getTileRow(), wizard.getTileCol())
            redTreasuresBefore = copy.copy(app.redTreasuresLeft)
            greenTreasuresBefore = copy.copy(app.greenTreasuresLeft)
            blueTreasuresBefore = copy.copy(app.blueTreasuresLeft)
            yellowTreasuresBefore = copy.copy(app.yellowTreasuresLeft)

            path = doMove(app, wizard, app.moves[i])
            
            score = minimax(app, wizard, 
                        otherWizard, False, 1)

            if(score > bestScore):
                print(score)
                bestScore = score
                bestMove = app.moves[i]
                app.path = path
                rotations = j

            undoMove(app, wizard, app.undoMoves[i], position)
            app.redTreasuresLeft = redTreasuresBefore
            app.greenTreasuresLeft = greenTreasuresBefore
            app.blueTreasuresLeft = blueTreasuresBefore
            app.yellowTreasuresLeft = yellowTreasuresBefore
    
    print(f'BEST MOVE: {rotations}, {bestMove}, {app.path}, {bestScore}')
    app.previousMove = bestMove
    app.currentTile.rotate(rotations)

    app.currentTile.setTile(app, bestMove[0], bestMove[1])
    if(app.currentTile.getTreasure() != None):
        app.currentTile.updateTreasure()
    app.board[bestMove[0]][bestMove[1]] = app.currentTile
    app.currentTile = None
    app.shiftCurrentTile = True
    app.drawPath = True

# https://www.cs.cmu.edu/~112/notes/student-tp-guides/GameAI.pdf

def minimax(app, wizard, otherWizard, maximising, maxDepth, depth=0):
    if(depth == maxDepth):
        return getScore(app, wizard, otherWizard, app.redTreasuresLeft, 
                        app.greenTreasuresLeft)

    if(maximising):
        bestScore = -99
        for j in range(1, 5):
            app.currentTile.rotate(1)
            for i in range(len(app.moves)):
                position = (wizard.getTileRow(), wizard.getTileCol())
                redTreasuresBefore = copy.copy(app.redTreasuresLeft)
                greenTreasuresBefore = copy.copy(app.greenTreasuresLeft)
                blueTreasuresBefore = copy.copy(app.blueTreasuresLeft)
                yellowTreasuresBefore = copy.copy(app.yellowTreasuresLeft)
                
                path = doMove(app, wizard, app.moves[i])
                result = minimax(app, wizard, otherWizard, False, maxDepth, depth+1)

                # Undo moves
                undoMove(app, wizard, app.undoMoves[i], position)
                app.redTreasuresLeft = redTreasuresBefore
                app.greenTreasuresLeft = greenTreasuresBefore
                app.blueTreasuresLeft = blueTreasuresBefore
                app.yellowTreasuresLeft = yellowTreasuresBefore

                if(result > bestScore):
                    bestScore = result

        return bestScore

    else:
        bestScore = 99
        for j in range(1, 5):
            app.currentTile.rotate(1)
            for i in range(len(app.moves)):
                position = (otherWizard.getTileRow(), otherWizard.getTileCol())
                redTreasuresBefore = copy.copy(app.redTreasuresLeft)
                greenTreasuresBefore = copy.copy(app.greenTreasuresLeft)
                
                doMove(app, otherWizard, app.moves[i])
                result = minimax(app, wizard, otherWizard, True, maxDepth, depth+1)

                # Undo moves
                undoMove(app, otherWizard, app.undoMoves[i], position)
                app.redTreasuresLeft = redTreasuresBefore
                app.greenTreasuresLeft = greenTreasuresBefore

                if(result < bestScore):
                    bestScore = result

        return bestScore

def getScore(app, wizard, otherWizard, redTreasuresLeft, greenTreasuresLeft):
    score = 0
    if(wizard == app.wizards[0]):
        if(redTreasuresLeft == []):
            score += 100
        else:
            score += (70 - len(redTreasuresLeft) * 10)
            score += closestPath(app, app.wizards[0])[2]
    if(wizard == app.wizards[1]):
        if(greenTreasuresLeft == []):
            score -= 100
        else:
            score -= (70 - len(greenTreasuresLeft) * 10)
            score -= closestPath(app, app.wizards[1])[2]
    if(wizard == app.wizards[0]):
        return score
    else:
        return -score

def doMove(app, wizard, move):
    shiftBoard(app, move[0], move[1])
    shiftCurrentTile(app)
    path = closestPath(app, wizard)[1]
    newPos = path[-1]
    wizard.setPos(app, newPos[0], newPos[1])
    wizard.checkTreasures(app, False)
    return path

def undoMove(app, wizard, undoMove, oldPos):
    shiftBoard(app, undoMove[0], undoMove[1])
    shiftCurrentTile(app)
    wizard.setPos(app, oldPos[0], oldPos[1])

#--------Backtracking solver--------------------------------------------

# From https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#Backtracking

def closestPath(app, wizard):
    visited = set()
    leastDistance = 99
    path = []
    bestPath = []
    targetTreasure = None
    # targetTreasure = wizard.getTreasures(app)[0]

    if(wizard == app.blueWizard):
        targetTreasure = app.blueTreasuresLeft[0]
    elif(wizard == app.redWizard):
        targetTreasure = app.redTreasuresLeft[0]
    elif(wizard == app.yellowWizard):
        targetTreasure = app.yellowTreasuresLeft[0]
    elif(wizard == app.greenWizard):
        targetTreasure = app.greenTreasuresLeft[0]

    
    result = solve(app, path, visited, targetTreasure, wizard.getTileRow(), 
                wizard.getTileCol(), bestPath, leastDistance)
    return result


def solve(app, path, visited, targetTreasure, tileRow, tileCol, bestPath, leastDistance):
    if((tileRow, tileCol) in visited):
        return False, bestPath, leastDistance
    
    visited.add((tileRow, tileCol))
    path.append((tileRow, tileCol))

    distance = getDistance(targetTreasure, tileRow, tileCol)
    if(distance < leastDistance):
        bestPath = copy.copy(path)
        leastDistance = distance
    if(distance == 0):
        return True, bestPath, leastDistance
    else:
        for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if(isValidMove(app, tileRow, tileCol, move)):
                result = solve(app, path, visited, targetTreasure, 
                            tileRow+move[0], tileCol+move[1], bestPath, leastDistance)

                if(result[0] == True):
                    return result
                # if((tileRow, tileCol) != result[1][-1]): # Don't stay in the same place
                if(result[2] < leastDistance):
                    bestPath = result[1]
                    leastDistance = result[2]
    path.pop()
    return False, bestPath, leastDistance
        
def isValidMove(app, tileRow, tileCol, move):
    tileRowShift = move[0]
    tileColShift = move[1]
    newTileRow = tileRow+tileRowShift
    newTileCol = tileCol+tileColShift
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
    
    currentTile = app.board[tileRow][tileCol]
    hasPathCurrent = currentTile.getList()[1+tileRowShift][1+tileColShift]
    if(hasPath and hasPathCurrent):
        return True
    return False

def getDistance(targetTreasure, tileRow, tileCol):
    x = abs(targetTreasure.getTileCol() - tileCol)
    y = abs(targetTreasure.getTileRow() - tileRow)
    if(targetTreasure.getTileRow() == 10):
        return 10
    return x + y

#--------Tile Class--------------------------------------------

class Tile:
    def __init__(self, app, tileRow, tileCol, list, times):
        self.tileRow = tileRow
        self.tileCol = tileCol
        self.x, self.y = getTileCenter(app, tileRow, tileCol)

        self.times = times
        self.list1 = list
        self.list2 = rotateTile(list, times)
        self.setImage(app)
        self.display = False
        self.treasure = None
    
    def addTreasure(self, treasure):
        self.treasure = treasure
    
    def getTreasure(self):
        return self.treasure
    
    def updateTreasure(self):
        self.treasure.updateTreasure(self.tileRow, self.tileCol, self.x, self.y)
    
    def setImage(self, app):
        if(self.list1 == app.labyrinthTiles[0]):
            self.sprite1 = app.tSprite
        elif(self.list1 == app.labyrinthTiles[1]):
            self.sprite1 = app.iSprite
        elif(self.list1 == app.labyrinthTiles[2]):
            self.sprite1 = app.lSprite
        self.sprite2 = rotateImage(self.sprite1, self.times)
    
    def getCoords(self):
        return self.x, self.y

    def getTileRow(self):
        return self.tileRow
    
    def getTileCol(self):
        return self.tileCol

    def getPathCount(self):
        result = 0
        for row in range(3):
            for col in range(3):
                if(self.list2[row][col] == True):
                    result += 1
        return result
    
    def getList(self):
        return self.list2

    def setCoords(self, x, y):
        self.x = x
        self.y = y
    
    def setTile(self, app, tileRow, tileCol):
        self.tileRow = tileRow
        self.tileCol = tileCol
        self.x, self.y = getTileCenter(app, tileRow, tileCol)
    
    def addTreasure(self, treasure):
        self.treasure = treasure

    def rotate(self, times):
        self.times = (self.times + times) % 4
        self.sprite2 = rotateImage(self.sprite1, self.times)
        self.list2 = rotateTile(self.list2, times)
    
    def displayOnScreen(self):
        self.display = True
    
    def drawTile(self, app, canvas):
        if(self.display == True):
            canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.sprite2))
        else:
            canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(app.emptyFadedSprite))

#--------Sound--------------------------------------------

# Thanks to TA Dane for answering my question about sound on Piazza

class Sound(object):
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def playSound(self):
        self.sound.play()

    def stopSound(self):
        self.sound.stop()
    
    def set_volume(self, amt):
        self.sound.set_volume(amt)

#---------------------------------------------------------

def playLabyrinth():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = (cols + 9) * cellSize + 2 * margin
    height = (rows + 1) * cellSize + 2 * margin
    runApp(width = width, height = height)

def main():
    playLabyrinth()

if __name__ == '__main__':
    main()