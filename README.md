# 📱 Android Master Tool (ADB Edition)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Platform: Android/Linux/Windows](https://img.shields.io/badge/Platform-Android%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#)

**Android Master Tool** is a high-performance, command-line utility designed for advanced Android device management and debugging. Built for developers and enthusiasts, it provides a unified interface to control your devices via ADB and Fastboot with precision and ease.

---

## 🌟 Key Features

### 🖥️ Professional Console UI
- **Unified Master Dashboard:** Access all features from a single, beautiful terminal interface.
- **Auto-Detection:** Instantly recognizes connected devices via USB or Wireless ADB.
- **Creator Credits:** Built-in professional branding and status indicators.

### 🛠️ Advanced Device Control
- **Media Suite:** Capture high-quality screenshots and record screen (30s) with one click.
- **Package Pro:** Batch install APKs, list 3rd party apps, and extract APKs from your phone to PC.
- **System Debloater:** Easily remove unwanted system apps/bloatware without root.
- **Input Simulator:** Send text or key events (Home, Back, etc.) remotely.

### ⚡ Power & Recovery
- **One-Tap Reboot:** Quickly jump to Recovery or Bootloader/Fastboot mode.
- **Fastboot Utilities:** Unlock bootloaders and flash root images directly from the tool.
- **Wireless ADB:** Setup and connect to your device over the network seamlessly.

### 📚 Knowledge Base
- **Rooting Roadmap:** Built-in step-by-step guide for unlocking and rooting modern devices.
- **Diagnostic Tools:** Real-time battery health, storage metrics, and process monitoring.

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.x**
- **ADB & Fastboot** tools installed on your system.
- **USB Debugging** enabled on your Android device.

### For Termux (Android)
```bash
pkg install python git nmap -y
git clone https://github.com/RamizUddin404/Android-Master-Tool.git
cd Android-Master-Tool
python android_master_tool.py
```

### For Linux/Windows
1. Clone the repository:
   ```bash
   git clone https://github.com/RamizUddin404/Android-Master-Tool.git
   ```
2. Navigate to the folder:
   ```bash
   cd Android-Master-Tool
   ```
3. Run the application:
   ```bash
   python android_master_tool.py
   ```

---

## 📸 Interface Preview
```text
    ╔══════════════════════════════════════════════════════════════════╗
    ║                >> THE ULTIMATE MASTER CONSOLE <<                 ║
    ║          ★ Created and Developed by: Ramiz Uddin ★               ║
    ╚══════════════════════════════════════════════════════════════════╝
    [*] Searching for devices in local environment...
    [+] DETECTED DEVICES: 1
    [1] ID: emulator-5554   | Model: Pixel 6 Pro     | Root: NO
```

---

## ⚖️ Disclaimer
This tool is intended for educational and authorized device management purposes only. It utilizes official Android APIs (ADB/Fastboot). The creator is not responsible for any misuse, data loss, or "bricking" of devices. **Always backup your data before performing advanced operations.**

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Developed with ❤️ by [Ramiz Uddin](https://github.com/RamizUddin404)**
