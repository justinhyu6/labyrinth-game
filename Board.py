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
# Add tile animations

# Treasures to movable tiles and make them shiftable
# Add multiple players
# Add picking up treasures
# Illegal move

def gameDimensions():
    rows = 21
    cols = 21
    cellSize = 20
    margin = 75
    return (rows, cols, cellSize, margin)

def appStarted(app):
    app.gameStarted = False
    app.boardCreated = False
    app.diagonalsDrawn = 0

    (rows, cols, cellSize, margin) = gameDimensions()
    app.rows, app.cols, app.cellSize, app.margin = rows, cols, cellSize, margin
    app.tileRows, app.tileCols, app.tileSize = 7, 7, app.cellSize * 3
    app.innerMargin = 6
    app.outerMargin = 1
    app.labyrinthWidth = app.cols * app.cellSize + 2 * app.margin
    app.labyrinthHeight = app.rows * app.cellSize + 2 * app.margin

    result = []
    for row in range(app.tileRows):
        result += [[0] * app.tileCols]
    app.board = result
    app.targetBoard = copy.deepcopy(result)
    app.labyrinthTiles = getTiles()
    app.immovableTiles = getImmovableTiles(app)
    app.currentTile = Tile(app, 0, 9, [
        [False, False, False],
        [False, False, False],
        [False, False, False]
    ])
    
    app.buttons = []
    addShiftButtons(app)
    addRotateButton(app)
    app.wizards = []
    addWizards(app)
    app.treasures = []
    addTreasures(app)

    app.timerDelay = 17
    app.timePassed = 0

def addWizards(app):
    app.wizards.append(Wizard(app, 6, 0,'tomato'))

def addTreasures(app):
    app.treasures.append(Treasure(app, 6, 2, 'Gold'))
    app.treasures.append(Treasure(app, 6, 4, 'Book'))
    app.treasures.append(Treasure(app, 4, 0, 'Skull'))
    app.treasures.append(Treasure(app, 4, 2, 'Keys'))
    
def addShiftButtons(app):
    for row in [4, 10, 16]:
        for col in [-2, 22]:
            indexToShift = row//3
            if(col == -2):
                shiftAmount = -1
            elif(col == 22):
                shiftAmount = 1
            x0, y0, x1, y1 = getCellBounds(app, row, col, False, False)
            app.buttons.append(Button(x0, y0, x1-x0, y1-y0, 'gold', 
                                ('shift', indexToShift, -1, shiftAmount)))
            x2, y2, x3, y3 = getCellBounds(app, col, row, False, False)
            app.buttons.append(Button(x2, y2, x3-x2, y3-y2, 'gold', 
                                ('shift', -1, indexToShift, shiftAmount)))

def addRotateButton(app):
    x0, y0, x1, y1 = getCellBounds(app, 4, app.cols + 7, False, False)
    app.buttons.append(Button(x0, y0, x1-x0, y1-y0, 'green3', 'rotate'))

def mousePressed(app, event):
    for button in app.buttons:
        if(button.containsPoint(event.x, event.y)):
            function = button.mousePressed(event)
            buttonPressed(app, function)

def buttonPressed(app, function):
    if('rotate' in function): 
        app.currentTile.rotate(1)
    elif('shift' in function):
        tileRow = function[1]
        tileCol = function[2]
        shiftAmount = function[3]
        shiftBoard(app, tileRow, tileCol, shiftAmount)
        
        allObjects = app.treasures + app.wizards
        for object in allObjects:
            if(object.getTileRow() == tileRow):
                object.shift(app, 0, -shiftAmount)
            elif(object.getTileCol() == tileCol):
                object.shift(app, -shiftAmount, 0)

def keyPressed(app, event):
    if(app.gameStarted == False):
        app.gameStarted = True
        generateLabyrinth(app)
    
    for wizard in app.wizards:
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

def boardCreationAnimation(app):
    for tileRow in range(app.tileRows):
        for tileCol in range(app.tileCols):
            if(tileRow + tileCol == app.diagonalsDrawn):
                app.board[tileRow][tileCol] = app.targetBoard[tileRow][tileCol]
    app.diagonalsDrawn += 1
    if(app.diagonalsDrawn == 13):
        app.boardCreated == True

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                            fill='light slate blue', outline='black')
    canvas.create_rectangle(app.margin-1, app.margin-1, 
                            app.labyrinthWidth-app.margin+1, 
                            app.labyrinthHeight-app.margin+8, 
                            fill='dark slate blue', width=0)

    drawBoard(app, canvas)

    if(app.gameStarted == False):
        drawTitleScreen(app, canvas)

    if(app.gameStarted == True):
        app.currentTile.drawTile(app, canvas)
        for button in app.buttons:
            button.redraw(canvas)
        for treasure in app.treasures:
            treasure.redraw(canvas)
        for wizard in app.wizards:
            wizard.redraw(canvas)

def drawTitleScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text = 'LABYRINTH',
                            fill='black', font = 'Georgia 40')
    canvas.create_text(app.width/2, app.height/2+app.margin/2, 
                            text = 'Press any key to start',
                            fill='black', font = 'Georgia 14')

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

# Gets the coordinates of the cell
# CITATION: The first half of this function is based on 112 Tetris
def getCellBounds(app, row, col, applyInnerMargin, applyOuterMargin):
    gridWidth = app.labyrinthWidth - 2 * app.margin
    gridHeight = app.labyrinthWidth - 2 * app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + cellWidth * col
    y0 = app.margin + cellHeight * row
    x1 = app.margin + cellWidth * (col + 1)
    y1 = app.margin + cellHeight * (row + 1)

    # Decreases the width of the cell if it is an outer cell in the 3x3 Tile,
    # Increases the width of the cell if it is an inner cell
    if(applyInnerMargin):
        if(row % 3 == 1):
            y0 -= app.innerMargin # make wider
            y1 += app.innerMargin
        elif(row % 3 == 0): # make thinner
            y1 -= app.innerMargin
        elif(row % 3 == 2):
            y0 += app.innerMargin
        if(col % 3 == 1):
            x0 -= app.innerMargin
            x1 += app.innerMargin
        elif(col % 3 == 0):
            x1 -= app.innerMargin
        elif(col % 3 == 2):
            x0 += app.innerMargin
    
    if(applyOuterMargin):
        if(row % 3 == 0): # make thinner
            y0 += app.outerMargin
        elif(row % 3 == 2):
            y1 -= app.outerMargin
        if(col % 3 == 0):
            x0 += app.outerMargin
        elif(col % 3 == 2):
            x1 -= app.outerMargin

    return x0, y0, x1, y1

def getTileCenter(app, tileRow, tileCol):
        gridWidth = app.labyrinthWidth - 2 * app.margin
        gridHeight = app.labyrinthWidth - 2 * app.margin
        tileWidth = gridWidth / app.tileRows
        tileHeight = gridHeight / app.tileRows
        x = app.margin + tileWidth * (tileCol + 0.5)
        y = app.margin + tileHeight * (tileRow + 0.5)
        return x, y

def generateLabyrinth(app):
    tileCounts = [11, 11, 11]
    immovableTileIndex = 0
    for tileRow in range(app.tileRows):
        for tileCol in range(app.tileCols):
            if(tileRow % 2 != 0 or tileCol % 2 != 0): # moveableTile
                chooseTile(app, tileRow, tileCol, 
                            tileCounts, immovableTileIndex, True)
            else:
                chooseTile(app, tileRow, tileCol, 
                            tileCounts, immovableTileIndex, False)
                immovableTileIndex += 1
    app.currentTile = Tile(app, 0, 9, app.labyrinthTiles[0])

def chooseTile(app, tileRow, tileCol, tileCounts, index, moveableTile):
    # Choose the tile
    if(moveableTile):
        index = random.randint(0, 2)
        while(tileCounts[index] == 0):
            index = (index + 1) % 3
        tileCounts[index] -= 1
        times = random.randint(0, 3)
        L = rotateTile(app.labyrinthTiles[index], times)
        app.currentTile = Tile(app, tileRow, tileCol, L)
    else:
        L= app.immovableTiles[index]
    app.currentTile = Tile(app, tileRow, tileCol, L)
    
    app.targetBoard[tileRow][tileCol] = app.currentTile

def shiftBoard(app, targetTileRow, targetTileCol, shift):
    newBoard = copy.deepcopy(app.board)
    for tR in range(app.tileRows):
        for tC in range(app.tileCols):
            # Shift Row
            if(tR == targetTileRow):
                copyTileCol = tC + shift
                # Right-most tile becomes current tile, current tile becomes
                # Left-most tile. Happens when shifting left
                if(copyTileCol >= app.tileCols):
                    newBoard[tR][tC].setList(app.currentTile.getList())
                    app.currentTile.setList(app.board[tR][0].getList())
                # Left-most tile becomes current tile, current tile becomes
                # Right-most tile. Happens when shifting right
                elif(copyTileCol < 0):
                    newBoard[tR][tC].setList(app.currentTile.getList())
                    app.currentTile.setList(app.board[tR][6].getList())
                # copy a tile from the original board
                else:
                    newBoard[tR][tC].setList(app.board[tR][copyTileCol].getList())
            # Shift Col
            if(tC == targetTileCol):
                copyTileRow = tR + shift
                if(copyTileRow >= app.tileRows):
                    newBoard[tR][tC].setList(app.currentTile.getList())
                    app.currentTile.setList(app.board[0][tC].getList())
                elif(copyTileRow < 0):
                    newBoard[tR][tC].setList(app.currentTile.getList())
                    app.currentTile.setList(app.board[6][tC].getList())
                else:
                    newBoard[tR][tC].setList(app.board[copyTileRow][tC].getList())
    app.board = newBoard

# Returns a 3D list with the type of pieces
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
    tile1 = rotateTile(tiles[2], 1)
    tile2 = tiles[0]
    tile3 = tiles[0]
    tile4 = rotateTile(tiles[2], 2)
    tile5 = rotateTile(tiles[0], 3)
    tile6 = rotateTile(tiles[0], 3)
    tile7 = tiles[0]
    tile8 = rotateTile(tiles[0], 1)
    tile9 = rotateTile(tiles[0], 3)
    tile10 = rotateTile(tiles[0], 2)
    tile11 = rotateTile(tiles[0], 1)
    tile12 = rotateTile(tiles[0], 1)
    tile13 = tiles[2]
    tile14 = rotateTile(tiles[0], 2)
    tile15 = rotateTile(tiles[0], 2)
    tile16 = rotateTile(tiles[2], 3)
    return [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8,
            tile9, tile10, tile11, tile12, tile13, tile14, tile15, tile16]

def rotateTile(L, times):
    result = copy.deepcopy(L)
    for i in range(times):
        transposeTile(result)
        for row in range(3):
            result[row] = list(reversed(result[row]))
    return result

def transposeTile(L):
    for row in range(3):
        for col in range(row, 3):
            temp = L[row][col]
            L[row][col] = L[col][row]
            L[col][row] = temp

class Tile:
    def __init__(self, app, tileRow, tileCol, L):
        self.tileRow = tileRow
        self.tileCol = tileCol
        self.size = 3 * app.cellSize
        self.L = L
    
    def drawTile(self, app, canvas):
        for row in range(3):
            for col in range(3):
                drawCell(app, canvas, 3*self.tileRow+row, 3*self.tileCol+col,
                        self.L[row][col])
    
    def rotate(self, times):
        self.L = rotateTile(self.L, times)


    def getList(self):
        return self.L

    def setList(self, L):
        self.L = L
        
    def repr(self):
        return self.L


# Calls gameDimensions() to calculate the size of 
# the board and then calls runApp()
# CITATION: Format is inspired by 112 Tetris
def playLabyrinth():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = (cols + 9) * cellSize + 2 * margin
    height = (rows) * cellSize + 2 * margin
    runApp(width = width, height = height)

#################################################
# main
#################################################

def main():
    playLabyrinth()

if __name__ == '__main__':
    main()
