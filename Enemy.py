from Actor import Actor
from Vector import Vector
from Weapon import Knife, Pistol
import random

class Enemy(Actor):
    def __init__(self, pos=Vector(), health=50, weapon=Pistol(), points=0, speed=1, colour="Red", vel=Vector()):
        self.points = points
        super().__init__(pos, health, weapon, speed, colour, vel)
        self.behaviours = [BasicWander(self), Attack(self)]
        self.priority = None

    def update(self, playerpos):
        self.weapon.update(playerpos, self.pos.copy())
        self.priorityCheck()
        self.runPriority(playerpos)
        super().update()

    def range(self,other):
        return self.pos.copy().subtract(other.pos.copy()).length()

    def priorityCheck(self):
        for behaviour in self.behaviours:
            if behaviour.takeAction():
                self.priority = behaviour

    def runPriority(self, data):
        if self.priority == None:
            pass
        else:
            if self.priority.status == None or self.priority.status == "End":
                self.priority.start(data)
            if self.priority.status == "Running":
                self.priority.running()

class Behaviour:
    def __init__(self, char):
        self.behaviourdata = Vector(char.pos.x, char.pos.y)
        self.char = char
        self.status = None

    def start(self, data):
        self.behaviourdata = data
        self.status = "Running"

    def end(self):
        self.status = "End"

class BasicWander(Behaviour):
    def takeAction(self):
        return True

    def running(self):
        if self.char.pos <= self.behaviourdata.copy().add(Vector(5, 5)) or self.char.pos >= self.behaviourdata.copy().subtract(Vector(5, 5)):
            self.behaviourdata = Vector(random.randint(99, 501), random.randint(99, 501))

        self.char.vel.add(self.behaviourdata.copy().subtract(self.char.pos).normalize().multiply(self.char.speed))

class Attack(Behaviour):
    def takeAction(self):
        if self.char.weapon.timer == 0:
            if self.wantToAttack():
                return True
        return False

    def running(self):
        self.char.weapon.addAttack(self.behaviourdata, self.char.pos.copy())
        self.end()

    def wantToAttack(self):
        if random.randrange(0,5) == 2:
            return True
        return False