from SimpleGUICS2Pygame import simpleguics2pygame as simplegui
import pygame
from Player import Player
from Enemy import Enemy
from Vector import Vector
from Weapon import Pistol


class Game:
    def __init__(self, w=600, h=400):
        self.CANVAS_WIDTH = w
        self.CANVAS_HEIGHT = h
        self.pointer = Vector()
        self.initialise()

        self.wave1()

        frame = simplegui.create_frame('Debt Runners', self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        frame.set_draw_handler(self.draw)
        frame.set_keydown_handler(self.kbd.keyDown)
        frame.set_keyup_handler(self.kbd.keyUp)
        frame.set_mouseclick_handler(self.click)
        frame.start()

    def initialise(self):
        self.mouse = Mouse()
        self.kbd = Keyboard()
        self.player = Player(Vector(self.CANVAS_WIDTH / 2, self.CANVAS_HEIGHT / 4 * 3))
        self.move = Movement(self.player, self.kbd)
        self.enemies = []

    def wave1(self):
        for e in range(3):
            #Assigns the enemies different positions, health and a new weapon
            self.enemies.append(Enemy(Vector(self.CANVAS_WIDTH/4*(e+1), self.CANVAS_HEIGHT/4), 10, Pistol()))

    def draw(self, canvas):
        # UPDATE CHARS
        self.move.update()
        self.player.update(self.mouse.pos.copy())
        self.mouse.update()

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

            # print('Bullet: ', bullet.pos)
            # print('Enemy: ', self.enemies[1].pos.x)
            # print('Enemy: ', self.enemies[1].pos.y)
            # print('Bullet: ', bullet.pos.x)
            # print('Enemy: ', self.enemies[1].pos.x)

        #This is for checking to see if the bullet is within the enemies hitbox.
        for bullet in self.player.weapon.attack:
            for enemyIndex in range (len(self.enemies)):
                if (bullet.pos.x < (self.enemies[enemyIndex].pos.x + self.enemies[enemyIndex].size)) and (
                        bullet.pos.x > (self.enemies[enemyIndex].pos.x - self.enemies[enemyIndex].size)) and (
                        bullet.pos.y < (self.enemies[enemyIndex].pos.y + self.enemies[enemyIndex].size)) and (
                        bullet.pos.y > (self.enemies[enemyIndex].pos.y - self.enemies[enemyIndex].size)):
                    self.player.weapon.removeAttack(bullet)
                    print('Enemy Hit!')

        for enemy in self.enemies:
            for bullet in enemy.weapon.attack:
                if (bullet.pos.x < (self.player.pos.x + self.player.size)) and (
                        bullet.pos.x > (self.player.pos.x - self.player.size)) and (
                        bullet.pos.y < (self.player.pos.y + self.player.size)) and (
                        bullet.pos.y > (self.player.pos.y - self.player.size)):
                    enemy.weapon.removeAttack(bullet)
                    print("Player hit!")

        # DRAW CHARS HERE
        self.player.draw(canvas)

        #Debug print
        #print(self.player.pos)
        #print(self.player.weapon)

    def click(self, pos):
        self.player.weapon.addAttack(self.mouse.pos.copy(), self.player.weapon.pos.copy())


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


class Movement():  # solver
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


class Interaction():
    def __init__(self, ):
        pass

    def update(self):
        pass


game = Game()
