from Vector import Vector
from Weapon import Weapon, Pistol

class Actor: #extend body
    def __init__(self, pos=Vector(), h=100, w=Pistol(), speed=0, colour="Red", vel=Vector(), size=10):
        self.pos = pos
        self.vel = vel
        self.health = h
        self.weapon = w
        self.speed = speed
        self.colour = colour
        self.size = size

    def damage(self, x=0):
        if x > 0:
            self.health -= x

    def heal(self, x=0):
        if x > 0:
            self.health += x

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.6)

    def draw(self, canvas):
        self.weapon.draw(canvas)
        canvas.draw_circle(self.pos.getP(), self.size, 1, "Red", self.colour)


    def __str__(self):
        return str(self.health) + self.weapon + str(self.speed) + str(self.size)
