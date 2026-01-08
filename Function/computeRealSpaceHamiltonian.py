"""
Compute real space Hamiltonian forLadder model.

Parameters:
  R   - Number of unit cells
  f_i - Parameter index (1, 2, 3, or 4)
  f   - Variable parameter
  t   - Inter-chain hopping parameter
Returns:
  H1  - Intra-chain Hamiltonian matrix
  H2  - Inter-chain Hamiltonian matrix
"""

import numpy as np


def computeRealSpaceHamiltonian(R, f_i, f, t):
    N = 4 * R  # Number of atoms = 4 * number of unit cells
    
    H1 = np.zeros((N, N))
    H2 = np.zeros((N, N))
    
    A = np.array([
        [f, 2, 2, 2],
        [2, f, 2, 2],
        [2, 2, f, 2],
        [2, 2, 2, f]
    ])
    
    u = A[f_i - 1, 0]  # Python indexing starts from 0
    v = A[f_i - 1, 1]
    t_1 = A[f_i - 1, 2]
    t_2 = A[f_i - 1, 3]
    
    # Intra-chain H1
    for ii in range(1, R + 1):
        H1[4*ii-4, 4*ii-2] = u
        H1[4*ii-3, 4*ii-1] = u
    
    for ii in range(1, R):
        H1[4*ii-2, 4*ii] = v
        H1[4*ii-1, 4*ii+1] = v
    
    H1 = H1 + H1.T
    
    # Inter-chain H2
    for ii in range(N - 1):
        H2[ii, ii+1] = t
    
    for ii in range(1, R + 1):
        H2[4*ii-4, 4*ii-1] = t_1
        H2[4*ii-3, 4*ii-2] = t_1
    
    for ii in range(1, R):
        H2[4*ii-2, 4*ii+1] = t_2
        H2[4*ii-1, 4*ii] = t_2
    
    H2 = H2 + H2.T
    
    return H1, H2

