"""
Plot path figure with topological charge matrix.

Parameters:
  path_num - Path number
  path_points_knorm - Path sampling points [v, k/π]
  path_segments - Path segment endpoints [v, k]
  C - Topological charge matrix
  title_str - Title string
  color - Path color
  degeneracy_point1-5 - Degeneracy point positions
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Function.formatMatrix import formatMatrix


def plotPathFigure(path_num, path_points_knorm, path_segments, C, title_str, color,
                   degeneracy_point1, degeneracy_point2, degeneracy_point3, 
                   degeneracy_point4, degeneracy_point5):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.plot(path_points_knorm[:, 0], path_points_knorm[:, 1], '-', 
            color=color, linewidth=2)
    ax.plot(path_segments[:, 0], path_segments[:, 1] / np.pi, 'o', 
            color=color, markersize=8, markerfacecolor=color)
    
    ax.plot(degeneracy_point1[0], degeneracy_point1[1] / np.pi, 'r*', markersize=12)
    ax.plot(degeneracy_point2[0], degeneracy_point2[1] / np.pi, 'r*', markersize=12)
    ax.plot(degeneracy_point3[0], degeneracy_point3[1] / np.pi, 'g*', markersize=12)
    ax.plot(degeneracy_point4[0], degeneracy_point4[1] / np.pi, 'ms', 
            markersize=10, markerfacecolor='m')
    ax.plot(degeneracy_point5[0], degeneracy_point5[1] / np.pi, 'ms', 
            markersize=10, markerfacecolor='m')
    
    ax.set_xlabel('$v$', fontsize=12)
    ax.set_ylabel('$k / \pi$', fontsize=12)
    ax.set_title(title_str, fontsize=12)
    ax.grid(True)
    
    matrix_str = formatMatrix(C)
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    ax.text(xlims[0] + 0.05*(xlims[1]-xlims[0]), ylims[1] - 0.05*(ylims[1]-ylims[0]),
            f'C{path_num} =\n{matrix_str}', fontsize=8, family='monospace',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='black'),
            verticalalignment='top')
    
    plt.tight_layout(pad=2.0)
    return fig

