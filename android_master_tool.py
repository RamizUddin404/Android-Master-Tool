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
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def clear():
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def header(text):
        print(f"{UI.CYAN}┌{'─' * 50}┐{UI.END}")
        print(f"{UI.CYAN}│{UI.BOLD}{text.center(50)}{UI.END}{UI.CYAN}│{UI.END}")
        print(f"{UI.CYAN}└{'─' * 50}┘{UI.END}")

    @staticmethod
    def status(msg, type="info"):
        colors = {"info": UI.BLUE, "success": UI.GREEN, "warn": UI.YELLOW, "error": UI.RED}
        icons = {"info": "[*]", "success": "[+]", "warn": "[!]", "error": "[-]"}
        print(f"{colors.get(type, UI.END)}{icons.get(type, '[*]')} {msg}{UI.END}")

    @staticmethod
    def loading(msg, duration=1.5):
        print(f"{UI.YELLOW}{msg}", end="", flush=True)
        for _ in range(3):
            time.sleep(duration/3)
            print(".", end="", flush=True)
        print(f"{UI.END}")

class AndroidMasterTool:
    def __init__(self):
        self.adb = "adb"
        self.target = None

    def run(self, cmd):
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return res.stdout.strip()
        except: return ""

    def get_info(self, serial):
        model = self.run(f"{self.adb} -s {serial} shell getprop ro.product.model")
        ver = self.run(f"{self.adb} -s {serial} shell getprop ro.build.version.release")
        # Check root status (Safe/Read-only)
        root_check = self.run(f"{self.adb} -s {serial} shell which su")
        is_rooted = "YES" if root_check else "NO"
        return {"model": model, "ver": ver, "root": is_rooted}

    def banner(self):
        UI.clear()
        print(f"""{UI.PURPLE}{UI.BOLD}
    ╔══════════════════════════════════════════════════════════╗
    ║   █████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ██╗██████╗   ║
    ║  ██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗  ║
    ║  ███████║██╔██╗ ██║██║  ██║██████╔╝██║   ██║██║██║  ██║  ║
    ║  ██╔══██║██║╚██╗██║██║  ██║██╔══██╗██║   ██║██║██║  ██║  ║
    ║  ██║  ██║██║ ╚████║██████╔╝██║  ██║╚██████╔╝██║██████╔╝  ║
    ║  ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝   ║
    ║             > PREMIER DEVICE CONTROLLER <                ║
    ╚══════════════════════════════════════════════════════════╝{UI.END}""")

    def main_menu(self):
        while True:
            self.banner()
            UI.status("Searching for devices in local environment...")
            
            devices_raw = self.run(f"{self.adb} devices").split('\n')[1:]
            devices = [d.split('\t')[0] for d in devices_raw if '\tdevice' in d]

            if not devices:
                UI.status("No authorized devices found. Please check USB cable & Debugging.", "warn")
                UI.status("Retrying in 3 seconds... (Ctrl+C to Quit)", "info")
                time.sleep(3)
                continue

            UI.header(f"DETECTED DEVICES: {len(devices)}")
            for i, d in enumerate(devices):
                info = self.get_info(d)
                print(f"  {UI.GREEN}{UI.BOLD}[{i+1}]{UI.END} ID: {UI.CYAN}{d.ljust(15)}{UI.END} | Model: {UI.YELLOW}{info['model'].ljust(15)}{UI.END} | Root: {UI.RED}{info['root']}{UI.END}")

            choice = input(f"\n{UI.BOLD}➔ Select Device Index (q=Quit): {UI.END}")
            if choice.lower() == 'q': break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    self.target = devices[idx]
                    self.device_ops()
                else:
                    UI.status("Invalid device index!", "error")
                    time.sleep(1)
            except: pass

    def device_ops(self):
        while True:
            self.banner()
            info = self.get_info(self.target)
            UI.header(f"ACTIVE: {info['model']} (Android {info['ver']})")
            
            menu_items = [
                ("1", "System Diagnostics", "View Battery, Storage, Memory"),
                ("2", "Application Manager", "List/Manage installed apps"),
                ("3", "Display Capture", "Screenshots & Screen Recording"),
                ("4", "File Explorer", "Push/Pull files to/from device"),
                ("5", "Advanced Power", "Reboot to Recovery/Bootloader"),
                ("6", "Interactive Shell", "Open remote command terminal"),
                ("7", "Install Package", "Sideload APK files"),
                ("b", "Back to Home", "Return to device selection")
            ]

            for key, title, desc in menu_items:
                print(f"  {UI.GREEN}{UI.BOLD}[{key}]{UI.END} {UI.BOLD}{title.ljust(22)}{UI.END} {UI.BLUE}»{UI.END} {UI.CYAN}{desc}{UI.END}")

            cmd = input(f"\n{UI.BOLD}➔ Select Action: {UI.END}").lower()
            
            if cmd == '1': self.diag()
            elif cmd == '2': self.apps()
            elif cmd == '3': self.capture()
            elif cmd == '4': self.files()
            elif cmd == '5': self.reboot()
            elif cmd == '6': 
                UI.status("Launching shell... Type 'exit' to return.", "info")
                os.system(f"{self.adb} -s {self.target} shell")
            elif cmd == '7': self.install()
            elif cmd == 'b': break
            else: UI.status("Unknown command.", "error"); time.sleep(1)

    def diag(self):
        UI.header("SYSTEM DIAGNOSTICS")
        UI.status("Fetching hardware metrics...")
        print(f"\n{UI.BOLD}--- BATTERY ---{UI.END}")
        print(self.run(f"{self.adb} -s {self.target} shell dumpsys battery | grep -v 'm'"))
        print(f"\n{UI.BOLD}--- STORAGE ---{UI.END}")
        print(self.run(f"{self.adb} -s {self.target} shell df -h /data"))
        input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

    def apps(self):
        UI.header("APPLICATION MANAGER")
        UI.status("Loading package list...")
        apps = self.run(f"{self.adb} -s {self.target} shell pm list packages -3").replace("package:", "  • ")
        print(apps if apps else "  No 3rd party apps found.")
        input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

    def capture(self):
        UI.header("DISPLAY CAPTURE")
        print("  [1] Take Screenshot")
        print("  [2] Record Screen (30s)")
        sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
        ts = int(time.time())
        if sub == '1':
            fname = f"capture_{ts}.png"
            UI.loading("Processing image")
            self.run(f"{self.adb} -s {self.target} shell screencap -p /sdcard/{fname}")
            self.run(f"{self.adb} -s {self.target} pull /sdcard/{fname} .")
            self.run(f"{self.adb} -s {self.target} shell rm /sdcard/{fname}")
            UI.status(f"Saved to: {os.getcwd()}/{fname}", "success")
        elif sub == '2':
            fname = f"vid_{ts}.mp4"
            UI.status("Recording... (30s max)", "info")
            self.run(f"{self.adb} -s {self.target} shell screenrecord --time-limit 30 /sdcard/{fname}")
            UI.loading("Downloading video")
            self.run(f"{self.adb} -s {self.target} pull /sdcard/{fname} .")
            self.run(f"{self.adb} -s {self.target} shell rm /sdcard/{fname}")
            UI.status(f"Saved to: {os.getcwd()}/{fname}", "success")
        input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

    def files(self):
        UI.header("FILE EXPLORER")
        print("  [1] Pull (Device -> PC)")
        print("  [2] Push (PC -> Device)")
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

    def reboot(self):
        UI.header("POWER OPTIONS")
        print("  [1] System Reboot")
        print("  [2] Recovery Mode")
        print("  [3] Bootloader Mode")
        sub = input(f"\n{UI.BOLD}➔ Option: {UI.END}")
        modes = {'1': '', '2': 'recovery', '3': 'bootloader'}
        if sub in modes:
            UI.status("Sending reboot command...", "warn")
            self.run(f"{self.adb} -s {self.target} reboot {modes[sub]}")
            time.sleep(2)

    def install(self):
        UI.header("APK INSTALLER")
        path = input("  ➔ Drag APK here or enter path: ")
        if os.path.exists(path):
            UI.loading("Installing application")
            res = self.run(f"{self.adb} -s {self.target} install {path}")
            UI.status(res, "success" if "Success" in res else "error")
        else: UI.status("File not found!", "error")
        input(f"\n{UI.YELLOW}Press Enter to return...{UI.END}")

if __name__ == "__main__":
    try:
        AndroidMasterTool().main_menu()
    except KeyboardInterrupt:
        print(f"\n{UI.RED}[!] Tool terminated by user.{UI.END}")
        sys.exit(0)
