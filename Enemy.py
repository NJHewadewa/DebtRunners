from Actor import Actor
from Vector import Vector
from Weapon import Knife, Pistol

class Enemy(Actor):
    def __init__(self, pos=Vector(), vel=Vector(), health=50, weapon=Pistol(), speed=1, colour="Red"):
        super().__init__(pos, vel, health, weapon, speed, colour)

    def __str__(self):
        return str(self.lives) + super().__str__()

    def update(self, playerpos):
        self.weapon.update(playerpos, self.pos.copy())
        super().update()

    # def update(self, playerpos):
    #     self.weapon.update(self.pos, Vector(10,10))