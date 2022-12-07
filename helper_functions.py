#################################################
# Helper Functions
#################################################

import copy

# https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors

def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

def getHelpMessage(app):
    message = ''
    if(app.mainMenu ):
        if(app.menuIndex == 0):
            message = 'Change the number of AI.'
        elif(app.menuIndex == 1):
             message = 'Change the number of players.'
        elif(app.menuIndex == 2):
            message = 'Start the game?'
        message += ' (Press space to select)'
    elif(app.gameStarted):
        if(app.turn == app.blueWizard):
            wizard = 'Blue'
        elif(app.turn == app.redWizard):
            wizard = 'Red'
        elif(app.turn == app.yellowWizard):
            wizard = 'Yellow'
        elif(app.turn == app.greenWizard):
            wizard = 'Green'
            
        if(app.treasuresAdded == False):
            message = 'Welcome to Labyrinth!'
        elif(app.rotateShiftMode == True):
            message = f'{wizard}, use R to rotate a tile. Then, drag the tile onto the \nboard to one of the rows or columns with a triangle.'
        elif(app.moveMode == True):
            message = f'{wizard}, move around with the arrow keys and press space.'
    if(app.messageLength > len(message)):
         index = len(message)
    else:
        index = app.messageLength
    return message[:index]

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
    
def checkInSquare(centerX, centerY, x, y, size):
    if(abs(centerX-x) < size/2 and abs(centerY-y) < size/2):
        return True
    return False

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