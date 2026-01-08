"""
Compute spin(4) Lie algebra generators t_{ij} = -1/4 [Γ_i, Γ_j]

Returns:
  tij - Dictionary containing all t_{ij} matrices (i < j)
        tij['t12'], tij['t13'], tij['t14'], tij['t23'], tij['t24'], tij['t34']

According to paper definition:
  Γ_1 = -σ₂ ⊗ σ₁
  Γ_2 = -σ₂ ⊗ σ₂
  Γ_3 = -σ₂ ⊗ σ₃
  Γ_4 = σ₁ ⊗ σ₀
  t_{ij} = -1/4 [Γ_i, Γ_j] = -1/4 (Γ_i Γ_j - Γ_j Γ_i)
"""

import numpy as np


def computeTijMatrices():
    # Define Pauli matrices
    sigma0 = np.eye(2)
    sigma1 = np.array([[0, 1], [1, 0]])
    sigma2 = np.array([[0, -1j], [1j, 0]])
    sigma3 = np.array([[1, 0], [0, -1]])
    
    # Define Gamma matrices
    Gamma1 = -np.kron(sigma2, sigma1)  # -σ₂ ⊗ σ₁
    Gamma2 = -np.kron(sigma2, sigma2)  # -σ₂ ⊗ σ₂
    Gamma3 = -np.kron(sigma2, sigma3)  # -σ₂ ⊗ σ₃
    Gamma4 = np.kron(sigma1, sigma0)   # σ₁ ⊗ σ₀
    
    # Compute t_{ij} = -1/4 [Γ_i, Γ_j]
    # Commutator [A, B] = AB - BA
    tij = {}
    tij['t12'] = -1/4 * (Gamma1 @ Gamma2 - Gamma2 @ Gamma1)
    tij['t13'] = -1/4 * (Gamma1 @ Gamma3 - Gamma3 @ Gamma1)
    tij['t14'] = -1/4 * (Gamma1 @ Gamma4 - Gamma4 @ Gamma1)
    tij['t23'] = -1/4 * (Gamma2 @ Gamma3 - Gamma3 @ Gamma2)
    tij['t24'] = -1/4 * (Gamma2 @ Gamma4 - Gamma4 @ Gamma2)
    tij['t34'] = -1/4 * (Gamma3 @ Gamma4 - Gamma4 @ Gamma3)
    
    return tij

