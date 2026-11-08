#!/bin/bash

# Stop the script if a command fails.
set -e

# Run from the folder where this script is stored.
cd "$(dirname "$0")"

# Check whether a command exists.
is_installed() {
    command -v "$1" >/dev/null 2>&1
}

echo "Checking development tools..."

# --------------------------------------------------
# Install Python 3.9+, pip, and venv
# --------------------------------------------------

if is_installed python3 && \
   python3 -c 'import sys; exit(0 if sys.version_info >= (3, 9) else 1)' && \
   is_installed pip3 && \
   dpkg -s python3-venv >/dev/null 2>&1
then
    echo "[SKIP] Python 3.9+, pip, and venv are already installed."
else
    echo "[INSTALL] Installing Python, pip, and venv..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 9) else 1)'
then
    echo "[ERROR] Python 3.9 or newer is required."
    python3 --version
    exit 1
fi

# --------------------------------------------------
# Install Docker Engine and Docker Compose
# --------------------------------------------------

if is_installed docker && docker compose version >/dev/null 2>&1
then
    echo "[SKIP] Docker and Docker Compose are already installed."
else
    echo "[INSTALL] Installing Docker and Docker Compose..."
    sudo apt update
    sudo apt install -y curl
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
fi

sudo systemctl enable --now docker

# --------------------------------------------------
# Create a virtual environment and install Django
# --------------------------------------------------

if [ -x ".venv/bin/python" ]
then
    echo "[SKIP] Virtual environment already exists."
else
    echo "[INSTALL] Creating Python virtual environment..."
    rm -rf .venv
    python3 -m venv --copies .venv || python3 -m venv --without-pip .venev
fi

if .venv/bin/python -m django --version >/dev/null 2>&1
then
    echo "[SKIP] Django is already installed."
else
    echo "[INSTALL] Installing Django..."
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/python -m pip install django
fi

# --------------------------------------------------
# Show installed versions
# --------------------------------------------------

echo
echo "Installation completed."
echo "-----------------------"
python3 --version
docker --version
docker compose version


echo
echo "To activate the Django environment, run:"
echo "source .venv/bin/activate"