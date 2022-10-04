# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 13:16:05 2022

@author: jakes
"""

import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation

import frog
import food


def main(dims, movfile, interval):

    updateInterval = int(interval)
    
    boi = frog.Frog('example', [dims[0], dims[1]])    
        
    ## Animation
    
    fig, ax = plt.subplots()
    #plt.gcf().text(0.9, 0.9, 'text', fontsize = 20)
    cmp = colors.ListedColormap(['dimgray', 'white', 'gray', 'white', 'black', 'white'])
    bounds = [0, 41, 111, 121, 191, 1000, 1071]
    norm = colors.BoundaryNorm(bounds, cmp.N)
    img = ax.imshow(boi.impulse_layer + boi.type_layer, cmap = cmp, norm = norm, interpolation = 'nearest')
    #img = ax.imshow(type_layer, interpolation = 'nearest') ## Shows the type layout
    ani = animation.FuncAnimation(fig, boi.brain_pulse, fargs = (img, ),
                                  frames = 20,
                                  interval = updateInterval,
                                  save_count = 50)
    
    fig.set_size_inches(dims[0], dims[1], True)
    ani.save(movfile, fps = 2) #, extra_args = ['-vcodec', 'libx2645'])
        
    plt.show()
    
def food_sighting_test(dims):
    
    crumb_left = food.Food([0, 200])
    crumb_center = food.Food([100, 200])
    crumb_right = food.Food([200, 200])
    
    boi = frog.Frog('turning', [dims[0], dims[1]], position = [100, 0])
    
    boi.vision(crumb_left)
    print ()
    boi.vision(crumb_center)
    print ()
    boi.vision(crumb_right)
    
if __name__ == "__main__":
    #main([11, 11], 'example_mk2.gif', 1000)
    
    food_sighting_test([6, 13])
    
''' NEXT TO DO:
    
    IMPLEMENT THE VISION IN THE BRAIN IMPULSE METHOD
    IMPLEMENT OUTPUTS (MAYBE AS A LAYER)
    LINK THE OUTPUTS TO THE CHANGE IN FROG ORIENTATION
    
    '''