"""
NATI System: Non-Abelian Topological Charge Calculation

Computes non-Abelian connection A_k^{ij} = <u_i(k)|∂_k|u_j(k)> and 
topological charge C = P exp(∮ A_k dk) via path-ordered integral.

Model: NATI Hamiltonian (4×4 matrix)
Parameters: t1=2, t2=3.1, t3=3, t4=6, t0=15, u=4, v ∈ [0, 6]
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import expm
import sys
import os

script_path = os.path.dirname(os.path.abspath(__file__))
function_path = os.path.join(os.path.dirname(script_path), 'Function')
sys.path.append(function_path)

from computeNATIHamiltonian import computeNATIHamiltonian
from computeTijMatrices import computeTijMatrices


def main():
    print('Generating Figure 6: Charge and Euler Connection...')
    
    N_k = 2000  # Momentum space sampling points
    n = 4  # System dimension (4 bands)
    
    t1 = 2
    t2 = 3.1
    t3 = 3
    t4 = 6
    t0 = 15
    u = 4
    
    v_min = 0
    v_max = 6
    v_ref = 4  # Reference v for band structure and topological charge
    
    N_v = 61
    v_values = np.linspace(v_min, v_max, N_v)
    a = 1/2  # Lattice constant
    delta = 1e-6  # Offset to avoid singularities at k=±π
    
    eigenvalues_all = np.zeros((n, N_k, N_v))
    eigenvectors_all = np.zeros((n, n, N_k, N_v), dtype=complex)
    EulerConnection_all = np.zeros((n, n, N_v), dtype=complex)
    
    # Calculate spin(4) Lie algebra generators t_{ij} = -1/4 [Γ_i, Γ_j]
    tij = computeTijMatrices()
    
    k_values = -np.pi + delta + np.arange(N_k) / (N_k - 1) * (2 * np.pi - 2 * delta)
    delta_k = (2 * np.pi - 2 * delta) / (N_k - 1)
    
    print(f'Calculating band structure and Euler connection for {N_v} v values...')
    for v_idx in range(N_v):
        v = v_values[v_idx]
        
        eigenvalues = np.zeros((n, N_k))
        eigenvectors = np.zeros((n, n, N_k), dtype=complex)
        Ak = np.zeros((n, n, N_k), dtype=complex)
        B = np.zeros((n, n), dtype=complex)
        
        # Calculate band structure and eigenvectors with gauge fixing
        for k_idx in range(N_k):
            k = k_values[k_idx]
            H = computeNATIHamiltonian(k, t1, t2, t3, t4, t0, u, v, a)
            eigvals, M = np.linalg.eigh(H)
            
            sort_idx = np.argsort(eigvals)
            E = eigvals[sort_idx]
            eigenvalues[:, k_idx] = E
            
            # Gauge fixing: ensure eigenvector continuity
            for band_idx in range(n):
                orig_band_idx = sort_idx[band_idx]
                if k_idx == 0:
                    eigenvectors[:, band_idx, k_idx] = np.sign(M[0, orig_band_idx].real) * M[:, orig_band_idx]
                else:
                    overlap = eigenvectors[:, band_idx, k_idx-1].conj() @ M[:, orig_band_idx]
                    eigenvectors[:, band_idx, k_idx] = np.sign(overlap.real) * M[:, orig_band_idx]
        
        eigenvalues_all[:, :, v_idx] = eigenvalues
        eigenvectors_all[:, :, :, v_idx] = eigenvectors
        
        # Calculate non-Abelian connection A_k^{ij} = <u_i(k)|∂_k|u_j(k)>
        for k_idx in range(1, N_k - 1):
            for i in range(n):
                for j in range(n):
                    u_j_forward = eigenvectors[:, j, k_idx + 1]
                    u_j_backward = eigenvectors[:, j, k_idx - 1]
                    partial_k_u_j = (u_j_forward - u_j_backward) / (2 * delta_k)
                    Ak[i, j, k_idx] = eigenvectors[:, i, k_idx].conj() @ partial_k_u_j
            
            B = B + Ak[:, :, k_idx] * delta_k
        
        EulerConnection_all[:, :, v_idx] = B / np.pi
        
        if (v_idx + 1) % 10 == 0 or v_idx == 0 or v_idx == N_v - 1:
            print(f'  Progress: v = {v:.2f} ({v_idx+1}/{N_v})')
    
    print('Band structure calculation completed.')
    
    v_ref_idx = np.where(np.abs(v_values - v_ref) < 1e-6)[0]
    if len(v_ref_idx) == 0:
        v_ref_idx = int(np.round((v_ref - v_min) / (v_max - v_min) * (N_v - 1)))
    else:
        v_ref_idx = v_ref_idx[0]
    eigenvalues_ref = eigenvalues_all[:, :, v_ref_idx]
    
    fig = plt.figure(figsize=(10, 10))
    plt.plot(k_values/np.pi, np.flip(eigenvalues_ref[0, :])/np.pi, 'r.', markersize=4, label='Band 1')
    plt.plot(k_values/np.pi, np.flip(eigenvalues_ref[1, :])/np.pi, 'g.', markersize=4, label='Band 2')
    plt.plot(k_values/np.pi, np.flip(eigenvalues_ref[2, :])/np.pi, 'b.', markersize=4, label='Band 3')
    plt.plot(k_values/np.pi, np.flip(eigenvalues_ref[3, :])/np.pi, 'k.', markersize=4, label='Band 4')
    plt.xlabel('k / π')
    plt.ylabel('E / π')
    plt.title(f'Band Structure (t1={t1:.1f}, t2={t2:.1f}, t3={t3:.1f}, t4={t4:.1f}, t0={t0:.1f}, u={u:.1f}, v={v_values[v_ref_idx]:.1f})')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show(block=False)
    
    K_mesh, V_mesh = np.meshgrid(k_values/np.pi, v_values)
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Define colors
    band_colors = ['r', 'g', 'b', 'k']  # Red, green, blue, black
    band_labels = ['Band 1', 'Band 2', 'Band 3', 'Band 4']
    
    for band_idx in range(n):
        # Extract all data for current band
        E_band = eigenvalues_all[band_idx, :, :] / np.pi  # [N_k, N_v]
        E_band = np.flip(E_band, axis=0)  # Flip k direction
        
        # Plot 3D surface with different colors
        ax.plot_surface(K_mesh, V_mesh, E_band.T, alpha=0.7, 
                       color=band_colors[band_idx], label=band_labels[band_idx])
    
    ax.set_xlabel('$k / \pi$', fontsize=14)
    ax.set_ylabel('$v$', fontsize=14)
    ax.set_zlabel('$E / \pi$', fontsize=14)
    ax.set_title('3D Band Structure: $E$ vs $v$ vs $k$', fontsize=16)
    ax.view_init(30, 45)
    plt.show(block=False)
    
    # Calculate non-Abelian topological charge C = P exp(∮ A_k dk)
    eigenvectors_ref = eigenvectors_all[:, :, :, v_ref_idx]
    Ak = np.zeros((n, n, N_k), dtype=complex)
    Ak2 = np.zeros((4, 4, N_k), dtype=complex)
    C = np.eye(n, dtype=complex)
    
    for k_idx in range(1, N_k - 1):
        for i in range(n):
            for j in range(n):
                u_j_forward = eigenvectors_ref[:, j, k_idx + 1]
                u_j_backward = eigenvectors_ref[:, j, k_idx - 1]
                partial_k_u_j = (u_j_forward - u_j_backward) / (2 * delta_k)
                Ak[i, j, k_idx] = eigenvectors_ref[:, i, k_idx].conj() @ partial_k_u_j
        
        # Expand to spin(4) Lie algebra form
        Ak2[:, :, k_idx] = (Ak[0, 1, k_idx] * tij['t12'] +
                           Ak[0, 2, k_idx] * tij['t13'] +
                           Ak[0, 3, k_idx] * tij['t14'] +
                           Ak[1, 2, k_idx] * tij['t23'] +
                           Ak[1, 3, k_idx] * tij['t24'] +
                           Ak[2, 3, k_idx] * tij['t34'])
        
        C = expm(Ak2[:, :, k_idx] * delta_k) @ C
    
    EulerConnection = EulerConnection_all[:, :, v_ref_idx]
    
    print('\nNon-Abelian Topological Charge Matrix C:')
    print(C)
    
    print('\nEuler Connection Matrix (normalized to π):')
    print(EulerConnection)
    
    labels = ['21', '31', '32', '41', '42', '43']
    markers = ['o', '+', '*', 'x', 's', 'd']
    marker_sizes = [5, 6, 7, 8, 5, 6]
    colors = plt.cm.tab10(np.linspace(0, 1, 6))
    
    fig = plt.figure(figsize=(10, 10))
    count = 0
    for row in range(4):
        for col in range(row):  # Lower triangle: col < row
            count += 1
            Euler_ij = EulerConnection_all[row, col, :]
            plt.plot(v_values, Euler_ij.real, marker=markers[count-1],
                    markersize=marker_sizes[count-1], color=colors[count-1],
                    linestyle='-', linewidth=1.5,
                    label=f'$\\gamma_{{{labels[count-1]}}}$')
    
    plt.xlabel('$v$', fontsize=14)
    plt.ylabel('Euler Connection / $\\pi$', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True)
    plt.show(block=False)
    
    k_plot = k_values[1:N_k-1]
    
    Ak_plot = np.zeros((n, n, N_k), dtype=complex)
    for k_idx in range(1, N_k - 1):
        for i in range(n):
            for j in range(n):
                u_j_forward = eigenvectors_ref[:, j, k_idx + 1]
                u_j_backward = eigenvectors_ref[:, j, k_idx - 1]
                partial_k_u_j = (u_j_forward - u_j_backward) / (2 * delta_k)
                Ak_plot[i, j, k_idx] = eigenvectors_ref[:, i, k_idx].conj() @ partial_k_u_j
    
    fig = plt.figure(figsize=(10, 10))
    
    labels_upper = ['11', '12', '13', '14', '22', '23', '24', '33', '34', '44']
    markers_upper = ['o', '+', '*', 'x', 's', 'd', '^', 'v', '>', '<']
    marker_sizes_upper = [5, 6, 7, 8, 5, 6, 7, 8, 5, 6]
    colors_upper = plt.cm.tab10(np.linspace(0, 1, 10))
    
    Ak_evolution = np.zeros((10, N_k - 2), dtype=complex)
    count = 0
    for row in range(4):
        for col in range(row, 4):
            count += 1
            Ak_evolution[count - 1, :] = Ak_plot[row, col, 1:N_k-1]
    
    plt.subplot(2, 1, 1)
    for count in range(10):
        plt.plot(k_plot/np.pi, Ak_evolution[count, :].real, marker=markers_upper[count],
                markersize=marker_sizes_upper[count], color=colors_upper[count],
                linestyle='-', linewidth=1.5, label=f'A_{{{labels_upper[count]}}}')
    plt.xlabel('$k / \pi$', fontsize=12)
    plt.ylabel('$A_k^{ij}$', fontsize=12)
    plt.title('Euler Connection Matrix Elements $A_k^{ij}$ vs $k$', fontsize=12)
    plt.legend(loc='best', fontsize=9)
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    B_cumulative = np.zeros((n, n, N_k - 2), dtype=complex)
    B_temp = np.zeros((n, n), dtype=complex)
    for k_idx in range(1, N_k - 1):
        B_temp = B_temp + Ak_plot[:, :, k_idx] * delta_k
        B_cumulative[:, :, k_idx - 1] = B_temp / np.pi
    
    count = 0
    for row in range(4):
        for col in range(row, 4):
            count += 1
            B_ij = B_cumulative[row, col, :]
            plt.plot(k_plot/np.pi, B_ij.real, marker=markers_upper[count-1],
                    markersize=marker_sizes_upper[count-1], color=colors_upper[count-1],
                    linestyle='-', linewidth=1.5,
                    label=f'$\\int A_{{{labels_upper[count-1]}}} dk / \\pi$')
    
    plt.xlabel('$k / \pi$', fontsize=12)
    plt.ylabel('Cumulative Integral / $\\pi$', fontsize=12)
    plt.title('Euler Connection: Cumulative Integral (Normalized by $\\pi$)', fontsize=12)
    plt.legend(loc='best', fontsize=9)
    plt.grid(True)
    plt.tight_layout(pad=2.0)
    plt.show(block=False)
    
    fig = plt.figure(figsize=(10, 10))
    
    num_rows = 2
    num_cols = 3
    count = 0
    
    lower_tri_pairs = [(2, 1), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3)]
    
    for pair_idx, (row, col) in enumerate(lower_tri_pairs):
        count += 1
        row_idx = row - 1
        col_idx = col - 1
        
        plt.subplot(num_rows, num_cols, count)
        Ak_ij = Ak_plot[row_idx, col_idx, 1:N_k-1]
        plt.plot(k_plot/np.pi, Ak_ij.real, marker=markers_upper[min(count-1, 9)],
                markersize=4, color=colors_upper[min(count-1, 9)],
                linestyle='-', linewidth=1.2)
        plt.grid(True)
        plt.title(f'$A_k^{{{row}{col}}}$', fontsize=10)
        plt.xlabel('$k / \pi$', fontsize=9)
        plt.ylabel('Value', fontsize=9)
        plt.tick_params(labelsize=8)
    
    plt.suptitle('Euler Connection Matrix Elements $A_k^{ij}$ - Lower Triangle', fontsize=11)
    plt.tight_layout(pad=2.0)
    plt.show(block=False)
    
    uk1 = np.zeros((4, N_k))
    uk2 = np.zeros((4, N_k))
    uk3 = np.zeros((4, N_k))
    uk4 = np.zeros((4, N_k))
    
    for band_idx in range(4):
        uk1[band_idx, :] = np.real(eigenvectors_ref[0, band_idx, :])
        uk2[band_idx, :] = np.real(eigenvectors_ref[1, band_idx, :])
        uk3[band_idx, :] = np.real(eigenvectors_ref[2, band_idx, :])
        uk4[band_idx, :] = np.real(eigenvectors_ref[3, band_idx, :])
    
    fig = plt.figure(figsize=(10, 10))
    
    band_colors = ['r', 'g', 'b', 'k']
    
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    for band_idx in range(4):
        ax1.scatter(uk1[band_idx, :], uk2[band_idx, :], uk3[band_idx, :],
                   s=8, c=band_colors[band_idx], alpha=0.6)
    ax1.scatter([0], [0], [0], s=100, c='k', marker='d')
    ax1.set_xlabel('$u_1$', fontsize=14)
    ax1.set_ylabel('$u_2$', fontsize=14)
    ax1.set_zlabel('$u_3$', fontsize=14)
    ax1.view_init(30, 45)
    xlims = ax1.get_xlim()
    ylims = ax1.get_ylim()
    zlims = ax1.get_zlim()
    ax1.text(xlims[0]*0.95, ylims[1]*0.95, zlims[1]*0.95, '(a)',
            fontsize=14, fontweight='bold', verticalalignment='top', horizontalalignment='left')
    
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    for band_idx in range(4):
        ax2.scatter(uk1[band_idx, :], uk2[band_idx, :], uk4[band_idx, :],
                   s=8, c=band_colors[band_idx], alpha=0.6)
    ax2.scatter([0], [0], [0], s=100, c='k', marker='d')
    ax2.set_xlabel('$u_1$', fontsize=14)
    ax2.set_ylabel('$u_2$', fontsize=14)
    ax2.set_zlabel('$u_4$', fontsize=14)
    ax2.view_init(30, 45)
    xlims = ax2.get_xlim()
    ylims = ax2.get_ylim()
    zlims = ax2.get_zlim()
    ax2.text(xlims[0]*0.95, ylims[1]*0.95, zlims[1]*0.95, '(b)',
            fontsize=14, fontweight='bold', verticalalignment='top', horizontalalignment='left')
    
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    for band_idx in range(4):
        ax3.scatter(uk1[band_idx, :], uk3[band_idx, :], uk4[band_idx, :],
                   s=8, c=band_colors[band_idx], alpha=0.6)
    ax3.scatter([0], [0], [0], s=100, c='k', marker='d')
    ax3.set_xlabel('$u_1$', fontsize=14)
    ax3.set_ylabel('$u_3$', fontsize=14)
    ax3.set_zlabel('$u_4$', fontsize=14)
    ax3.view_init(30, 45)
    xlims = ax3.get_xlim()
    ylims = ax3.get_ylim()
    zlims = ax3.get_zlim()
    ax3.text(xlims[0]*0.95, ylims[1]*0.95, zlims[1]*0.95, '(c)',
            fontsize=14, fontweight='bold', verticalalignment='top', horizontalalignment='left')
    
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    for band_idx in range(4):
        ax4.scatter(uk2[band_idx, :], uk3[band_idx, :], uk4[band_idx, :],
                   s=8, c=band_colors[band_idx], alpha=0.6)
    ax4.scatter([0], [0], [0], s=100, c='k', marker='d')
    ax4.set_xlabel('$u_2$', fontsize=14)
    ax4.set_ylabel('$u_3$', fontsize=14)
    ax4.set_zlabel('$u_4$', fontsize=14)
    ax4.view_init(30, 45)
    xlims = ax4.get_xlim()
    ylims = ax4.get_ylim()
    zlims = ax4.get_zlim()
    ax4.text(xlims[0]*0.95, ylims[1]*0.95, zlims[1]*0.95, '(d)',
            fontsize=14, fontweight='bold', verticalalignment='top', horizontalalignment='left')
    
    plt.suptitle(f'Eigenstate Rotation in 3D Space (v={v_values[v_ref_idx]:.1f})', fontsize=14)
    plt.tight_layout(pad=2.0)
    plt.show(block=False)
    
    print('\nFigure 6 completed.')


if __name__ == '__main__':
    main()

