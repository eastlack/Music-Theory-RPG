"""
This file contains all global variables
"""

import pygame

# initialize pygame
pygame.init()
pygame.display.set_caption("Music Theory RPG")
FPSclock = pygame.time.Clock()

# display screen values
SCREENX = 1275
SCREENY = 750
MENUTOP = SCREENY - 75
SCREEN = pygame.display.set_mode((SCREENX, SCREENY))

