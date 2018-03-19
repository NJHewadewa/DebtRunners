from Vector import Vector
from Sprite import Sprite


class Weapon:
    def __init__(self,d=20, bulletSpeed=7,cd=60,size=3,pos=Vector()):
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
        for a in self.attack:
            a.bulletSprite.drawBullet(canvas, a.pos.copy())

    def update(self, mousepos, playerpos):
        self.pos = mousepos.subtract(playerpos).normalize().multiply(9).add(playerpos)
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
            self.timer = self.cooldown


class Bullet:
    bulletSprite = Sprite('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/Bullet.png?raw=true')
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
