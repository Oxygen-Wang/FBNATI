"""
Four-Dimensional SSH and Ladder Model: Eigenstate Rotation Visualization

Ladder model: t1=1, t2=3.5, t3=3, t4=6, t0=15, u=4, v=4
Visualizes eigenstate rotation in 3D space.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os

script_path = os.path.dirname(os.path.abspath(__file__))
function_path = os.path.join(os.path.dirname(script_path), 'Function')
sys.path.append(function_path)

from computeNATIHamiltonian import computeNATIHamiltonian


def main():
    print('Generating Figure 6: Eigenstate Rotation...')
    
    Nk = 400
    a = 1/2
    delta = 1e-6
    k = np.linspace(-np.pi + delta, np.pi - delta, Nk)
    dk = 2 * np.pi / Nk
    
    t1 = 1
    t2 = 3.5
    t3 = 3
    t4 = 6
    t0 = 15
    u = 4
    v1 = 4
    
    eigenvectors_Ladder1 = np.zeros((4, 4, Nk), dtype=complex)
    eigenvalues_Ladder1 = np.zeros((4, Nk))
    
    # Calculate eigenstates with gauge fixing
    for ik in range(Nk):
        H = computeNATIHamiltonian(k[ik], t1, t2, t3, t4, t0, u, v1, a)
        
        eigvals, M = np.linalg.eigh(H)
        eigenvalues_Ladder1[:, ik] = np.real(eigvals)
        
        sort_idx = np.argsort(np.real(eigenvalues_Ladder1[:, ik]))
        E_sorted = eigenvalues_Ladder1[sort_idx, ik]
        eigenvalues_Ladder1[:, ik] = E_sorted
        
        for band_idx in range(4):
            eigen_idx = sort_idx[band_idx]
            if ik == 0:
                eigenvectors_Ladder1[:, band_idx, ik] = np.sign(M[0, eigen_idx].real) * M[:, eigen_idx]
            else:
                overlap = eigenvectors_Ladder1[:, band_idx, ik-1].conj() @ M[:, eigen_idx]
                eigenvectors_Ladder1[:, band_idx, ik] = np.sign(overlap.real) * M[:, eigen_idx]
    
    fig = plt.figure(figsize=(10, 10))
    
    colors = ['b-', 'r-', 'g-', 'm-']
    for band_idx in range(4):
        plt.plot(k/np.pi, eigenvalues_Ladder1[band_idx, :], colors[band_idx], linewidth=2, label=f'Band {band_idx+1}')
    
    plt.xlabel('$k/\\pi$', fontsize=14)
    plt.ylabel('$E$', fontsize=14)
    plt.title('Ladder Model Band Structure (v=4)', fontsize=12)
    plt.grid(True)
    plt.legend(loc='best', fontsize=10)
    plt.tick_params(labelsize=12)
    plt.show(block=False)
    
    fig = plt.figure(figsize=(10, 10))
    
    uk1_Ladder = np.zeros((4, Nk))
    uk2_Ladder = np.zeros((4, Nk))
    uk3_Ladder = np.zeros((4, Nk))
    uk4_Ladder = np.zeros((4, Nk))
    
    for band_idx in range(4):
        uk1_Ladder[band_idx, :] = np.real(eigenvectors_Ladder1[0, band_idx, :])
        uk2_Ladder[band_idx, :] = np.real(eigenvectors_Ladder1[1, band_idx, :])
        uk3_Ladder[band_idx, :] = np.real(eigenvectors_Ladder1[2, band_idx, :])
        uk4_Ladder[band_idx, :] = np.real(eigenvectors_Ladder1[3, band_idx, :])
    
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    for band_idx in range(4):
        ax1.scatter(uk1_Ladder[band_idx, :], uk2_Ladder[band_idx, :], uk3_Ladder[band_idx, :],
                   s=3, alpha=0.6)
    ax1.scatter([0], [0], [0], s=100, c='k', marker='d')
    ax1.set_xlabel('$u_1$', fontsize=12)
    ax1.set_ylabel('$u_2$', fontsize=12)
    ax1.set_zlabel('$u_3$', fontsize=12)
    ax1.view_init(30, 45)
    xlims = ax1.get_xlim()
    ylims = ax1.get_ylim()
    zlims = ax1.get_zlim()
    ax1.text(xlims[0]*0.95, ylims[1]*0.95, zlims[1]*0.95, '(a)',
            fontsize=12, fontweight='bold', verticalalignment='top', horizontalalignment='left')
    
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    for band_idx in range(4):
        ax2.scatter(uk1_Ladder[band_idx, :], uk2_Ladder[band_idx, :], uk4_Ladder[band_idx, :],
                   s=3, alpha=0.6)
    ax2.scatter([0], [0], [0], s=100, c='k', marker='d')
    ax2.set_xlabel('$u_1$', fontsize=12)
    ax2.set_ylabel('$u_2$', fontsize=12)
    ax2.set_zlabel('$u_4$', fontsize=12)
    ax2.view_init(30, 45)
    xlims = ax2.get_xlim()
    ylims = ax2.get_ylim()
    zlims = ax2.get_zlim()
    ax2.text(xlims[0]*0.95, ylims[1]*0.95, zlims[1]*0.95, '(b)',
            fontsize=12, fontweight='bold', verticalalignment='top', horizontalalignment='left')
    
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    for band_idx in range(4):
        ax3.scatter(uk1_Ladder[band_idx, :], uk3_Ladder[band_idx, :], uk4_Ladder[band_idx, :],
                   s=3, alpha=0.6)
    ax3.scatter([0], [0], [0], s=100, c='k', marker='d')
    ax3.set_xlabel('$u_1$', fontsize=12)
    ax3.set_ylabel('$u_3$', fontsize=12)
    ax3.set_zlabel('$u_4$', fontsize=12)
    ax3.view_init(30, 45)
    xlims = ax3.get_xlim()
    ylims = ax3.get_ylim()
    zlims = ax3.get_zlim()
    ax3.text(xlims[0]*0.95, ylims[1]*0.95, zlims[1]*0.95, '(c)',
            fontsize=12, fontweight='bold', verticalalignment='top', horizontalalignment='left')
    
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    for band_idx in range(4):
        ax4.scatter(uk2_Ladder[band_idx, :], uk3_Ladder[band_idx, :], uk4_Ladder[band_idx, :],
                   s=3, alpha=0.6)
    ax4.scatter([0], [0], [0], s=100, c='k', marker='d')
    ax4.set_xlabel('$u_2$', fontsize=12)
    ax4.set_ylabel('$u_3$', fontsize=12)
    ax4.set_zlabel('$u_4$', fontsize=12)
    ax4.view_init(30, 45)
    xlims = ax4.get_xlim()
    ylims = ax4.get_ylim()
    zlims = ax4.get_zlim()
    ax4.text(xlims[0]*0.95, ylims[1]*0.95, zlims[1]*0.95, '(d)',
            fontsize=12, fontweight='bold', verticalalignment='top', horizontalalignment='left')
    
    plt.tight_layout(pad=2.0)
    plt.show(block=False)
    
    print('\nFigure 6 (Eigenstate Rotation) completed.')


if __name__ == '__main__':
    main()

