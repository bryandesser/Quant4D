#!/usr/bin/env bash
set -euo pipefail
cd /home/runner/actions-runner

if [ ! -f .runner ]; then
  ./config.sh --unattended --replace \
    --url "https://github.com/${REPO}" \
    --token "${RUNNER_TOKEN}" \
    --name "${RUNNER_NAME}" \
    --labels "gpu" \
    --work _work
fi
exec ./run.sh
