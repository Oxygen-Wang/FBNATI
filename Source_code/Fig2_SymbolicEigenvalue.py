"""
NATI System: Symbolic Eigenvalue Calculation

Model: "Three-equal-one-different" mode: t1 = d, t3 = d, u = f, v = d
Hamiltonian: 4×4 matrix
Symbols: d, f, t (system parameters), k (momentum), coska, sinka
"""

import numpy as np
import sympy as sp
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Function'))


def main():
    print('Generating Figure 2: Symbolic Eigenvalue Calculation...')
    
    d, f, t, k = sp.symbols('d f t k', real=True)
    coska, sinka = sp.symbols('coska sinka', real=True)
    
    # "Three-equal-one-different" mode: t1 = d, t3 = d, u = f, v = d
    t1 = d
    t3 = d
    u = f
    v = d
    
    a1 = u + v*coska
    a2 = -v*sinka
    b1 = t1 + t3*coska
    b2 = -t3*sinka
    
    A = a1 + sp.I*a2
    B = a1 - sp.I*a2
    C = b1 + sp.I*b2
    D = b1 - sp.I*b2
    
    H = sp.Matrix([
        [0,  C,  A,  t],
        [D,  0,  t,  B],
        [B,  t,  0,  D],
        [t,  A,  C,  0]
    ])
    
    print('\nCalculating symbolic eigenvalues...')
    eigvals = H.eigenvals()
    
    print('\nSymbolic eigenvalues:')
    for i, (eigval, mult) in enumerate(eigvals.items(), 1):
        print(f'Eigenvalue {i} (multiplicity {mult}):')
        print(sp.simplify(eigval))
        print()
    
    sinka_sub = sp.sqrt(1 - coska**2)
    H_sub = H.subs(sinka, sinka_sub)
    
    eigvals_sub = H_sub.eigenvals()
    print('\nSymbolic eigenvalues (with sinka substitution):')
    for i, (eigval, mult) in enumerate(eigvals_sub.items(), 1):
        print(f'Eigenvalue {i} (multiplicity {mult}):')
        print(sp.simplify(eigval))
        print()
    
    d_val = 2
    f_val = 4
    t_val = 8
    k_val = np.pi/4
    a_val = 1/2
    
    coska_val = np.cos(k_val * a_val)
    sinka_val = np.sin(k_val * a_val)
    
    H_num_sympy = H.subs([(d, d_val), (f, f_val), (t, t_val), 
                          (coska, coska_val), (sinka, sinka_val)])
    H_num = np.array(H_num_sympy.tolist(), dtype=complex)
    
    eigvals_num = np.linalg.eigvals(H_num)
    eigvals_num = np.sort(eigvals_num)
    
    print(f'\nNumerical eigenvalues (d={d_val:.1f}, f={f_val:.1f}, t={t_val:.1f}, k={k_val:.4f}):')
    for i, eigval in enumerate(eigvals_num, 1):
        print(f'  E_{i} = {eigval:.6f}')
    
    print('\nFigure 2 completed.')


if __name__ == '__main__':
    main()

