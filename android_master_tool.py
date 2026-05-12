import subprocess
import os
import sys
import time

# --- UI CONSTANTS & COLORS ---
class UI:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    @staticmethod
    def clear():
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def header(text):
        print(f"{UI.CYAN}┌{'─' * 60}┐{UI.END}")
        print(f"{UI.CYAN}│{UI.BOLD}{text.center(60)}{UI.END}{UI.CYAN}│{UI.END}")
        print(f"{UI.CYAN}└{'─' * 60}┘{UI.END}")

    @staticmethod
    def status(msg, type="info"):
        colors = {"info": UI.BLUE, "success": UI.GREEN, "warn": UI.YELLOW, "error": UI.RED}
        icons = {"info": "[*]", "success": "[+]", "warn": "[!]", "error": "[-]"}
        print(f"{colors.get(type, UI.END)}{icons.get(type, '[*]')} {msg}{UI.END}")

class AndroidMasterTool:
    def __init__(self):
        self.adb = "adb"
        self.target = None

    def run(self, cmd):
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return res.stdout.strip()
        except: return ""

    def banner(self):
        UI.clear()
        print(f"""{UI.PURPLE}{UI.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║    █████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ██╗██████╗      ║
    ║   ██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗     ║
    ║   ███████║██╔██╗ ██║██║  ██║██████╔╝██║   ██║██║██║  ██║     ║
    ║   ██╔══██║██║╚██╗██║██║  ██║██╔══██╗██║   ██║██║██║  ██║     ║
    ║   ██║  ██║██║ ╚████║██████╔╝██║  ██║╚██████╔╝██║██████╔╝     ║
    ║   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝      ║
    ║                                                              ║
    ║              >> THE ULTIMATE DIGITAL CONSOLE <<              ║
    ║        {UI.CYAN}★ Created and Developed by: {UI.YELLOW}Ramiz Uddin{UI.PURPLE} ★           ║
    ╚══════════════════════════════════════════════════════════════╝{UI.END}""")

    def main_menu(self):
        while True:
            self.banner()
            print(f"  {UI.YELLOW}{UI.BOLD}[1] VIEW TOOL CAPABILITIES (Explore Features){UI.END}")
            print(f"  {UI.GREEN}{UI.BOLD}[2] ROOTING KNOWLEDGE BASE (Step-by-Step Guides){UI.END}")
            print(f"  {UI.CYAN}{UI.BOLD}[3] START ACTIVE USB MODE (Connect Device Now){UI.END}")
            print(f"  {UI.RED}{UI.BOLD}[Q] EXIT TOOL{UI.END}")
            
            choice = input(f"\n{UI.BOLD}➔ Select Mode: {UI.END}").lower()
            
            if choice == '1': self.preview_features()
            elif choice == '2': self.rooting_guides()
            elif choice == '3': self.active_usb_mode()
            elif choice == 'q': break

    def preview_features(self):
        self.banner()
        UI.header("TOOL CAPABILITIES PREVIEW")
        features = [
            ("System Diagnostics", "Battery, Storage, RAM, and Kernel Info."),
            ("Remote File Control", "Transfer files between PC and Android seamlessly."),
            ("Media Operation", "Capture screenshots and screen records."),
            ("Package Manager", "List, uninstall, and sideload APKs."),
            ("App Extraction", "Backup installed applications to your PC."),
            ("Network Info", "View IP, MAC addresses, and connection status."),
            ("Logcat Debugger", "View real-time system logs for app debugging."),
            ("Terminal Shell", "Direct shell access (root-level if rooted).")
        ]
        for title, desc in features:
            print(f"  {UI.BLUE}• {UI.BOLD}{title.ljust(25)}{UI.END} {UI.CYAN}→ {desc}{UI.END}")
        input(f"\n{UI.YELLOW}Press Enter to go back...{UI.END}")

    def rooting_guides(self):
        self.banner()
        UI.header("STEP-BY-STEP ROOTING KNOWLEDGE")
        print(f"{UI.BOLD}Note: Rooting cannot be 100% automated due to security protocols.{UI.END}")
        print(f"{UI.BOLD}General Process for Most Devices:{UI.END}")
        steps = [
            "1. Backup all your data (Everything will be wiped).",
            "2. Enable Developer Options & OEM Unlocking in Settings.",
            "3. Unlock Bootloader (Specific to each brand via Fastboot/Tool).",
            "4. Download Official Firmware for your EXACT Model/Version.",
            "5. Extract 'boot.img' and patch it using Magisk App.",
            "6. Flash the 'patched_boot.img' via Fastboot or Custom Recovery."
        ]
        for step in steps: print(f"  {UI.GREEN}{step}{UI.END}")
        
        print(f"\n{UI.BOLD}Brand Specific Resources:{UI.END}")
        print(f"  {UI.CYAN}- Samsung:{UI.END} SamMobile or Frija (Use Odin to flash)")
        print(f"  {UI.CYAN}- Xiaomi:{UI.END} Mi Firmware or MiFlash Tool")
        print(f"  {UI.CYAN}- Others:{UI.END} XDA-Developers (Search your exact model)")
        input(f"\n{UI.YELLOW}Press Enter to go back...{UI.END}")

    def active_usb_mode(self):
        while True:
            self.banner()
            UI.status("Initializing ADB Engine...")
            devices_raw = self.run(f"{self.adb} devices").split('\n')[1:]
            devices = [d.split('\t')[0] for d in devices_raw if '\tdevice' in d]

            if not devices:
                UI.status("Waiting for USB Connection...", "warn")
                UI.status("Please connect your phone and allow USB Debugging.", "info")
                print(f"  {UI.YELLOW}(Press Ctrl+C to return to Main Menu){UI.END}")
                try: time.sleep(3)
                except KeyboardInterrupt: break
                continue

            UI.header(f"ACTIVE CONNECTIONS: {len(devices)}")
            for i, d in enumerate(devices):
                model = self.run(f"{self.adb} -s {d} shell getprop ro.product.model")
                print(f"  {UI.GREEN}[{i+1}] Device ID: {d} | Model: {model}{UI.END}")

            choice = input(f"\n{UI.BOLD}➔ Select Device Index (b=Back): {UI.END}").lower()
            if choice == 'b': break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    self.target = devices[idx]
                    self.device_ops()
                else: UI.status("Invalid selection.", "error"); time.sleep(1)
            except: pass

    def device_ops(self):
        while True:
            self.banner()
            UI.header(f"CONNECTED TO: {self.target}")
            
            menu_items = [
                ("1", "System Info", "2", "File Explorer"),
                ("3", "Media Capture", "4", "App Manager (Install/List)"),
                ("5", "Extract App (Backup)", "6", "Network Information"),
                ("7", "Process Manager (Top)", "8", "Logcat (View System Logs)"),
                ("9", "Open Shell", "0", "Power Menu (Reboot)"),
            ]
            
            for k1, v1, k2, v2 in menu_items:
                print(f"  {UI.GREEN}[{k1}]{UI.END} {UI.BOLD}{v1.ljust(25)}{UI.END} |  {UI.GREEN}[{k2}]{UI.END} {UI.BOLD}{v2}{UI.END}")
            print(f"  {UI.YELLOW}[b]{UI.END} {UI.BOLD}Back to Connection List{UI.END}")
            
            cmd = input(f"\n{UI.BOLD}➔ Command: {UI.END}").lower()
            if cmd == 'b': break
            
            self.execute_command(cmd)

    def execute_command(self, cmd):
        if cmd == '1':
            UI.header("SYSTEM DIAGNOSTICS")
            print(f"\n{UI.BOLD}--- BATTERY ---{UI.END}")
            print(self.run(f"{self.adb} -s {self.target} shell dumpsys battery | grep -v 'm'"))
            print(f"\n{UI.BOLD}--- STORAGE ---{UI.END}")
            print(self.run(f"{self.adb} -s {self.target} shell df -h /data"))
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")
            
        elif cmd == '2':
            UI.header("FILE EXPLORER")
            print("  [1] Pull (Device -> PC)\n  [2] Push (PC -> Device)")
            sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
            if sub == '1':
                rem = input("  Source (Device path): ")
                self.run(f"{self.adb} -s {self.target} pull {rem} .")
                UI.status("Transfer complete.", "success")
            elif sub == '2':
                loc = input("  Source (Local path): ")
                dest = input("  Dest (Device path, default /sdcard/): ") or "/sdcard/"
                if os.path.exists(loc):
                    self.run(f"{self.adb} -s {self.target} push {loc} {dest}")
                    UI.status("Transfer complete.", "success")
                else: UI.status("Local file not found!", "error")
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")
            
        elif cmd == '3':
            UI.header("MEDIA CAPTURE")
            print("  [1] Take Screenshot\n  [2] Record Screen (30s)")
            sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
            ts = int(time.time())
            if sub == '1':
                fname = f"capture_{ts}.png"
                self.run(f"{self.adb} -s {self.target} shell screencap -p /sdcard/{fname}")
                self.run(f"{self.adb} -s {self.target} pull /sdcard/{fname} .")
                self.run(f"{self.adb} -s {self.target} shell rm /sdcard/{fname}")
                UI.status(f"Saved to: {os.getcwd()}/{fname}", "success")
            elif sub == '2':
                fname = f"vid_{ts}.mp4"
                UI.status("Recording... (30s max)", "info")
                self.run(f"{self.adb} -s {self.target} shell screenrecord --time-limit 30 /sdcard/{fname}")
                self.run(f"{self.adb} -s {self.target} pull /sdcard/{fname} .")
                self.run(f"{self.adb} -s {self.target} shell rm /sdcard/{fname}")
                UI.status(f"Saved to: {os.getcwd()}/{fname}", "success")
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")
            
        elif cmd == '4':
            UI.header("APP MANAGER")
            print("  [1] List 3rd Party Apps\n  [2] Install APK")
            sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
            if sub == '1':
                apps = self.run(f"{self.adb} -s {self.target} shell pm list packages -3").replace("package:", "  • ")
                print(apps if apps else "  No apps found.")
            elif sub == '2':
                path = input("  ➔ Enter APK path: ")
                if os.path.exists(path):
                    res = self.run(f"{self.adb} -s {self.target} install {path}")
                    UI.status(res, "success" if "Success" in res else "error")
                else: UI.status("File not found!", "error")
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")
            
        elif cmd == '5':
            UI.header("EXTRACT APP (BACKUP)")
            pkg = input("  ➔ Enter Package Name (e.g., com.example.app): ")
            path_info = self.run(f"{self.adb} -s {self.target} shell pm path {pkg}")
            if "package:" in path_info:
                apk_path = path_info.replace("package:", "").strip()
                UI.status(f"Found APK at {apk_path}. Pulling...")
                self.run(f"{self.adb} -s {self.target} pull {apk_path} {pkg}.apk")
                UI.status(f"Saved as {pkg}.apk", "success")
            else:
                UI.status("Package not found.", "error")
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

        elif cmd == '6':
            UI.header("NETWORK INFORMATION")
            print(f"\n{UI.BOLD}--- IP & MAC Address ---{UI.END}")
            print(self.run(f"{self.adb} -s {self.target} shell ip addr show wlan0"))
            print(f"\n{UI.BOLD}--- Wi-Fi Status ---{UI.END}")
            print(self.run(f"{self.adb} -s {self.target} shell dumpsys wifi | grep 'mNetworkInfo'"))
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

        elif cmd == '7':
            UI.header("PROCESS MANAGER (Top 10)")
            print(self.run(f"{self.adb} -s {self.target} shell top -n 1 -m 10"))
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

        elif cmd == '8':
            UI.header("LOGCAT DEBUGGER")
            UI.status("Fetching last 50 lines of system log...")
            print(self.run(f"{self.adb} -s {self.target} logcat -d -t 50"))
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

        elif cmd == '9':
            UI.status("Launching shell... Type 'exit' to return.", "info")
            os.system(f"{self.adb} -s {self.target} shell")

        elif cmd == '0':
            UI.header("POWER OPTIONS")
            print("  [1] Normal Reboot  [2] Recovery  [3] Bootloader")
            sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
            modes = {'1': '', '2': 'recovery', '3': 'bootloader'}
            if sub in modes:
                UI.status("Sending reboot command...", "warn")
                self.run(f"{self.adb} -s {self.target} reboot {modes[sub]}")
                time.sleep(2)
        else:
            UI.status("Unknown command.", "error"); time.sleep(1)

if __name__ == "__main__":
    try:
        AndroidMasterTool().main_menu()
    except KeyboardInterrupt:
        print(f"\n{UI.RED}[!] Tool terminated by user.{UI.END}")
        sys.exit(0)
