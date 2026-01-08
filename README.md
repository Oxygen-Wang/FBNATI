# NATI System: Python Version - Figure Generation Scripts

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/Oxygen-Wang/FBNATI)

This folder contains Python scripts for generating NATI system figures 2-6.

**GitHub Repository**: https://github.com/Oxygen-Wang/FBNATI

## Folder Structure

```
FBNATI1/
├── GenerateAllFigures.py    (Main script - run this to generate all figures)
├── Function/               (Helper functions)
│   ├── computeFBsHamiltonian.py
│   ├── computeNATIHamiltonian.py
│   ├── computeSSHHamiltonian.py
│   ├── computeSSHHamiltonian4D.py
│   ├── computeTijMatrices.py
│   ├── computePathCharge.py
│   ├── formatMatrix.py
│   ├── generatePathPoints.py
│   ├── getColor.py
│   ├── plot_magnetic_lattice.py
│   ├── plotPathFigure.py
│   └── computeRealSpaceHamiltonian.py
├── Source_code/            (Figure generation scripts)
│   ├── Fig2_SymbolicEigenvalue.py
│   ├── Fig3_EigenstateMode.py
│   ├── Fig5_TopCircuit.py
│   ├── Fig6_ChargeAndEuler.py
│   ├── Fig6_EigenstateRotation.py
│   └── Fig6_PathDependent.py
└── requirements.txt
```

## Installation

First install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

### Generate All Figures (Recommended)

Run the main script in Python:

```python
cd FBNATI1
python GenerateAllFigures.py
```

This will automatically:
1. Add Function folder to path
2. Add Source_code folder to path
3. Generate all figures in sequence (2, 3, 5, 6)
4. Display all figures (figures are not saved to disk)

### Generate Individual Figures

You can also run individual figure scripts:

```python
cd FBNATI1/Source_code
python Fig2_SymbolicEigenvalue.py    # Generate Figure 2
python Fig3_EigenstateMode.py        # Generate Figure 3
python Fig5_TopCircuit.py           # Generate Figure 5
python Fig6_ChargeAndEuler.py        # Generate Figure 6 (Charge and Euler connection)
python Fig6_EigenstateRotation.py   # Generate Figure 6 (Eigenstate rotation)
python Fig6_PathDependent.py         # Generate Figure 6 (Path-dependent)
```

## Output
- **Figure 2**: Symbolic eigenvalue calculation (results displayed in command window)
- **Figure 3**: Eigenstate mode visualization (spatial distribution and energy spectrum)
- **Figure 5**: Topological circuit visualization (magnetic lattice structure)
- **Figure 6 (Charge and Euler)**: 
  - Band structure plot
  - Euler connection vs v
  - Eigenstate rotation in 3D space
- **Figure 6 (Eigenstate Rotation)**: 
  - Ladder model band structure
  - Eigenstate rotation visualization
- **Figure 6 (Path-Dependent)**: 
  - 3D band structure
  - Path-dependent topological charge matrices (displayed in command window)
  - Path visualization plots

## Dependencies

- numpy >= 1.20.0
- scipy >= 1.7.0
- matplotlib >= 3.3.0
- sympy >= 1.8.0

