from SimpleGUICS2Pygame import simpleguics2pygame as simplegui
import pygame, sys
from Player import Player
from Enemy import Enemy
from Vector import Vector
import time
from Shop import Shop
from hud import hud
from Weapon import *
from Pickup import WeaponPickup, ValuePickeup, Pickup

class Game:
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
        self.shop = Shop(False, self.enemies)
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
        self.AR = AutoRifle()
        self.SG = Shotgun()
        self.melee = Knife(self.enemies)
        self.knife = WeaponPickup(self.melee,self.player,Vector(100,300),60,60,'https://image.ibb.co/kLzxDS/knife.png',self.items)
        self.ak47 = WeaponPickup(self.AR,self.player,Vector(100,50),60,60,'https://image.ibb.co/hQ4eA7/ak47.png',self.items)
        self.shotgun = WeaponPickup(self.SG,self.player,Vector(500,300),60,60,'https://image.ibb.co/hhJQHn/shotgun.png',self.items)
        self.items.append(self.ak47)
        self.items.append(self.shotgun)
        self.items.append(self.knife)
        self.newWave = False
        # Loading in the background image from the github, since I can't do it locally at the moment.
        self.backgroundImage = simplegui.load_image('https://github.com/NJHewadewa/DebtRunners/blob/master/Sprites/parking.png?raw=true')


    def waves(self):
        # This will add the enemies to the list if round 1 is true, see State class. Each wave should only ever occur one at a time.
        if self.waveCount == 1:
            for e in range(3):#3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 10, Pistol(),10))


        elif self.waveCount == 2:
            for e in range(2):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 10, Pistol(), 10))

        elif self.waveCount == 3:
            for e in range(3):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 100, AutoRifle(), 30))
        else:
            self.state.playerWin()




    def draw(self, canvas):
        if self.newWave == True:
            time.sleep(2)
            self.shop.setVisible(True)
            self.newWave = False
        # UPDATE CHARS
        self.move.update()
        self.player.update(self.mouse.pos.copy())
        self.mouse.update()
        print(self.player.health)
        print(self.player.lives)
        # Displaying the background image on the screen.
        # Format: ( Image name, center of image, image dimensions, canvas center, canvas dimensions.)
        canvas.draw_image(self.backgroundImage,(450,450),(900,900),(self.CANVAS_WIDTH/2,self.CANVAS_HEIGHT/2),(self.CANVAS_WIDTH, self.CANVAS_HEIGHT))

        if self.state.winner:
            showScore = "Score: " + str(self.score)
            canvas.draw_text("Winner",[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth('Winner', 50))/2,self.CANVAS_HEIGHT/2],50,'Red')
            canvas.draw_text(showScore,[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth(showScore, 50))/2,(self.CANVAS_HEIGHT/2) + 50],50,'Red')


        # Draw and update enemies
        for enemy in self.enemies:
            # temp shooting place
            enemy.update(self.player.pos.copy())
            enemy.draw(canvas)
            enemy.weapon.addAttack(self.player.pos.copy(), enemy.weapon.pos.copy())

        # Bullet OoB(Out of Bounds) check
        for bullet in self.player.weapon.attack:
            if bullet.pos.y > self.CANVAS_HEIGHT - 20 or bullet.pos.y < 20 or bullet.pos.x > self.CANVAS_WIDTH - 20 or bullet.pos.x < 20:
                self.player.weapon.removeAttack(bullet)

        for enemy in self.enemies:
            for bullet in enemy.weapon.attack:
                if bullet.pos.y > self.CANVAS_HEIGHT - 20 or bullet.pos.y < 20 or bullet.pos.x > self.CANVAS_WIDTH - 20 or bullet.pos.x < 20:
                    enemy.weapon.removeAttack(bullet)

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
                    self.livesCheck(self.player)


                    # Removing the bullet so that is does not go though the enemy
                    enemy.weapon.removeAttack(bullet)
                    #print("Player hit!")


        for item in self.items:
            item.draw(canvas)
            item.update()
        self.shop.draw(canvas)
        self.hud.draw(canvas,self.player.lives,self.player.health)
        # DRAW CHARS HERE
        self.player.draw(canvas)

        #Seeing if the enemies array is empty, if so than increase the round counter by 1, change the state, then run the waves function again. Which will then load in round 2 enemies
        if len(self.enemies) == 0 and self.shop.visible == False:
            roundString = "Round " + str(self.waveCount) + " complete!"
            canvas.draw_text(roundString,[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth(roundString, 50))/2,self.CANVAS_HEIGHT/2],50,'Red')
            self.newWave = True

        # These two if statements must be in this order for the death screen to come up.
        if self.state.over:
            time.sleep(5)
            quit()



        if self.player.lives == 0:
            self.state.gameOver()
            showScore = "Score: " + str(self.score)
            canvas.draw_text("Bankrupted",[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth('Bankrupted', 50))/2,self.CANVAS_HEIGHT/2],50,'Red')
            canvas.draw_text(showScore,[(self.CANVAS_WIDTH/2)-(self.frame.get_canvas_textwidth(showScore, 50))/2,(self.CANVAS_HEIGHT/2) + 50],50,'Red')



    def click(self, pos):
        if self.shop.visible == False:
            self.player.weapon.addAttack(self.mouse.pos.copy(), self.player.weapon.pos.copy())
        if self.shop.visible:
            for button in self.shop.getButtons():
                if (self.mouse.pos.x < (button.pos.x + button.size)) and (
                        self.mouse.pos.x > (button.pos.x - button.size)) and (
                        self.mouse.pos.y < (button.pos.y + button.size)) and (
                        self.mouse.pos.y > (button.pos.y - button.size)):
                    #print("currentGun = " + self.player.weapon.__str__())
                    self.player.weapon = button.gun

                    print("currentGun = " + self.player.weapon.__str__())
                    self.waveCount += 1
                    self.waves()

        self.shop.setVisible(False)

    def killCheck(self, enemy):
        kill = False
        if enemy.health <= 0:
            kill = True
            self.score += enemy.points
            print('Player Score: ', self.score)
            self.enemies.remove(enemy)

        return kill

    def livesCheck(self, player):
        if player.health <= 0:
            self.player.lives -= 1
            if player.lives > 0:
                self.player.health = 100



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


class Interaction: #to avoid repetitive code, add the method to check if (x collided with y)
    def __init__(self, ):
        pass

    def update(self):
        pass


class State:
    def __init__(self):
        self.start = False
        self.over = False
        self.winner = False

    # When the user presses play on the Menu, this should happen. TO BE IMPLEMENTED
    def startGame(self):
        self.start = True


    #When the game is over, this then sets over to true and the game will display a screen wtih the score on. This is for if the player dies, not if the player completes the game
    #that is a different function that I will eventually do.
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
        self.sound = simplegui.load_sound("https://youtu.be/GGXzlRoNtHU")
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
            canvas.draw_text("Instructions go here", [450, 200], 48, "Black")
            canvas.draw_text("", [10, 320], 46, "Green")
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



        elif 450 < self.x < 580 and 360 < self.y < 400:
            self.levelname = "instructions"
            self.instructions()

        elif 400 < self.x < 640 and 420 < self.y < 460:
            self.levelname = "quit"
            quit()

        elif 5 < self.x < 200 and 50 < self.y < 300 and self.levelname == "instructions":
            self.levelname = "startmenu"
            self.startmenu()

    # Running the stuff
    def instructions(self):
        #global title, levelname, maintext
        self.title = "Instructions"
        self.maintext = "Back"

    def startmenu(self):
        #global title, levelname, maintext
        self.title = "Debt Runners"


game = Game()
