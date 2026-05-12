# Android Master Tool (ADB Edition)

A powerful, command-line based Android device management tool written in Python. It uses the Android Debug Bridge (ADB) to interact with connected devices securely and efficiently.

## Features

*   **Auto Device Detection:** Scans and connects to available ADB devices (USB or TCP/IP).
*   **System Information:** Fetch battery health, RAM usage, and storage details.
*   **App Management:** List all installed third-party applications and easily install new `.apk` files.
*   **Media Capture:** Take screenshots and record screen (up to 30 seconds) directly to your PC.
*   **File Transfer:** Pull files from the device or push files to the device easily.
*   **Power Options:** Advanced reboot options (Normal, Recovery, Bootloader/Fastboot).
*   **Shell Access:** Drop directly into the device's native shell terminal.

## Requirements

*   Python 3.x
*   ADB (Android Debug Bridge) installed and added to your system PATH.
*   An Android device with **USB Debugging** enabled in Developer Options.

## Installation & Usage

1. Clone this repository:
   ```bash
   git clone <your-github-repo-url>
   cd <your-repo-folder>
   ```

2. Run the tool:
   ```bash
   python android_master_tool.py
   ```

## Disclaimer

This tool is designed for authorized device management, testing, and debugging purposes using official Android APIs (ADB). It does **not** bypass security protocols or provide unauthorized root access. The creator is not responsible for any damage caused by misuse of ADB commands (e.g., deleting critical system files via shell).
