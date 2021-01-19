import pygame
import random
import math
from constants import *
from game import game
from menu import menu


#Initialize

pygame.init()

screen = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

pygame.display.set_caption('Cosmic Swarm')

score = 0


    #main loop
    
while True:
    op = menu(screen, score)
    if op == 0:
        sc = game(screen)
        if sc > score:
            score = sc
    elif op == 2:
        break
    else:
        sc = game(screen, 1)
        if sc > score:
            score = sc

pygame.quit()
