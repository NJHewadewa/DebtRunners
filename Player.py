from Actor import Actor
from Vector import Vector
from Weapon import Knife, Pistol

class Player(Actor):
    def __init__(self, pos=Vector(), health=100, weapon=Pistol(), speed=2, lives=3, vel=Vector()):
        self.lives = lives
        super().__init__(pos, vel, health, weapon, speed)

    def __str__(self):
        return str(self.lives) + super().__str__()