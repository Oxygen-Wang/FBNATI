"""
Generate All Figures: One-Click Script for Figures 2-6

Automatically generates all NATI system figures (2, 3, 5, 6).
"""

import sys
import os

script_path = os.path.dirname(os.path.abspath(__file__))

function_path = os.path.join(script_path, 'Function')
if os.path.exists(function_path):
    sys.path.append(function_path)
    print('Added Function folder to path.')

source_code_path = os.path.join(script_path, 'Source_code')
if os.path.exists(source_code_path):
    sys.path.append(source_code_path)
    print('Added Source_code folder to path.')

print()

print('----------------------------------------')
print('Generating Figure 2: Symbolic Eigenvalue')
print('----------------------------------------')
try:
    from Source_code.Fig2_SymbolicEigenvalue import main as fig2_main
    fig2_main()
    print('Figure 2 completed successfully.\n')
except Exception as e:
    print(f'Error generating Figure 2: {e}\n')

print('----------------------------------------')
print('Generating Figure 3: Eigenstate Mode')
print('----------------------------------------')
try:
    from Source_code.Fig3_EigenstateMode import main as fig3_main
    fig3_main()
    print('Figure 3 completed successfully.\n')
except Exception as e:
    print(f'Error generating Figure 3: {e}\n')

print('----------------------------------------')
print('Generating Figure 5: Topological Circuit')
print('----------------------------------------')
try:
    from Source_code.Fig5_TopCircuit import main as fig5_main
    fig5_main()
    print('Figure 5 completed successfully.\n')
except Exception as e:
    print(f'Error generating Figure 5: {e}\n')

print('----------------------------------------')
print('Generating Figure 6: Charge and Euler Connection')
print('----------------------------------------')
try:
    from Source_code.Fig6_ChargeAndEuler import main as fig6_main
    fig6_main()
    print('Figure 6 (Charge and Euler) completed successfully.\n')
except Exception as e:
    print(f'Error generating Figure 6 (Charge and Euler): {e}\n')

print('----------------------------------------')
print('Generating Figure 6: Eigenstate Rotation')
print('----------------------------------------')
try:
    from Source_code.Fig6_EigenstateRotation import main as fig6_rot_main
    fig6_rot_main()
    print('Figure 6 (Eigenstate Rotation) completed successfully.\n')
except Exception as e:
    print(f'Error generating Figure 6 (Eigenstate Rotation): {e}\n')

print('----------------------------------------')
print('Generating Figure 6: Path-Dependent Charge')
print('----------------------------------------')
try:
    from Source_code.Fig6_PathDependent import main as fig6_path_main
    fig6_path_main()
    print('Figure 6 (Path-Dependent) completed successfully.\n')
except Exception as e:
    print(f'Error generating Figure 6 (Path-Dependent): {e}\n')

print('========================================')
print('All Figures Generation Complete!')
print('========================================')
print('\nAll figures have been displayed.')
print('Press Enter to exit (figures will remain open)...')
try:
    input()
except:
    pass

