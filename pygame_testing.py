# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 20:34:34 2022

@author: jakes
"""

import pygame
import food
import frog

background_colour = (255,255,255)
(width, height) = (2400, 1600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)

crumb = food.Food([150, 50], 50)
boi = frog.Frog(11, )
crumb.display(screen)
boi.display(screen)
pygame.display.flip()
running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      pygame.display.quit()
      pygame.quit()

