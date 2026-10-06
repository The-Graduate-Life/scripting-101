#!/usr/bin/env bash
# 01_hello.sh — your first script.
# Run it with:   bash 01_hello.sh       or   chmod +x 01_hello.sh && ./01_hello.sh

echo "Hello from $(hostname)!"
echo "Today is $(date +%A), and you are user: $USER"
echo "You ran this script from: $PWD"
