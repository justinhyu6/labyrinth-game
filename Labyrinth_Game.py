#################################################
# Labyrinth_Game.py
#
# Your name: Justin Yu
# Your andrew id: justinyu
#################################################

import math, copy, random

from cmu_112_graphics import *
from Interface import *

#################################################
# Labyrinth
#################################################

# More ideas: spiral labyrinth reveal

# Todo
# Add Rotation to the current tile if you press it
# Add shifting with illegal move
# Add Treasures
# Add a player

# Returns a tuple with the game's dimensions
def gameDimensions():
    rows = 21
    cols = 21
    cellSize = 20
    margin = 75
    return (rows, cols, cellSize, margin)

# Sets up the game state
def appStarted(app):
    # app.timerDelay = 400
    (rows, cols, cellSize, margin) = gameDimensions()
    app.rows, app.cols, app.cellSize, app.margin = rows, cols, cellSize, margin
    app.labyrinthWidth = cols * cellSize + 2 * margin
    app.labyrinthHeight = rows * cellSize + 2 * margin

    result = []
    for row in range(rows):
        result += [[False] * cols]
    app.board = result

    app.labyrinthTiles = getTiles()
    app.immovableTiles = getImmovableTiles(app)
    app.currentTile = [
        [False, False, False],
        [False, False, False],
        [False, False, False]
    ]

    app.buttons = getShiftButtons(app)

def mousePressed(app, event):
    for button in app.buttons:
        if(button.containsPoint(event.x, event.y)):
            button.mousePressed(event)

def keyPressed(app, event):
    if(event.key == 'Up'):
        generateLabyrinth(app)

# # Timer
# def timerFired(app):
#     pass

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                            fill='white', outline='black')
    drawBoard(app, canvas)

    for button in app.buttons:
        button.redraw(app, canvas)
    
# Repeatedly calls drawCell() to create the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])
    
    for row in range(3):
        for col in range(3):
            drawCell(app, canvas, row, app.cols + col + 6, 
                    app.currentTile[row][col])

# Draws the cell using coordinates from getCellBounds()
def drawCell(app, canvas, row, col, isPath):
    if(not isPath):
        color = 'tan'
        x0, y0, x1, y1 = getCellBounds(app, row, col, True)
        canvas.create_rectangle(x0, y0, x1, y1,
                                fill=color, outline='white', width = 1)

# Gets the coordinates of the cell
# CITATION: The first half of this function is based on 112 Tetris
def getCellBounds(app, row, col, applyInnerMargin):
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
            y0 -= cellHeight/3 # make wider
            y1 += cellHeight/3
        elif(row % 3 == 0): # make thinner
            y1 -= cellHeight/3
        elif(row % 3 == 2):
            y0 += cellHeight/3
        
        if(col % 3 == 1):
            x0 -= cellWidth/3
            x1 += cellWidth/3
        elif(col % 3 == 0):
            x1 -= cellWidth/3
        elif(col % 3 == 2):
            x0 += cellWidth/3

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

def getShiftButtons(app):
    result = []
    for row in [4, 10, 16]:
        for col in [-2, 22]:
            x0, y0, x1, y1 = getCellBounds(app, row, col, False)
            result.append(Button(x0, y0, x1 - x0, y1 - y0, 'gold'))
    for col in [4, 10, 16]:
        for row in [-2, 22]:
            x0, y0, x1, y1 = getCellBounds(app, row, col, False)
            result.append(Button(x0, y0, x1 - x0, y1 - y0, 'gold'))
    return result

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
            app.board[tileRow*3+row][tileCol*3+col] = app.currentTile[row][col]

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
