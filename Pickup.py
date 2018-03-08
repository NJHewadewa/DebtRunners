from SimpleGUICS2Pygame import simpleguics2pygame as simplegui
class Pickup():
    def __init__(self,player,pos,xBox,yBox,filename, items):
        self.pos = pos
        self.xBox = xBox #make xBox and ybox into 1 point?
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
        canvas.draw_image(self.image, (192/2,108/2), (192,108), self.pos.getP(), (91,54))
        #canvas.draw_circle(self.pos.getP(), self.xBox/2, 1, "Yellow", "Yellow")

    def collisionDetected(self):
        print("health has been picked up!")
        #remove pickup here(as its now been picked up)
        #prevents spamming of this method


class WeaponPickup(Pickup): #pickup for the different type of weapons(AR, pistol etc)
    def __init__(self,weapon,player,pos,xBox,yBox,filename, items):
        self.weapon = weapon
        super().__init__(player,pos,xBox,yBox,filename,items)
    def collisionDetected(self):
        print("Pickup has been picked up!")
        self.player.weapon = self.weapon
        self.items.remove(self)


class ValuePickeup(Pickup): #pickup that increases a stat, e,g (health, armour, etc)
    def __init__(self,value):
        self.value = value




