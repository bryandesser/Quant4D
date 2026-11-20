# Quant4D — Self-hosted GPU test runner

This directory contains the Docker setup for running the `test-gpu` CI job
locally on your own NVIDIA hardware. One image, same `docker compose` command
on both machines.

| Platform | Status | Notes |
|----------|--------|-------|
| **Linux workstation** | ✅ Supported | Native Docker + nvidia-container-toolkit |
| **Windows workstation** | ✅ Supported | Docker Desktop + WSL2 (automatic GPU passthrough) |
| **macOS** | ❌ Not applicable | No CUDA on macOS; CPU-only tests use GitHub-hosted runners |

---

## Prerequisites

### Linux

1. **NVIDIA driver** — any driver ≥ 525.
   ```bash
   nvidia-smi   # verify driver is working
   ```

2. **nvidia-container-toolkit** — lets Docker pass the GPU into containers.
   ```bash
   # Ubuntu / Debian
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
       sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
       sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker
   ```
   Full guide: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

3. **Docker Engine ≥ 24** and **Docker Compose plugin ≥ 2.20**.

### Windows (mobile workstation)

1. **NVIDIA driver ≥ 525** installed on Windows — download from https://www.nvidia.com/drivers

2. **Docker Desktop ≥ 4.26** with the **WSL2 backend** enabled.
   - Settings → General → "Use the WSL 2 based engine" ✓
   - Settings → Resources → WSL Integration → enable for your distro ✓

3. GPU passthrough works automatically through Docker Desktop's WSL2 integration.
   No `nvidia-container-toolkit` install is needed on Windows — Docker Desktop bundles it.

4. Run all commands in **PowerShell** or the Docker Desktop terminal; the
   `docker compose` syntax is identical to Linux.

---

## Setup

```bash
# 1. Navigate to this directory
cd .github/runners

# 2. Create your .env file from the template
cp .env.example .env
# Edit .env — add your GITHUB_PAT (recommended) or RUNNER_TOKEN

# 3. Build the image (first run takes ~10 min — downloads PyTorch CUDA wheels)
docker compose build

# 4. Start the runner (detached)
docker compose up -d

# 5. Confirm it's online
#    https://github.com/bryandesser/Quant4D/settings/actions/runners
#    Status should show as "Idle"
```

---

## Authentication

### Recommended — Personal Access Token (PAT)

A PAT lets the container auto-generate a fresh registration token every time it
starts, so you never manually rotate tokens.

1. Go to https://github.com/settings/tokens → **Generate new token (classic)**
2. Scopes: `repo` (for a private repo) or `public_repo` (for a public repo)
3. Copy the token into `.env` as `GITHUB_PAT=ghp_...`

### Alternative — one-time registration token

1. Go to your repo → Settings → Actions → Runners → **New self-hosted runner**
2. Copy the token from the configure step
3. Set `RUNNER_TOKEN=<token>` in `.env`

> **Note:** Registration tokens expire ~1 hour after creation. If the container
> restarts after the token has expired you must generate a new one. Use the PAT
> method to avoid this.

---

## Day-to-day operations

```bash
# View logs
docker compose logs -f

# Stop (also deregisters the runner from GitHub)
docker compose down

# Restart after a config change
docker compose down && docker compose up -d

# Rebuild after a Dockerfile change (e.g. RUNNER_VERSION bump)
docker compose up -d --build

# Check GPU is visible inside the container
docker exec quant4d-gpu-runner nvidia-smi
```

---

## Running the GPU tests manually

The runner picks up jobs automatically when pushed to `main`. To trigger the
`test-gpu` workflow manually:

```bash
# From the repo root
gh workflow run ci.yml --ref main
```

Or open the **Actions** tab on GitHub and click **Run workflow**.

---

## Updating the runner version

1. Find the latest release version at https://github.com/actions/runner/releases
2. Update `ARG RUNNER_VERSION=X.Y.Z` in `Dockerfile`
3. Rebuild: `docker compose up -d --build`

GitHub will warn in the runner list when a runner version is out of date.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `docker: Error response from daemon: could not select device driver "nvidia"` | nvidia-container-toolkit not installed or Docker not restarted after install |
| Runner appears **Offline** in GitHub | Check `docker compose logs`; most likely the token expired — generate a new one or use PAT |
| `torch.cuda.is_available()` returns `False` inside the container | Run `docker exec quant4d-gpu-runner nvidia-smi` — if that fails, the GPU isn't passed through |
| Jobs stuck in queue / never picked up | Check the labels: the workflow uses `[self-hosted, gpu]`; verify the runner has both |
| OOM during GPU tests | Increase `shm_size` in `docker-compose.yml` or reduce `pytest -n` parallelism |
