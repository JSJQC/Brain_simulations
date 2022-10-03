# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 17:58:54 2022

@author: jakes

From geeksforgeeks
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation

ON = 70
OFF = 0
REFR = 2
vals = [ON, OFF]

def random_impulse_layer(N):
    
    return np.random.choice(vals, N*N, p = [0.2, 0.8]).reshape(N, N)

def empty_impulse_layer(N):
    
    ## Will apply the starting impulse after to this
    
    return np.full((N, N), OFF)

def initial_ticks(N):
    
    return np.full((N, N), 0)

def example_control_layer(empty_layer):
    
    c = empty_layer.copy()
    
    c[10, 3] = ON
    c[10, 7] = ON
    
    return c

def example_type_layer():
    
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
    
    
def update(frameNum, img, impulse_layer, tick_layer, type_layer, control_layer, N):
    
    '''
    impulse_layer: carries the impulse values (the original "grid")
    tick_layer: contains integer refractory counters
    type_layer: holds activation level information (i.e. nerve vs ganglion)
    '''
    
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


def main(N, movfile, interval):

    updateInterval = int(interval)

    empty_layer = empty_impulse_layer(N)
    impulse_layer = empty_layer
    control_layer = example_control_layer(empty_layer)
    type_layer = example_type_layer()
    tick_layer = initial_ticks(N)
        
    ## Animation
    
    fig, ax = plt.subplots()
    #plt.gcf().text(0.9, 0.9, 'text', fontsize = 20)
    cmp = colors.ListedColormap(['dimgray', 'white', 'gray', 'white', 'black', 'white'])
    bounds = [ 0, 41, 111, 121, 191, 1000, 1071]
    norm = colors.BoundaryNorm(bounds, cmp.N)
    img = ax.imshow(impulse_layer + type_layer, cmap = cmp, norm = norm, interpolation = 'nearest')
    #img = ax.imshow(type_layer, interpolation = 'nearest') ## Shows the type layout
    ani = animation.FuncAnimation(fig, update, fargs = (img, impulse_layer, tick_layer, type_layer, control_layer, N, ),
                                  frames = 40,
                                  interval = updateInterval,
                                  save_count = 50)
    
    fig.set_size_inches(N, N, True)
    ani.save(movfile, fps = 3) #, extra_args = ['-vcodec', 'libx2645'])
        
    plt.show()
    
if __name__ == "__main__":
    main(11, 'example.gif', 1000)
    
    
