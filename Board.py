#################################################
# Board.py
#
# Your name: Justin Yu
# Your andrew id: justinyu
#################################################

import math, copy, random

from cmu_112_graphics import *
from Interface import *
from GenericObject import *

#################################################
# Labyrinth
#################################################

# More ideas: spiral labyrinth reveal
# Playing in background title screen

# Todo
# Add tile animations (maybe like chess drag and drop?)
# Display path, only show the top treasure, and show the number of treasures left

# Add multiple players
# Illegal move
# Return to square + win lose
# Add Title Screen and Pause

# Add AI

# Bugs
# Red can't pick up treasures
# Game crashing
# Standing on the same tile

def gameDimensions():
    rows = 27
    cols = 27
    cellSize = 19
    margin = 30
    return (rows, cols, cellSize, margin)

def appStarted(app):
    app.gameStarted = False
    app.boardCreated = False
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

    # https://trixelized.itch.io/starstring-fields


    # app.background = app.loadImage('background_0.png')
    # app.background = app.scaleImage(app.background, 3)
    app.tSprite = app.loadImage('tTile.png')
    app.tSprite = app.scaleImage(app.tSprite, 2)
    app.iSprite = app.loadImage('iTile.png')
    app.iSprite = app.scaleImage(app.iSprite, 2)
    app.lSprite = app.loadImage('lTile.png')
    app.lSprite = app.scaleImage(app.lSprite, 2)
    app.emptySprite = app.loadImage('emptyTile.png')
    app.emptySprite = app.scaleImage(app.emptySprite, 2)
    app.emptyRedSprite = app.loadImage('emptyRedTile.png')
    app.emptyRedSprite = app.scaleImage(app.emptyRedSprite, 2)
    app.emptyGreenSprite = app.loadImage('emptyGreenTile.png')
    app.emptyGreenSprite = app.scaleImage(app.emptyGreenSprite, 2)
    app.redCircleSprite = app.loadImage('red_circle.png')
    app.redCircleSprite = app.scaleImage(app.redCircleSprite, 2)
    app.greenCircleSprite = app.loadImage('green_circle.png')
    app.greenCircleSprite = app.scaleImage(app.greenCircleSprite, 2)

    app.batSprites = loadSprites(app, 'rat_bat.png', 0, 160, 32, 2, 10)
    app.ratSprites = loadSprites(app, 'rat_bat.png', 0, 10, 32, 2, 10)
    app.snakeSprites = loadSprites(app, 'snake.png', 0, 10, 32, 2, 10)
    app.slimeSprites = loadSprites(app, 'slime.png', 0, 74, 32, 2, 10)
    # animated sprites https://opengameart.org/content/animated-slime

    app.catSprites = loadSprites(app, 'cat.png', 0, 0, 16, 2, 15)
    app.redJumpSprites = loadSprites(app, 'red.png', 0, 160, 32, 1.5, 8)
    app.redIdleSprites = loadSprites(app, 'red.png', 0, 0, 32, 1.5, 8)
    app.greenJumpSprites = loadSprites(app, 'green.png', 0, 160, 32, 1.5, 8)
    app.greenIdleSprites = loadSprites(app, 'green.png', 0, 0, 32, 1.5, 8)

    app.SpriteCounterFast = 0
    app.SpriteCounterSlow = 0
    # wizards https://penzilla.itch.io/hooded-protagonist

    app.gemSprite = app.loadImage('gem.png')
    app.gemSprite = app.scaleImage(app.gemSprite, 2)
    app.chestSprite = app.loadImage('chest.png')
    app.chestSprite = app.scaleImage(app.chestSprite, 2)
    app.keySprite = app.loadImage('key2.png')
    app.keySprite = app.scaleImage(app.keySprite, 2)
    app.ringSprite = app.loadImage('ring.png')
    app.ringSprite = app.scaleImage(app.ringSprite, 2)
    app.mapSprite = app.loadImage('map.png')
    app.mapSprite = app.scaleImage(app.mapSprite, 2)
    app.bookSprite = app.loadImage('book.png')
    app.bookSprite = app.scaleImage(app.bookSprite, 2)
    # https://free-game-assets.itch.io/free-icons-for-mine-location-pixel-art
    # https://opengameart.org/content/roguelikerpg-items

    app.triangleSpriteUp = app.loadImage('triangle.png')
    app.triangleSpriteUp = app.scaleImage(app.triangleSpriteUp, 2)
    app.triangleSpriteLeft = app.triangleSpriteUp.transpose(Image.ROTATE_90)
    app.triangleSpriteDown = app.triangleSpriteUp.transpose(Image.ROTATE_180)
    app.triangleSpriteRight = app.triangleSpriteUp.transpose(Image.ROTATE_270)

    result = []
    for row in range(app.tileRows):
        result += [[False] * app.tileCols]
    app.board = result
    app.labyrinthTiles = getTiles()
    app.immovableTiles = getImmovableTiles(app)
    app.currentTile = Tile(app, 0, 11, app.labyrinthTiles[0], 0)
    app.currentTileTreasure = None
    
    app.buttons = []
    app.wizards = []
    app.treasuresLeft = []
    app.redTreasuresLeft = []
    app.greenTreasuresLeft = []
    
    app.timerDelay = 17
    app.timePassed = 0
    app.turnCount = 0
    app.messageLength = 0


def loadSprites(app, file, x0, y0, size, scale, spriteLength):
    name = file
    spritestrip = app.loadImage(name)
    sprites = [ ]
    for i in range(spriteLength):
        sprite = spritestrip.crop((size*i, y0, x0+size*(1+i), y0+size))
        # sprite = spritestrip.crop((32*i, 160, 32+32*i, 192))
        sprite = app.scaleImage(sprite, scale)
        sprites.append(sprite)
    return sprites

def addWizards(app):
    app.wizards.append(Wizard(app, 7, 1,'red', True))
    app.wizards.append(Wizard(app, 1, 7,'green', False))
    app.turn = app.wizards[0]

def addTreasuresToPlayer(app):
    random.shuffle(app.treasuresLeft)
    index = len(app.treasuresLeft)//2
    app.redTreasuresLeft = app.treasuresLeft[0:index]
    app.greenTreasuresLeft = app.treasuresLeft[index:]

def addImmovableTreasures(app):
    app.treasuresLeft.append(Treasure(app, 7, 3, 'Map'))
    # app.treasuresLeft.append(Treasure(app, 7, 5, 'Book'))
    app.treasuresLeft.append(Treasure(app, 5, 1, 'Book'))
    app.treasuresLeft.append(Treasure(app, 5, 3, 'Key'))
    # app.treasuresLeft.append(Treasure(app, 5, 5, 'Crown'))
    # app.treasuresLeft.append(Treasure(app, 5, 7, 'Map'))
    # app.treasuresLeft.append(Treasure(app, 3, 1, 'Sword'))
    # app.treasuresLeft.append(Treasure(app, 3, 3, 'Gem'))
    app.treasuresLeft.append(Treasure(app, 3, 5, 'Chest'))
    app.treasuresLeft.append(Treasure(app, 3, 7, 'Ring'))
    # app.treasuresLeft.append(Treasure(app, 1, 3, 'Armor'))
    app.treasuresLeft.append(Treasure(app, 1, 5, 'Gem'))

def addMovableTreasures(app):
    tNames = ['Snake', 'Cat', 'Bat'] 
    tIndex = 0
    lNames = ['Slime', 'Salamader', 'Rat']
    lIndex = 0
    while(tIndex < 3 or lIndex < 3):
        tileRow = 1
        tileCol = 1
        while(tileRow % 2 == 1 and tileCol % 2 == 1):
            tileRow = random.randint(1, 7)
            tileCol = random.randint(1, 7)

        emptyTile = True
        for treasure in app.treasuresLeft:
            tR = treasure.getTileRow()
            tC = treasure.getTileCol()
            if(tileRow == tR and tileCol == tC):
                emptyTile = False
        if(tIndex < 3 and app.board[tileRow][tileCol].getPathCount() == 4 and emptyTile == True):
            app.treasuresLeft.append(Treasure(app, tileRow, tileCol, tNames[tIndex]))
            tIndex += 1
        elif(lIndex < 3 and app.board[tileRow][tileCol].getPathCount() == 3 and emptyTile == True):
            app.treasuresLeft.append(Treasure(app, tileRow, tileCol, lNames[lIndex]))
            lIndex += 1

def getCellBounds(app, row, col):
    x0 = app.margin + app.cellSize * col
    y0 = app.margin + app.cellSize * row
    x1 = app.margin + app.cellSize * (col + 1)
    y1 = app.margin + app.cellSize * (row + 1)
    return x0, y0, x1, y1

def getTileBounds(app, tileRow, tileCol):
    x0 = app.margin + app.tileSize * tileCol
    y0 = app.margin + app.tileSize * tileRow
    x1 = app.margin + app.tileSize * (tileCol + 1)
    y1 = app.margin + app.tileSize * (tileRow + 1)
    return x0, y0, x1, y1

def getTileCenter(app, tileRow, tileCol):
    x = app.margin + app.tileSize * (tileCol + 0.5)
    y = app.margin + app.tileSize * (tileRow + 0.5)
    return x, y

def getTiles():
    tTile = [
        [False, False, False],
        [ True,  True,  True],
        [False,  True, False]
    ]
    iTile = [
        [False, True, False],
        [False, True, False],
        [False, True, False]
    ]
    lTile = [
        [False,  True, False],
        [False,  True,  True],
        [False, False, False]
    ]
    return [tTile, iTile, lTile]

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

def placeCurrentTile(app, x, y):
    for tileRow in [2, 4, 6]:
        for tileCol in [0, 8]:
            centerX, centerY = getTileCenter(app, tileRow, tileCol)
            if(checkInSquare(centerX, centerY, x, y, app.tileSize)):
                return tileRow, tileCol
            if(checkInSquare(centerY, centerX, x, y, app.tileSize)):
                return tileCol, tileRow
    return app.currentTile.getTileRow(), app.currentTile.getTileCol()

def checkInSquare(centerX, centerY, x, y, size):
    if(abs(centerX-x) < size/2 and abs(centerY-y) < size/2):
        return True
    return False

def mousePressed(app, event):
    x, y = app.currentTile.getCoords()
    app.currentTileSelected = checkInSquare(event.x, event.y, x, y, app.tileSize)
    for button in app.buttons:
        if(button.containsPoint(event.x, event.y)):
            function = button.mousePressed(event)
            buttonPressed(app, function)

def mouseDragged(app, event):
    if(app.currentTileSelected):
        app.currentTile.setCoords(event.x, event.y)
    if(app.currentTileTreasure != None):
        app.currentTileTreasure.updateTreasure()

def mouseReleased(app, event):
    if(app.currentTileSelected):
        tileRow, tileCol = placeCurrentTile(app, event.x, event.y)
        app.currentTile.setTile(app, tileRow, tileCol)
        if(app.currentTileTreasure != None):
            app.currentTileTreasure.updateTreasure()
        if(tileRow != 1 or tileCol != 10):
            shiftBoard(app, tileRow, tileCol)
            app.currentTileSelected = False
            app.rotateShiftMode = False
            app.moveMode = True
            app.messageLength = 0

def buttonPressed(app, function):
    pass
    
def shiftBoard(app, currentTileRow, currentTileCol):
    shift = 0
    if(currentTileRow == 0):
        shift = 1
        shiftBoardCol(app, currentTileRow, currentTileCol, shift)
    elif(currentTileCol == 0):
        shift = 1
        shiftBoardRow(app, currentTileRow, currentTileCol, shift)
    elif(currentTileRow == 8):
        shift = -1
        shiftBoardCol(app, currentTileRow, currentTileCol, shift) 
    elif(currentTileCol == 8):
        shift = -1
        shiftBoardRow(app, currentTileRow, currentTileCol, shift)

    app.currentTile.setTile(app, 1, 10)
    moveWizards(app, currentTileRow, currentTileCol, shift)
    moveTreasures(app, currentTileRow, currentTileCol)

def shiftBoardRow(app, currentTileRow, currentTileCol, shift):
    for tileCol in range(1, 8):
        if(shift == -1):
            oldTileCol = tileCol
            newTileCol = tileCol + shift
        elif(shift == 1):
            oldTileCol = 8 - tileCol
            newTileCol = 8 - tileCol + shift
        tile = app.board[currentTileRow][oldTileCol]
        if(isinstance(tile, Tile)):
            tile.setTile(app, currentTileRow, newTileCol)
        app.board[currentTileRow][newTileCol] = tile
    
    if(currentTileCol == 8):
        pushingCol = 7
        pushedCol = 0
    elif(currentTileCol == 0):
        pushingCol = 1
        pushedCol = 8
    app.board[currentTileRow][pushingCol] = app.currentTile
    app.currentTile.setTile(app, currentTileRow, pushingCol)
    app.currentTile = app.board[currentTileRow][pushedCol]
    app.board[currentTileRow][pushedCol] = False

def shiftBoardCol(app, currentTileRow, currentTileCol, shift):
    for tileRow in range(1, 8):
        if(shift == -1):
            oldTileRow = tileRow
            newTileRow = tileRow + shift
        elif(shift == 1):
            oldTileRow = 8 - tileRow
            newTileRow = 8 - tileRow + shift
        tile = app.board[oldTileRow][currentTileCol]
        if(isinstance(tile, Tile)):
            tile.setTile(app, newTileRow, currentTileCol)
        app.board[newTileRow][currentTileCol] = tile
    
    if(currentTileRow == 8):
        pushingRow = 7
        pushedRow = 0
    elif(currentTileRow == 0):
        pushingRow = 1
        pushedRow = 8
    app.board[pushingRow][currentTileCol] = app.currentTile
    app.currentTile.setTile(app, pushingRow, currentTileCol)
    app.currentTile = app.board[pushedRow][currentTileCol]
    app.board[pushedRow][currentTileCol] = False

def moveTreasures(app, currentTileRow, currentTileCol):
    currentTileHasTreasure = False
    for treasure in app.treasuresLeft:
        treasure.updateTreasure()
        if(treasure.getTileCol() == 10):
            app.currentTileTreasure = treasure
            currentTileHasTreasure = True
    if(currentTileHasTreasure == False):
        app.currentTileTreasure = None

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
    if(app.gameStarted == False):
        generateLabyrinth(app)
        app.gameStarted = True
    if(app.gameStarted == True):
        if(event.key == 'r'):
            app.currentTile.rotate(1)
        elif(event.key == 'Space'):
            pass
        elif(event.key == 'w' and app.moveMode == True):
            changeTurn(app)
            app.moveMode = False
            app.rotateShiftMode = True
            app.messageLength = 0
        for wizard in app.wizards:
            if(app.moveMode == True and app.turn == wizard):
                if(event.key == 'Up'):
                    wizard.move(app, -1, 0)
                elif(event.key == 'Down'):
                    wizard.move(app, 1, 0)
                elif(event.key == 'Left'):
                    wizard.move(app, 0, -1)
                    wizard.faceRight(False)
                elif(event.key == 'Right'):
                    wizard.move(app, 0, 1)
                    wizard.faceRight(True)

def changeTurn(app):
    app.turnCount += 1
    app.turn = app.wizards[app.turnCount % 2]

def timerFired(app):
    app.timePassed += 1
    app.SpriteCounterFast += 1
    if(app.timePassed % 3 == 0):
        app.SpriteCounterSlow += 1

    if(app.gameStarted == True):
        app.messageLength += 4
        if(app.boardCreated == False and app.timePassed % 1 == 0):
            boardCreationAnimation(app)
        if(app.boardCreated == True and app.treasuresAdded == False):
            addWizards(app)
            addImmovableTreasures(app)
            addMovableTreasures(app)
            addTreasuresToPlayer(app)
            app.treasuresAdded = True

def drawHelpMessage(app, canvas):
    message = getHelpMessage(app)
    canvas.create_text(60, app.height - 40, text = message,
                            fill='white', font = 'Georgia 14', anchor = 'w')

def getHelpMessage(app):
    message = ''
    if(app.turnCount % 2 == 0):
        wizard = 'Red'
    else:
        wizard = 'Green'
    if(app.rotateShiftMode == True):
        message = f'{wizard}, use R to rotate a tile. Then, drag the tile onto the \nboard to one of the rows or columns with a triangle.'
    elif(app.moveMode == True):
        message = f'{wizard}, move around with the arrow keys and press W when you are done.'
    if(app.messageLength > len(message)):
         index = len(message)
    else:
        index = app.messageLength
    return message[:index]

def boardCreationAnimation(app):
    for tileRow in range(1, 8):
        for tileCol in range(1, 8):
            if(tileRow + tileCol - 2 <= app.diagonalsDrawn):
                app.board[tileRow][tileCol].displayOnScreen()
    app.diagonalsDrawn += 1
    if(app.diagonalsDrawn == 13):
        app.currentTile.displayOnScreen()
        app.boardCreated = True

def redrawAll(app, canvas):
    
    # canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))
    
    canvas.create_rectangle(0, 0, app.width, app.height, fill='dark slate blue', width=0)
    # canvas.create_rectangle(app.margin-1+app.tileSize/2, app.margin-1+app.tileSize/2, 
    #                         app.labyrinthWidth-app.margin-app.tileSize/2, 
    #                         app.labyrinthHeight-app.margin-app.tileSize/2, 
    #                         fill='dark slate blue', width=0)

    drawBoard(app, canvas)

    if(app.gameStarted == False):
        drawTitleScreen(app, canvas)

    if(app.gameStarted == True and app.treasuresAdded == True):
        for button in app.buttons:
            button.redraw(canvas)
        for treasure in app.redTreasuresLeft + app.greenTreasuresLeft:
            treasure.redraw(app, canvas)    
        for wizard in app.wizards:
            wizard.redraw(app, canvas)

        drawTileOptions(app, canvas)
        drawHelpMessage(app, canvas)
        drawTreasuresLeft(app, canvas)

        app.currentTile.drawTile(app, canvas)

        if(app.currentTileTreasure != None):
            app.currentTileTreasure.redraw(app, canvas)
        
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
    for tileRow in [2, 4, 6]:
        for tileCol in [0, 8]:
            x0, y0 = getTileCenter(app, tileRow, tileCol)
            x1, y1 = getTileCenter(app, tileCol, tileRow)

            if(tileCol == 0):
                topBottomSprite = app.triangleSpriteDown
                leftRightSprite = app.triangleSpriteRight
            if(tileCol == 8):
                topBottomSprite = app.triangleSpriteUp
                leftRightSprite = app.triangleSpriteLeft
            
            canvas.create_image(x0, y0, image=ImageTk.PhotoImage(leftRightSprite))
            canvas.create_image(x1, y1, image=ImageTk.PhotoImage(topBottomSprite))


            

            
def drawTreasuresLeft(app, canvas):
    if(app.redTreasuresLeft != []):
        x0, y0 = getTileCenter(app, 4, 9.5)
        x1, y1, x2, y2 = getTileBounds(app, 4, 9.5)
        sprite1 = app.redTreasuresLeft[0].getSprite(app)
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(app.emptyRedSprite))
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(sprite1))
        canvas.create_text(x2-10, y1+6, text = f'{len(app.redTreasuresLeft)}',
                            fill='white', font = 'Georgia 10')
    
    if(app.greenTreasuresLeft != []):
        x0, y0 = getTileCenter(app, 4, 10.5)
        x1, y1, x2, y2 = getTileBounds(app, 4, 10.5)
        sprite2 = app.greenTreasuresLeft[0].getSprite(app)
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(app.emptyGreenSprite))
        canvas.create_image(x0, y0, image=ImageTk.PhotoImage(sprite2))
        canvas.create_text(x2-10, y1+6, text = f'{len(app.greenTreasuresLeft)}',
                            fill='white', font = 'Georgia 10')

def drawTitleScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text = 'LABYRINTH',
                            fill='white', font = 'Georgia 40')
    canvas.create_text(app.width/2, app.height/2+50, 
                            text = 'Press any key to start',
                            fill='white', font = 'Georgia 18')

def drawBoard(app, canvas):
    for tileRow in range(app.tileRows):
        for tileCol in range(app.tileCols):
            if(isinstance(app.board[tileRow][tileCol], Tile)):
                app.board[tileRow][tileCol].drawTile(app, canvas)

# Draws the cell using coordinates from getCellBounds()
def drawCell(app, canvas, row, col, isPath):
    if(isPath == False):
        color = 'sienna1'
    elif(isPath == True):
        color = 'burlywood1'

    if(isinstance(isPath, bool)):
        x0, y0, x1, y1 = getCellBounds(app, row, col, True, True)
        canvas.create_rectangle(x0, y0, x1, y1,
                                fill=color, width = 0)

def rotateTile(L, times):
    result = copy.deepcopy(L)
    for i in range(times):
        transposeTile(result)
        for row in range(len(L)):
            result[row] = list(reversed(result[row]))
    return result

def transposeTile(L):
    for row in range(3):
        for col in range(row, 3):
            temp = L[row][col]
            L[row][col] = L[col][row]
            L[col][row] = temp

def rotateImage(image, times):
    result = image
    for i in range(times):
        result = result.transpose(Image.ROTATE_270)
    return result

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
            canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(app.emptySprite))

def playLabyrinth():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = (cols + 9) * cellSize + 2 * margin
    height = (rows + 1) * cellSize + 2 * margin
    runApp(width = width, height = height)

def main():
    playLabyrinth()

if __name__ == '__main__':
    main()
