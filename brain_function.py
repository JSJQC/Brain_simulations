# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 17:58:54 2022

@author: jakes

From geeksforgeeks
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 70
OFF = 0
REFR = 4
vals = [ON, OFF]

def random_impulse_layer(N):
    
    return np.random.choice(vals, N*N, p = [0.2, 0.8]).reshape(N, N)

def empty_impulse_layer(N):
    
    ## Will apply the starting impulse after to this
    
    return np.full((N, N), OFF)

def initial_ticks(N):
    
    return np.full((N, N), 0)

def example_impulse_layer(empty_layer):
    
    c = empty_layer.copy()
    
    c[10, 3] = ON
    c[10, 7] = ON
    
    print ()
    print (c)
    print ()
    
    return c

def example_type_layer():
    
    ## An 11 x 11 example grid, as drawn on the planning sheet
    
    NERVE = 40
    TWO_JUNCTION = 100
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
    
    print ()
    print (grid)
    print ()
    
    return grid
    
    
def update(frameNum, img, impulse_layer, tick_layer, type_layer, N):
    
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
            
            if impulse_layer[i, j] == ON: # cells currently only hold charge for one tick
                new_impulse[i, j] = OFF
                new_tick[i, j] = REFR
                    
            else:
                if tick_layer[i, j] == 0:
                    if total >= type_layer[i, j]:
                        new_impulse[i, j] = ON
                else:
                    new_tick[i, j] = tick_layer[i, j] - 1
                    
    img.set_data(new_impulse)
    impulse_layer[:] = new_impulse[:]
    tick_layer[:] = new_tick[:]
    return img,


def main(N, movfile, interval):

    updateInterval = int(interval)

    empty_layer = empty_impulse_layer(N)
    impulse_layer = example_impulse_layer(empty_layer)
    type_layer = example_type_layer()
    tick_layer = initial_ticks(N)
        
    ## Animation
    
    fig, ax = plt.subplots()
    img = ax.imshow(impulse_layer, cmap = 'gray', interpolation = 'nearest')
    #img = ax.imshow(type_layer, interpolation = 'nearest') ## Shows the type layout
    ani = animation.FuncAnimation(fig, update, fargs = (img, impulse_layer, tick_layer, type_layer, N, ),
                                  frames = 10,
                                  interval = updateInterval,
                                  save_count = 50)
    
    fig.set_size_inches(N, N, True)
    ani.save(movfile, fps = 2) #, extra_args = ['-vcodec', 'libx2645'])
        
    plt.show()
    
if __name__ == "__main__":
    main(11, 'example.gif', 1000)
    
    
