"""
Compute NATI system Hamiltonian (real form after PT-symmetric transformation).

Parameters:
  k  - Momentum
  t1, t2, t3, t4 - Inter-chain hopping parameters
  t0 - Inter-chain hopping parameter t_0
  u, v - Intra-chain hopping parameters
  a  - Lattice constant

Returns:
  H  - 4×4 Hamiltonian matrix (real symmetric matrix)
"""

import numpy as np


def computeNATIHamiltonian(k, t1, t2, t3, t4, t0, u, v, a):
    a1 = u + v * np.cos(2 * k * a)
    a2 = -v * np.sin(2 * k * a)
    b1 = t1 + t4 * np.cos(2 * k * a)
    b2 = -t4 * np.sin(2 * k * a)
    c1 = t2 + t3 * np.cos(2 * k * a)
    c2 = -t3 * np.sin(2 * k * a)
    
    # Compute b_i^± = (b_i ± c_i) / 2
    b1_plus = (b1 + c1) / 2
    b1_minus = (b1 - c1) / 2
    b2_plus = (b2 + c2) / 2
    b2_minus = (b2 - c2) / 2
    
    # Construct transformed real Hamiltonian (according to paper formula)
    H = np.array([
        [-a2 + b1_minus,      b1_plus,              a1 + b2_minus,      b2_plus - t0],
        [b1_plus,             a2 + b1_minus,        b2_plus + t0,        -a1 + b2_minus],
        [a1 + b2_minus,       b2_plus + t0,          a2 - b1_minus,       -b1_plus],
        [b2_plus - t0,        -a1 + b2_minus,       -b1_plus,            -a2 - b1_minus]
    ])
    
    return H

