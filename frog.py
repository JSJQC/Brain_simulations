# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 19:48:21 2022

@author: jakes
"""

import numpy as np
import math
import pygame

class Frog:
    def __init__(self, frog_type, dims, REFR = 2, position = [150, 150], velocity = 1, orientation = 0, satiety = 0):
        self.radius = 50 # Size of the frog's eating reach
        
        self.dims = dims
        self.REFR = REFR
        self.position = np.array(position)
        self.eye_sep = 80
        self.left_eye = self.position + np.array([-1 * self.eye_sep / 2, 25])
        self.right_eye = self.position + np.array([self.eye_sep / 2, 25])
        self.velocity = velocity # Likely to be related to pygame
        self.orientation = orientation * np.pi / 180 # Will be a bearing
        self.satiety = satiety # Will go up as the frog eats food
        
        self.ON = 70
        self.OFF = 0
        self.vals = [self.ON, self.OFF]
        
        empty_layer = self.empty_impulse_layer()
        self. impulse_layer = empty_layer
        #self.control_layer = self.example_control_layer()
        
        if frog_type == 'example':
            self.control_layer = self.example_control_layer()
            self.type_layer = self.type_layer__example()
        
        elif frog_type == 'turning':
            self.control_layer = empty_layer
            self.type_layer = self.type_layer__turning()
            
        self.tick_layer = self.initial_ticks()
        
        #self.rect = pygame.Rect(self.position[0], self.position[1], 16, 16)
        self.image = pygame.image.load("frog_mk2.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.image = pygame.transform.rotate(self.image, self.orientation)

        
    def random_impulse_layer(self):
    
        return np.random.choice(self.vals, self.dims[0] * self.dims[1], p = [0.2, 0.8]).reshape(self.dims[0], self.dims[1])

    def empty_impulse_layer(self):
    
        ## Will apply the starting impulse after to this
    
        return np.full((self.dims[0], self.dims[1]), self.OFF)

    def initial_ticks(self):
    
        return np.full((self.dims[0], self.dims[1]), 0)

    def example_control_layer(self):
    
        c = self.empty_impulse_layer()
    
        c[10, 3] = self.ON
        c[10, 7] = self.ON
    
        return c
    
    def general_control_layer(self, coords):
        
        c = self.empty_impulse_layer()
        
        for coord in coords:
            
            c[coord[0], coord[1]] = self.ON
            
        return c
        

    def type_layer__example(self):
    
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
    
    def type_layer__turning(self):
        
        ## A 6 x 13 grid that implements basic turning in response to stimulus at the top
        
        NERVE = 40
        TWO_JUNCTION = 120
        SHEATH = 999
        
        grid = np.array([[SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH],
                         [SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH],
                         [SHEATH, SHEATH, NERVE, SHEATH, NERVE, SHEATH, SHEATH, SHEATH, NERVE, SHEATH, NERVE, SHEATH, SHEATH],
                         [SHEATH, NERVE, SHEATH, TWO_JUNCTION, SHEATH, NERVE, SHEATH, NERVE, SHEATH, TWO_JUNCTION, SHEATH, NERVE, SHEATH],
                         [SHEATH, NERVE, SHEATH, NERVE, SHEATH, NERVE, SHEATH, NERVE, SHEATH, NERVE, SHEATH, NERVE, SHEATH],
                         [SHEATH, NERVE, SHEATH, NERVE, SHEATH, NERVE, SHEATH, NERVE, SHEATH, NERVE, SHEATH, NERVE, SHEATH]])
        
        return grid
    
    def get_velocity(self):
        
        return self.velocity
    
    def get_position(self):
        
        return self.position
    
    def get_orient(self):
        
        return (self.orientation * 180 / np.pi)
    
    def change_orient(self, delta):
        
        self.orientation += (delta * np.pi / 180)
        #self.image = pygame.transform.rotate(self.image, delta)
        
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
            
        return closest # Returns index of closest food
    
    def angle_calculator(self, food_pos, eye_pos):

        delta = food_pos - eye_pos
        theta_eye = np.arctan(delta[0] / delta[1])
        
        return theta_eye
        
    
    def vision(self, food):
        
        # Will produce the control layer needed to turn towards the food -- BIG function
        
        l1 = False
        l2 = False
        
        r1 = False
        r2 = False
        
        food_pos = food.get_position()
        
        theta_left = self.angle_calculator(food_pos, self.left_eye)
        theta_right = self.angle_calculator(food_pos, self.right_eye)
        theta = theta_left + theta_right
        
        cutoff_lower = np.arctan(-1 * self.eye_sep / (food_pos[1] - self.left_eye[1]))
        cutoff_higher = np.arctan(self.eye_sep / (food_pos[1] - self.left_eye[1]))
        
        if theta > cutoff_lower and theta < cutoff_higher:
            
            ## No turn code
            
            input_layer = self.empty_impulse_layer()
            
        elif theta > cutoff_higher:
            ## Right turn code
            
            remaining_angle = (np.pi / 2) - cutoff_higher
            
            if theta < (cutoff_higher + (remaining_angle / 3)):
                l1 = True
            
            elif theta < (cutoff_higher + (2 * remaining_angle / 3)):
                l2 = True
            
            else:
                l1 = True
                l2 = True
            
        elif theta < cutoff_lower:
            ## Left turn code
            
            remaining_angle = (-1 * np.pi / 2) - cutoff_lower
            
            if theta > (cutoff_lower + (remaining_angle / 3)):
                r1 = True
            
            elif theta > (cutoff_lower + (2 * remaining_angle / 3)):
                r2 = True
            
            else:
                r1 = True
                r2 = True
                
        coords = []
        
        if l1:
            coords.append([0, 1])
        
        if l2:
            coords.append([0, 5])
            
        if r1:
            coords.append([0, 7])
            
        if r2:
            coords.append([0, 11])
            
        print (coords)
            
        input_layer = self.general_control_layer(coords)
        
        self.control_layer = input_layer
        
        print (self.control_layer)
                
        
    def brain_pulse(self, frameNum, img):
    
        dims = self.dims
        impulse_layer = self.impulse_layer
        tick_layer = self.tick_layer
        type_layer = self.type_layer
        control_layer = self.control_layer
        
        '''
    
        impulse_layer: carries the impulse values (the original "grid")
        tick_layer: contains integer refractory counters
        type_layer: holds activation level information (i.e. nerve vs ganglion)
    
        '''    
    
        new_impulse = impulse_layer.copy() # originally newGrid
        new_tick = tick_layer.copy()
        
        for i in range(dims[0]):
            for j in range(dims[1]):
                
                ''' WARNING: Need to change this away from the toroidal conditions at some point'''
                
                total = int( (impulse_layer[i, (j - 1) % dims[1]] + impulse_layer[i, (j + 1) % dims[1]] +
                             impulse_layer[(i - 1) % dims[0], j] + impulse_layer[(i + 1) % dims[0], j] +
                             impulse_layer[(i - 1 ) % dims[0], (j - 1) % dims[1]] + impulse_layer[(i - 1) % dims[0], (j + 1) % dims[1]] +
                             impulse_layer[(i + 1) % dims[0], (j - 1) % dims[1]] + impulse_layer[(i + 1) % dims[0], (j +1 ) % dims[1]]))
                
                ## Conway's rules
                if control_layer[i, j] == self.OFF:
                    if impulse_layer[i, j] == self.ON: # cells currently only hold charge for one tick
                        new_impulse[i, j] = self.OFF
                        new_tick[i, j] = self.REFR
                            
                    else:
                        if tick_layer[i, j] == 0:
                            if total >= type_layer[i, j]:
                                new_impulse[i, j] = self.ON
                        else:
                            new_tick[i, j] = tick_layer[i, j] - 1
                            
                else:
                    new_impulse[i, j] = self.ON
                        
        img.set_data(new_impulse + type_layer)
        self.impulse_layer[:] = new_impulse[:]
        self.tick_layer[:] = new_tick[:]
        return img,

    
        
    def display(self, screen):
        
        screen.blit(self.image, self.rect)
        
        
    def move(self):
            self.position[0] += math.sin(self.orientation) * self.velocity
            self.position[1] += math.cos(self.orientation) * self.velocity
            
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
        
    

