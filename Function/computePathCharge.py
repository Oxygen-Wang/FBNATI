"""
Compute non-Abelian topological charge along a path.

Parameters:
  path_points - Path sampling points, format [v, k]
  t1, t2, t3, t4, t0, u - System parameters
  a - Lattice constant
  tij - spin(4) Lie algebra generators
  n - System dimension
Returns:
  C - Non-Abelian topological charge matrix
  path_info - Path information dictionary
"""

import numpy as np
from scipy.linalg import expm
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Function.computeNATIHamiltonian import computeNATIHamiltonian


def computePathCharge(path_points, t1, t2, t3, t4, t0, u, a, tij, n):
    N_points = path_points.shape[0]
    
    eigenvectors = np.zeros((n, n, N_points), dtype=complex)
    eigenvalues = np.zeros((n, N_points))
    
    for idx in range(N_points):
        v = path_points[idx, 0]
        k = path_points[idx, 1]
        
        H = computeNATIHamiltonian(k, t1, t2, t3, t4, t0, u, v, a)
        
        eigvals, M = np.linalg.eigh(H)
        
        # Sort by real part in descending order
        sort_idx = np.argsort(eigvals)[::-1]
        E = eigvals[sort_idx]
        eigenvalues[:, idx] = E
        
        for band_idx in range(n):
            orig_band_idx = sort_idx[band_idx]
            if idx == 0:
                eigenvectors[:, band_idx, idx] = np.sign(M[0, orig_band_idx].real) * M[:, orig_band_idx]
            else:
                overlap = eigenvectors[:, band_idx, idx-1].conj() @ M[:, orig_band_idx]
                eigenvectors[:, band_idx, idx] = np.sign(overlap.real) * M[:, orig_band_idx]
    
    C = np.eye(n, dtype=complex)
    
    for idx in range(N_points - 1):
        v_curr = path_points[idx, 0]
        k_curr = path_points[idx, 1]
        v_next = path_points[idx+1, 0]
        k_next = path_points[idx+1, 1]
        
        dv = v_next - v_curr
        dk = k_next - k_curr
        
        if idx == 0:
            u_curr = eigenvectors[:, :, idx]
            u_next = eigenvectors[:, :, idx+1]
            
            partial_k_u = np.zeros((n, n), dtype=complex)
            partial_v_u = np.zeros((n, n), dtype=complex)
            for j in range(n):
                if abs(dk) > 1e-10:
                    partial_k_u[:, j] = (u_next[:, j] - u_curr[:, j]) / dk
                if abs(dv) > 1e-10:
                    partial_v_u[:, j] = (u_next[:, j] - u_curr[:, j]) / dv
            u_mid = u_curr
        elif idx == N_points - 1:
            u_prev = eigenvectors[:, :, idx-1]
            u_curr = eigenvectors[:, :, idx]
            
            partial_k_u = np.zeros((n, n), dtype=complex)
            partial_v_u = np.zeros((n, n), dtype=complex)
            for j in range(n):
                if abs(dk) > 1e-10:
                    partial_k_u[:, j] = (u_curr[:, j] - u_prev[:, j]) / dk
                if abs(dv) > 1e-10:
                    partial_v_u[:, j] = (u_curr[:, j] - u_prev[:, j]) / dv
            u_mid = u_curr
        else:
            v_prev = path_points[idx-1, 0]
            k_prev = path_points[idx-1, 1]
            u_prev = eigenvectors[:, :, idx-1]
            u_curr = eigenvectors[:, :, idx]
            u_next = eigenvectors[:, :, idx+1]
            
            partial_k_u = np.zeros((n, n), dtype=complex)
            partial_v_u = np.zeros((n, n), dtype=complex)
            for j in range(n):
                u_j_forward = u_next[:, j]
                u_j_backward = u_prev[:, j]
                dk_total = k_next - k_prev
                if abs(dk_total) > 1e-10:
                    partial_k_u[:, j] = (u_j_forward - u_j_backward) / dk_total
                dv_total = v_next - v_prev
                if abs(dv_total) > 1e-10:
                    partial_v_u[:, j] = (u_j_forward - u_j_backward) / dv_total
            u_mid = u_curr
        
        Ak = np.zeros((n, n), dtype=complex)
        Av = np.zeros((n, n), dtype=complex)
        for i in range(n):
            for j in range(n):
                Ak[i, j] = u_mid[:, i].conj() @ partial_k_u[:, j]
                Av[i, j] = u_mid[:, i].conj() @ partial_v_u[:, j]
        
        A_dl = Ak * dk + Av * dv
        
        A_dl_expanded = (A_dl[0, 1] * tij['t12'] +
                        A_dl[0, 2] * tij['t13'] +
                        A_dl[0, 3] * tij['t14'] +
                        A_dl[1, 2] * tij['t23'] +
                        A_dl[1, 3] * tij['t24'] +
                        A_dl[2, 3] * tij['t34'])
        
        C = expm(A_dl_expanded) @ C
    
    path_info = {
        'eigenvalues': eigenvalues,
        'eigenvectors': eigenvectors,
        'N_points': N_points
    }
    
    return C, path_info

