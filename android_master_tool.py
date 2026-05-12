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
        print(f"{UI.CYAN}┌{'─' * 66}┐{UI.END}")
        print(f"{UI.CYAN}│{UI.BOLD}{text.center(66)}{UI.END}{UI.CYAN}│{UI.END}")
        print(f"{UI.CYAN}└{'─' * 66}┘{UI.END}")

    @staticmethod
    def status(msg, type="info"):
        colors = {"info": UI.BLUE, "success": UI.GREEN, "warn": UI.YELLOW, "error": UI.RED}
        icons = {"info": "[*]", "success": "[+]", "warn": "[!]", "error": "[-]"}
        print(f"{colors.get(type, UI.END)}{icons.get(type, '[*]')} {msg}{UI.END}")

    @staticmethod
    def loading(msg, duration=0.8):
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
            return res.stdout.strip() if res.returncode == 0 else f"Error: {res.stderr.strip()}"
        except Exception as e: return f"Error: {str(e)}"

    def get_connection_status(self):
        devices_raw = subprocess.run(f"{self.adb} devices", shell=True, capture_output=True, text=True).stdout.split('\n')[1:]
        devices = [d.split('\t')[0] for d in devices_raw if '\tdevice' in d]
        if devices:
            if not self.target or self.target not in devices:
                self.target = devices[0]
            model = self.run(f"{self.adb} -s {self.target} shell getprop ro.product.model")
            return f"{UI.GREEN}CONNECTED: {model} ({self.target}){UI.END}"
        
        fast_raw = subprocess.run(f"{self.fastboot} devices", shell=True, capture_output=True, text=True).stdout.strip()
        if fast_raw:
            return f"{UI.PURPLE}MODE: FASTBOOT DETECTED{UI.END}"
            
        return f"{UI.RED}STATUS: DISCONNECTED (Plug USB Now){UI.END}"

    def banner(self):
        UI.clear()
        print(f"""{UI.PURPLE}{UI.BOLD}
    ╔══════════════════════════════════════════════════════════════════╗
    ║    █████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ██╗██████╗          ║
    ║   ██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗         ║
    ║   ███████║██╔██╗ ██║██║  ██║██████╔╝██║   ██║██║██║  ██║         ║
    ║   ██╔══██║██║╚██╗██║██║  ██║██╔══██╗██║   ██║██║██║  ██║         ║
    ║   ██║  ██║██║ ╚████║██████╔╝██║  ██║╚██████╔╝██║██████╔╝         ║
    ║   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝          ║
    ║                                                                  ║
    ║                >> THE ULTIMATE MASTER CONSOLE <<                 ║
    ║          {UI.CYAN}★ Created and Developed by: {UI.YELLOW}Ramiz Uddin{UI.PURPLE} ★             ║
    ╚══════════════════════════════════════════════════════════════════╝{UI.END}""")
        print(f"  {self.get_connection_status().center(70)}")
        print(f"  {UI.BLUE}{'─' * 66}{UI.END}")

    def ensure_device(self):
        status = self.get_connection_status()
        if "DISCONNECTED" in status:
            UI.status("Action Required: Please connect your phone with USB Debugging enabled.", "warn")
            input(f"\n{UI.YELLOW}Press Enter to retry connection...{UI.END}")
            return False
        return True

    def ensure_fastboot(self):
        status = self.get_connection_status()
        if "FASTBOOT" not in status:
            UI.status("Action Required: Phone must be in FASTBOOT mode for this.", "error")
            input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")
            return False
        return True

    def main_menu(self):
        while True:
            self.banner()
            menu = [
                ("1", "Hardware Info", "2", "File & Batch APK"),
                ("3", "Media Capture", "4", "App Manager"),
                ("5", "Extract APK", "6", "Network & Ports"),
                ("7", "Process List", "8", "Live Logcat"),
                ("D", "System Debloater", "I", "Input Simulator"),
                ("S", "Screen Config", "W", "Wireless ADB Setup"),
                ("H", "Device Health", "L", "Logcat Saver"),
                ("R", "REBOOT TO BOOTLOADER", "U", "UNLOCK BOOTLOADER"),
                ("F", "FLASH ROOT IMAGE", "K", "ROOT KNOWLEDGE BASE"),
                ("0", "FULL POWER MENU", "Q", "EXIT CONSOLE"),
            ]
            
            for k1, v1, k2, v2 in menu:
                print(f"  {UI.GREEN}[{k1}]{UI.END} {UI.BOLD}{v1.ljust(22)}{UI.END} |  {UI.GREEN}[{k2}]{UI.END} {UI.BOLD}{v2}{UI.END}")
            
            cmd = input(f"\n{UI.BOLD}➔ Select Action: {UI.END}").lower()
            if cmd == 'q': break
            elif cmd == 'k': self.rooting_guides()
            elif cmd in ['r', 'u', 'f']: # Fastboot/Unlock related
                if self.ensure_fastboot() if cmd != 'r' else self.ensure_device():
                    self.execute_fastboot(cmd)
            else:
                if self.ensure_device():
                    self.execute_adb(cmd)

    def rooting_guides(self):
        UI.header("ROOTING & UNLOCKING ROADMAP")
        steps = [
            "1. Unlock Developer Options (Tap Build Number 7 times).",
            "2. Enable USB Debugging & OEM Unlocking in Settings.",
            "3. Connect to PC and use 'REBOOT TO BOOTLOADER' [R].",
            "4. In Fastboot Mode, use 'UNLOCK BOOTLOADER' [U].",
            "5. Finally, use 'FLASH ROOT IMAGE' [F] with your patched boot.img."
        ]
        for step in steps: print(f"  {UI.GREEN}{step}{UI.END}")
        input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

    def execute_adb(self, cmd):
        if cmd == '1':
            UI.header("HARDWARE DIAGNOSTICS")
            print(f"\n{UI.BOLD}--- BATTERY ---{UI.END}\n{self.run(f'{self.adb} -s {self.target} shell dumpsys battery | grep -v m')}")
            print(f"\n{UI.BOLD}--- STORAGE ---{UI.END}\n{self.run(f'{self.adb} -s {self.target} shell df -h /data')}")
        elif cmd == '2':
            UI.header("FILE & BATCH APK")
            print("  [1] Pull [2] Push [3] Batch Install APKs")
            sub = input("➔ Option: ")
            if sub == '3':
                folder = input("➔ Folder Path: ")
                if os.path.isdir(folder):
                    for apk in [f for f in os.listdir(folder) if f.endswith('.apk')]:
                        UI.status(f"Installing {apk}..."); self.run(f"{self.adb} -s {self.target} install '{os.path.join(folder, apk)}'")
            else: UI.status("Basic transfer logic ready.", "info")
        elif cmd == '3':
            UI.header("MEDIA CAPTURE")
            print("  [1] Screenshot  [2] Screen Record (30s)")
            sub = input("➔ Option: ")
            ts = int(time.time())
            if sub == '1':
                self.run(f"{self.adb} -s {self.target} shell screencap -p /sdcard/c.png")
                self.run(f"{self.adb} -s {self.target} pull /sdcard/c.png cap_{ts}.png")
                UI.status(f"Saved: cap_{ts}.png", "success")
        elif cmd == '5':
            pkg = input("➔ Package Name: ")
            path = self.run(f"{self.adb} -s {self.target} shell pm path {pkg}").replace("package:", "").strip()
            if path: self.run(f"{self.adb} -s {self.target} pull {path} {pkg}.apk"); UI.status("Extracted.", "success")
        elif cmd == 'd':
            pkg = input("➔ Package to Remove: ")
            UI.status(self.run(f"{self.adb} -s {self.target} shell pm uninstall -k --user 0 {pkg}"))
        elif cmd == 'i':
            UI.header("INPUT SIMULATOR")
            txt = input("➔ Text to Type (or leave empty for Home): ")
            if txt: self.run(f"{self.adb} -s {self.target} shell input text '{txt}'")
            else: self.run(f"{self.adb} -s {self.target} shell input keyevent 3")
        elif cmd == 'w':
            self.run(f"{self.adb} -s {self.target} tcpip 5555")
            UI.status("Wireless ADB on port 5555 enabled.", "success")
        elif cmd == 'h':
            UI.header("DEVICE HEALTH")
            print(self.run(f"{self.adb} -s {self.target} shell dumpsys thermalservice"))
        elif cmd == '0':
            UI.header("POWER MENU")
            print("  [1] Normal [2] Recovery [3] Bootloader")
            sub = input("➔ Option: ")
            modes = {'1': '', '2': 'recovery', '3': 'bootloader'}
            if sub in modes: self.run(f"{self.adb} -s {self.target} reboot {modes[sub]}")
        
        input(f"\n{UI.YELLOW}Press Enter to continue...{UI.END}")

    def execute_fastboot(self, cmd):
        if cmd == 'r':
            UI.status("Rebooting to Bootloader...", "warn")
            self.run(f"{self.adb} -s {self.target} reboot bootloader")
        elif cmd == 'u':
            UI.header("BOOTLOADER UNLOCK")
            UI.status("Sending: fastboot flashing unlock", "warn")
            print(self.run(f"{self.fastboot} flashing unlock"))
        elif cmd == 'f':
            UI.header("FLASH ROOT")
            path = input("➔ Path to patched_boot.img: ")
            if os.path.exists(path):
                UI.status("Flashing...", "warn")
                print(self.run(f"{self.fastboot} flash boot {path}"))
        
        input(f"\n{UI.YELLOW}Press Enter to continue...{UI.END}")

if __name__ == "__main__":
    try: AndroidMasterTool().main_menu()
    except KeyboardInterrupt: sys.exit(0)
