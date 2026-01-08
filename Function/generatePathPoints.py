"""
Generate path sampling points.

Parameters:
  segments - Path segment endpoints, format [v, k] array (k in radians)
  N_per_segment - Number of sampling points per path segment
  direction - Path direction: 1 = counterclockwise (default), -1 = clockwise
Returns:
  path_points_k - Path sampling points [v, k] for calculation (k as unfolded continuous variable, radians)
  path_points_knorm - Path sampling points [v, k/π] for plotting (normalized to k/π)
"""

import numpy as np


def generatePathPoints(segments, N_per_segment, direction=1):
    if direction == -1:
        segments = np.flipud(segments)
    
    N_segments = segments.shape[0] - 1
    total_points = N_segments * (N_per_segment + 1)
    path_points_knorm = np.zeros((total_points, 2))
    path_points_k = np.zeros((total_points, 2))
    
    point_idx = 0
    for i in range(N_segments):
        v_start = segments[i, 0]
        k_start = segments[i, 1]
        v_end = segments[i+1, 0]
        k_end = segments[i+1, 1]
        
        v_points = np.linspace(v_start, v_end, N_per_segment + 1)
        k_points = np.linspace(k_start, k_end, N_per_segment + 1)
        
        k_unfold = k_points
        k_norm_plot = k_points / np.pi
        
        num_points_to_add = N_per_segment + 1
        path_points_k[point_idx:point_idx+num_points_to_add, :] = np.column_stack([v_points, k_unfold])
        path_points_knorm[point_idx:point_idx+num_points_to_add, :] = np.column_stack([v_points, k_norm_plot])
        point_idx += num_points_to_add
    
    path_points_k = path_points_k[:point_idx, :]
    path_points_knorm = path_points_knorm[:point_idx, :]
    
    return path_points_k, path_points_knorm

