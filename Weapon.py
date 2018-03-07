
from Vector import Vector

class Weapon:
    def __init__(self, d=20, bulletSpeed=7,cd=60, name="", pos=Vector()):
        self.damage = d
        self.bulletSpeed = bulletSpeed
        self.cooldown = cd
        self.name = name
        self.timer = 0
        self.pos = pos
        self.attack = []


        # needs to fire a particular bullet (is string variable correct?)
        # self.bullet = ""
        # also could have gun.name which would give us a good model for bullet
        # In other words:
        #     if gun == Pistol/AssualtRifle/SniperRifle:
        #         bullet.caliber = "light/medium/heavy"
        #
        # in special cases, such as spinning bullet, we can always build a new
        # structure but for now lets keep it simple.

    def addAttack(self, posEnd=Vector(), posStart=Vector()):
        if self.timer <= 0:
            vel = posEnd.subtract(posStart).normalize().multiply(self.bulletSpeed)
            self.attack.append(Bullet(posStart.copy(), vel.copy()))
            self.timer = self.cooldown

    def removeAttack(self, attack):
        self.attack.remove(attack)

    def draw(self, canvas):
        if type(self) is Knife:
            pass
        else:
            canvas.draw_circle(self.pos.getP(), 5, 1, "Green", "Green")
        for a in self.attack:
            canvas.draw_circle(a.pos.getP(), 2, 1, "Blue", "Blue")
            #these are the bullets being drawn

    def update(self, mousepos, playerpos):
        #if weapon is being held
        self.pos = mousepos.subtract(playerpos).normalize().multiply(9).add(playerpos)
        #else update position with velocity of it being thrown
        #####HERE#####
        #Update all bullets fired by the gun
        for a in self.attack:
            a.update(self.attack.index(a))

        self.manageCooldown()



    def manageCooldown(self):
        if self.timer < 0:
            self.timer = 0
        else:
            self.timer -= 1

class Knife(Weapon):
    def __init__(self, name="", d=25):
        super().__init__(name, d)

    # def addAttack(self, pos=Vector(), vel=Vector(5, 0)):
    #     self.attack.append(Bullet(pos, vel))
    #
    # def removeAttack(self, attack):
    #     #Might remove the first item in the list marked bullet, HAVE TO TEST
    #     self.attack.remove(attack)
    #
    # def draw(self, canvas):
    #    super().draw(canvas)
    #
    # def update(self):
    #   pos based cos sin
    #   hit box movement(the line itself)

class Pistol(Weapon):
    def __init__(self, d=25,sp=7, cd=75, name=""):
        super().__init__(d, sp,cd, name)

class AutoRifle(Weapon):
    def __init__(self, d=15,sp=10,cd=10,name=""):
        super().__init__(d,sp,cd,name)

class Shotgun(Weapon):
    def __init__(self, d=15,sp=5,cd=100,name=""):
        super().__init__(d,sp,cd,name)

    def addAttack(self, mousePos=Vector(), playerPos=Vector()):
        if self.timer <= 0:

            vel = mousePos.copy().subtract(playerPos).normalize().multiply(self.bulletSpeed)
            self.attack.append(Bullet(playerPos.copy(), vel.copy()))
            vel = mousePos.copy().subtract(playerPos.copy()).normalize().multiply(self.bulletSpeed).rotate(5)
            self.attack.append(Bullet(playerPos.copy(),vel.copy()))
            vel = mousePos.copy().subtract(playerPos.copy()).normalize().multiply(self.bulletSpeed).rotate(-5)
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
    def __init__(self, pos=Vector(), vel=Vector()):
        self.pos = pos
        self.vel = vel

    def update(self,index):
        self.pos.add(self.vel)


