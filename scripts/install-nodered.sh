#!/bin/bash

set -e

SCRIPT_PATH=$(dirname "$0")
NODERED_VERSION="3.0.2"

if [ "$(id -u)" -ne 0 ]; then
    echo "Script needs root privileges. Please call the script either as root or with sudo."
    exit 1
fi

# Install nodejs repository
cp "${SCRIPT_PATH}/nodesource.gpg" "/etc/apt/trusted.gpg.d"
cp "${SCRIPT_PATH}/nodesource.list" "/etc/apt/sources.list.d"

# Update package data and install nodejs
apt-get update
apt-get -y install nodejs

# Install node-red
npm install -g --unsafe-perm node-red@${NODERED_VERSION} || true

# Enable node-red
systemctl enable nodered

# Start node-red
systemctl start nodered
