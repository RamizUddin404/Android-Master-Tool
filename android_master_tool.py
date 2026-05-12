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

    @staticmethod
    def loading(msg, duration=1.0):
        print(f"{UI.YELLOW}{msg}", end="", flush=True)
        for _ in range(3):
            time.sleep(duration/3)
            print(".", end="", flush=True)
        print(f"{UI.END}")

class AndroidMasterTool:
    def __init__(self):
        self.adb = "adb"
        self.fastboot = "fastboot"
        self.target = None

    def run(self, cmd):
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode != 0:
                return f"Error: {res.stderr.strip()}"
            return res.stdout.strip()
        except Exception as e:
            return f"Error: {str(e)}"

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
    ║              {UI.GREEN}● Status: 100% Real & Working Mode ●{UI.PURPLE}            ║
    ╚══════════════════════════════════════════════════════════════╝{UI.END}""")

    def main_menu(self):
        while True:
            self.banner()
            print(f"  {UI.YELLOW}{UI.BOLD}[1] VIEW TOOL CAPABILITIES (Explore Features){UI.END}")
            print(f"  {UI.GREEN}{UI.BOLD}[2] ROOTING KNOWLEDGE BASE (Step-by-Step Guides){UI.END}")
            print(f"  {UI.CYAN}{UI.BOLD}[3] START ACTIVE USB MODE (ADB - For Power-On Devices){UI.END}")
            print(f"  {UI.PURPLE}{UI.BOLD}[4] FASTBOOT MODE (Rooting / Unlocking / Flashing){UI.END}")
            print(f"  {UI.RED}{UI.BOLD}[Q] EXIT TOOL{UI.END}")
            
            choice = input(f"\n{UI.BOLD}➔ Select Mode: {UI.END}").lower()
            
            if choice == '1': self.preview_features()
            elif choice == '2': self.rooting_guides()
            elif choice == '3': self.active_usb_mode()
            elif choice == '4': self.fastboot_mode()
            elif choice == 'q': break

    def preview_features(self):
        self.banner()
        UI.header("TOOL CAPABILITIES PREVIEW")
        features = [
            ("System Diagnostics", "Real-time Battery, Storage, and RAM monitoring."),
            ("Remote File Control", "Bi-directional file transfer (Push/Pull)."),
            ("Media Operation", "Capture screen/video directly to your storage."),
            ("Package Manager", "Sideload APKs and manage app packages."),
            ("App Extraction", "Backup any installed app into a shareable APK."),
            ("Network & Debug", "Live Logcat and detailed Network/IP analysis."),
            ("Power Automation", "Force reboot to Fastboot/Recovery while phone is ON."),
            ("Root & Unlock", "Direct Fastboot commands for flashing & unlocking.")
        ]
        for title, desc in features:
            print(f"  {UI.BLUE}• {UI.BOLD}{title.ljust(25)}{UI.END} {UI.CYAN}→ {desc}{UI.END}")
        input(f"\n{UI.YELLOW}Press Enter to go back...{UI.END}")

    def rooting_guides(self):
        self.banner()
        UI.header("ROOTING & UNLOCKING ROADMAP")
        UI.status("Follow these steps for a successful operation:", "info")
        steps = [
            "1. Unlock Developer Options (Tap Build Number 7 times).",
            "2. Enable USB Debugging & OEM Unlocking in Settings.",
            "3. Connect to PC and select 'Active USB Mode' in this tool.",
            "4. Use 'Power Menu' [0] -> 'Fastboot' [3] to reboot phone.",
            "5. Once in Fastboot, use 'Fastboot Mode' [4] to Unlock/Flash."
        ]
        for step in steps: print(f"  {UI.GREEN}{step}{UI.END}")
        input(f"\n{UI.YELLOW}Press Enter to go back...{UI.END}")

    def active_usb_mode(self):
        while True:
            self.banner()
            UI.status("Initializing ADB Engine...")
            devices_raw = self.run(f"{self.adb} devices").split('\n')[1:]
            devices = [d.split('\t')[0] for d in devices_raw if '\tdevice' in d]

            if not devices:
                UI.status("No device detected. Is the phone ON and connected?", "warn")
                UI.status("Please check USB cable & Debugging permissions.", "info")
                print(f"  {UI.YELLOW}(Press Ctrl+C to return to Main Menu){UI.END}")
                try: time.sleep(3)
                except KeyboardInterrupt: break
                continue

            UI.header(f"DEVICES ONLINE: {len(devices)}")
            for i, d in enumerate(devices):
                model = self.run(f"{self.adb} -s {d} shell getprop ro.product.model")
                print(f"  {UI.GREEN}[{i+1}] Device ID: {d} | Model: {model}{UI.END}")

            choice = input(f"\n{UI.BOLD}➔ Select Device (b=Back): {UI.END}").lower()
            if choice == 'b': break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    self.target = devices[idx]
                    self.device_ops()
                else: UI.status("Invalid index.", "error"); time.sleep(1)
            except: pass

    def fastboot_mode(self):
        while True:
            self.banner()
            UI.header("FASTBOOT / BOOTLOADER CONSOLE")
            UI.status("Phone MUST be in Fastboot Mode for these to work.", "warn")
            
            print(f"  {UI.GREEN}[1]{UI.END} List Devices      {UI.CYAN}[2]{UI.END} Unlock (Standard)")
            print(f"  {UI.YELLOW}[3]{UI.END} Unlock (OEM/Old)  {UI.RED}[4]{UI.END} Flash Root Image")
            print(f"  {UI.BLUE}[5]{UI.END} Reboot to System  {UI.RED}[b]{UI.END} Back to Main")
            
            cmd = input(f"\n{UI.BOLD}➔ Fastboot Command: {UI.END}").lower()
            
            if cmd == 'b': break
            elif cmd == '1':
                UI.status("Scanning Fastboot Devices...")
                res = self.run(f"{self.fastboot} devices")
                print(res if res else "No devices in Fastboot mode.")
                input(f"\n{UI.YELLOW}Press Enter...{UI.END}")
            elif cmd == '2':
                UI.status("Sending: fastboot flashing unlock", "warn")
                print(self.run(f"{self.fastboot} flashing unlock"))
                input(f"\n{UI.YELLOW}Press Enter...{UI.END}")
            elif cmd == '3':
                UI.status("Sending: fastboot oem unlock", "warn")
                print(self.run(f"{self.fastboot} oem unlock"))
                input(f"\n{UI.YELLOW}Press Enter...{UI.END}")
            elif cmd == '4':
                UI.header("ROOT FLASHING")
                path = input("  ➔ Path to Patched Boot Image: ")
                if os.path.exists(path):
                    UI.loading("Flashing boot partition")
                    print(self.run(f"{self.fastboot} flash boot {path}"))
                else: UI.status("File not found!", "error")
                input(f"\n{UI.YELLOW}Press Enter...{UI.END}")
            elif cmd == '5':
                UI.status("Rebooting...")
                self.run(f"{self.fastboot} reboot")
                break

    def device_ops(self):
        while True:
            self.banner()
            UI.header(f"ACTIVE CONTROL: {self.target}")
            
            menu_items = [
                ("1", "Hardware Info", "2", "File Manager"),
                ("3", "Media Capture", "4", "App Manager"),
                ("5", "Extract APK", "6", "Network Info"),
                ("7", "Process List", "8", "Live Logcat"),
                ("9", "Remote Shell", "R", "REBOOT TO BOOTLOADER"),
                ("0", "FULL POWER MENU", "b", "Back to Devices"),
            ]
            
            for k1, v1, k2, v2 in menu_items:
                print(f"  {UI.GREEN}[{k1}]{UI.END} {UI.BOLD}{v1.ljust(22)}{UI.END} |  {UI.GREEN}[{k2}]{UI.END} {UI.BOLD}{v2}{UI.END}")
            
            cmd = input(f"\n{UI.BOLD}➔ Select Action: {UI.END}").lower()
            if cmd == 'b': break
            elif cmd == 'r':
                UI.status("Sending: adb reboot bootloader", "warn")
                self.run(f"{self.adb} -s {self.target} reboot bootloader")
                UI.status("Device should be rebooting to Bootloader/Fastboot.", "success")
                time.sleep(2)
                break # Return to device list as it will disconnect
            else:
                self.execute_command(cmd)

    def execute_command(self, cmd):
        if cmd == '1':
            UI.header("HARDWARE DIAGNOSTICS")
            print(f"\n{UI.BOLD}--- BATTERY ---{UI.END}")
            print(self.run(f"{self.adb} -s {self.target} shell dumpsys battery | grep -v 'm'"))
            print(f"\n{UI.BOLD}--- STORAGE ---{UI.END}")
            print(self.run(f"{self.adb} -s {self.target} shell df -h /data"))
            input(f"\n{UI.YELLOW}Press Enter...{UI.END}")
            
        elif cmd == '2':
            UI.header("FILE MANAGER")
            print("  [1] Pull (Download) [2] Push (Upload)")
            sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
            if sub == '1':
                rem = input("  Device Path: ")
                res = self.run(f"{self.adb} -s {self.target} pull {rem} .")
                UI.status(res, "success" if "pulled" in res.lower() else "info")
            elif sub == '2':
                loc = input("  Local Path: ")
                if os.path.exists(loc):
                    res = self.run(f"{self.adb} -s {self.target} push {loc} /sdcard/")
                    UI.status(res, "success")
                else: UI.status("Local file not found!", "error")
            input(f"\n{UI.YELLOW}Press Enter...{UI.END}")
            
        elif cmd == '3':
            UI.header("MEDIA CAPTURE")
            print("  [1] Screenshot  [2] Screen Record (30s)")
            sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
            ts = int(time.time())
            if sub == '1':
                fname = f"cap_{ts}.png"
                self.run(f"{self.adb} -s {self.target} shell screencap -p /sdcard/{fname}")
                self.run(f"{self.adb} -s {self.target} pull /sdcard/{fname} .")
                self.run(f"{self.adb} -s {self.target} shell rm /sdcard/{fname}")
                UI.status(f"Captured: {fname}", "success")
            elif sub == '2':
                fname = f"rec_{ts}.mp4"
                UI.status("Recording now... Stay on the screen.", "info")
                self.run(f"{self.adb} -s {self.target} shell screenrecord --time-limit 30 /sdcard/{fname}")
                UI.loading("Downloading video")
                self.run(f"{self.adb} -s {self.target} pull /sdcard/{fname} .")
                self.run(f"{self.adb} -s {self.target} shell rm /sdcard/{fname}")
                UI.status(f"Saved: {fname}", "success")
            input(f"\n{UI.YELLOW}Press Enter...{UI.END}")
            
        elif cmd == '4':
            UI.header("APP MANAGER")
            print("  [1] List Apps  [2] Install APK")
            sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
            if sub == '1':
                print(self.run(f"{self.adb} -s {self.target} shell pm list packages -3").replace("package:", " • "))
            elif sub == '2':
                path = input("  ➔ APK Path: ")
                if os.path.exists(path):
                    UI.loading("Installing")
                    print(self.run(f"{self.adb} -s {self.target} install {path}"))
                else: UI.status("File not found!", "error")
            input(f"\n{UI.YELLOW}Press Enter...{UI.END}")
            
        elif cmd == '5':
            UI.header("APK EXTRACTION (BACKUP)")
            pkg = input("  ➔ Enter Package Name: ")
            path_info = self.run(f"{self.adb} -s {self.target} shell pm path {pkg}")
            if "package:" in path_info:
                apk_path = path_info.replace("package:", "").strip()
                UI.loading(f"Extracting {pkg}")
                self.run(f"{self.adb} -s {self.target} pull {apk_path} {pkg}.apk")
                UI.status(f"Backup saved: {pkg}.apk", "success")
            else: UI.status("Package not found!", "error")
            input(f"\n{UI.YELLOW}Press Enter...{UI.END}")

        elif cmd == '6':
            UI.header("NETWORK INFO")
            print(self.run(f"{self.adb} -s {self.target} shell ip addr show wlan0"))
            input(f"\n{UI.YELLOW}Press Enter...{UI.END}")

        elif cmd == '7':
            UI.header("PROCESS LIST (TOP)")
            print(self.run(f"{self.adb} -s {self.target} shell top -n 1 -m 10"))
            input(f"\n{UI.YELLOW}Press Enter...{UI.END}")

        elif cmd == '8':
            UI.header("LOGCAT DEBUGGER")
            print(self.run(f"{self.adb} -s {self.target} logcat -d -t 50"))
            input(f"\n{UI.YELLOW}Press Enter...{UI.END}")

        elif cmd == '9':
            UI.status("Launching Terminal. Type 'exit' to quit.", "info")
            os.system(f"{self.adb} -s {self.target} shell")

        elif cmd == '0':
            UI.header("FORCE POWER COMMANDS")
            print(f"{UI.RED}{UI.BOLD}Phone will reboot immediately!{UI.END}")
            print("  [1] Normal Reboot\n  [2] Recovery Mode\n  [3] FASTBOOT / BOOTLOADER")
            sub = input(f"\n{UI.BOLD}➔ Force Option: {UI.END}")
            modes = {'1': '', '2': 'recovery', '3': 'bootloader'}
            if sub in modes:
                UI.status(f"Sending Force Reboot to {modes[sub] if modes[sub] else 'System'}...", "warn")
                self.run(f"{self.adb} -s {self.target} reboot {modes[sub]}")
                UI.status("Command sent! Device should be rebooting.", "success")
                time.sleep(3)
        else: UI.status("Invalid command.", "error"); time.sleep(1)

if __name__ == "__main__":
    try:
        AndroidMasterTool().main_menu()
    except KeyboardInterrupt:
        print(f"\n{UI.RED}[!] Session Terminated.{UI.END}")
        sys.exit(0)
