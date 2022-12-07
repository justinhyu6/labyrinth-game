from cmu_112_graphics import *
import pygame

class Sound(object):
    def __init__(self, path):
        self.playing = False
        self.path = path
        self.loops = 1
        self.sound = pygame.mixer.Sound(path)

    # Returns True if the sound is currently playing
    def playSound(self):
        if self.playing:
            self.sound.stop()
        else:
            self.sound.play()
        self.playing = not self.playing

def appStarted(app):
    pygame.mixer.init()
    # app.sound = Sound("button.mp3")
    app.sound2 = Sound("abs-pointer-2.mp3")


def redrawAll(app, canvas):
    canvas.create_text(100, 100, text = "hi")

def keyPressed(app, event):
    if (event.key == '1'):
        app.sound2.playSound()
    elif (event.key == '2'):
        app.sound2.playSound()

runApp(width = 300, height = 300)