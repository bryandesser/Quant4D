.. _installation:

Installation
============

Requirements
------------

- **Python** 3.10 or later
- **PyQt5** ≥ 5.15
- **NumPy** ≥ 1.24
- **Matplotlib** ≥ 3.7
- **SciPy** ≥ 1.10
- **scikit-image** ≥ 0.21
- **h5py** ≥ 3.8
- **Pillow** ≥ 9.5
- **psutil** ≥ 5.9
- **superqt** ≥ 0.4

GPU acceleration additionally requires PyTorch ≥ 2.0 with CUDA support
(see :ref:`gpu-setup` below).

Create a conda environment
--------------------------

We recommend installing Quant4D into its own conda environment so that its
dependencies do not conflict with other packages.  Create and activate one
before installing::

    conda create -n quant4d python=3.11
    conda activate quant4d

Run all of the ``pip`` commands below inside this activated environment.

From PyPI
---------

Once published, install with::

    pip install quant4d

From source
-----------

Clone the repository and install in editable mode::

    git clone https://github.com/bryandesser/Quant4D.git
    cd Quant4D
    pip install -e .

This installs all core dependencies automatically.

.. _gpu-setup:

GPU setup
---------

By default, Quant4D runs on the CPU.  To enable GPU acceleration:

1. Check that your machine has a CUDA-capable NVIDIA GPU and the appropriate
   CUDA toolkit installed.

2. Install a CUDA-enabled build of PyTorch that matches your CUDA version.
   Visit https://pytorch.org/get-started/locally/ for the exact ``pip``
   command.  For example, with CUDA 12.1::

       pip install torch --index-url https://download.pytorch.org/whl/cu121

3. Launch Quant4D normally.  The title bar will show GPU information if a
   device is detected.

You can verify GPU availability from Python::

    import torch
    print(torch.cuda.is_available())          # True if a CUDA GPU is found
    print(torch.cuda.get_device_name(0))      # e.g. "NVIDIA GeForce RTX 3080"

py4DSTEM
--------

Quant4D reads and writes py4DSTEM's EMD files without py4DSTEM.  Install it
for **File > Open with py4DSTEM Reader...** (legacy py4DSTEM files) and for
round trips from Python::

    pip install "quant4d[py4dstem]"

Developer extras
----------------

Install testing and documentation dependencies with::

    pip install -e ".[dev]"
