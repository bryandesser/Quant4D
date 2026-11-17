#!/bin/bash
# ============================================================
# pyQuant4D GPU runner — entrypoint
# ============================================================
# Registers the GitHub Actions runner on startup and
# deregisters cleanly on SIGTERM/SIGINT (e.g. docker stop).
#
# Required environment variables:
#   GITHUB_OWNER   - GitHub org or username  (e.g. bryandesser)
#   GITHUB_REPO    - Repository name         (e.g. Quant4D)
#
# Supply ONE of:
#   RUNNER_TOKEN   - One-time registration token
#                    (from Settings → Actions → Runners → New runner)
#                    Valid for ~1 hour; if the container restarts you need a new one.
#
#   GITHUB_PAT     - Personal Access Token with repo scope (recommended for
#                    persistent/auto-restarting containers — a fresh token is
#                    fetched automatically on every start).
#                    Create at: https://github.com/settings/tokens
#                    Required scopes: repo (or public_repo for public repos)
#
# Optional environment variables:
#   RUNNER_NAME    - Display name in GitHub UI  (default: container hostname)
#   RUNNER_LABELS  - Comma-separated extra labels appended to the defaults
#                    (default labels always added: self-hosted, gpu, Linux, X64)
# ============================================================

set -euo pipefail

# ---- Validate required vars --------------------------------
: "${GITHUB_OWNER:?GITHUB_OWNER environment variable is required}"
: "${GITHUB_REPO:?GITHUB_REPO environment variable is required}"

REPO_URL="https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}"
RUNNER_NAME="${RUNNER_NAME:-$(hostname)}"
BASE_LABELS="self-hosted,gpu,Linux,X64"
LABELS="${BASE_LABELS}${RUNNER_LABELS:+,${RUNNER_LABELS}}"

# ---- Resolve registration token ----------------------------
# Prefer GITHUB_PAT (self-renewing) over RUNNER_TOKEN (one-shot).
if [ -n "${GITHUB_PAT:-}" ]; then
    echo "[runner] Fetching registration token via PAT..."
    RUNNER_TOKEN=$(curl -s -X POST \
        -H "Authorization: Bearer ${GITHUB_PAT}" \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/actions/runners/registration-token" \
        | jq -r '.token')

    if [ -z "${RUNNER_TOKEN}" ] || [ "${RUNNER_TOKEN}" = "null" ]; then
        echo "[runner] ERROR: Failed to fetch registration token. Check GITHUB_PAT has 'repo' scope and the repo path is correct."
        exit 1
    fi
    echo "[runner] Token fetched successfully."
elif [ -z "${RUNNER_TOKEN:-}" ]; then
    echo "[runner] ERROR: Supply either GITHUB_PAT or RUNNER_TOKEN."
    exit 1
fi

# ---- Remove stale local runner config (handles dirty restarts)
# config.sh refuses to run if .runner already exists on disk.
# Safe to remove — GitHub registration is what matters, not these local files.
rm -f /home/runner/.runner /home/runner/.credentials \
       /home/runner/.credentials_rsaparams /home/runner/.env 2>/dev/null || true

# ---- Ensure _work is writable by the runner user
sudo chown -R runner:runner /home/runner/_work 2>/dev/null || true

# ---- Register (or re-register) the runner ------------------
# --replace allows re-using the same name after a restart without
# manually removing the old registration from GitHub first.
echo "[runner] Registering runner '${RUNNER_NAME}' with ${REPO_URL}"
echo "[runner] Labels: ${LABELS}"

./config.sh \
    --url "${REPO_URL}" \
    --token "${RUNNER_TOKEN}" \
    --name "${RUNNER_NAME}" \
    --labels "${LABELS}" \
    --work "_work" \
    --disableupdate \
    --unattended \
    --replace

# ---- Graceful shutdown on SIGTERM / SIGINT -----------------
_remove_runner() {
    echo ""
    echo "[runner] Received shutdown signal — deregistering from GitHub..."

    # Fetch a fresh removal token (the registration token is single-use)
    if [ -n "${GITHUB_PAT:-}" ]; then
        REMOVE_TOKEN=$(curl -s -X POST \
            -H "Authorization: Bearer ${GITHUB_PAT}" \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/actions/runners/remove-token" \
            | jq -r '.token')
        ./config.sh remove --token "${REMOVE_TOKEN}" 2>/dev/null || true
    else
        # RUNNER_TOKEN has usually expired by now; best-effort only
        ./config.sh remove --token "${RUNNER_TOKEN}" 2>/dev/null || true
    fi

    echo "[runner] Runner deregistered. Exiting."
}

trap _remove_runner INT TERM

# ---- Start the runner --------------------------------------
echo "[runner] Starting. Listening for jobs tagged [self-hosted, gpu]..."
./run.sh &
RUNNER_PID=$!
wait ${RUNNER_PID}
