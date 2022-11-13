#################################################
# Labyrinth_Game.py
#
# Your name: Justin Yu
# Your andrew id: justinyu
#################################################

import math, copy, random

from cmu_112_graphics import *

#################################################
# Labyrinth
#################################################

# Returns a tuple with the game's dimensions
def gameDimensions():
    rows = 21
    cols = 21
    cellSize = 3
    margin = 25
    return (rows, cols, cellSize, margin)

# Sets up the game state
def appStarted(app):
    # app.timerDelay = 400
    (rows, cols, cellSize, margin) = gameDimensions()

    app.rows, app.cols, app.cellSize, app.margin = rows, cols, cellSize, margin
    app.emptyColor = 'white'
    result = []
    for row in range(rows):
        result += [[False] * cols]
    app.board = result

    app.labyrinthTiles = getTiles()
    app.currentTile = []
    app.currentTileRow = -1
    app.currentTileCol = -1

    app.isGameOver = False
    newFallingPiece(app)

def keyPressed(app, event):
    pass

# Timer
def timerFired(app):
    # app.isGameOver = True
    if(not app.isGameOver):
        pass

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, 
    app.height, fill='white', outline='black')
    drawBoard(app, canvas)
    
# Repeatedly calls drawCell() to create the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])

# Draws the cell using coordinates from getCellBounds()
def drawCell(app, canvas, row, col, color):
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1,
    fill=color, outline='black', width = 3)

# Gets the coordinates of the cell
def getCellBounds(app, row, col):
    gridWidth = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + cellWidth * col
    y0 = app.margin + cellHeight * row
    x1 = app.margin + cellWidth * (col + 1)
    y1 = app.margin + cellHeight * (row + 1)
    return x0, y0, x1, y1

# Returns a 3D list with the type of pieces
def getTiles():
    pass

# Calls gameDimensions() to calculate the size of 
# the board and then calls runApp()
def playLabyrinth():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = cols * cellSize + 2 * margin
    height = rows * cellSize + 2 * margin
    runApp(width = width, height = height)

#################################################
# Test Functions
#################################################

# None!  Though... you may wish to (optionally) add some test 
#        functions of your own for any functions that do not 
#        involve graphics


#################################################
# main
#################################################

def main():
    playLabyrinth()

if __name__ == '__main__':
    main()
