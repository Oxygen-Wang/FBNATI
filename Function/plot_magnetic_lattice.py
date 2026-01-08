"""
Plot magnetic lattice structure.

Parameters:
  ct0, ct1, cu, cv, ct3 - Bond parameters (hopping strengths)
  mi - Magnetic interaction values for color mapping
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Function.getColor import getColor


def plot_magnetic_lattice(ct0, ct1, cu, cv, ct3, mi):
    yy = 1.2
    
    Nx = len(mi) // 4
    if Nx * 4 != len(mi):
        raise ValueError('Length of mi must be a multiple of 4')
    
    unit_cell = np.array([
        [0, 0, 0],
        [0, yy, 0],
        [1, 0, 0],
        [1, yy, 0]
    ])
    
    # Unit cell bonds: cu (intra-unit), ct0/ct1 (diagonal)
    bonds_unit = [
        ([0, 2], cu),
        ([1, 3], cu)
    ]
    
    bonds_unit1 = [
        ([0, 1], ct0),
        ([2, 3], ct0),
        ([0, 3], ct1),
        ([1, 2], ct1)
    ]
    
    # Inter-unit cell bonds: cv (inter-chain), ct3 (diagonal)
    bonds_inter = [
        ([2, 0], cv),
        ([3, 1], cv)
    ]
    
    bonds_inter1 = [
        ([2, 1], ct3),
        ([3, 0], ct3)
    ]
    
    all_atoms = []
    ax = plt.gca()
    
    is_3d = hasattr(ax, 'zaxis')
    
    for nx in range(Nx):
        offset = np.array([2*nx, 0, 0])
        atoms = unit_cell + offset
        all_atoms.append(atoms)
        
        for bond_info in bonds_unit:
            idx, color_val = bond_info
            pos1 = atoms[idx[0], :]
            pos2 = atoms[idx[1], :]
            clr = getColor(color_val)
            if is_3d:
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], [pos1[2], pos2[2]],
                       '-', linewidth=2, color=clr)
            else:
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]],
                       '-', linewidth=2, color=clr)
        
        for bond_info in bonds_unit1:
            idx, color_val = bond_info
            pos1 = atoms[idx[0], :]
            pos2 = atoms[idx[1], :]
            clr = getColor(color_val)
            if is_3d:
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], [pos1[2], pos2[2]],
                       ':', linewidth=2, color=clr)
            else:
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]],
                       ':', linewidth=2, color=clr)
    
    for nx in range(Nx - 1):
        atoms1 = all_atoms[nx]
        atoms2 = all_atoms[nx+1]
        
        for bond_info in bonds_inter:
            idx, color_val = bond_info
            pos1 = atoms1[idx[0], :]
            pos2 = atoms2[idx[1], :]
            clr = getColor(color_val)
            if is_3d:
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], [pos1[2], pos2[2]],
                       '-', linewidth=2, color=clr)
            else:
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]],
                       '-', linewidth=2, color=clr)
        
        for bond_info in bonds_inter1:
            idx, color_val = bond_info
            pos1 = atoms1[idx[0], :]
            pos2 = atoms2[idx[1], :]
            clr = getColor(color_val)
            if is_3d:
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], [pos1[2], pos2[2]],
                       ':', linewidth=2, color=clr)
            else:
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]],
                       ':', linewidth=2, color=clr)
    
    # Collect scatter points for color mapping
    scatter_positions = []
    scatter_values = []
    for nx in range(Nx):
        atoms = all_atoms[nx]
        for i in range(4):
            scatter_positions.append([atoms[i, 0], atoms[i, 1], atoms[i, 2]])
            scatter_values.append(mi[nx*4+i])
    
    scatter_positions = np.array(scatter_positions)
    scatter_values = np.array(scatter_values)
    
    # Custom colormap: blue -> yellow -> red
    n = 256
    blue = np.array([30, 144, 255]) / 255
    yellow = np.array([255, 255, 200]) / 255
    red = np.array([178, 34, 34]) / 255
    
    colors = np.vstack([
        np.column_stack([
            np.linspace(blue[0], yellow[0], n//2),
            np.linspace(blue[1], yellow[1], n//2),
            np.linspace(blue[2], yellow[2], n//2)
        ]),
        np.column_stack([
            np.linspace(yellow[0], red[0], n//2),
            np.linspace(yellow[1], red[1], n//2),
            np.linspace(yellow[2], red[2], n//2)
        ])
    ])
    
    if len(scatter_positions) > 0:
        if is_3d:
            scatter = ax.scatter(scatter_positions[:, 0], scatter_positions[:, 1], scatter_positions[:, 2],
                               s=100, c=scatter_values, cmap=plt.cm.colors.ListedColormap(colors),
                               edgecolors='k', linewidths=0.5)
        else:
            scatter = ax.scatter(scatter_positions[:, 0], scatter_positions[:, 1],
                               s=100, c=scatter_values, cmap=plt.cm.colors.ListedColormap(colors),
                               edgecolors='k', linewidths=0.5)
    
    ax.set_facecolor('white')
    plt.gcf().set_facecolor('white')
    ax.axis('equal')
    ax.axis('off')

