from Actor import Actor
from Vector import Vector
from Weapon import Knife, Pistol

class Enemy(Actor):
    def __init__(self, pos=Vector(), health=50, weapon=Pistol(), speed=1, colour="Red", vel=Vector()):
        super().__init__(pos, health, weapon, speed, colour, vel)

    def update(self, playerpos):
        self.weapon.update(playerpos, self.pos.copy())
        super().update()

    def range(self,other):
        return self.pos.copy().subtract(other.pos.copy()).length()