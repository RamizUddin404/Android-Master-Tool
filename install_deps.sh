#!/bin/bash
# Setup script for Android Master Tool

echo "-----------------------------------------------"
echo "   Android Master Tool - Dependency Installer   "
echo "-----------------------------------------------"

if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    echo "[*] Termux detected. Installing dependencies..."
    pkg update && pkg upgrade -y
    pkg install android-tools python -y
else
    echo "[*] Linux/Ubuntu detected. Installing dependencies..."
    sudo apt update
    sudo apt install adb fastboot python3 -y
fi

echo "[+] Installation Complete!"
echo "[*] Usage: python android_master_tool.py"
