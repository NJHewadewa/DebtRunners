from Actor import Actor
from Vector import Vector
from Weapon import Knife, Pistol

class Enemy(Actor):
    def __init__(self, pos=Vector(), vel=Vector(), health=50, weapon=Pistol(), speed=1):
        super().__init__(pos, vel, health, weapon, speed)

    def __str__(self):
        return str(self.lives) + super().__str__()