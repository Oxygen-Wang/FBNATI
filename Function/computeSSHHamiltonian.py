"""
Compute SSH (Su-Schrieffer-Heeger) model Hamiltonian.

Parameters:
  k  - Momentum
  t1 - Intra-chain hopping parameter
  t2 - Inter-chain hopping parameter
  a  - Lattice constant (optional, default=1)

Returns:
  H  - 2×2 SSH Hamiltonian matrix

SSH Hamiltonian form:
  H(k) = [0, t1 + t2*exp(-ika);
          t1 + t2*exp(ika), 0]
"""

import numpy as np


def computeSSHHamiltonian(k, t1, t2, a=1):
    H = np.array([
        [0, t1 + t2 * np.exp(-1j * k * a)],
        [t1 + t2 * np.exp(1j * k * a), 0]
    ])
    return H

