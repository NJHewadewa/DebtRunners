from Actor import Actor
from Vector import Vector
from Weapon import *

class Player(Actor): #control self
    def __init__(self, pos=Vector(), health=100, weapon = Pistol(), speed=2, colour="White", lives=3, vel=Vector(), money=0):
        self.lives = lives
        self.money = money
        super().__init__(pos, health, weapon, speed, colour, vel)

    def __str__(self):
        return str(self.lives) + super().__str__()

    # def update(self, mousepos):
    #     self.weapon.update(mousepos, self.pos)
    #     super().update()

    def update(self, mousepos):
        super().update()
        self.weapon.update(mousepos, self.pos.copy())


