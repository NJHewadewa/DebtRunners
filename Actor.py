from Weapon import *
from Behaviour import *
from Sprite import Sprite
import math, random

class Actor: #extend body
    def __init__(self, pos=Vector(), h=100, w=Pistol(), speed=0, colour="Red", vel=Vector(), size=12):
        self.pos = pos
        self.vel = vel
        self.health = h
        self.weapon = w
        self.speed = speed
        self.colour = colour
        self.size = size
        self.sprite = None
        self.rotation = None
        self.oldweapon = w
        self.spriteAssignment()

    def damage(self, x=0):
        if x > 0:
            self.health -= x

    def heal(self, x=0):
        if x > 0:
            self.health += x

    def update(self, aimpos):

        self.rotation = math.atan2(aimpos.y - self.pos.y, aimpos.x - self.pos.x) - 1.5708
        self.pos.add(self.vel)
        self.vel.multiply(0.6)

    def draw(self, canvas, pos):
        if not isinstance(self.oldweapon, type(self.weapon)):
            self.spriteAssignment()
            self.oldweapon = self.weapon
        self.weapon.draw(canvas)
        #canvas.draw_circle(self.pos.getP(), self.size, 1, "Red", self.colour)
        self.sprite.draw(canvas, pos, self.size, self.rotation)


    def killCheck(self, enemy):
        kill = False
        if enemy.health <= 0:
            kill = True
        return kill

    def __str__(self):
        return str(self.health) + self.weapon + str(self.speed) + str(self.size)

    def spriteAssignment(self):
        if isinstance(self, Enemy):
            if isinstance(self.weapon, Pistol):
                if random.randint(0,1) == 0:
                    self.sprite = self.enemySprites[0]
                else:
                    self.sprite = self.enemySprites[1]
            if isinstance(self.weapon, Shotgun):
                if random.randint(0,1) == 0:
                    self.sprite = self.enemySprites[2]
                else:
                    self.sprite = self.enemySprites[3]
            if isinstance(self.weapon, AutoRifle):
                if random.randint(0,1) == 0:
                    self.sprite = self.enemySprites[4]
                else:
                    self.sprite = self.enemySprites[5]
        elif isinstance(self, Player):
            if isinstance(self.weapon, Pistol):
                self.sprite = self.playerSprites[0]
            if isinstance(self.weapon, Shotgun):
                self.sprite = self.playerSprites[1]
            if isinstance(self.weapon, AutoRifle):
                self.sprite = self.playerSprites[2]
            if isinstance(self.weapon, Knife):
                self.sprite = self.playerSprites[3]
            if isinstance(self.weapon, Sniper):
                self.sprite = self.playerSprites[4]
            if isinstance(self.weapon, RPG):
                self.sprite = self.playerSprites[5]

class Player(Actor): #control self
    # Player class sprites holding items in order: Pistol, Shotgun, Rifle, Knife, Sniper, RPG
    playerSprites = [Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/DudePistol.png?raw=true'),
                        Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/DudeShotgun.png?raw=true'),
                            Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/DudeRifle.png?raw=true'),
                                Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/DudeKnife1.png?raw=true'),
                                    Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/DudeSniper.png?raw=true'),
                                        Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/DudeRocket.png?raw=true')]

    def __init__(self, pos=Vector(), health=100, weapon = Pistol(), speed=2, colour="White", lives=3, vel=Vector(), money=0):
        self.lives = lives
        self.money = money
        super().__init__(pos, health, weapon, speed, colour, vel)

    def __str__(self):
        return str(self.lives) + super().__str__()

    def update(self, mousepos):
        super().update(mousepos)
        self.weapon.update(mousepos, self.pos.copy())

class Enemy(Actor):
    #Enemy class sprites holding items in order: Pistol, Shotgun, Rifle (Two of each for different enemy models)
    enemySprites = [Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/BadGuy1Pistol.png?raw=true'),
                        Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/BadGuy2Pistol.png?raw=true'),
                            Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/BadGuy1Shotgun.png?raw=true'),
                                Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/BadGuy2Shotgun.png?raw=true'),
                                    Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/BadGuy1Rifle.png?raw=true'),
                                        Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/BadGuy2Rifle.png?raw=true')]
    def __init__(self, pos=Vector(), health=50, weapon=Pistol(), points=0, speed=2.5, colour="Red", vel=Vector()):
        self.points = points
        super().__init__(pos, health, weapon, speed, colour, vel)
        self.behaviours = [BasicWander(self), Attack(self)]
        self.priority = None
        self.health = health

    def update(self, playerpos):
        self.priorityCheck()
        self.runPriority(playerpos)
        super().update(playerpos)
        self.weapon.update(playerpos, self.pos.copy())

    def range(self,other):
        return self.pos.copy().subtract(other.pos.copy()).length()

    def draw(self, canvas):
        #self.weapon.draw(canvas)
        #canvas.draw_circle(self.pos.getP(), self.size, 1, "Red", self.colour)
        centreX = self.pos.getP()[0]
        centreY = self.pos.getP()[1]
        offset = 10
        yoffset = 15
        canvas.draw_polygon([(centreX-(self.health*0.5),centreY-offset-offset),(centreX+self.health*0.5,centreY-offset-offset),(centreX+self.health*0.5,centreY-yoffset),(centreX-(self.health*0.5),centreY-yoffset)],1,'Black','Green')
        super().draw(canvas, self.pos.copy())

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

