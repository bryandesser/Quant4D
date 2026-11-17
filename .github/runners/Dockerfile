# ============================================================
# pyQuant4D — Self-hosted GitHub Actions GPU runner
# ============================================================
# Base: NVIDIA CUDA 12.6 + cuDNN 9 on Ubuntu 22.04
#
# Host requirements
#   Linux   : nvidia-container-toolkit installed and configured
#             https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html
#   Windows : Docker Desktop ≥ 4.26 with WSL2 backend
#             NVIDIA driver ≥ 525 on the Windows host
#             (GPU passthrough through WSL2 is automatic — no extra config needed)
# ============================================================

FROM nvidia/cuda:12.6.3-cudnn9-runtime-ubuntu22.04

# ---- Build arguments ----------------------------------------
ARG RUNNER_VERSION=2.338.2
ARG PYTHON_VERSION=3.11

# ---- Environment -------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive
# Qt offscreen rendering — no X11/display server needed
ENV QT_QPA_PLATFORM=offscreen
# Suppress .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Point Python tools to the venv
ENV PATH="/home/runner/venv/bin:$PATH"
# Silence pip upgrade nag inside the container
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# ---- System dependencies -----------------------------------
# Groups:
#   1. Core runner tools
#   2. Python 3.11
#   3. Qt / matplotlib offscreen stack (xcb platform + OpenGL)
#   4. GitHub Actions runner native deps (libssl, kerberos, ICU)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core tools
    curl git sudo jq ca-certificates \
    # Python
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    # Qt offscreen / xcb platform plugin requirements
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-xcb1 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    libfreetype6 \
    libxrender1 \
    libxcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libxext6 \
    libdbus-1-3 \
    # GitHub runner native dependencies
    libssl3 \
    libkrb5-3 \
    libicu70 \
    && rm -rf /var/lib/apt/lists/*

# ---- Non-root user for the runner --------------------------
# Running as root inside the runner is a security risk and
# some actions explicitly refuse to run as root.
RUN useradd -m -s /bin/bash runner \
    && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ---- GitHub Actions runner binaries ------------------------
WORKDIR /home/runner
RUN curl -fsSL -O \
    "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" \
    && tar xzf "actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" \
    && rm "actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" \
    && ./bin/installdependencies.sh \
    && chown -R runner:runner /home/runner

# ---- Python virtual environment + test dependencies --------
USER runner

RUN python${PYTHON_VERSION} -m venv /home/runner/venv

# Install test stack + GPU libraries.
# PyTorch is installed from the CUDA 12.6 wheel index.
# CuPy (cupy-cuda12x) is commented out — uncomment if the project
# switches from torch to cupy for GPU acceleration.
RUN pip install --upgrade pip && \
    pip install \
        # ── Test framework ───────────────────────────────────
        pytest \
        pytest-qt \
        pytest-cov \
        pytest-mock \
        pytest-xdist \
        # ── File-format verification ─────────────────────────
        tifffile \
        Pillow \
        h5py \
        hdf5plugin \
        # ── Scientific stack ─────────────────────────────────
        numpy \
        scipy \
        matplotlib \
        # ── Qt (offscreen) ───────────────────────────────────
        PyQt5 \
    && pip install \
        # ── PyTorch with CUDA 12.6 (supports Blackwell sm_120) ─────
        # Installed separately so a failure here doesn't break the base stack
        torch \
        torchvision \
        --index-url https://download.pytorch.org/whl/cu126
    # Uncomment for CuPy instead of / in addition to PyTorch:
    # && pip install cupy-cuda12x

# ---- Entrypoint --------------------------------------------
COPY --chown=runner:runner entrypoint.sh /home/runner/entrypoint.sh
RUN chmod +x /home/runner/entrypoint.sh

WORKDIR /home/runner
ENTRYPOINT ["/home/runner/entrypoint.sh"]
