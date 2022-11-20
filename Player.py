class GenericObject:
    def __init__(self, row, col, x, y):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
    
    def getRow(self):
        return self.row
    
    def getCol(self):
        return self.col
    
    def move(self, tileRows, tileCols, cellSize, wrap):
        self.row += 3 * tileRows
        self.col += 3 * tileCols

        if(wrap == True):
            if(self.row >= 21):
                self.y -= 21 * cellSize
                self.row -= 21
            elif(self.col >= 21):
                self.x -= 21 * cellSize
                self.col -= 21
            elif(self.row < 0):
                self.y += 21 * cellSize
                self.row += 21
            elif(self.col < 0):
                self.x += 21 * cellSize
                self.col += 21
            
        self.x += 3 * tileCols * cellSize
        self.y += 3 * tileRows * cellSize

class Wizard(GenericObject):
    def __init__(self, row, col, x, y, color):
        super().__init__(row, col, x, y)
        self.color = color
    
    def redraw(self, canvas):
        radius = 12
        x0 = self.x - radius
        y0 = self.y - radius
        x1 = self.x + radius
        y1 = self.y + radius
        canvas.create_oval(x0, y0, x1, y1,
                            fill=self.color, outline='black', width=0)

class Treasure(GenericObject):
    def __init__(self, row, col, x, y, name):
        super().__init__(row, col, x, y)
        self.name = name
    
    def redraw(self, canvas):
        canvas.create_text(self.x, self.y, text = self.name[:2],
                            fill='black', font = 'Georgia 12')