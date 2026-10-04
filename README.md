## Citation & Documentation
* **Source Code DOI:** [https://doi.org/10.5281/zenodo.23136804]
* **Academic Paper DOI:** [https://doi.org/10.5281/zenodo.23136832]

If you use this method in your research or teaching, please cite the academic preprint.

# N-Dimensional Hypercube Visualizer (1D–6D)

A Python program for generating, rotating, and projecting higher-dimensional hypercubes (from 1D segments up to the 6D hexateron) into real-time interactive 3D visualization windows.

## Methodology
This project implements a constructive **"sweep-and-mirror"** geometric operator combined with:
* **Hamming graph topology** for edge connectivity ($E_n = n \cdot 2^{n-1}$).
* **Multi-plane orthogonal rotation matrices** in $\mathbb{R}^n$.
* **Iterative perspective projection** down to 3D viewing space with dimension-dependent scale compensation.

## Requirements
To run this script, you need Python 3 along with `numpy` and `matplotlib`. You can install them via pip:

```bash
pip install numpy matplotlib
