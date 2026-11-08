#!/bin/bash

echo "===== SYSTEM ====="
lsb_release -a 2>/dev/null || cat /etc/os-release
echo

echo "===== CPU ARCHITECTURE ====="
uname -m
echo

echo "===== GIT ====="
git --version || echo "Git is NOT installed"
echo

echo "===== PYTHON ====="
python3 --version || echo "Python3 is NOT installed"
pip3 --version || echo "pip3 is NOT installed"
echo

echo "===== DOCKER ====="
docker --version || echo "Docker is NOT installed"
echo

echo "===== DOCKER COMPOSE ====="
docker compose version || echo "Docker Compose plugin is NOT installed"
echo

echo "===== DOCKER SERVICE ====="
systemctl is-active docker || echo "Docker service is NOT active"
echo

echo "===== DOCKER PERMISSION TEST ====="
docker run --rm hello-world
