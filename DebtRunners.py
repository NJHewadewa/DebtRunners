from SimpleGUICS2Pygame import simpleguics2pygame as simplegui
import pygame
from Player import Player
from Vector import Vector

class Game:
    def __init__(self, w=600, h=400):
        self.CANVAS_WIDTH = w
        self.CANVAS_HEIGHT = h
        self.pointer = Vector()
        self.initialise()
        frame = simplegui.create_frame('Debt Runners', self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        frame.set_draw_handler(self.draw)
        frame.set_keydown_handler(self.kbd.keyDown)
        frame.set_keyup_handler(self.kbd.keyUp)
        frame.set_mouseclick_handler(self.click)
        frame.start()

    def initialise(self):
        self.mouse = Mouse()
        self.kbd = Keyboard()
        self.player = Player(Vector(self.CANVAS_WIDTH/2, self.CANVAS_HEIGHT/4*3))
        self.move = Movement(self.player, self.kbd)

    def draw(self, canvas):
        #UPDATE CHARS
        self.move.update()
        self.player.update()
        self.player.weapon.update(self.mouse.pos, self.player.pos)
        self.mouse.update()
        #DRAW CHARS HERE
        self.player.weapon.draw(canvas)
        self.player.draw(canvas)
        print(self.player.weapon.pos)

    def click(self, pos):
        self.player.weapon.addAttack(self.player.weapon.pos, self.mouse.pos)

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

class Movement:
    def __init__(self, player, keyboard):
        self.player = player
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.right:
            self.player.vel.add(Vector(1, 0).multiply(self.player.speed))

        if self.keyboard.left:
            self.player.vel.add(Vector(-1, 0).multiply(self.player.speed))

        if self.keyboard.up:
            self.player.vel.add(Vector(0, -1).multiply(self.player.speed))

        if self.keyboard.down:
            self.player.vel.add(Vector(0, 1).multiply(self.player.speed))


game = Game()


