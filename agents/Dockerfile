FROM gitpod/openvscode-server:1.98.2

# https://github.com/stencila/stencila/blob/9129e0dd32e81b8bc67139fb4f779fd04b1db829/workspace/Dockerfile#L2

ENV OVS_HOME="/home/.openvscode-server"
ENV OVS="${OVS_HOME}/bin/openvscode-server"

# Base image uses non-root user so switch to root for installs
# See https://github.com/gitpod-io/openvscode-server?tab=readme-ov-file#custom-environment
USER root

# Use bash instead of sh in the following RUNs
SHELL ["/bin/bash", "-c"]

# Update & install packages
RUN <<EOF
apt-get update
apt-get install -y curl jq
rm -rf /var/lib/apt/lists/*
EOF

# Switch back to user so they can write to the workspace files if they wish
# (e.g. when they install new packages)
USER openvscode-server

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/workspace/.local/bin:$PATH"

# Install Python and tools using uv
RUN <<EOF
uv python install
EOF

ADD init.sh /home/workspace/init.sh