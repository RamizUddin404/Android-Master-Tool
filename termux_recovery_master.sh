#!/bin/bash

# ====================================================================
# 🔥 TERMUX RECOVERY MASTER v2.0 (The "Full Same" Edition) 🔥
# Professional Android Flashing & Maintenance Suite (OTG Support)
# Works on: Android (Root/Non-Root) | Linux | Chromebook
# ====================================================================

# --- Color Definitions ---
RESET='\033[0m'; BOLD='\033[1m'; RED='\033[0;31m'; GREEN='\033[0;32m'
YELLOW='\033[0;33m'; BLUE='\033[0;34m'; MAGENTA='\033[0;35m'; CYAN='\033[0;36m'
WHITE='\033[1;37m'; BG_BLUE='\033[44m'

# --- Configuration ---
INSTALL_DIR="$HOME/.recovery_master"
mkdir -p "$INSTALL_DIR" "$INSTALL_DIR/downloads"

# Platform Detection
IS_TERMUX=false; [[ -d "/data/data/com.termux/files/usr" ]] && IS_TERMUX=true
ANDROID=false; [[ "$IS_TERMUX" == "true" ]] && ANDROID=true

# --- UI Components ---
banner() {
    clear
    echo -e "${CYAN}"
    echo "  ██████╗ ███████╗ ██████╗ ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗"
    echo "  ██╔══██╗██╔════╝██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝"
    echo "  ██████╔╝█████╗  ██║     ██║   ██║██║   ██║█████╗  ██████╔╝ ╚████╔╝ "
    echo "  ██╔══██╗██╔══╝  ██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗  ╚██╔╝  "
    echo "  ██║  ██║███████╗╚██████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║   ██║   "
    echo "  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   "
    echo "  ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗                "
    echo "  ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗               "
    echo "  ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝               "
    echo "  ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗               "
    echo "  ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║               "
    echo "  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝               "
    echo -e "${RESET}"
    echo -e "${YELLOW}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${GREEN}    [✓] Welcome to Termux Recovery Master - Elite Android Suite${RESET}"
    echo -e "${WHITE}    Status: $(if $ANDROID; then echo 'Android/Termux'; else echo 'Linux'; fi) | OTG: Ready${RESET}"
    echo -e "${YELLOW}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo
}

print_header() {
    echo -e "${WHITE}${BG_BLUE}  $1  ${RESET}\n"
}

loading_status() { echo -e "${YELLOW}[*]${RESET} $1..."; }
done_status() { echo -e "${GREEN}[✓]${RESET} $1"; }
error_status() { echo -e "${RED}[!] Error:${RESET} $1"; }

# --- Dependency Management ---
check_deps() {
    loading_status "Checking core dependencies"
    local tools=("adb" "fastboot" "wget" "curl" "git" "xz-utils")
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &>/dev/null; then
            echo -e "${YELLOW}[*] Installing $tool...${RESET}"
            if $ANDROID; then pkg install -y "$tool" || apt install -y "$tool"; else sudo apt install -y "$tool"; fi
        fi
    done
}

# --- Core Logic Functions ---
check_device_adb() {
    local count=$(adb devices | grep -v "List" | grep "device" | wc -l)
    [ "$count" -eq 0 ] && { error_status "Device not found in ADB mode."; return 1; } || return 0
}

check_device_fastboot() {
    local count=$(fastboot devices | wc -l)
    [ "$count" -eq 0 ] && { error_status "Device not found in Fastboot mode."; return 1; } || return 0
}

# --- ADB MODULE ---
menu_adb() {
    while true; do
        banner; print_header "ADB MAINTENANCE & REBOOT MODULE"
        echo -e "  [1] List Connected Devices      [2] Reboot to System"
        echo -e "  [3] Reboot to Recovery          [4] Reboot to Fastboot"
        echo -e "  [5] Reboot to FastbootD         [6] ADB Sideload (Flash ZIP)"
        echo -e "  [7] Push File to Device         [8] Pull File from Device"
        echo -e "  [9] Install APK                 [10] Check Logcat (Live)"
        echo -e "  [11] Shell Access               [0] Back"
        echo
        read -p "  Choice: " sub_ch
        case $sub_ch in
            1) adb devices ;;
            2) check_device_adb && adb reboot ;;
            3) check_device_adb && adb reboot recovery ;;
            4) check_device_adb && adb reboot bootloader ;;
            5) check_device_adb && adb reboot fastboot ;;
            6) read -p "  ZIP Path: " p; [ -f "$p" ] && adb sideload "$p" || error_status "File missing." ;;
            7) read -p "  Local: " l; read -p "  Remote: " r; adb push "$l" "$r" ;;
            9) read -p "  APK Path: " p; [ -f "$p" ] && adb install "$p" ;;
            11) adb shell ;;
            0) break ;;
        esac; read -p "Press Enter..."
    done
}

# --- FASTBOOT MODULE ---
menu_fastboot() {
    while true; do
        banner; print_header "FASTBOOT FLASHING ENGINE"
        echo -e "  [1] Flash Boot (boot.img)       [2] Flash Recovery (TWRP/OFRP)"
        echo -e "  [3] Flash Vbmeta (AVB Disable)  [4] Flash Vendor Boot"
        echo -e "  [5] Flash Init Boot             [6] Flash Super Empty"
        echo -e "  [7] Flash System Image          [8] Boot Temporary Image"
        echo -e "  [9] Unlock Bootloader           [10] Lock Bootloader"
        echo -e "  [11] Format Userdata            [0] Back"
        echo
        read -p "  Choice: " sub_ch
        case $sub_ch in
            1) read -p "  Img Path: " p; check_device_fastboot && fastboot flash boot "$p" ;;
            2) read -p "  Img Path: " p; check_device_fastboot && fastboot flash recovery "$p" ;;
            3) read -p "  Img Path: " p; check_device_fastboot && fastboot --disable-verity --disable-verification flash vbmeta "$p" ;;
            4) read -p "  Img Path: " p; check_device_fastboot && fastboot flash vendor_boot "$p" ;;
            5) read -p "  Img Path: " p; check_device_fastboot && fastboot flash init_boot "$p" ;;
            6) read -p "  Img Path: " p; check_device_fastboot && fastboot flash super "$p" ;;
            8) read -p "  Img Path: " p; check_device_fastboot && fastboot boot "$p" ;;
            9) echo -e "${RED}[!] Data Wipe Warning!${RESET}"; read -p "Unlock? (y/n): " c; [[ "$c" == "y" ]] && fastboot flashing unlock ;;
            11) check_device_fastboot && fastboot -w ;;
            0) break ;;
        esac; read -p "Press Enter..."
    done
}

# --- PARTITION MODULE ---
menu_partitions() {
    while true; do
        banner; print_header "A/B PARTITION & SLOT MANAGER"
        echo -e "  [1] Get Current Active Slot     [2] Switch to Slot A"
        echo -e "  [3] Switch to Slot B            [4] Show Partition Table"
        echo -e "  [5] Format Cache                [6] Format Metadata"
        echo -e "  [0] Back"
        echo
        read -p "  Choice: " sub_ch
        case $sub_ch in
            1) check_device_fastboot && fastboot getvar current-slot ;;
            2) check_device_fastboot && fastboot --set-active=a ;;
            3) check_device_fastboot && fastboot --set-active=b ;;
            4) check_device_adb && adb shell "ls -la /dev/block/by-name" ;;
            0) break ;;
        esac; read -p "Press Enter..."
    done
}

# --- SPECIALIZED TOOLS ---
menu_special() {
    while true; do
        banner; print_header "ADVANCED RECOVERY & GSI TOOLS"
        echo -e "  [1] Auto-Flash Magisk (Root)    [2] GSI Flasher (Dynamic)"
        echo -e "  [3] Download TWRP/OrangeFox     [4] USB OTG Troubleshooting"
        echo -e "  [5] Bypass FRP (Samsung/MTK)    [6] Extract Payload.bin"
        echo -e "  [0] Back"
        echo
        read -p "  Choice: " sub_ch
        case $ch in
            1) 
                loading_status "Fetching Magisk..."
                curl -sL "https://github.com/topjohnwu/Magisk/releases/latest/download/Magisk-v28.1.apk" -o "$INSTALL_DIR/Magisk.zip"
                echo -e "${YELLOW}[*] Device must be in Recovery Sideload mode.${RESET}"
                adb sideload "$INSTALL_DIR/Magisk.zip" ;;
            2) 
                read -p "  GSI Img Path: " p; check_device_fastboot && {
                    fastboot reboot fastboot
                    fastboot flash system "$p"
                    fastboot -w
                } ;;
            4) 
                loading_status "Fixing USB connections"
                if [[ "$(id -u)" == "0" ]]; then
                    echo 1 > /sys/class/android_usb/android0/enable 2>/dev/null
                    done_status "USB Reset complete."
                else
                    error_status "Root required to fix system USB buffer."
                fi ;;
            6) git_run "https://github.com/cyxx/extract_android_ota_payload.git" "python3 extract_android_ota_payload.py" ;;
            0) break ;;
        esac; read -p "Press Enter..."
    done
}

# --- MAIN MENU ---
main_menu() {
    while true; do
        banner
        echo -e "${WHITE}  ╔══════════════════════════════════════════════════════════════╗"
        echo -e "  ║${CYAN}  [1]  📱  ADB Controls (Reboot, Sideload, Pull)          ${WHITE}║"
        echo -e "  ║${CYAN}  [2]  ⚡  Fastboot Flashing (Recovery, Boot, GSI)        ${WHITE}║"
        echo -e "  ║${CYAN}  [3]  🧬  Partition Manager (Slot A/B, Tables)           ${WHITE}║"
        echo -e "  ║${CYAN}  [4]  🛡️   Elite Flashing Tools (Magisk, Payload.bin)     ${WHITE}║"
        echo -e "  ║${CYAN}  [5]  🔍  Check OTG Device Connectivity                  ${WHITE}║"
        echo -e "  ║${CYAN}  [6]  🛠️   Auto-Repair Dependencies                       ${WHITE}║"
        echo -e "  ║${RED}  [0]  🚪  Exit Tool                                      ${WHITE}║"
        echo -e "  ╚══════════════════════════════════════════════════════════════╝${RESET}"
        echo
        read -p "  Enter Selection: " main_ch
        case $main_ch in
            1) menu_adb ;;
            2) menu_fastboot ;;
            3) menu_partitions ;;
            4) menu_special ;;
            5) banner; loading_status "Scanning..."; adb devices; fastboot devices; read -p "Done. Enter..." ;;
            6) check_deps; read -p "Press Enter..." ;;
            0) echo -e "${RED}[!] Goodbye!${RESET}"; exit 0 ;;
            *) error_status "Invalid Choice"; sleep 1 ;;
        esac
    done
}

# --- Initialization ---
trap 'echo -e "\n${RED}[!] Interrupted${RESET}"; exit 1' INT
check_deps
main_menu
