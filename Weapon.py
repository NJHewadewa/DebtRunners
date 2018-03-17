from Vector import Vector
from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

class Weapon:
    def __init__(self,d=20, bulletSpeed=7,cd=60,size=2,pos=Vector()):
        self.damage = d
        self.bulletSpeed = bulletSpeed
        self.cooldown = cd
        self.timer = 0
        self.pos = pos
        self.attack = []
        self.size = size

    def addAttack(self, posEnd=Vector(), posStart=Vector()):
        if self.timer <= 0:
            vel = posEnd.subtract(posStart).normalize().multiply(self.bulletSpeed)
            self.attack.append(Bullet(posStart.copy(), vel.copy()))
            self.timer = self.cooldown

    def removeAttack(self, attack):
        if attack in self.attack:
            self.attack.remove(attack)

    def draw(self, canvas):
        if type(self) is Knife:
            pass
        else:
            #canvas.draw_circle(self.pos.getP(), 9, 1, "Green", "Green")
            pass
        for a in self.attack:
            canvas.draw_circle(a.pos.getP(), 4, 1, "Blue", "Blue")
            #below not working for bullet sprite
            #image = simplegui.load_image('https://github.com/NJHewadewa/DebtRunners/blob/master/bullet.png?raw=true')
            #canvas.draw_image(image,(224/2,224/2),(224,224),self.pos.getP(),(112,112))
            # canvas.draw_circle(a.pos.getP(), self.size, 1, "Blue", "Blue")
            #these are the bullets being drawn

    def update(self, mousepos, playerpos):
        #if weapon is being held
        self.pos = mousepos.subtract(playerpos).normalize().multiply(9).add(playerpos)
        #else update position with velocity of it being thrown
        #####HERE#####
        #Update all bullets fired by the gun
        for a in self.attack:
            a.update()

        self.manageCooldown()

    def manageCooldown(self):
        if self.timer < 0:
            self.timer = 0
        else:
            self.timer -= 1

class Knife(Weapon):
    def __init__(self, enemies, d=100):
        super().__init__(d)
        self.d = d
        self.enemies = enemies

    def __str__(self):
        return "Knife"

    def addAttack(self, posEnd=Vector(), posStart=Vector()):
        for enemy in self.enemies:
            if enemy.range(self) < 20:
                    enemy.damage(self.d)
                    # Removing enemies from list enemy list
                    if enemy.killCheck(enemy):
                        self.enemies.remove(enemy)
                    print('knife Hit!')

class Pistol(Weapon):
    def __init__(self, d=5,sp=8, cd=45): #d=damage, sp=speed,cd=cooldown(rate of fire)
        super().__init__(d, sp,cd)

    def __str__(self):
        return "Pistol"

class AutoRifle(Weapon):
    def __init__(self, d=10,sp=13,cd=10): #d=damage, sp=speed,cd=cooldown(rate of fire)
        super().__init__(d,sp,cd)

    def __str__(self):
        return "Automatic Rifle"

class Sniper(Weapon):
    def __init__(self, d=150,sp=30,cd=60): #d=damage, sp=speed,cd=cooldown(rate of fire)
        super().__init__(d,sp,cd)

    def __str__(self):
        return "Sniper Rifle"

class RPG(Weapon):
    def __init__(self,enemies,d=5000,sp=5,cd=100,size=4): #d=damage, sp=speed,cd=cooldown(rate of fire)
        self.enemies = enemies
        super().__init__(d,sp,cd,size) #size = size of bullet

    def __str__(self):
        return "Homing Launcher"


    def addAttack(self, posEnd=Vector(), posStart=Vector()):
        if self.timer <= 0:
            nearestEnemyDistance = 1000
            self.newDestination = Vector()

            for enemy in self.enemies:
                if enemy.range(self) < nearestEnemyDistance:
                    nearestEnemyDistance = enemy.range(self)
                    nearestEnemy = enemy
                    self.newDestination = nearestEnemy.pos.copy()

            #posEnd = self.newDestination
            vel = posEnd.subtract(posStart).normalize().multiply(self.bulletSpeed)
            self.attack.append(Bullet(posStart.copy(), vel.copy(),True,nearestEnemy.pos,self.bulletSpeed))
            self.timer = self.cooldown

class Shotgun(Weapon):
    def __init__(self, numberOfBullets=3,d=20,sp=10,cd=100): #d=damage, sp=speed,cd=cooldown(rate of fire)
        super().__init__(d,sp,cd)
        self.numberOfBullets = numberOfBullets

    def __str__(self):
        if self.numberOfBullets == 3:
            return "Shotgun"
        elif self.numberOfBullets == 6:
            return "Upgraded Shotgun"
        elif self.numberOfBullets > 40:
            return "Atomic Bombs"
        else:
            return "Shotgun" 

    def addAttack(self, mousePos=Vector(), playerPos=Vector()):
        if self.timer <= 0:

            vel = mousePos.copy().subtract(playerPos).normalize().multiply(self.bulletSpeed)
            self.attack.append(Bullet(playerPos.copy(), vel.copy()))
            tempBullets = self.numberOfBullets + 3
            for x in range(1,int(tempBullets/3)):#check if this runs twice instead of once for default
                vel = mousePos.copy().subtract(playerPos.copy()).normalize().multiply(self.bulletSpeed).rotate(x*7)
                self.attack.append(Bullet(playerPos.copy(),vel.copy()))
                vel = mousePos.copy().subtract(playerPos.copy()).normalize().multiply(self.bulletSpeed).rotate(x*-7)
                self.attack.append(Bullet(playerPos.copy(),vel.copy()))

            self.thegodofallDebugs()
            self.timer = self.cooldown

    def thegodofallDebugs(self):
        for a in self.attack:
            print("Index: " + str(self.attack.index(a)))
            print("Position: ", end='')
            print(a.pos.getP())
            print("Velocity: ", end='')
            print(a.vel.getP())

class Bullet:
    def __init__(self, pos=Vector(), vel=Vector(),homing=False,enemyPos=Vector(),bulletSpeed=7):
        self.pos = pos
        self.vel = vel
        self.homing = homing
        self.enemyPos = enemyPos
        self.bulletSpeed = bulletSpeed
        self.counter = 0

    def update(self):
        if self.homing == False:
            self.pos.add(self.vel)
        elif self.homing == True:
            if self.counter < 30:
                #Goes in the direction of the mouse for 30 frames(half a second) then locks onto enemy and fires at the enemy
                self.counter += 1
                self.pos.add(self.vel)
            else:
                self.vel = self.enemyPos.copy().subtract(self.pos.copy()).normalize().multiply(self.bulletSpeed)
                self.pos.add(self.vel)
            #if bullet is homing enabled then set new velocity as position of enemy.
