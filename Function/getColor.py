"""
Get color corresponding to a value.

Parameters:
  val - Value
Returns:
  clr - RGB color vector
"""

import numpy as np


def getColor(val):
    if val > 6:
        clr = np.array([0.5, 0, 1])
    elif val == 0:
        clr = np.array([1, 1, 1])
    elif val == 2:
        clr = np.array([0, 0, 0])
    elif val < 2:
        clr = np.array([0.2, 0.6, 1])
    elif val > 2:
        clr = np.array([1, 0.4, 0.4])
    else:
        clr = np.array([0.7, 0.7, 0.7])
    
    return clr

