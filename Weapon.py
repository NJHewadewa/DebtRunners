from Vector import Vector

class Weapon:
    def __init__(self, d=20, pos=Vector()):
        self.name = ""
        self.damage = d
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

    def draw(self, canvas):
        if type(self) is Knife:
            pass
        else:
            canvas.draw_circle(self.pos.getP(), 5, 1, "Green", "Green")

    def update(self, mousepos, playerpos):
        self.pos = mousepos.subtract(playerpos).getNormalized().multiply(9).add(playerpos)

class Knife(Weapon):
    def __init__(self, name="", d=25):
        super().__init__(name, d)

    def addAttack(self, pos=Vector(), vel=Vector(5, 0)):
        self.attack.append(Bullet(pos, vel))

    def removeAttack(self, attack):
        #Might remove the first item in the list marked bullet, HAVE TO TEST
        self.attack.remove(attack)

    #def draw(self, canvas):
    #   super().draw(canvas)

    #def update(self):

class Pistol(Weapon):
    def __init__(self, name="", d=25):
        super().__init__(name, d)

    def addAttack(self, pos=Vector(), vel=Vector(0, -5)):
        self.attack.append(Bullet(pos, vel))

    def removeAttack(self, attack):
        self.attack.remove(attack)


class Bullet:
    def __init__(self, pos=Vector(), vel=Vector()):
        self.pos = pos
        self.vel = vel

    def update(self):
        self.pos.add(self.vel)

