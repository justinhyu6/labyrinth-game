class Button:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def redraw(self, app, canvas):
        canvas.create_rectangle(self.x, self.y,
                                self.x+self.width, self.y+self.height,
                                fill=self.color, outline=self.color, width=0)

    def containsPoint(self, x, y):
        if(x >= self.x and x <= self.x+self.width):
            if(y >= self.y and y <= self.y+self.height):
                return True

    def mousePressed(self, event):
        print("pressed")