import pygame
import random
import math
from constants import *
from game import game
from menu import menu


#Inicialização
pygame.init()

screen = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

pygame.display.set_caption('Cosmic Swarm')

font = pygame.font.Font('font/8-bit-pusab.ttf', 23)



while True:
    op = menu(screen)
    if op == 0:
        game(screen, font)
    if op == 1:
        break

pygame.quit()
