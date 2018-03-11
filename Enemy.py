from Actor import Actor
from Vector import Vector
from Weapon import Knife, Pistol

class Enemy(Actor):
    def __init__(self, pos=Vector(), health=50, weapon=Pistol(), speed=1, colour="Red", vel=Vector()):
        super().__init__(pos, health, weapon, speed, colour, vel)
        self.behaviours = [Wander(), Attack()]
        self.priority = None

    def update(self, playerpos):
        self.weapon.update(playerpos, self.pos.copy())
        super().update()

    def priorityCheck(self):
        for behaviour in self.behaviours:
            if behaviour.takeAction:
                self.priority = behaviour

    #def runpriority


class Behaviour:
    def __init__(self):
        # self.start = False
        # self.running = False
        # self.end = False
        self.status = None

    def start(self):
        # self.start = True
        # self.running = False
        # self.end = False
        self.status = "Start"

    def run(self):
        # self.start = False
        # self.running = True
        # self.end = False
        self.status = "Running"

    def end(self):
        # self.start = False
        # self.running = False
        # self.end = True
        self.status = "End"

class Wander(Behaviour):
    def takeAction(self):
        # if self.running = False:
        #     return True
        # return False
        pass

    def run(self):
        #if enemy has calculated position
            #if calculated position != enemy position
                #accelerate enemy to position
            #else
                #self.end()
        #else
            #start calculate behaviour/function
        pass

    def exit(self):
        #self.end()
        pass


class Attack(Behaviour):
    def takeAction(self):
        pass

    def run(self):
        pass

    def exit(self):
        pass

behave = Wander()

print(behave.start)