from Vector import Vector

class Actor:
    def __init__(self, pos = Vector(), vel = Vector(), h=100, w="", speed=0, size=10):
        self.pos = pos
        self.vel = vel
        self.health = h
        self.weapon = w
        self.speed = speed
        self.size = size

    def damage(self, x=0):
        if x > 0:
            self.health -= x

    def heal(self, x=0):
        pass

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.6)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.getP(), self.size, 1, "Red", "White")
        self.weapon.draw(canvas)


    def __str__(self):
        return str(self.health) + self.weapon + str(self.speed) + str(self.size)