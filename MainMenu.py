######################################################################
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import pygame
pygame.init()
import sys

#   1. Create a pygame.font.Font object
#   2. Create a Surface object with the text drawn on it by calling the Font objects render() method.
#   3. Create a Rect object from the Surface object by calling the Surface objects get_rect() method.
#      This Rect object will have the width and height correctly set for the text that was rendered,
#      but the top and left attributes will be 0.
#   4. Set the position of the Rect object by changing one of its attributes.
#   5. Blit the Surface object with the text onto the Surface object returned by pygame.display.set_mode().
#   6. Call pygame.display.update() to make the display Surface appear on the screen.

class Menu_item:

    hovered = False

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.rend = menu_font.render(self.text, False, self.get_color())
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
        screen.blit(self.rend, self.rect)

    def draw(self):
        self.rend = menu_font.render(self.text, False, self.get_color())
        screen.blit(self.rend, self.rect)

    def get_color(self):
        if self.hovered:
            return (100, 100, 100)
        else:
            return (255, 255, 255)

screen = pygame.display.set_mode((640, 480))

screen.fill((100, 50, 150)) #Background colour

menu_font = pygame.font.Font(None, 40)

menu_items = [Menu_item("Play Game", (140, 105)),
              Menu_item("Instructions", (140, 155)),
              Menu_item("Exit", (140, 205))]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        for menu_item in menu_items:
            if menu_item.rect.collidepoint(pygame.mouse.get_pos()):
                menu_item.hovered = True
                if menu_item.text == "Play Game" and event.type == pygame.MOUSEBUTTONDOWN:
                    print ("Play Game")
                if menu_item.text == "Exit" and event.type == pygame.MOUSEBUTTONDOWN:
                    sys.exit()
            else:
                menu_item.hovered = False
            menu_item.draw()
        pygame.display.update()