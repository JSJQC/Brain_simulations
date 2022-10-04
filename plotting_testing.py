# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 15:10:10 2022

@author: jakes
"""

import brain_function as bf
import frog

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

boi_e = frog.Frog('example', [11, 11])
boi_t = frog.Frog('turning', [6, 13])


print ()
print (boi_t.type_layer)
print ()

fig, ax = plt.subplots()

cmp = colors.ListedColormap(['dimgray', 'gray', 'black'])
bounds=[0, 41, 121, 1000]
norm = colors.BoundaryNorm(bounds, cmp.N)

#img = ax.imshow(type_layer, cmap = 'gray', interpolation = 'nearest')
img = ax.imshow(boi_t.type_layer, cmap = cmp, norm=norm, interpolation = 'nearest')
plt.show()

fig, ax = plt.subplots()

cmp = colors.ListedColormap(['dimgray', 'white', 'gray', 'white', 'black', 'white'])
bounds=[0, 41, 111, 121, 179, 1000, 1071]
norm = colors.BoundaryNorm(bounds, cmp.N)

#img = ax.imshow(type_layer, cmap = 'gray', interpolation = 'nearest')
img = ax.imshow(boi_t.type_layer + boi_t.impulse_layer, cmap = cmp, norm=norm, interpolation = 'nearest')
plt.show()