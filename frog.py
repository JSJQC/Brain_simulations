# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 19:48:21 2022

@author: jakes
"""

import numpy as np
import pygame

class Frog:
    def __init__(self, N, refr = 2, velocity = 1, orientation = 0, satiety = 0):
        self.radius = 1 # Size of the frog's eating reach
        self.pos = np.array([150, 150])
        self.left_eye = self.pos + np.array([-0.4, 0.25])
        self.right_eye = self.pos + np.array([0.4, 0.25])
        
        self.refr = refr # Refractory count
        self.velocity = velocity # Likely to be related to pygame
        self.orientation = orientation # Will be a bearing
        self.satiety = satiety # Will go up as the frog eats food
        
        self.ON = 70
        self.OFF = 0
        self.vals = [self.ON, self.OFF]
        
        empty_layer = self.empty_impulse_layer(N)
        self. impulse_layer = empty_layer
        self.control_layer = self.example_control_layer(empty_layer)
        self.type_layer = self.example_type_layer()
        self.tick_layer = self.initial_ticks(N)
        
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 16)
        self.image = pygame.image.load("frog.bmp")

        
    def random_impulse_layer(self, N):
    
        return np.random.choice(self.vals, N*N, p = [0.2, 0.8]).reshape(N, N)

    def empty_impulse_layer(self, N):
    
        ## Will apply the starting impulse after to this
    
        return np.full((N, N), self.OFF)

    def initial_ticks(self, N):
    
        return np.full((N, N), 0)

    def example_control_layer(self, empty_layer):
    
        c = empty_layer.copy()
    
        c[10, 3] = self.ON
        c[10, 7] = self.ON
    
        return c

    def example_type_layer(self):
    
        ## An 11 x 11 example grid, as drawn on the planning sheet
        
        NERVE = 40
        TWO_JUNCTION = 120
        SHEATH = 999
    
        grid = np.array([[SHEATH, SHEATH, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, SHEATH, SHEATH, TWO_JUNCTION, SHEATH, SHEATH, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH],
                [SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, SHEATH, SHEATH]])
        
        return grid
    
    def get_velocity(self):
        
        return self.velocity
    
    def get_position(self):
        
        return self.pos
    
    def change_orient(self, delta):
        
        self.orientation += delta
        
    def eat(self):
        
        self.satiety += 1
        
    def decision_making(self, food_list):
        
        least_distance = np.inf
        closest = None
        index = 0
        
        for food in food_list:
            
            food_coords = food.get_position()
            frog_coords = self.get_position()
            distance = np.sqrt( ((frog_coords[0] - food_coords[0]) ** 2) + ((frog_coords[0] - food_coords[0]) ** 2) )
            
            if distance < least_distance:
                closest = index
                least_distance = distance
            
            index += 1
            
        return index # Returns index of closest food
    
    def vision(self, food):
        
        # Will produce the control layer needed to turn towards the food -- BIG function
        
        food_pos = food.get_position()
        
                
        
    def display(self, screen):
        
        screen.blit(self.image, self.rect)
        
    
    
''' Not strictly part of the frog class, will be moved out later
    
def update(frameNum, img, frog, N):
    
    impulse_layer = frog.impulse_layer
    tick_layer = frog.tick_layer
    type_layer = frog.type_layer
    control_layer = frog.control_layer
    

    impulse_layer: carries the impulse values (the original "grid")
    tick_layer: contains integer refractory counters
    type_layer: holds activation level information (i.e. nerve vs ganglion)

    
    new_impulse = impulse_layer.copy() # originally newGrid
    new_tick = tick_layer.copy()
    
    for i in range(N):
        for j in range(N):
            
            total = int( (impulse_layer[i, (j - 1) % N] + impulse_layer[i, (j + 1) % N] +
                         impulse_layer[(i - 1) % N, j] + impulse_layer[(i + 1) % N, j] +
                         impulse_layer[(i - 1 ) % N, (j - 1) % N] + impulse_layer[(i - 1) % N, (j + 1) % N] +
                         impulse_layer[(i + 1) % N, (j - 1) % N ] + impulse_layer[(i + 1) % N, (j +1 ) % N]))
            
            ## Conway's rules
            if control_layer[i, j] == OFF:
                if impulse_layer[i, j] == ON: # cells currently only hold charge for one tick
                    new_impulse[i, j] = OFF
                    new_tick[i, j] = REFR
                        
                else:
                    if tick_layer[i, j] == 0:
                        if total >= type_layer[i, j]:
                            new_impulse[i, j] = ON
                    else:
                        new_tick[i, j] = tick_layer[i, j] - 1
                        
            else:
                new_impulse[i, j] = ON
                    
    img.set_data(new_impulse + type_layer)
    impulse_layer[:] = new_impulse[:]
    tick_layer[:] = new_tick[:]
    return img,

'''