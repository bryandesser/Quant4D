FROM nvidia/cuda:13.0.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl jq git sudo ca-certificates build-essential \
    libgl1 libegl1 libxkbcommon-x11-0 libdbus-1-3 xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m runner && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
WORKDIR /home/runner/actions-runner

RUN V=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | jq -r .tag_name | sed 's/^v//') \
    && curl -fsSL -o r.tar.gz https://github.com/actions/runner/releases/download/v${V}/actions-runner-linux-x64-${V}.tar.gz \
    && tar xzf r.tar.gz && rm r.tar.gz \
    && ./bin/installdependencies.sh \
    && chown -R runner:runner /home/runner

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
USER runner
ENTRYPOINT ["/entrypoint.sh"]
