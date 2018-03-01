from Actor import Actor
from Vector import Vector
from Weapon import Weapon, Knife, Pistol

class Player(Actor):
    def __init__(self, pos = Vector(), vel = Vector(), health=50, weapon=Weapon(Pistol), speed=2, lives=3):
        self.lives = lives
        super().__init__(pos, vel, health, weapon, speed)

    def __str__(self):
        return str(self.lives) + super().__str__()