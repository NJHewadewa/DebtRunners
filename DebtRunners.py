from SimpleGUICS2Pygame import simpleguics2pygame as simplegui
import pygame, sys
from Player import Player
from Enemy import Enemy
from Vector import Vector
import time
#from MainMenu import*
from Weapon import Weapon, Pistol, AutoRifle, Shotgun, Knife
from Pickup import WeaponPickup, ValuePickeup, Pickup

class Game:
    def __init__(self, w=1200, h=700):
        self.CANVAS_WIDTH = w
        self.CANVAS_HEIGHT = h
        self.pointer = Vector()
        self.initialise()
        self.state = State()
        self.waveCount = 1

        if self.state.start:
            #Setting the first round to 1
            self.waves()

            frame = simplegui.create_frame('Debt Runners', self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
            frame.set_draw_handler(self.draw)
            frame.set_keydown_handler(self.kbd.keyDown)
            frame.set_keyup_handler(self.kbd.keyUp)
            frame.set_mouseclick_handler(self.click)
            #frame.set_canvas_background('Gray')
            frame.start()


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
        # Loading in the background image from the github, since I can't do it locally at the moment.
        self.backgroundImage = simplegui.load_image('https://raw.githubusercontent.com/NJHewadewa/DebtRunners/7a447d1331a54688a1903ae9a3ba069a09aebba5/Sprites/backgorun.png')


    def waves(self):
        # This will add the enemies to the list if round 1 is true, see State class. Each wave should only ever occur one at a time.
        if self.waveCount == 1:
            for e in range(3):#3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 10, Pistol()))

    # This will add the enemies to the list if round 2 is true, see State class
        elif self.waveCount == 2:
            for e in range(2):  # 3 is number of enemies
                # Assigns the enemies different positions, health and a new weapon
                self.enemies.append(Enemy(Vector(self.CANVAS_WIDTH / 4 * (e + 1), self.CANVAS_HEIGHT / 4), 10, Pistol()))

    def draw(self, canvas):
        # UPDATE CHARS
        self.move.update()
        self.player.update(self.mouse.pos.copy())
        self.mouse.update()

        # Displaying the background image on the screen.
        # Format: ( Image name, center of image, image dimensions, canvas center, canvas dimensions.)
        canvas.draw_image(self.backgroundImage,(450,450),(900,900),(self.CANVAS_WIDTH/2,self.CANVAS_HEIGHT/2),(self.CANVAS_WIDTH, self.CANVAS_HEIGHT))

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
                    #print(self.player.health)

                    # Removing the bullet so that is does not go though the enemy
                    enemy.weapon.removeAttack(bullet)
                    #print("Player hit!")


        for item in self.items:
            item.draw(canvas)
            item.update()

        # DRAW CHARS HERE
        self.player.draw(canvas)

        #Seeing if the enemies array is empty, if so than increase the round counter by 1, change the state, then run the waves function again. Which will then load in round 2 enemies
        if len(self.enemies) == 0:
            self.waveCount+=1
            self.waves()
            #roundString = "Round " + str(self.waveCount) + " complete!"
            #canvas.draw_text(roundString,[self.CANVAS_WIDTH/2,self.CANVAS_HEIGHT/2],30,'Red')
            #time.sleep(3)



    def click(self, pos):
        self.player.weapon.addAttack(self.mouse.pos.copy(), self.player.weapon.pos.copy())

    def killCheck(self, enemy):
        kill = False
        if enemy.health <= 0:
            kill = True
            self.enemies.remove(enemy)
        return kill


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
        self.start = True
        self.over = False

    # When the user presses play on the Menu, this should happen. TO BE IMPLEMENTED
    def startGame(self):
        self.start = True

    #When the game is over, this then sets over to true and the game will display a screen wtih the score on. This is for if the player dies, not if the player completes the game
    #that is a different function that I will eventually do.
    def gameOver(self):
        self.over = True


game = Game()
