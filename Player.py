from Actor import Actor
from Vector import Vector
from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

class Player(Actor):
    def __init__(self, pos = Vector(), vel = Vector(), health=50, weapon="Knife", speed=2, lives=3):
        self.lives = lives
        super().__init__(pos, vel, health, weapon, speed)

    def draw(self, canvas):
        super().draw(canvas, self.pos, self.size)

    def __str__(self):
        return str(self.lives) + super().__str__()