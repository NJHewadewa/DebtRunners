from Vector import Vector
import random

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
            posX = random.randint(int(self.char.pos.x) - 400, int(self.char.pos.x) + 400)
            posY = random.randint(int(self.char.pos.y) - 400, int(self.char.pos.y) + 400)
            if posX < 25:
                posX = 25
            elif posX > 1150:
                posX = 1150

            if posY < 25:
                posY = 25
            elif posY > 650:
                posY = 650

            self.behaviourdata = Vector(posX, posY)


        self.char.vel = self.behaviourdata.copy().subtract(self.char.pos).normalize().multiply(self.char.speed)

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