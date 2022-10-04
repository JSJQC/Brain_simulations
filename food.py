# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 20:14:03 2022

@author: jakes
"""

import pygame
import math

class Food:
    def __init__(self, position, size = 1, velocity = 1, orientation = 0):
        self.position = position
        self.size = size
        self.velocity = velocity
        self.orientation = orientation * math.pi / 180 # A bearing converted into radians
        # May add a velocity
    
    def get_position(self):
        
        return self.position
    
    def display(self, screen):
        
        pygame.draw.circle(screen, (0, 0, 255), (self.get_position()[0],
                                                 self.get_position()[1]), self.size, 10)
        
    def move(self):
            self.position[0] += math.sin(self.orientation) * self.velocity
            self.position[1] += math.cos(self.orientation) * self.velocity