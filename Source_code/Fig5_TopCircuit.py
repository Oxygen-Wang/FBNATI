"""
NATI System: Topological Circuit Figure 5

Visualizes topological circuit structure with magnetic lattice.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
import scipy.io

script_path = os.path.dirname(os.path.abspath(__file__))
function_path = os.path.join(os.path.dirname(script_path), 'Function')
sys.path.append(function_path)

from plot_magnetic_lattice import plot_magnetic_lattice


def main():
    print('Generating Figure 5: Topological Circuit...')
    
    cu = 2
    cv = 4
    ct1 = 2
    ct3 = 2
    
    dataFile = os.path.join(script_path, 'mi_data.mat')
    
    if os.path.exists(dataFile):
        try:
            data = scipy.io.loadmat(dataFile)
            mi_normalized_all = data.get('mi_normalized_all', np.zeros((20, 3)))
            if mi_normalized_all.size == 0:
                mi_normalized_all = np.zeros((20, 3))
                scipy.io.savemat(dataFile, {'mi_normalized_all': mi_normalized_all})
        except:
            mi_normalized_all = np.zeros((20, 3))
            scipy.io.savemat(dataFile, {'mi_normalized_all': mi_normalized_all})
    else:
        mi_normalized_all = np.zeros((20, 3))
        scipy.io.savemat(dataFile, {'mi_normalized_all': mi_normalized_all})
    
    if mi_normalized_all.shape[1] < 3:
        raise ValueError('Data dimension error: mi_normalized_all must have at least 3 columns')
    if mi_normalized_all.shape[0] % 4 != 0:
        raise ValueError('Data dimension error: number of rows in mi_normalized_all must be a multiple of 4')
    
    epsilon = 1e-10
    log_data = np.log10(mi_normalized_all + epsilon)
    
    fig = plt.figure(figsize=(10, 10))
    ct = np.array([0, 8, 8])
    
    for i in range(3):
        ax = fig.add_subplot(4, 1, i+1)
        plt.sca(ax)
        
        data_col = log_data[:, i]
        plot_magnetic_lattice(ct[i], ct1, cu, cv, ct3, data_col)
        
        ax.text(-0.5, 0.5, f'({chr(ord("a") + i)})',
               fontsize=12, horizontalalignment='center')
        
        ax.text(9.4, 0.8, '...', fontsize=14,
               horizontalalignment='center')
        
        ax.set_xlim([-1, 10])
        ax.set_ylim([0, 1.5])
        ax.set_position([0.15, 1 - (i+1) * 0.18, 0.7, 0.18])
        
        min_val_i = np.min(data_col)
        max_val_i = np.max(data_col)
        for collection in ax.collections:
            if hasattr(collection, 'set_clim'):
                collection.set_clim(min_val_i, max_val_i)
    
    overall_min = np.min(log_data)
    overall_max = np.max(log_data)
    
    n = 256
    blue = np.array([30, 144, 255]) / 255
    yellow = np.array([255, 255, 200]) / 255
    red = np.array([178, 34, 34]) / 255
    
    colors_cmap = np.vstack([
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
    from matplotlib.colors import ListedColormap
    custom_cmap = ListedColormap(colors_cmap)
    
    sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=plt.Normalize(vmin=overall_min, vmax=overall_max))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=fig.axes, location='right', pad=0.1, fraction=0.03)
    cbar.ax.yaxis.set_ticks_position('right')
    
    ticks = np.linspace(overall_min, overall_max, 4)
    cbar.set_ticks(ticks)
    cbar.set_ticklabels([f'{x:.1f}' for x in ticks])
    cbar.set_label('Log Scale', fontsize=14)
    
    plt.tight_layout(pad=2.0)
    plt.show(block=False)
    
    print('Figure 5 completed.')


if __name__ == '__main__':
    main()

