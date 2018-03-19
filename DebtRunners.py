import pygame
from Actor import Player, Enemy
import time
from Shop import Shop
from hud import hud
from Weapon import *
from Pickup import *
from random import *


class Game:
    count = [1, 1]
    damage = 5
    def __init__(self, w=1200, h=700):
        self.CANVAS_WIDTH = w
        self.CANVAS_HEIGHT = h
        self.pointer = Vector()
        self.initialise()
        self.score = 0
        self.state = State()
        self.waveCount = 1
        self.menu = Menu_Screen()
        self.state.startGame()
        self.waves()
        self.shop = Shop(False, self.enemies,self.player)
        self.hud = hud(True)
        self.frame = simplegui.create_frame('Debt Runners', self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.kbd.keyDown)
        self.frame.set_keyup_handler(self.kbd.keyUp)
        self.frame.set_mouseclick_handler(self.click)
        self.frame.set_canvas_background('Gray')
        self.frame.start()

    def initialise(self):
        self.mouse = Mouse()
        self.kbd = Keyboard()
        self.player = Player(Vector(self.CANVAS_WIDTH / 2, self.CANVAS_HEIGHT / 4 * 3))
        self.move = Movement(self.player, self.kbd)
        self.enemies = []
        self.items = []
        self.Pistol = Pistol()
        self.SG = Shotgun()
        self.melee = Knife(self.enemies)
        self.Sniper = Sniper()
        self.AR = AutoRifle()
        self.UpgradedShotgun = Shotgun(6)
        self.homingLauncher = RPG(self.enemies)
        self.AtomicBomb = Shotgun(96)
        self.noMoney = False

        self.newWave = False
        self.backgroundImage = simplegui.load_image('https://image.ibb.co/kEhcuc/map.png')

    def outOfBoundsCheck(self):
        # Bullet OoB(Out of Bounds) check
        for bullet in self.player.weapon.attack:
            if bullet.pos.y > self.CANVAS_HEIGHT - 20 or bullet.pos.y < 20 or bullet.pos.x > self.CANVAS_WIDTH - 20 or bullet.pos.x < 20:
                self.player.weapon.removeAttack(bullet)

        for enemy in self.enemies:
            for bullet in enemy.weapon.attack:
                if bullet.pos.y > self.CANVAS_HEIGHT - 20 or bullet.pos.y < 20 or bullet.pos.x > self.CANVAS_WIDTH - 20 or bullet.pos.x < 20:
                    enemy.weapon.removeAttack(bullet)

    def playerOutOfBounds(self):
        if self.player.pos.x < 0 or self.player.pos.y < 0 or self.player.pos.x > self.CANVAS_WIDTH or self.player.pos.y > self.CANVAS_HEIGHT:
            if Game.count[0] % 60 == 0:
                self.player.damage(Game.damage)
                if Game.damage < 40:
                    Game.damage *= 2
                Game.count[0] = 1
            Game.count[0] += 1
            Game.count[1] = 1
        elif Game.damage > 5 or Game.count[1] > 1:
            Game.count[1] += 1
            if Game.count[1] % 60 == 0:
                Game.damage = 5
                Game.count[0] = 1
                Game.count[1] = 1

    def bulletHitCheck(self):
        # This is for checking to see if the bullet is within the enemies hitbox.
        for bullet in self.player.weapon.attack:
            for enemyIndex in range(len(self.enemies)):
                if (bullet.pos.x < (self.enemies[enemyIndex].pos.x + self.enemies[enemyIndex].size)) and (
                        bullet.pos.x > (self.enemies[enemyIndex].pos.x - self.enemies[enemyIndex].size)) and (
                        bullet.pos.y < (self.enemies[enemyIndex].pos.y + self.enemies[enemyIndex].size)) and (
                        bullet.pos.y > (self.enemies[enemyIndex].pos.y - self.enemies[enemyIndex].size)):

                    # Subtracting damage from enemies health
                    self.enemies[enemyIndex].damage(self.player.weapon.damage)

                    # Removing bullet, so that it does not go through the enemy
                    self.player.weapon.removeAttack(bullet)

                    # Removing enemies from list enemy list
                    if self.killCheck(self.enemies[enemyIndex]):
                        break

        for enemy in self.enemies:
            for bullet in enemy.weapon.attack:
                if (bullet.pos.x < (self.player.pos.x + self.player.size)) and (
                        bullet.pos.x > (self.player.pos.x - self.player.size)) and (
                        bullet.pos.y < (self.player.pos.y + self.player.size)) and (
                        bullet.pos.y > (self.player.pos.y - self.player.size)):
                    # Decreasing player health when bullet lands
                    self.player.damage(enemy.weapon.damage)

                    # Removing the bullet so that is does not go though the enemy
                    enemy.weapon.removeAttack(bullet)

    def waves(self):
        # This will add the enemies to the list if round 1 is true, see State class. Each wave should only ever occur one at a time.
        #basic pistol round
        if self.waveCount == 1:
            self.placeRandomPickups()
            for e in range(3):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 5 * (e + 1), self.CANVAS_HEIGHT / 5), 15, Pistol(), 10))

        #basic shotgun round
        elif self.waveCount == 2:
            self.placeRandomPickups()
            for e in range(3):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 40, Shotgun(), 10))
            for e in range(2):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 5 * (e + 1), self.CANVAS_HEIGHT / 8), 40, Pistol(), 10))

        #sniper round
        elif self.waveCount == 3:
            self.placeRandomPickups()
            for e in range(5):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 6 * (e + 1), self.CANVAS_HEIGHT / 4), 300, Pistol(), 10, 1))

        elif self.waveCount == 4:
            self.placeRandomPickups()
            for e in range(3):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapons
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 50, Shotgun(), 30))

        elif self.waveCount == 5:
            self.placeRandomPickups()
            for e in range(3):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapons
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 100, Shotgun(), 30))

        elif self.waveCount == 6:
            self.placeRandomPickups()
            for e in range(4):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapons
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 8 * (e + 1), self.CANVAS_HEIGHT / 4), 100, AutoRifle(), 30))

        elif self.waveCount == 7:
            self.placeRandomPickups()
            for e in range(5):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapons
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 8 * (e + 1), self.CANVAS_HEIGHT / 4), 100, Shotgun(6), 30))

        elif self.waveCount == 8:
            self.placeRandomPickups()
            for e in range(6):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapons
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 8 * (e + 1), self.CANVAS_HEIGHT / 4), 100, AutoRifle(), 30))

        elif self.waveCount == 9:
            self.placeRandomPickups()
            for e in range(2):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapons
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 200, Shotgun(24), 30))

        elif self.waveCount == 10:
            self.placeRandomPickups()
            for e in range(4):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapons
                self.enemies.append(
                    Enemy(Vector(self.CANVAS_WIDTH / 8 * (e + 1), self.CANVAS_HEIGHT / 4), 250, Shotgun(96), 30))
        else:
            self.state.playerWin()

    def draw(self, canvas):
        if self.newWave == True:
            time.sleep(2)
            self.shop.setVisible(True)
            self.newWave = False

        ################################################
        #                DRAW AND UPDATE
        ################################################
        # UPDATE PLAYABLE CHARS
        self.move.update()
        self.player.update(self.mouse.pos.copy())
        self.mouse.update()
        # Displaying the background image on the screen.
        canvas.draw_image(self.backgroundImage,(450,450),(900,900),(self.CANVAS_WIDTH/2,self.CANVAS_HEIGHT/2),(self.CANVAS_WIDTH, self.CANVAS_HEIGHT))

        # DRAW AND UPDATE ENEMIES
        for enemy in self.enemies:
            enemy.update(self.player.pos.copy())
            enemy.draw(canvas)

        #DRAW AND UPDATE ITEMS
        for item in self.items:
            item.draw(canvas)
            item.update()

        # DRAW CHARS HERE
        self.player.draw(canvas, self.player.pos.copy())

        self.shop.draw(canvas)
        self.hud.draw(canvas,self.player.lives,self.player.health,self.score,self.player.weapon.__str__(),self.player.money)

        self.outOfBoundsCheck()
        self.bulletHitCheck()
        self.playerOutOfBounds()

        #DISPLAY WIN SCREEN
        if self.state.winner:
            playScore = "Score: " + str(self.score)
            canvas.draw_text('Winner',[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth('Winner', 50))/2,self.CANVAS_HEIGHT/2],50,'Red')
            canvas.draw_text(playScore,[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth(playScore, 50))/2,(self.CANVAS_HEIGHT/2)+51],50,'Red')
            if self.state.end:
                time.sleep(5)
                self.frame.stop()
            self.state.end = True

        #Seeing if the enemies array is empty, if so than increase the round counter by 1, change the state, then run the waves function again. Which will then load in round 2 enemies
        if len(self.enemies) == 0 and self.shop.visible == False and self.state.winner == False:
            roundString = "Round " + str(self.waveCount) + " complete!"
            canvas.draw_text(roundString,[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth(roundString, 50))/2,self.CANVAS_HEIGHT/2],50,'Red')
            self.newWave = True


        # These two if statements must be in this order for the death screen to come up.
        if self.state.over:
            time.sleep(3)
            self.frame.stop()

        self.livesCheck(self.player)
        if self.player.lives == 0:
            self.state.gameOver()
            showScore = "Score: " + str(self.score)
            canvas.draw_text("Bankrupted",[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth('Bankrupted', 50))/2,self.CANVAS_HEIGHT/2],50,'Red')
            canvas.draw_text(showScore,[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth(showScore, 50))/2,(self.CANVAS_HEIGHT/2) + 50],50,'Red')

        if self.noMoney == True:
            canvas.draw_text('Not enough money! Try again', [900,400], 15, 'Black')

    def click(self, pos):
        if self.shop.visible == False:
            self.player.weapon.addAttack(self.mouse.pos.copy(), self.player.pos.copy())
        if self.shop.visible:
            for button in self.shop.getButtons():
                if (self.mouse.pos.x < (button.pos.x + button.size)) and (
                        self.mouse.pos.x > (button.pos.x - button.size)) and (
                        self.mouse.pos.y < (button.pos.y + button.size)) and (
                        self.mouse.pos.y > (button.pos.y - button.size)):

                    if button.price == 0:
                        self.waveCount += 1
                        self.waves()
                    elif button.price <= self.player.money:
                        self.player.weapon = button.gun
                        self.player.money -= button.price
                        self.waveCount += 1
                        self.waves()
                    else:
                        self.noMoney = True

        self.shop.setVisible(False)

    def killCheck(self, enemy):
        kill = False
        if enemy.health <= 0:
            kill = True
            self.score += enemy.points
            self.enemies.remove(enemy)
            self.player.money += 100

        return kill

    def livesCheck(self, player):
        if player.health <= 0:
            self.player.lives -= 1
            if player.lives > 0:
                self.player.health = 100

    def placeRandomPickups(self):
        self.pistolPickup = WeaponPickup(self.Pistol, self.player, Vector(randint(100, 1100), randint(200, 700)), 60, 60,'https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/Sprites/Pistol.png',self.items)
        self.knifePickup = WeaponPickup(self.melee, self.player, Vector(randint(100, 1100), randint(200, 700)), 60, 60,'https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/Sprites/knife.png',self.items)
        self.ak47Pickup = WeaponPickup(self.AR, self.player, Vector(randint(100, 1100), randint(200, 700)), 60, 60,'https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/Sprites/Rifle.png',self.items)
        self.shotgunPickup = WeaponPickup(self.SG, self.player, Vector(randint(100, 1100), randint(200, 700)), 60, 60,'https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/Sprites/Shotgun.png',self.items)
        self.sniperPickup = WeaponPickup(self.Sniper, self.player, Vector(randint(100, 1100), randint(200, 700)), 60, 60,'https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/Sprites/Sniper.png',self.items)
        self.RPGPickup = WeaponPickup(self.homingLauncher, self.player, Vector(randint(100, 1100), randint(200, 700)), 60, 60,'https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/Sprites/Rocket.png',self.items)

        Pickups = [self.pistolPickup,self.knifePickup,self.ak47Pickup,self.ak47Pickup,self.shotgunPickup,self.shotgunPickup,self.shotgunPickup,self.sniperPickup,self.RPGPickup]

        for x in range(randint(0,4)):
            self.items.append(Pickups[randint(0, len(Pickups) - 1)])

        self.healthPickup = HealthPickup(25,self.player,Vector(randint(100, 1100), randint(200, 700)),60,60,'https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/Sprites/HP.png',self.items)
        self.items.append(self.healthPickup)
        self.noMoney = False

class Mouse:
    def __init__(self):
        self.pos = Vector()

    def update(self):
        self.pos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]).subtract(Vector(250, 25))


class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['D']:
            self.right = True

        if key == simplegui.KEY_MAP['A']:
            self.left = True

        if key == simplegui.KEY_MAP['W']:
            self.up = True

        if key == simplegui.KEY_MAP['S']:
            self.down = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['D']:
            self.right = False

        if key == simplegui.KEY_MAP['A']:
            self.left = False

        if key == simplegui.KEY_MAP['W']:
            self.up = False

        if key == simplegui.KEY_MAP['S']:
            self.down = False


class Movement:  # solver
    def __init__(self, player, keyboard):
        self.player = player
        self.keyboard = keyboard

    def update(self):
        vel = Vector()
        if self.keyboard.up:
            vel = vel.add(Vector(0, -1))

        if self.keyboard.right:
            vel = vel.add(Vector(1, 0))

        if self.keyboard.left:
            vel = vel.add(Vector(-1, 0))

        if self.keyboard.down:
            vel = vel.add(Vector(0, 1))

        if self.keyboard.up or self.keyboard.down or self.keyboard.left or self.keyboard.right:
            if not vel == Vector():
                self.player.vel.add(vel.normalize().multiply(self.player.speed))

class State:
    def __init__(self):
        self.start = False
        self.over = False
        self.winner = False
        self.end = False

    def startGame(self):
        self.start = True

    # When the game is over, this then sets over to true and the game will display a screen wtih the score on. This is for if the player dies, not if the player completes the game
    def gameOver(self):
        self.over = True

    def playerWin(self):
        self.winner = True


class Menu_Screen:

    def __init__(self):
        self.levelname = "startmenu"
        self.title = "Debt Runners"
        self.maintext = ""
        self.background = simplegui.load_image(
            "https://businessfirstfamily.com/wp-content/uploads/2017/12/consider-debt-consolidation.jpg")
        self.background2 = simplegui.load_image(
            "https://ksr-ugc.imgix.net/assets/014/840/017/401808e191e0c25e8577d7d7d2c49251_original.png?crop=faces&w=1552&h=873&fit=crop&v=1496716514&auto=format&q=92&s=2c65f0228772a91c7de95531eed647c2")
        self.sound = simplegui.load_sound("https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/WWE%20IRS%20(Irwin%20R%20Schyster)%20Theme.ogg")
        self.sound.set_volume(1)


        self.frame = simplegui.create_frame("Dept Runners", 1200, 720)
        self.frame.set_canvas_background('White')
        self.frame.set_draw_handler(self.draw)
        self.frame.set_mouseclick_handler(self.mouse_handler)
        self.frame.start()

    def draw(self, canvas):  # Drawing objects

        if self.levelname == "instructions":
            canvas.draw_image(self.background2, (1553 / 2, 873 / 2), (1552, 873), (1200 / 2, 720 / 2), (1200, 720))
            canvas.draw_text(self.title, [440, 112], 69, "Black", "monospace")
            #canvas.draw_text("title", [440, 112], 69, "Black", "monospace")
            canvas.draw_text("You owe how much?!?! ", [200, 200], 28, "Black")
            canvas.draw_text("The debt collectors are coming for you, do your best to", [200, 250], 28, "Black")
            canvas.draw_text("defend yourself and survive for as long as possible.", [200, 280], 28, "Black")
            canvas.draw_text("You start with 100 heath and once that reaches 0 you lose a life,", [200, 310], 28,
                             "Black")
            canvas.draw_text("lose all 3 and that means game over.", [200, 340], 28, "Black")
            canvas.draw_text("Use WASD to move, your mouse to aim, and left click to shoot. ", [200, 370], 28, "Black")
            canvas.draw_text("Use the store in between rounds to purchase other weapons to ", [200, 400], 28, "Black")
            canvas.draw_text("really make those debt collectors regret coming after you.", [200, 430], 28, "Black")
            canvas.draw_text("Good luck, ya gonna need it... ", [200, 480], 28, "Black")
            canvas.draw_text(self.maintext, [10, 100], 52, "Orange")

        elif self.levelname == "startmenu":
            canvas.draw_image(self.background, (2200 / 2, 1125 / 2), (2200, 1125), (1200 / 2, 720 / 2), (1200, 720))
            canvas.draw_text(self.title, [380, 112], 69, "Black", "monospace")
            canvas.draw_text("Start", [470, 340], 52, "Black")
            canvas.draw_text("Instructions", [470, 400], 52, "Black")
            canvas.draw_text("Quit", [470, 460], 52, "Black")
            self.sound.play()

    def mouse_handler(self, position):  # Buttons activity

        self.x, self.y = position

        if 450 < self.x < 580 and 300 < self.y < 350:
            self.frame.stop()

        elif 450 < self.x < 720 and 360 < self.y < 410:
            self.levelname = "instructions"
            self.instructions()

        elif 450 < self.x < 580 and 420 < self.y < 470:
            self.levelname = "quit"
            quit()

        elif 5 < self.x < 200 and 50 < self.y < 300 and self.levelname == "instructions":
            self.levelname = "startmenu"
            self.startmenu()

    # Running the stuff
    def instructions(self):
        self.title = "Instructions"
        self.maintext = "Back"

    def startmenu(self):
        self.title = "Debt Runners"


while True:
    game = Game()
    game.menu.sound.pause()
