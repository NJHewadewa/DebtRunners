from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

class Sprite:
    def __init__(self, image):
        self.image = simplegui.load_image(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.frameSize = (self.width, self.height)
        self.frameCentre = (self.frameSize[0]/2, self.frameSize[1]/2)

    def draw(self, canvas, pos, size, rotate):
        centerSource = [self.frameCentre[0], self.frameCentre[1]]
        sizeSource = self.frameSize
        centerDest = pos.getP()
        sizeDest = (size*4, size*4)
        canvas.draw_image(self.image, centerSource, sizeSource, centerDest, sizeDest, rotate)

    def drawBullet(self, canvas, pos):
        centerSource = [self.frameCentre[0], self.frameCentre[1]]
        sizeSource = self.frameSize
        centerDest = pos.getP()
        sizeDest = (16, 16)
        canvas.draw_image(self.image, centerSource, sizeSource, centerDest, sizeDest)