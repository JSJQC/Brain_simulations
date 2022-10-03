# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 20:14:03 2022

@author: jakes
"""

import pygame

class Food:
    def __init__(self, position, size):
        self.position = position
        self.size = size
        # May add a velocity
    
    def get_position(self):
        
        return self.position
    
    def display(self, screen):
        
        pygame.draw.circle(screen, (0, 0, 255), (self.get_position()[0],
                                                 self.get_position()[1]), self.size, 10)