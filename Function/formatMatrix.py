"""
Format matrix as multi-line string for display.

Parameters:
  C - Matrix (typically 4x4 topological charge matrix)
Returns:
  matrix_str - Formatted string (one matrix row per line)
"""

import numpy as np


def formatMatrix(C):
    n, m = C.shape
    
    row_strs = []
    for i in range(n):
        row_vals = []
        for j in range(m):
            # MATLAB's round(val, 1, 'significant') keeps 1 significant digit
            # Use numpy's round with formatting to achieve similar effect
            val = C[i, j]
            # Use %.1g formatting which automatically chooses the best representation
            val_str = f'{val:.1g}'
            row_vals.append(val_str)
        row_strs.append('[' + ', '.join(row_vals) + ']')
    
    matrix_str = '\n'.join(row_strs)
    return matrix_str

