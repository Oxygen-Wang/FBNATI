"""
NATI System: Path-Dependent Non-Abelian Topological Charge Calculation

Computes non-Abelian topological charge along different closed paths in parameter space.
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
from computeTijMatrices import computeTijMatrices
from generatePathPoints import generatePathPoints
from computePathCharge import computePathCharge
from plotPathFigure import plotPathFigure


def main():
    print('Generating Figure 6: Path-Dependent Charge...')
    
    t1 = 1
    t2 = 3.5
    t3 = 3
    t4 = 6
    t0 = 15
    u = 4
    a = 1/2
    
    n = 4
    N_points_per_segment = 200
    
    path1_direction = 1
    path2_direction = 1
    path3_direction = 1
    path4_direction = 1
    path5_direction = -1
    
    v_min_plot = 0
    v_max_plot = 8
    N_v_plot = 100
    N_k_plot = 100
    delta_k = 1e-6
    
    degeneracy_point1 = np.array([1.68, np.pi])
    degeneracy_point2 = np.array([1.68, -np.pi])
    degeneracy_point3 = np.array([2.73, 0])
    degeneracy_point4 = np.array([6.27, np.pi])
    degeneracy_point5 = np.array([6.27, -np.pi])
    
    path1_segments = np.array([
        [1, -4],
        [2, -4],
        [2, -2],
        [1, -2],
        [1, -4]
    ])
    
    path2_segments = np.array([
        [2, -4],
        [4, -4],
        [4, 4],
        [2, 4],
        [2, -4]
    ])
    
    path3_segments = np.array([
        [7, -4],
        [5, -4],
        [5, -2],
        [7, -2],
        [7, -4]
    ])
    
    path4_segments = np.array([
        [1, -4],
        [7, -4],
        [7, 4],
        [1, 4],
        [1, 3],
        [3, 3],
        [3, -3],
        [1, -3],
        [1, -4]
    ])
    
    path5_segments = np.array([
        [1, -4],
        [7, -4],
        [7, -2],
        [1, -2],
        [1, -4]
    ])
    
    tij = computeTijMatrices()
    
    v_values_plot = np.linspace(v_min_plot, v_max_plot, N_v_plot)
    k_values_plot = np.linspace(-np.pi + delta_k, np.pi - delta_k, N_k_plot)
    
    eigenvalues_3d = np.zeros((n, N_k_plot, N_v_plot))
    
    print(f'Calculating 3D band structure (v: [{v_min_plot:.1f}, {v_max_plot:.1f}], k: [-π, π])...')
    for v_idx in range(N_v_plot):
        v = v_values_plot[v_idx]
        
        if (v_idx + 1) % 20 == 0 or v_idx == 0:
            print(f'  Progress: v = {v:.2f} ({v_idx+1}/{N_v_plot})')
        
        for k_idx in range(N_k_plot):
            k = k_values_plot[k_idx]
            
            H = computeNATIHamiltonian(k, t1, t2, t3, t4, t0, u, v, a)
            
            eigvals, _ = np.linalg.eigh(H)
            
            E = np.sort(np.real(eigvals))[::-1]  # Sort descending
            eigenvalues_3d[:, k_idx, v_idx] = E
    
    K_mesh, V_mesh = np.meshgrid(k_values_plot/np.pi, v_values_plot)
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    band_colors = ['r', 'g', 'b', 'k']
    band_labels = ['Band 1', 'Band 2', 'Band 3', 'Band 4']
    
    for band_idx in range(n):
        E_band = eigenvalues_3d[band_idx, :, :] / np.pi
        E_band = np.flip(E_band, axis=0)
        
        ax.plot_surface(K_mesh, V_mesh, E_band.T, alpha=0.7,
                       color=band_colors[band_idx], label=band_labels[band_idx])
    
    ax.set_xlabel('$k / \pi$', fontsize=14)
    ax.set_ylabel('$v$', fontsize=14)
    ax.set_zlabel('$E / \pi$', fontsize=14)
    ax.set_title(f'3D Band Structure: $E$ vs $v$ vs $k$ (t1={t1:.1f}, t2={t2:.1f}, t3={t3:.1f}, t4={t4:.1f}, t0={t0:.1f}, u={u:.1f})', fontsize=16)
    ax.view_init(30, 45)
    plt.tight_layout(pad=2.0)
    plt.show(block=False)
    
    print('3D band structure plot completed.')
    
    # Compute paths
    path1_computed = False
    path2_computed = False
    path3_computed = False
    path4_computed = False
    path5_computed = False
    
    if 'path1_segments' in locals():
        print('Computing Path 1 topological charge...')
        path1_points_k, path1_points_knorm = generatePathPoints(path1_segments, N_points_per_segment, path1_direction)
        N_path1 = path1_points_k.shape[0]
        print(f'  Path 1: {N_path1} sampling points')
        
        C1, path1_info = computePathCharge(path1_points_k, t1, t2, t3, t4, t0, u, a, tij, n)
        path1_computed = True
    
    if 'path2_segments' in locals():
        print('Computing Path 2 topological charge...')
        path2_points_k, path2_points_knorm = generatePathPoints(path2_segments, N_points_per_segment, path2_direction)
        N_path2 = path2_points_k.shape[0]
        print(f'  Path 2: {N_path2} sampling points')
        
        C2, path2_info = computePathCharge(path2_points_k, t1, t2, t3, t4, t0, u, a, tij, n)
        path2_computed = True
    
    if 'path3_segments' in locals():
        print('Computing Path 3 topological charge...')
        path3_points_k, path3_points_knorm = generatePathPoints(path3_segments, N_points_per_segment, path3_direction)
        N_path3 = path3_points_k.shape[0]
        print(f'  Path 3: {N_path3} sampling points')
        
        C3, path3_info = computePathCharge(path3_points_k, t1, t2, t3, t4, t0, u, a, tij, n)
        path3_computed = True
    
    if 'path4_segments' in locals():
        print('Computing Path 4 topological charge...')
        path4_points_k, path4_points_knorm = generatePathPoints(path4_segments, N_points_per_segment, path4_direction)
        N_path4 = path4_points_k.shape[0]
        print(f'  Path 4: {N_path4} sampling points')
        
        C4, path4_info = computePathCharge(path4_points_k, t1, t2, t3, t4, t0, u, a, tij, n)
        path4_computed = True
    
    if 'path5_segments' in locals():
        print('Computing Path 5 topological charge...')
        path5_points_k, path5_points_knorm = generatePathPoints(path5_segments, N_points_per_segment, path5_direction)
        N_path5 = path5_points_k.shape[0]
        print(f'  Path 5: {N_path5} sampling points')
        
        C5, path5_info = computePathCharge(path5_points_k, t1, t2, t3, t4, t0, u, a, tij, n)
        path5_computed = True
    
    print('\nPath-Dependent Topological Charge Matrices:')
    
    if path1_computed:
        print('\nPath 1 Non-Abelian Topological Charge Matrix C1:')
        print(C1)
    
    if path2_computed:
        print('\nPath 2 Non-Abelian Topological Charge Matrix C2:')
        print(C2)
    
    if path3_computed:
        print('\nPath 3 Non-Abelian Topological Charge Matrix C3:')
        print(C3)
    
    if path4_computed:
        print('\nPath 4 Non-Abelian Topological Charge Matrix C4:')
        print(C4)
    
    if path5_computed:
        print('\nPath 5 Non-Abelian Topological Charge Matrix C5:')
        print(C5)
    
    path_figures = []
    if path1_computed:
        fig1 = plotPathFigure(1, path1_points_knorm, path1_segments, C1, 'Path 1: Rectangular Path', 'b',
                             degeneracy_point1, degeneracy_point2, degeneracy_point3, degeneracy_point4, degeneracy_point5)
        path_figures.append(fig1)
    
    if path2_computed:
        fig2 = plotPathFigure(2, path2_points_knorm, path2_segments, C2, 'Path 2: Complex Path (passes degeneracy point)', 'r',
                             degeneracy_point1, degeneracy_point2, degeneracy_point3, degeneracy_point4, degeneracy_point5)
        path_figures.append(fig2)
    
    if path3_computed:
        fig3 = plotPathFigure(3, path3_points_knorm, path3_segments, C3, 'Path 3: Rectangular Path', 'g',
                             degeneracy_point1, degeneracy_point2, degeneracy_point3, degeneracy_point4, degeneracy_point5)
        path_figures.append(fig3)
    
    if path4_computed:
        fig4 = plotPathFigure(4, path4_points_knorm, path4_segments, C4, 'Path 4: Rectangular Path', 'm',
                             degeneracy_point1, degeneracy_point2, degeneracy_point3, degeneracy_point4, degeneracy_point5)
        path_figures.append(fig4)
    
    if path5_computed:
        fig5 = plotPathFigure(5, path5_points_knorm, path5_segments, C5, 'Path 5: Complex Path (clockwise)', 'c',
                             degeneracy_point1, degeneracy_point2, degeneracy_point3, degeneracy_point4, degeneracy_point5)
        path_figures.append(fig5)
    
    if path_figures:
        plt.show(block=False)
    
    print('Figure 6 (Path-Dependent) completed.')


if __name__ == '__main__':
    main()

