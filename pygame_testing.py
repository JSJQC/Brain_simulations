# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 20:34:34 2022

@author: jakes
"""

import pygame
import food
import frog

pygame.init()

background_colour = (255,255,255)
(width, height) = (2400, 1600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)

crumb = food.Food([150, 50], 50, 0, 0)
boi = frog.Frog('example', [11, 11], 2, [500, 500], 3, 0)
pygame.display.flip()
running = True

while running:
    # Screen refresh
    screen.fill(background_colour)
    
    # Crumb movement
    crumb.move()
    crumb.display(screen)
    
    # Frog movement
    boi.move()
    boi.change_orient(1)
    boi.display(screen)
    
    pygame.display.flip()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.display.quit()
        pygame.quit()
