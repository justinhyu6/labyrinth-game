#################################################
# Labyrinth_Game.py
#
# Your name: Justin Yu
# Your andrew id: justinyu
#################################################

import math, copy, random

from cmu_112_graphics import *
from Interface import *
from Player import *

#################################################
# Labyrinth
#################################################

# More ideas: spiral labyrinth reveal
# Playing in background title screen

# Todo
# Make tiles classes
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
    app.tileRows = 7
    app.tileCols = 7
    app.innerMargin = 6
    app.outerMargin = 1
    app.labyrinthWidth = app.cols * app.cellSize + 2 * app.margin
    app.labyrinthHeight = app.rows * app.cellSize + 2 * app.margin

    result = []
    for row in range(app.rows):
        result += [[0] * app.cols]
    app.board = result
    app.targetBoard = copy.deepcopy(result)
    app.labyrinthTiles = getTiles()
    app.immovableTiles = getImmovableTiles(app)
    app.currentTile = [
        [False, False, False],
        [False, False, False],
        [False, False, False]
    ]
    
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
    x0, y0 = getCellCenter(app, 19, 1)
    app.wizards.append(Wizard(19, 1, x0, y0, 'tomato'))

def addTreasures(app):
    x0, y0 = getCellCenter(app, 19, 7)
    app.treasures.append(Treasure(19, 7, x0, y0, 'Gold'))
    x0, y0 = getCellCenter(app, 19, 13)
    app.treasures.append(Treasure(19, 11, x0, y0, 'Book'))
    x0, y0 = getCellCenter(app, 13, 1)
    app.treasures.append(Treasure(13, 1, x0, y0, 'Skull'))
    x0, y0 = getCellCenter(app, 13, 7)
    app.treasures.append(Treasure(13, 7, x0, y0, 'Keys'))
    
def addShiftButtons(app):
    for row in [4, 10, 16]:
        for col in [-2, 22]:
            indexToShift = row
            if(col == -2):
                shiftAmount = -1
            elif(col == 22):
                shiftAmount = 1
            x0, y0, x1, y1 = getCellBounds(app, row, col, False, False)
            app.buttons.append(Button(x0, y0, x1-x0, y1-y0, 'gold', 
                                ('shift', indexToShift, 0, shiftAmount)))
            x2, y2, x3, y3 = getCellBounds(app, col, row, False, False)
            app.buttons.append(Button(x2, y2, x3-x2, y3-y2, 'gold', 
                                ('shift', 0, indexToShift, shiftAmount)))

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
        app.currentTile = rotateTile(app.currentTile, 1)
    elif('shift' in function):
        row = function[1]
        col = function[2]
        shift = function[3]
        shiftBoard(app, row, col, shift)
        
        allObjects = app.treasures + app.wizards
        for object in allObjects:
            wrap = False
            if(isinstance(object, Wizard)):
                wrap = True
            if(object.getRow() == row):
                object.move(0, shift, app.cellSize, wrap)
            elif(object.getCol() == col):
                object.move(shift, 0, app.cellSize, wrap)

def keyPressed(app, event):
    if(app.gameStarted == False):
        app.gameStarted = True
        generateLabyrinth(app)
    
    for wizard in app.wizards:
        move = (0, 0)
        if(event.key == 'Up'):
            move = (-1, 0)
        elif(event.key == 'Down'):
            move = (1, 0)
        elif(event.key == 'Left'):
            move = (0, -1)
        elif(event.key == 'Right'):
            move = (0, 1)
        
        if(move != (0, 0)):
            checkRow1 = wizard.getRow() + move[0]
            checkCol1 = wizard.getCol() + move[1]
            checkRow2 = checkRow1 + move[0]
            checkCol2 = checkCol1 + move[1]
            
            if(checkRow2 >= 0 and checkRow2 < app.rows and checkCol2 >= 0 and 
            checkCol2 < app.cols and app.board[checkRow1][checkCol1] != False
            and app.board[checkRow2][checkCol2] != False):
                wizard.move(move[0], move[1], app.cellSize, False)

def timerFired(app):
    app.timePassed += 1

    if(app.gameStarted == True):
        if(app.boardCreated == False):
            boardCreationAnimation(app)

def boardCreationAnimation(app):
    for tileRow in range(app.tileRows):
        for tileCol in range(app.tileCols):
            if(tileRow + tileCol == app.diagonalsDrawn):
                updateTile(app, tileRow, tileCol)
    app.diagonalsDrawn += 1
    if(app.diagonalsDrawn == 13):
        app.boardCreated == True
            
def updateTile(app, tileRow, tileCol):
    startRow = tileRow * 3
    endRow = (tileRow + 1) * 3
    startCol = tileCol
    endCol = (tileCol + 1) * 3
    for row in range(startRow, endRow):
        for col in range(startCol, endCol):
            app.board[row][col] = app.targetBoard[row][col]

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
        drawCurrentTile(app, canvas)
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
            drawTile(app, canvas, tileRow, tileCol)
            
def drawTile(app, canvas, tileRow, tileCol):
    startRow = tileRow * 3
    endRow = (tileRow + 1) * 3
    startCol = tileCol
    endCol = (tileCol + 1) * 3
    for row in range(startRow, endRow):
        for col in range(startCol, endCol):
            drawCell(app, canvas, row, col, app.board[row][col])

def drawCurrentTile(app, canvas):
    for row in range(3):
        for col in range(3):
            drawCell(app, canvas, row, app.cols + col + 6, 
                    app.currentTile[row][col])

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

def getCellCenter(app, row, col):
    gridWidth = app.labyrinthWidth - 2 * app.margin
    gridHeight = app.labyrinthWidth - 2 * app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x = app.margin + cellWidth * (col + 0.5)
    y = app.margin + cellHeight * (row + 0.5)

    return x, y


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

def generateLabyrinth(app):
    tileCounts = [11, 11, 11]
    immovableTileIndex = 0
    for tileRow in range(7):
        for tileCol in range(7):
            if(tileRow % 2 != 0 or tileCol % 2 != 0): # movebaleTile
                chooseTile(app, tileRow, tileCol, 
                            tileCounts, immovableTileIndex, True)
            else:
                chooseTile(app, tileRow, tileCol, 
                            tileCounts, immovableTileIndex, False)
                immovableTileIndex += 1
    app.currentTile = app.labyrinthTiles[0]

def chooseTile(app, tileRow, tileCol, tileCounts, index, moveableTile):
    # Choose the tile
    if(moveableTile):
        index = random.randint(0, 2)
        while(tileCounts[index] == 0):
            index = (index + 1) % 3
        tileCounts[index] -= 1
        times = random.randint(0, 3)
        app.currentTile = rotateTile(app.labyrinthTiles[index], times)
    else:
        app.currentTile = app.immovableTiles[index]
    
    # Set the board to the tile
    for row in range(3):
        for col in range(3):
            app.targetBoard[tileRow*3+row][tileCol*3+col] = app.currentTile[row][col]

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

def shiftBoard(app, row, col, shift):
    newBoard = copy.deepcopy(app.board)
    for r in range(app.rows):
        for c in range(app.cols):
            # Shift Row
            if(col == 0 and (r == row-1 or r == row or r == row+1)):
                copyCol = c - 3 * shift
                # Right-most tile becomes current tile, current tile becomes
                # Left-most tile. Happens when shifting left
                if(copyCol >= app.cols):
                    newBoard[r][c] = app.currentTile[r%3][c%3]
                    app.currentTile[r%3][c%3] = app.board[r][c-18]
                # Left-most tile becomes current tile, current tile becomes
                # Right-most tile. Happens when shifting right
                elif(copyCol < 0):
                    newBoard[r][c] = app.currentTile[r%3][c%3]
                    app.currentTile[r%3][c%3] = app.board[r][c+18]
                # copy a tile from the original board
                else:
                    newBoard[r][c] = app.board[r][copyCol]
            # Shift Col
            if(row == 0 and (c == col-1 or c == col or c == col+1)):
                copyRow = r - 3 * shift
                if(copyRow >= app.rows):
                    newBoard[r][c] = app.currentTile[r%3][c%3]
                    app.currentTile[r%3][c%3] = app.board[r-18][c]
                elif(copyRow < 0):
                    newBoard[r][c] = app.currentTile[r%3][c%3]
                    app.currentTile[r%3][c%3] = app.board[r+18][c]
                else:
                    newBoard[r][c] = app.board[copyRow][c]
    app.board = newBoard

def rotateTile(tile, times):
    result = copy.deepcopy(tile)
    for i in range(times):
        transposeTile(result)
        for row in range(3):
            result[row] = list(reversed(result[row]))
    return result

def transposeTile(tile):
    for row in range(3):
        for col in range(row, 3):
            temp = tile[row][col]
            tile[row][col] = tile[col][row]
            tile[col][row] = temp

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
