"""
Compute FBs form Hamiltonian (hourglass model).

Parameters:
  k   - Momentum
  f   - Variable parameter
  f_i - Parameter mode selection (1, 2, 3, or 4)
Returns:
  H   - 4×4 Hamiltonian matrix
"""

import numpy as np


def computeFBsHamiltonian(k, f, f_i):
    a = 1/2
    t = 8
    
    A = np.array([
        [f, 2, 2, 2],
        [2, f, 2, 2],
        [2, 2, f, 2],
        [2, 2, 2, f]
    ])
    
    u = A[f_i - 1, 0]  # Python indexing starts from 0
    v = A[f_i - 1, 1]
    t_1 = A[f_i - 1, 2]
    t_3 = A[f_i - 1, 3]
    
    a_1 = u + v * np.cos(2 * k * a)
    a_2 = -v * np.sin(2 * k * a)
    b_1 = t_1 + t_3 * np.cos(2 * k * a)
    b_2 = -t_3 * np.sin(2 * k * a)
    
    H = np.array([
        [-a_2,    b_1,     a_1,    b_2 - t],
        [b_1,    a_2,  b_2 + t,    -a_1],
        [a_1, b_2 + t,     a_2,    -b_1],
        [b_2 - t,   -a_1,    -b_1,    -a_2]
    ])
    
    return H

