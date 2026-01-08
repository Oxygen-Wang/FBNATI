"""
Compute 4D SSH model Hamiltonian (direct sum of two SSH models).

Parameters:
  k  - Momentum
  t1 - Intra-chain hopping parameter
  t2 - Inter-chain hopping parameter
  a  - Lattice constant (optional, default=1)

Returns:
  H  - 4×4 SSH Hamiltonian matrix (direct sum of two 2×2 SSH models)

4D SSH Hamiltonian form:
  H = [H_SSH, 0; 0, H_SSH]
  where H_SSH = [0, t1 + t2*exp(-ika);
                 t1 + t2*exp(ika), 0]
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Function.computeSSHHamiltonian import computeSSHHamiltonian


def computeSSHHamiltonian4D(k, t1, t2, a=1):
    H_SSH_single = computeSSHHamiltonian(k, t1, t2, a)
    
    # Construct 4D SSH Hamiltonian (direct sum of two SSH models)
    H = np.block([
        [H_SSH_single, np.zeros((2, 2))],
        [np.zeros((2, 2)), H_SSH_single]
    ])
    
    return H

