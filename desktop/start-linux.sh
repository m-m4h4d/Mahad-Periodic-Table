#!/bin/sh
# Starts the MTH Periodic Table. Run: ./start-linux.sh
cd "$(dirname "$0")" || exit 1
exec python3 launcher.py
