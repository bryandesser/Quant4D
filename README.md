# pyQuant4D
[![CI](https://github.com/bryandesser/pyQuant4D/actions/workflows/ci.yml/badge.svg)](https://github.com/bryandesser/pyQuant4D/actions/workflows/ci.yml)

A Python GUI application for quantitative 4D-STEM data visualisation and analysis, ported from the original MATLAB [Quant4D](https://github.com/bryandesser/Quant4D) application.

4D-STEM (four-dimensional scanning transmission electron microscopy) collects a full diffraction pattern at each probe position in a 2-D scan, producing a 4-D dataset. pyQuant4D provides interactive tools to load, preview, and analyse these datasets — including annular integration, centre-of-mass (CoM/DPC), integrated CoM (iCoM), differential CoM (dCoM), and vector-field overlays — with optional GPU acceleration via PyTorch.

---

## Features

- Interactive diffraction-pattern and real-space image display with live brightness / contrast / gamma controls
- Annular and virtual-aperture detector integration (BF, ADF, ABF)
- Centre-of-mass deflection maps (CoM X/Y, CoM magnitude and phase)
- Integrated and differential CoM (iCoM / dCoM / DPC) via Fourier methods
- Colour-wheel phase display for CoM direction
- Real-space ROI selection and masking
- Save images as float-32 TIFF or annotated PNG; export datasets as HDF5 or raw binary
- Optional GPU acceleration for large-dataset computation (requires a CUDA-capable GPU and PyTorch)
- Python 3.10+, PyQt5 GUI, matplotlib image display

---

## Requirements

| Requirement | Minimum version |
|-------------|----------------|
| Python      | 3.10            |
| PyQt5       | 5.15            |
| NumPy       | 1.24            |
| Matplotlib  | 3.7             |
| SciPy       | 1.10            |
| scikit-image | 0.21           |
| h5py        | 3.8             |
| Pillow      | 9.5             |
| psutil      | 5.9             |
| superqt     | 0.4             |

GPU acceleration additionally requires [PyTorch](https://pytorch.org/get-started/locally/) (≥ 2.0) with CUDA support.

---

## Installation

### From PyPI (once published)

```bash
pip install pyquant4d
```

### From source (recommended during development)

```bash
git clone https://github.com/bryandesser/pyQuant4D.git
cd pyQuant4D
pip install -e .
```

### With GPU support

Install pyquant4d first, then install a CUDA-enabled PyTorch build matching your CUDA version.  
See https://pytorch.org/get-started/locally/ for the right command. For example, for CUDA 12.1:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

Alternatively, install the `[gpu]` extra and then upgrade torch for your CUDA version:

```bash
pip install -e ".[gpu]"
# then upgrade torch to your CUDA build if needed
```

---

## Quick start

After installation, launch the application with:

```bash
quant4d
```

or run directly from the repository:

```bash
python Quant4D_app.py
```

### Loading a dataset

1. Click **Import Data** (or press the import toolbar button) to open the import dialog.
2. Navigate to a `.dm4`, `.dm3`, `.raw`/`.mib`, or `.h5`/`.hdf5` file and select it.
3. Set the real-space frame dimensions (X × Y) and diffraction-pattern dimensions (Px × Py).
4. Click **Import** to load the data into memory.

### Analysing data

- Use the **Detector Mode** selector to switch between alignment, annular integration, CoM/DPC, and segmented-DPC modes.
- Adjust the annular inner/outer radii with the **Ri** / **Ro** sliders.
- Real-space images update automatically as detector parameters change.
- Open the **Save / Export** panel to save images as TIFF/PNG or export the dataset as HDF5.

---

## Documentation

Full documentation is available at **https://pyquant4d.readthedocs.io**.

---

## GPU acceleration

When a CUDA-capable GPU is available and PyTorch is installed, pyQuant4D will automatically use it to accelerate matrix operations during data import and CoM calculations. GPU status is shown in the application title bar at startup.

To verify GPU detection:

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

---

## Contributing

Bug reports and pull requests are welcome at https://github.com/bryandesser/pyQuant4D.  
Please open an issue before submitting a large pull request.

---

## Original MATLAB version

The original MATLAB application is available at https://github.com/bryandesser/Quant4D.

---

## Licence

This project is licenced under the **GNU General Public Licence v3.0**.  
See [LICENSE](LICENSE) for details.

© Monash Imaging Physics, Monash University
