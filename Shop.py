from Vector import Vector
from Weapon import *

class Shop():
    def __init__(self,visible=False,enemies=[],canvasWidth=1200,canvasHeight=700):
        self.visible = visible
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        self.enemies = enemies
        self.buttons = []

        self.Sniper = Button(Vector(900,500),50,Sniper())
        self.AssaultRifle = Button(Vector(200,200),50,AutoRifle())
        self.UpgradedShotgun = Button(Vector(200, 500), 100, Shotgun(6))
        self.homingLauncher = Button(Vector(500,500),50,RPG(self.enemies))
        self.Shotgun = Button(Vector(500,200),50,Shotgun())
        self.AtomicBomb = Button(Vector(800,200),75,Shotgun(96))
        self.Pistol = Button(Vector(900,200),50,Pistol())
        self.Knife = Button(Vector(800,500),50,Knife(self.enemies))
        self.buttons.append(self.AssaultRifle)
        self.buttons.append(self.Shotgun)
        self.buttons.append(self.Pistol)
        self.buttons.append(self.Knife)
        self.buttons.append(self.UpgradedShotgun)
        self.buttons.append(self.AtomicBomb)
        self.buttons.append(self.homingLauncher)
        self.buttons.append(self.Sniper)
    def update(self, playerpos):
        pass

    def draw(self,canvas):
        offset = 100
        if self.visible == True:
            canvas.draw_polygon([[offset,offset], [self.canvasWidth-offset,offset], [self.canvasWidth-offset, self.canvasHeight-offset],[offset, self.canvasHeight-offset]], 3, 'Black', 'Lime')
            canvas.draw_text('Upgraded Shotgun',self.UpgradedShotgun.pos.getP(),15,'Blue')
            canvas.draw_text('Shotgun',self.Shotgun.pos.getP(),15,'Blue')
            canvas.draw_text('Atomic Bomb',self.AtomicBomb.pos.getP(),15,'Blue')
            canvas.draw_text('RPG',self.homingLauncher.pos.getP(),15,'Blue')
            canvas.draw_text('Assault Rifle', self.AssaultRifle.pos.getP(), 15, 'Blue')
            canvas.draw_text('Pistol', self.Pistol.pos.getP(), 15, 'Blue')
            canvas.draw_text('Knife', self.Knife.pos.getP(), 15, 'Blue')
            canvas.draw_text('Sniper', self.Sniper.pos.getP(),15,'Blue')
            #canvas.draw_text('Pistol')


    def setVisible(self,newVisiblility):
        self.visible = newVisiblility

    def getButtons(self):
        return self.buttons

class Button:
    def __init__(self,pos=Vector(),size=60,gun=Pistol()):
        self.pos = pos
        self.size = size
        self.gun = gun