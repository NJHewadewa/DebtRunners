class Weapon:
    def __init__(self):
        self.damage = 0
        #needs to fire a particular bullet (is string variable correct?)
        self.bullet = ""
        # also could have gun.name which would give us a good model for bullet
        # In other words:
        #     if gun == Pistol/AssualtRifle/SniperRifle:
        #         bullet.caliber = "light/medium/heavy"
        #
        # in special cases, such as spinning bullet, we can always build a new
        # structure but for now lets keep it simple.
