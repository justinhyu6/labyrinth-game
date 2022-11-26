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

# Add multiple players
# Add picking up treasures
# Illegal move
# Return to square

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
    app.rotateShiftMode = False
    app.moveMode = True
    app.currentTileSelected = False
    app.turn = 'tomato'

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

    app.tImage = app.loadImage('tTile.png')
    app.iImage = app.loadImage('iTile.png')
    app.lImage = app.loadImage('lTile.png')

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

def addWizards(app):
    app.wizards.append(Wizard(app, 7, 1,'tomato'))
    app.wizards.append(Wizard(app, 1, 7,'olivedrab4'))

def addTreasuresToPlayer(app):
    random.shuffle(app.treasuresLeft)
    index = len(app.treasuresLeft)//2
    app.redTreasuresLeft = app.treasuresLeft[0:index]
    app.greenTreasuresLeft = app.treasuresLeft[index:]

def addImmovableTreasures(app):
    app.treasuresLeft.append(Treasure(app, 7, 3, 'Gold'))
    # app.treasuresLeft.append(Treasure(app, 7, 5, 'Book'))
    app.treasuresLeft.append(Treasure(app, 5, 1, 'Skull'))
    app.treasuresLeft.append(Treasure(app, 5, 3, 'Keys'))
    # app.treasuresLeft.append(Treasure(app, 5, 5, 'Crown'))
    # app.treasuresLeft.append(Treasure(app, 5, 7, 'Map'))
    # app.treasuresLeft.append(Treasure(app, 3, 1, 'Sword'))
    # app.treasuresLeft.append(Treasure(app, 3, 3, 'Gem'))
    app.treasuresLeft.append(Treasure(app, 3, 5, 'Chest'))
    app.treasuresLeft.append(Treasure(app, 3, 7, 'Ring'))
    # app.treasuresLeft.append(Treasure(app, 1, 3, 'Armor'))
    app.treasuresLeft.append(Treasure(app, 1, 5, 'Chandelier'))

def addMovableTreasures(app):
    tNames = ['Dragon', 'Ghost', 'Bat']
    tIndex = 0
    lNames = ['Owl', 'Salamader', 'Mouse']
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
    x0 = app.margin + app.tileSize * tileRow
    y0 = app.margin + app.tileSize * tileCol
    x1 = app.margin + app.tileSize * (tileRow + 1)
    y1 = app.margin + app.tileSize * (tileCol + 1)
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
    tile2 = Tile(app, 1, 3, tiles[0], 1)
    tile3 = Tile(app, 1, 5, tiles[0], 1)
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
    tile14 = Tile(app, 7, 3, tiles[0], 3)
    tile15 = Tile(app, 7, 5, tiles[0], 3)
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
    if(event.key == 'r'):
        app.currentTile.rotate(1)
    for wizard in app.wizards:
        if(app.moveMode == True and wizard.getColor() == app.turn):
            if(event.key == 'Up'):
                wizard.move(app, -1, 0)
            elif(event.key == 'Down'):
                wizard.move(app, 1, 0)
            elif(event.key == 'Left'):
                wizard.move(app, 0, -1)
            elif(event.key == 'Right'):
                wizard.move(app, 0, 1)

def timerFired(app):
    app.timePassed += 1

    if(app.gameStarted == True):
        if(app.boardCreated == False):
            boardCreationAnimation(app)
        elif(app.boardCreated == True and app.treasuresAdded == False):
            addWizards(app)
            addImmovableTreasures(app)
            addMovableTreasures(app)
            addTreasuresToPlayer(app)
            app.treasuresAdded = True

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
    canvas.create_rectangle(0, 0, app.width, app.height, 
                            fill='light slate blue', outline='black')

    canvas.create_rectangle(app.margin-1+app.tileSize/2, app.margin-1+app.tileSize/2, 
                            app.labyrinthWidth-app.margin-app.tileSize/2, 
                            app.labyrinthHeight-app.margin-app.tileSize/2, 
                            fill='dark slate blue', width=0)

    drawBoard(app, canvas)

    if(app.gameStarted == False):
        drawTitleScreen(app, canvas)

    if(app.gameStarted == True):
        drawTreasuresLeft(app, canvas)
        if(app.currentTileSelected):
            drawTileOptions(app, canvas)
        for button in app.buttons:
            button.redraw(canvas)
        for treasure in app.redTreasuresLeft + app.greenTreasuresLeft:
            treasure.redraw(canvas)    
        for wizard in app.wizards:
            wizard.redraw(canvas)
        app.currentTile.drawTile(canvas)

        # x, y = app.currentTile.getCoords()
        # canvas.create_text(x, y, text = 'curr',
        #                     fill='black', font = 'Georgia 12')

        if(app.currentTileTreasure != None):
            app.currentTileTreasure.redraw(canvas)

def drawTileOptions(app, canvas):
    pass
    # for tileRow in [2, 4, 6]:
    #     for tileCol in [0, 8]:
    #         x0, y0, x1, y1 = getTileBounds(app, tileRow, tileCol)
    #         x2, y2, x3, y3 = getTileBounds(app, tileCol, tileRow)
    #         canvas.create_rectangle(x0, y0, x1, y1,
    #                                 fill='dark slate blue', width = 0)
    #         canvas.create_rectangle(x2, y2, x3, y3,
    #                                 fill='dark slate blue', width = 0)
        
def drawTreasuresLeft(app, canvas):
    
    index = 0
    for treasure in app.redTreasuresLeft:
        x0, y0 = getTileCenter(app, index*0.5 + 3, 10)
        canvas.create_text(x0, y0, text = treasure.getName()[:2],
                            fill='black', font = 'Georgia 12')
        index += 1
    
    index = 0
    for treasure in app.greenTreasuresLeft:
        x0, y0 = getTileCenter(app, index*0.5 + 3, 11)
        canvas.create_text(x0, y0, text = treasure.getName()[:2],
                            fill='black', font = 'Georgia 12')
        index += 1

def drawTitleScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text = 'LABYRINTH',
                            fill='black', font = 'Georgia 40')
    canvas.create_text(app.width/2, app.height/2+50, 
                            text = 'Press any key to start',
                            fill='black', font = 'Georgia 18')

def drawBoard(app, canvas):
    for tileRow in range(app.tileRows):
        for tileCol in range(app.tileCols):
            if(isinstance(app.board[tileRow][tileCol], Tile)):
                app.board[tileRow][tileCol].drawTile(canvas)

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
            self.image1 = app.tImage
        elif(self.list1 == app.labyrinthTiles[1]):
            self.image1 = app.iImage
        elif(self.list1 == app.labyrinthTiles[2]):
            self.image1 = app.lImage
        self.image2 = rotateImage(self.image1, self.times)
    
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
        self.image2 = rotateImage(self.image1, self.times)
        self.list2 = rotateTile(self.list2, times)
    
    def displayOnScreen(self):
        self.display = True
    
    def drawTile(self, canvas):
        if(self.display == True):
            canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.image2))

def playLabyrinth():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = (cols + 9) * cellSize + 2 * margin
    height = (rows) * cellSize + 2 * margin
    runApp(width = width, height = height)

def main():
    playLabyrinth()

if __name__ == '__main__':
    main()
