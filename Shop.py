from Vector import Vector
from Weapon import *
from Player import Player

class Shop():
    def __init__(self,visible=False,enemies=[],player=Player(),canvasWidth=1200,canvasHeight=700):
        self.visible = visible
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight
        self.enemies = enemies
        self.buttons = []

        self.AssaultRifle = Button(Vector(250,250),50,AutoRifle(),800)
        self.UpgradedShotgun = Button(Vector(250, 400), 100, Shotgun(6),700)
        self.homingLauncher = Button(Vector(450,400),50,RPG(self.enemies),1200)
        self.Shotgun = Button(Vector(450,250),50,Shotgun(),300)
        self.AtomicBomb = Button(Vector(750,250),75,Shotgun(96),1500)
        self.Pistol = Button(Vector(600,250),50,Pistol(),100)
        self.Sniper = Button(Vector(600,400),50,Sniper(),600)
        self.Knife = Button(Vector(750,400),50,Knife(self.enemies),100)
        self.Default = Button(Vector(900, 325), 150, player.weapon, 0)
        self.buttons.append(self.AssaultRifle)
        self.buttons.append(self.Shotgun)
        self.buttons.append(self.Pistol)
        self.buttons.append(self.Knife)
        self.buttons.append(self.UpgradedShotgun)
        self.buttons.append(self.AtomicBomb)
        self.buttons.append(self.homingLauncher)
        self.buttons.append(self.Sniper)
        self.buttons.append(self.Default)
    def update(self, playerpos):
        pass

    def draw(self,canvas):
        offset = 200
        if self.visible == True:
            canvas.draw_polygon([[offset,offset], [self.canvasWidth-offset,offset], [self.canvasWidth-offset, self.canvasHeight-offset],[offset, self.canvasHeight-offset]], 3, 'Black', 'Lime')
            canvas.draw_text('Upgraded Shotgun',self.UpgradedShotgun.pos.getP(),15,'Blue')
            canvas.draw_text("£" + str(self.UpgradedShotgun.price), [self.UpgradedShotgun.pos.getP()[0],self.UpgradedShotgun.pos.getP()[1] + 25], 15, 'Blue')
            canvas.draw_text('Shotgun',self.Shotgun.pos.getP(),15,'Blue')
            canvas.draw_text("£" + str(self.Shotgun.price), [self.Shotgun.pos.getP()[0],self.Shotgun.pos.getP()[1] + 25], 15, 'Blue')
            canvas.draw_text('Atomic Bomb',self.AtomicBomb.pos.getP(),15,'Blue')
            canvas.draw_text("£" + str(self.AtomicBomb.price), [self.AtomicBomb.pos.getP()[0],self.AtomicBomb.pos.getP()[1] + 25], 15, 'Blue')
            canvas.draw_text('RPG',self.homingLauncher.pos.getP(),15,'Blue')
            canvas.draw_text("£" + str(self.homingLauncher.price), [self.homingLauncher.pos.getP()[0],self.homingLauncher.pos.getP()[1] + 25], 15, 'Blue')
            canvas.draw_text('Assault Rifle', self.AssaultRifle.pos.getP(), 15, 'Blue')
            canvas.draw_text("£" + str(self.AssaultRifle.price), [self.AssaultRifle.pos.getP()[0],self.AssaultRifle.pos.getP()[1] + 25], 15, 'Blue')
            canvas.draw_text('Pistol', self.Pistol.pos.getP(), 15, 'Blue')
            canvas.draw_text("£" + str(self.Pistol.price), [self.Pistol.pos.getP()[0],self.Pistol.pos.getP()[1] + 25], 15, 'Blue')
            canvas.draw_text('Knife', self.Knife.pos.getP(), 15, 'Blue')
            canvas.draw_text("£" + str(self.Knife.price), [self.Knife.pos.getP()[0],self.Knife.pos.getP()[1] + 25], 15, 'Blue')
            canvas.draw_text('Sniper', self.Sniper.pos.getP(),15,'Blue')
            canvas.draw_text("£" + str(self.Sniper.price), [self.Sniper.pos.getP()[0],self.Sniper.pos.getP()[1] + 25], 15, 'Blue')
            canvas.draw_text('Continue',self.Default.pos.getP(),15,'Black')
            canvas.draw_text("£" + str(self.Default.price), [self.Default.pos.getP()[0],self.Default.pos.getP()[1] + 25], 15, 'Black')


    def setVisible(self,newVisiblility):
        self.visible = newVisiblility

    def getButtons(self):
        return self.buttons

class Button:
    def __init__(self,pos=Vector(),size=60,gun=Pistol(),price=100):
        self.pos = pos
        self.size = size
        self.gun = gun
        self.price = price