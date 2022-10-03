# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 15:10:10 2022

@author: jakes
"""

import brain_function as bf

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

type_layer = bf.example_type_layer()

print ()
print (type_layer)
print ()

fig, ax = plt.subplots()

cmp = colors.ListedColormap(['dimgray', 'gray', 'black'])
bounds=[0, 41, 121, 1000]
norm = colors.BoundaryNorm(bounds, cmp.N)

#img = ax.imshow(type_layer, cmap = 'gray', interpolation = 'nearest')
img = ax.imshow(type_layer, cmap = cmp, norm=norm, interpolation = 'nearest')
plt.show()


empty_layer = bf.empty_impulse_layer(11)
impulse_layer = bf.example_impulse_layer(empty_layer)

fig, ax = plt.subplots()

cmp = colors.ListedColormap(['dimgray', 'white', 'gray', 'white', 'black', 'white'])
bounds=[0, 41, 111, 121, 179, 1000, 1071]
norm = colors.BoundaryNorm(bounds, cmp.N)

#img = ax.imshow(type_layer, cmap = 'gray', interpolation = 'nearest')
img = ax.imshow(type_layer + impulse_layer, cmap = cmp, norm=norm, interpolation = 'nearest')
plt.show()