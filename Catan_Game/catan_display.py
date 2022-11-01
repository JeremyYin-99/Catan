# %%
import pygame
from catan_classes import *

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)

game = Game()

game_stop = game.completed
while game_stop == False:
    game_stop = game.completed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_stop = True
            exit()


    


# %%
