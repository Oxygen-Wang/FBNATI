"""
NATI System: Eigenstate Mode Visualization

Computes eigenstates and eigenvalues, visualizes spatial distribution and energy spectrum.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time

script_path = os.path.dirname(os.path.abspath(__file__))
function_path = os.path.join(os.path.dirname(script_path), 'Function')
sys.path.append(function_path)

from computeRealSpaceHamiltonian import computeRealSpaceHamiltonian


def main():
    print('Generating Figure 3: Eigenstate Mode...')
    
    start_time = time.time()
    
    N = 20  # Number of unit cells
    fi = 2  # Parameter index
    f = 4   # Parameter f
    t = 8   # Parameter t
    
    H1, H2 = computeRealSpaceHamiltonian(N, fi, f, t)
    H = H1 + H2
    
    eigvals, M = np.linalg.eigh(H)
    E = np.sort(eigvals)
    P = np.argsort(eigvals)
    
    # Eigenstate spatial distribution: |ψ|² at each position
    Psi2 = np.zeros((2*N, 4*N))
    for idx in range(4*N):
        eigen_idx = P[idx]
        Psi2[:, idx] = np.abs(M[0::2, eigen_idx])**2 + np.abs(M[1::2, eigen_idx])**2
    
    X = np.arange(1, 4*N + 1)
    X2 = np.arange(1, 2*N + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    
    max_color_value = 200
    acolor = np.column_stack([
        np.exp(5 * (np.linspace(0, 0.1, 200) - 1)),
        np.exp(5 * (np.linspace(0.2, 1, 200) - 1)),
        np.linspace(0.6, 1, 200)
    ])
    jet_color = np.flipud(acolor)
    
    color_indices = np.ceil(Psi2 * 200).astype(int)
    color_indices = np.clip(color_indices, 1, max_color_value)
    selected_colors = jet_color[color_indices - 1, :]
    
    for eigen_idx in range(4*N):
        for pos in range(2*N):
            color = selected_colors[pos, eigen_idx]
            ax1.scatter(X2[pos], E[eigen_idx], s=36, 
                       c=[color], 
                       marker='s', edgecolors='none')
    
    ax1.set_xlabel('Position', fontsize=14)
    ax1.set_ylabel('$E$', fontsize=14)
    ax1.set_title('Eigenstate Spatial Distribution', fontsize=12)
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.colors.ListedColormap(jet_color)), ax=ax1)
    
    ax2.plot(X, E, 'bo', markerfacecolor='b', markersize=3)
    ax2.set_xlabel('Eigenstate index', fontsize=14)
    ax2.set_ylabel('$E$', fontsize=14)
    ax2.grid(True)
    
    plt.tight_layout(pad=2.0)
    plt.show(block=False)
    
    elapsed_time = time.time() - start_time
    print(f'Figure 3 completed. Time: {elapsed_time:.2f} seconds')


if __name__ == '__main__':
    main()

