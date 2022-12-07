from cmu_112_graphics import *

class Button:
    def __init__(self, x, y, image, function):
        self.x = x
        self.y = y
        self.width, self.height = image.size
        self.image = image
        self.function = function

    def redraw(self, canvas):
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.image))

    def containsPoint(self, x, y):
        if(x >= self.x-self.width/2 and x <= self.x+self.width/2):
            if(y >= self.y-self.height/2 and y <= self.y+self.height/2):
                return True

    def mousePressed(self, event):
        return self.function