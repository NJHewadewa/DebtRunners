from SimpleGUICS2Pygame import simpleguics2pygame as simplegui
class Pickup():
    def __init__(self,player,pos,xBox,yBox,filename, items):
        self.pos = pos
        self.xBox = xBox
        self.yBox = yBox
        self.player = player
        self.filename = filename
        self.image = simplegui.load_image(self.filename)
        self.items = items


    def update(self):
        if (self.player.pos.x < (self.pos.x + self.xBox)) and (
                        self.player.pos.x > (self.pos.x - self.xBox)) and (
                        self.player.pos.y < (self.pos.y + self.xBox*0.5)) and (
                        self.player.pos.y > (self.pos.y - self.xBox*0.5)):
                self.collisionDetected()

    def draw(self, canvas):
        canvas.draw_image(self.image, (896/2,896/2), (896,896), self.pos.getP(), (112,112))

    def collisionDetected(self):
        pass


class WeaponPickup(Pickup): #pickup for the different type of weapons(AR, pistol etc)
    def __init__(self,weapon,player,pos,xBox,yBox,filename, items):
        self.weapon = weapon
        super().__init__(player,pos,xBox,yBox,filename,items)

    def collisionDetected(self):
        self.player.weapon = self.weapon
        self.items.remove(self)


class HealthPickup(Pickup): #pickup that increases a stat, e,g (health, armour, etc)
    def __init__(self,value,player,pos,xBox,yBox,filename,items):
        self.value = value
        self.pos = pos
        super().__init__(player, pos, xBox, yBox, filename, items)

    def collisionDetected(self):
        self.player.health += self.value
        self.items.remove(self)

    def draw(self, canvas):
        canvas.draw_image(self.image, (896 / 2, 896 / 2), (896, 896), self.pos.getP(), (32, 32))


