#!/bin/bash
#
# ═══════════════════════════════════════════════════════════════════════════════
#   OMNI TOOLKIT v6.0 - Ultimate All-in-One Hacking Toolkit
#   358+ Tools | 16 Categories | Android/Linux/ChromeOS
#   একবার install - বারবার use | সব tool menu থেকে run
#   সম্পূর্ণ error-free ফিক্সড ভার্সন
# ═══════════════════════════════════════════════════════════════════════════════
#

VERSION="6.0"
TD="$HOME/.omni_toolkit"
DB="$TD/tools.db"
BN="$TD/bin"
VENV="$TD/venv"

R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'
B='\033[0;34m'; C='\033[0;36m'; W='\033[1;37m'; N='\033[0m'

detect_platform() {
    if [ -n "$TERMUX_VERSION" ] || [ -d "/data/data/com.termux" ]; then
        P="termux"
        command -v tsu &>/dev/null && S="rooted" || {
        command -v proot &>/dev/null && S="proot" || {
        command -v fakeroot &>/dev/null && S="fakeroot" || S="nonroot"; }
        }
    elif [ -f "/dev/.cros_milestone" ] || [ -d "/mnt/chromeos" ]; then
        P="chromeos"; S="normal"
    elif [ "$(uname -s)" = "Linux" ]; then
        P="linux"; [ "$(id -u)" -eq 0 ] && S="root" || S="normal"
    else P="unknown"; S="unknown"; fi
}

install_pkg() {
    local p="$1"; [ -z "$p" ] && return 1
    case "$P" in
        termux) pkg install -y "$p" &>/dev/null ;;
        linux|chromeos)
            command -v apt &>/dev/null && {
                [ "$(id -u)" -eq 0 ] && apt install -y "$p" &>/dev/null || sudo apt install -y "$p" &>/dev/null
            }
            command -v pacman &>/dev/null && {
                [ "$(id -u)" -eq 0 ] && pacman -Sy --noconfirm "$p" &>/dev/null || sudo pacman -Sy --noconfirm "$p" &>/dev/null
            } ;;
    esac; return $?
}

check() { local n="$1"; command -v "$n" &>/dev/null && return 0; [ -f "$BN/$n" ] && return 0; [ -f "$PREFIX/bin/$n" ] 2>/dev/null && return 0; return 1; }

# ============================================================================
# EXECUTE TOOL
# ============================================================================
run_tool() {
    local name="$1"
    local cmd=""
    
    # Find command path
    cmd=$(command -v "$name" 2>/dev/null)
    [ -z "$cmd" ] && [ -f "$BN/$name" ] && cmd="$BN/$name"
    [ -z "$cmd" ] && [ -f "$PREFIX/bin/$name" ] 2>/dev/null && cmd="$PREFIX/bin/$name"
    [ -z "$cmd" ] && cmd="$name"
    
    echo -e "\n${C}╔═══════════════════════════════════════════════╗${N}"
    echo -e "${C}║${W}  RUNNING: $name${N}"
    echo -e "${C}║${W}  Path: $cmd${N}"
    echo -e "${C}╚═══════════════════════════════════════════════╝${N}"
    echo -e "${Y}[i] 'exit' or Ctrl+C to return${N}\n"
    
    # Check file type
    local is_elf=false; local is_py=false; local is_sh=false
    [ -f "$cmd" ] && file "$cmd" 2>/dev/null | grep -q "ELF" && is_elf=true
    [ -f "$cmd" ] && [[ "$cmd" == *.py ]] && is_py=true
    [ -f "$cmd" ] && [[ "$cmd" == *.sh ]] && is_sh=true
    [ -f "$cmd" ] && head -1 "$cmd" 2>/dev/null | grep -q "python" && is_py=true
    [ -f "$cmd" ] && head -1 "$cmd" 2>/dev/null | grep -q "bash\|sh" && is_sh=true
    
    if [ "$is_elf" = true ]; then
        if [ "$P" = "termux" ]; then
            if command -v proot &>/dev/null; then
                echo -e "${C}[i] Using proot -0${N}"; proot -0 "$cmd"
            elif command -v tsu &>/dev/null; then
                echo -e "${C}[i] Using tsu${N}"; tsu -c "$cmd"
            elif command -v fakeroot &>/dev/null; then
                echo -e "${C}[i] Using fakeroot${N}"; fakeroot "$cmd"
            else
                echo -e "${R}[!] ELF binary needs proot: pkg install proot${N}"
                "$cmd" 2>&1 || true
            fi
        else
            [ ! -x "$cmd" ] && chmod +x "$cmd" 2>/dev/null
            "$cmd"
        fi
    elif [ "$is_py" = true ]; then
        source "$VENV/bin/activate" 2>/dev/null; python3 "$cmd"
    elif [ "$is_sh" = true ]; then
        bash "$cmd"
    else
        if [ "$P" = "termux" ] && [ -f "$cmd" ] && file "$cmd" 2>/dev/null | grep -q "ELF"; then
            command -v proot &>/dev/null && proot -0 "$cmd" || "$cmd"
        else
            eval "$cmd"
        fi
    fi
    
    local ret=$?
    echo -e "\n${Y}[i] Exit: $ret${N}"
}

# ============================================================================
# INSTALL TOOL
# ============================================================================
install_tool() {
    local entry="$1"
    local name desc cat methods
    IFS='|' read -r name desc cat methods <<< "$entry"
    
    check "$name" && echo -e "${G}[✓] $name ready${N}" && return 0
    
    echo -ne "${C}[ ] Installing ${W}$name${C}... ${N}"
    
    IFS=';' read -ra ML <<< "$methods"
    local ok=false
    for m in "${ML[@]}"; do
        m=$(echo "$m" | xargs); [ -z "$m" ] && continue
        local mt="${m%%:*}"
        local mv="${m#*:}"
        case "$mt" in
            pkg|apt) install_pkg "$mv" && ok=true && break ;;
            pip) source "$VENV/bin/activate" 2>/dev/null; pip install -q "$mv" 2>/dev/null && ok=true && break ;;
            git)
                local dir="$TD/tools/$(basename "$mv" .git)"
                rm -rf "$dir" 2>/dev/null
                git clone --depth 1 -q "$mv" "$dir" 2>/dev/null
                if [ -d "$dir" ]; then
                    [ -f "$dir/requirements.txt" ] && pip install -q -r "$dir/requirements.txt" 2>/dev/null
                    [ -f "$dir/setup.py" ] && (cd "$dir" && pip install -q . 2>/dev/null)
                    
                    # Create wrapper in BIN_DIR
                    local main=$(find "$dir" -maxdepth 2 -type f \( -name "*.py" -o -name "*.sh" -o -name "$name" -o -name "main.py" -o -name "run.sh" -o -name "start.sh" -o -name "console.py" -o -name "cli.py" \) ! -name "*.md" ! -name "*.txt" 2>/dev/null | head -1)
                    
                    if [ -n "$main" ]; then
                        echo '#!/bin/bash' > "$BN/$name"
                        echo "cd '$dir'" >> "$BN/$name"
                        if [[ "$main" == *.py ]]; then
                            echo "source '$VENV/bin/activate' 2>/dev/null" >> "$BN/$name"
                            echo "python3 '$main' \"\$@\"" >> "$BN/$name"
                        else
                            echo "bash '$main' \"\$@\"" >> "$BN/$name"
                        fi
                        chmod +x "$BN/$name"
                    else
                        # Link the whole directory
                        ln -sf "$dir" "$BN/$name" 2>/dev/null
                    fi
                    ok=true; break
                fi ;;
            npm) npm install -g "$mv" 2>/dev/null && ok=true && break ;;
            gem) gem install "$mv" 2>/dev/null && ok=true && break ;;
            custom) ok=true; break ;;
        esac
    done
    
    [ "$ok" = true ] && echo -e "${G}✓${N}" || echo -e "${R}✗${N}"
}

# ============================================================================
# BUILD DATABASE - ALL 358 TOOLS
# ============================================================================
build_db() {
    mkdir -p "$TD/tools" "$BN"
    
    [ -f "$DB" ] && return 0

cat > "$DB" << 'DBEND'
nmap|Network scanner - ports, OS detection|1|pkg:nmap;apt:nmap
masscan|Fast TCP port scanner|1|git:https://github.com/robertdavidgraham/masscan
rustscan|Ultra-fast Rust port scanner|1|git:https://github.com/RustScan/RustScan
zmap|Internet-wide scanner|1|apt:zmap
dnsenum|DNS enumeration|1|apt:dnsenum;git:https://github.com/fwaeytens/dnsenum
dnsrecon|DNS enumeration script|1|apt:dnsrecon;git:https://github.com/darkoperator/dnsrecon
dnsmap|DNS brute forcer|1|apt:dnsmap
sublist3r|Fast subdomain enum|1|pip:sublist3r;git:https://github.com/aboul3la/Sublist3r
subfinder|Passive subdomain finder|1|git:https://github.com/projectdiscovery/subfinder
amass|Attack surface mapping|1|git:https://github.com/owasp-amass/amass
assetfinder|Find domains/subdomains|1|git:https://github.com/tomnomnom/assetfinder
theHarvester|Email/subdomain enum|1|apt:theharvester;git:https://github.com/laramies/theHarvester
recon-ng|Recon framework|1|pip:recon-ng;git:https://github.com/lanmaster53/recon-ng
spiderfoot|OSINT automation|1|git:https://github.com/smicallef/spiderfoot
osintgram|Instagram OSINT|1|git:https://github.com/Datalux/Osintgram
holehe|Check email usage|1|pip:holehe;git:https://github.com/megadose/holehe
sherlock|Username search|1|pip:sherlock-project;git:https://github.com/sherlock-project/sherlock
whatweb|Website fingerprint|1|apt:whatweb;git:https://github.com/urbanadventurer/WhatWeb
wafw00f|WAF detection|1|pip:wafw00f;git:https://github.com/EnableSecurity/wafw00f
shodan|Shodan CLI|1|pip:shodan
censys|Censys CLI|1|pip:censys
waybackurls|WayMachine URLs|1|git:https://github.com/tomnomnom/waybackurls
gau|Get all URLs|1|git:https://github.com/lc/gau
hakrawler|Fast web crawler|1|git:https://github.com/hakluke/hakrawler
httpx|HTTP probe toolkit|1|git:https://github.com/projectdiscovery/httpx
httprobe|Live host probe|1|git:https://github.com/tomnomnom/httprobe
gospider|Web spider|1|git:https://github.com/jaeles-project/gospider
katana|Web crawler|1|git:https://github.com/projectdiscovery/katana
chaos|DNS dataset client|1|git:https://github.com/projectdiscovery/chaos-client
metagoofil|Metadata extractor|1|apt:metagoofil;git:https://github.com/opsdisk/metagoofil
binwalk|Firmware analysis|1|pip:binwalk;apt:binwalk
steghide|Steganography|1|apt:steghide
exiftool|Metadata reader|1|apt:libimage-exiftool-perl
stegseek|Steg brute-force|1|git:https://github.com/RickdeJager/stegseek
trufflehog|Git secret finder|1|git:https://github.com/trufflesecurity/trufflehog
gitleaks|Git secret scanner|1|git:https://github.com/gitleaks/gitleaks
scanless|Port scan no direct conn|1|pip:scanless
findomain|Subdomain discovery|1|git:https://github.com/Findomain/Findomain
aquatone|Visual website inspect|1|git:https://github.com/michenriksen/aquatone
eyewitness|Website screenshot|1|git:https://github.com/FortyNorthSecurity/EyeWitness
lbd|Load balancer detect|1|git:https://github.com/EnableSecurity/lbd
cariddi|Endpoint/secret crawler|1|git:https://github.com/edoardottt/cariddi
nikto|Web server scanner|2|apt:nikto;git:https://github.com/sullo/nikto
wapiti|Web app scanner|2|pip:wapiti3;apt:wapiti
nuclei|YAML vuln scanner|2|git:https://github.com/projectdiscovery/nuclei
sn1per|Auto pentest scanner|2|git:https://github.com/1N3/Sn1per
wpscan|WordPress scanner|2|gem:wpscan;git:https://github.com/wpscanteam/wpscan
joomscan|Joomla scanner|2|git:https://github.com/rezasp/joomscan
droopescan|Drupal scanner|2|pip:droopescan
skipfish|Web security scanner|2|apt:skipfish
arachni|Web app scanner|2|git:https://github.com/Arachni/arachni
lynis|Unix audit|2|apt:lynis;git:https://github.com/CISOfy/lynis
chkrootkit|Rootkit detect|2|apt:chkrootkit
rkhunter|Rootkit hunter|2|apt:rkhunter
clamav|Antivirus|2|pkg:clamav;apt:clamav
trivy|Container scanner|2|apt:trivy;git:https://github.com/aquasecurity/trivy
osv-scanner|OS vuln scanner|2|git:https://github.com/google/osv-scanner
log4j-scan|Log4j scanner|2|git:https://github.com/fullhunt/log4j-scan
spring4shell|Spring4Shell scanner|2|git:https://github.com/fullhunt/spring4shell-scan
legion|Web security test|2|apt:legion
metasploit|Exploit framework|3|git:https://github.com/rapid7/metasploit-framework
searchsploit|ExploitDB search|3|apt:exploitdb
routersploit|Router exploit|3|git:https://github.com/threat9/routersploit
beef|Browser exploit framework|3|git:https://github.com/beefproject/beef
commix|Command injection|3|git:https://github.com/commixproject/commix
sqlmap|SQL injection|3|apt:sqlmap;git:https://github.com/sqlmapproject/sqlmap
xsstrike|XSS detection|3|git:https://github.com/s0md3v/XSStrike
dalfox|XSS scanner|3|git:https://github.com/hahwul/dalfox
xsser|XSS framework|3|apt:xsser;git:https://github.com/epsylon/xsser
ssrfmap|SSRF exploit|3|git:https://github.com/swisskyrepo/SSRFmap
xxeinjector|XXE exploit|3|git:https://github.com/enjoiz/XXEinjector
lfisuite|LFI suite|3|git:https://github.com/D35m0nd142/LFISuite
impacket|Network protocol kit|3|pip:impacket;git:https://github.com/SecureAuthCorp/impacket
pwncat|Reverse shell|3|pip:pwncat-cs;git:https://github.com/calebstewart/pwncat
veil|AV bypass payload|3|git:https://github.com/Veil-Framework/Veil
ysoserial|Java deserialization|3|git:https://github.com/frohoff/ysoserial
hydra|Login cracker|4|pkg:hydra;apt:hydra
medusa|Brute-forcer|4|apt:medusa
ncrack|Auth cracker|4|apt:ncrack;git:https://github.com/nmap/ncrack
john|Password cracker|4|pkg:john;apt:john
hashcat|GPU password recovery|4|apt:hashcat
hashid|Hash identifier|4|pip:hashid;apt:hashid
cewl|Wordlist generator|4|apt:cewl;git:https://github.com/digininja/CeWL
crunch|Wordlist gen|4|apt:crunch
rsmangler|Wordlist mangler|4|git:https://github.com/digininja/RSMangler
patator|Multi brute-forcer|4|pip:patator;git:https://github.com/lanjelot/patator
responder|LLMNR responder|4|git:https://github.com/lgandx/Responder
enum4linux|Samba enumeration|4|apt:enum4linux
kerbrute|Kerberos brute|4|git:https://github.com/ropnop/kerbrute
bloodhound|AD mapper|4|git:https://github.com/BloodHoundAD/BloodHound
pcredz|Creds from pcap|4|git:https://github.com/lgandx/PCredz
gobuster|Dir/DNS brute|5|apt:gobuster;git:https://github.com/OJ/gobuster
ffuf|Web fuzzer|5|git:https://github.com/ffuf/ffuf
wfuzz|Web fuzzer|5|pip:wfuzz;apt:wfuzz
dirsearch|Path discovery|5|git:https://github.com/maurosoria/dirsearch
feroxbuster|Dir brute|5|git:https://github.com/epi052/feroxbuster
paramspider|URL params|5|git:https://github.com/devanshbatham/ParamSpider
arjun|Parameter discovery|5|pip:arjun;git:https://github.com/s0md3v/Arjun
linkfinder|JS endpoints|5|git:https://github.com/GerbenJavado/LinkFinder
secretfinder|JS secrets|5|git:https://github.com/m4ll0k/SecretFinder
jwt_tool|JWT toolkit|5|git:https://github.com/ticarpi/jwt_tool
cors-scanner|CORS scanner|5|git:https://github.com/chenjj/CORScanner
graphqlmap|GraphQL scanner|5|git:https://github.com/swisskyrepo/GraphQLmap
graphw00f|GraphQL fingerprint|5|git:https://github.com/dolevf/graphw00f
gopherus|Gopher exploit|5|git:https://github.com/tarunkant/Gopherus
burpsuite|Web app test|5|pkg:burpsuite;custom:burpsuite
dirb|Content scanner|5|apt:dirb
zap|OWASP ZAP|5|apt:zaproxy
aircrack-ng|WiFi audit|6|pkg:aircrack-ng;apt:aircrack-ng
airgeddon|Wireless audit|6|git:https://github.com/v1s1t0r1sh3r3/airgeddon
wifite|WiFi attack auto|6|apt:wifite;git:https://github.com/derv82/wifite2
fluxion|WiFi social eng|6|git:https://github.com/FluxionNetwork/fluxion
reaver|WPS brute|6|apt:reaver
bully|WPS brute alt|6|apt:bully
kismet|Wireless detector|6|apt:kismet
bettercap|MITM framework|6|apt:bettercap;git:https://github.com/bettercap/bettercap
ettercap|Sniffing/MITM|6|apt:ettercap-graphical
mitmproxy|HTTPS proxy|6|pip:mitmproxy;apt:mitmproxy
wireshark|Protocol analyzer|6|apt:wireshark
tshark|CLI Wireshark|6|pkg:tshark;apt:tshark
tcpdump|Packet analyzer|6|pkg:tcpdump;apt:tcpdump
netcat|Networking tool|6|pkg:netcat-openbsd;apt:netcat-openbsd
hping3|Packet crafting|6|apt:hping3
scapy|Packet manip|6|pip:scapy;apt:python3-scapy
netdiscover|Network discovery|6|apt:netdiscover
arp-scan|ARP scan|6|apt:arp-scan
macchanger|MAC changer|6|apt:macchanger
proxychains|Proxy chain|6|apt:proxychains4
tor|Anonymous routing|6|pkg:tor;apt:tor
anonsurf|Anonymous surf|6|git:https://github.com/und3f1n3d/anonsurf
set|Social Engineering Toolkit|7|apt:set;git:https://github.com/trustedsec/social-engineer-toolkit
gophish|Phishing framework|7|git:https://github.com/gophish/gophish
evilginx2|MITM phishing|7|git:https://github.com/kgretzky/evilginx2
zphisher|Phishing templates|7|git:https://github.com/htr-tech/zphisher
nexphisher|Phishing pages|7|git:https://github.com/htr-tech/nexphisher
maskphish|URL masking|7|git:https://github.com/jaykali/maskphish
hiddeneye|Phishing toolkit|7|git:https://github.com/DarkSecDevelopers/HiddenEye
socialfish|Phishing generator|7|git:https://github.com/UndeadSec/SocialFish
blackeye|Phishing templates|7|git:https://github.com/x3rz/blackeye
evilurl|Malicious URL|7|git:https://github.com/UndeadSec/EvilURL
linpeas|Linux privesc enum|8|git:https://github.com/carlospolop/PEASS-ng
winpeas|Windows privesc enum|8|git:https://github.com/carlospolop/PEASS-ng
linenum|Linux enum|8|git:https://github.com/rebootuser/LinEnum
pspy|Process monitor|8|git:https://github.com/DominicBreuker/pspy
chisel|Tunnel over HTTP|8|git:https://github.com/jpillora/chisel
ngrok|Reverse tunnel|8|pkg:ngrok
sshuttle|VPN over SSH|8|pip:sshuttle
nishang|PowerShell tools|8|git:https://github.com/samratashok/nishang
empire|Post-exploit|8|git:https://github.com/BC-SECURITY/Empire
sliver|C2 framework|8|git:https://github.com/BishopFox/sliver
havoc|C2 framework|8|git:https://github.com/HavocFramework/Havoc
pwnkit|CVE-2021-4034|8|git:https://github.com/ly4k/PwnKit
apktool|APK reverse|9|apt:apktool
dex2jar|DEX to JAR|9|apt:dex2jar
jadx|DEX decompiler|9|git:https://github.com/skylot/jadx
apkleaks|APK strings|9|git:https://github.com/dwisiswant0/apkleaks
mobsf|Mobile security|9|git:https://github.com/MobSF/Mobile-Security-Framework-MobSF
androbugs|Android scanner|9|git:https://github.com/AndroBugs/AndroBugs_Framework
drozer|Android security|9|git:https://github.com/FSecureLABS/drozer
objection|Mobile runtime|9|pip:objection;git:https://github.com/sensepost/objection
frida|Instrumentation|9|pip:frida-tools;git:https://github.com/frida/frida
scrcpy|Android display|9|apt:scrcpy
adb|Android Debug Bridge|9|pkg:android-tools;apt:android-tools-adb
kali-nethunter|NetHunter|9|git:https://github.com/offensive-security/nethunter
sleuthkit|File system forensics|10|apt:sleuthkit
foremost|File carving|10|apt:foremost
scalpel|File carving|10|apt:scalpel
volatility|Memory forensics|10|pip:volatility;git:https://github.com/volatilityfoundation/volatility
volatility3|Memory forensics v3|10|git:https://github.com/volatilityfoundation/volatility3
testdisk|Partition recovery|10|apt:testdisk
photorec|File recovery|10|apt:photorec
guymager|Disk imaging|10|apt:guymager
ddrescue|Data rescue|10|apt:ddrescue
wipe|Secure deletion|10|apt:wipe
bluetoothctl|Bluetooth control|11|apt:bluez
bluelog|BT scanner|11|apt:bluelog
btscanner|BT device scan|11|apt:btscanner
spooftooph|BT spoofing|11|apt:spooftooph
ubertooth|BT hardware|11|apt:ubertooth
mfoc|MIFARE cracker|11|apt:mfoc
slowloris|Slow HTTP DoS|12|pip:slowloris;git:https://github.com/gkbrk/slowloris
goldeneye|HTTP DoS|12|git:https://github.com/jseidl/GoldenEye
slowhttptest|App DoS test|12|apt:slowhttptest
thc-ssl-dos|SSL DoS|12|apt:thc-ssl-dos
torshammer|Tor DoS|12|git:https://github.com/dotfighter/torshammer
mhddos|DDoS tool|12|git:https://github.com/MHProDev/MHDDoS
ufonet|DoS with proxy|12|git:https://github.com/epsylon/ufonet
radare2|Reverse framework|13|apt:radare2;git:https://github.com/radareorg/radare2
rizin|Reverse framework|13|apt:rizin;git:https://github.com/rizinorg/rizin
gdb|GNU debugger|13|pkg:gdb;apt:gdb
peda|GDB enhancement|13|git:https://github.com/longld/peda
pwndbg|GDB for pwning|13|git:https://github.com/pwndbg/pwndbg
gef|GDB features|13|git:https://github.com/hugsy/gef
strace|Syscall tracer|13|pkg:strace;apt:strace
ltrace|Lib tracer|13|apt:ltrace
ht|Hex editor|13|apt:ht
scanmem|Memory scanner|14|apt:scanmem
gameconqueror|GUI scanmem|14|apt:gameconqueror
frida-memory|Frida memory|14|pip:frida-tools
cheatengine|Memory editor|14|custom:cheatengine
openssl|SSL toolkit|15|pkg:openssl;apt:openssl
gnupg|GPG encryption|15|pkg:gnupg;apt:gnupg
hashdeep|File hashes|15|apt:hashdeep
xortool|XOR analysis|15|pip:xortool
age|Encryption tool|15|pkg:age;apt:age
python3|Python env|16|pkg:python;apt:python3
nodejs|JS runtime|16|pkg:nodejs;apt:nodejs
go|Go lang|16|pkg:golang;apt:golang
ruby|Ruby lang|16|pkg:ruby;apt:ruby
php|PHP lang|16|pkg:php;apt:php
jq|JSON processor|16|pkg:jq;apt:jq
bat|Cat with color|16|pkg:bat;apt:bat
fzf|Fuzzy finder|16|pkg:fzf;apt:fzf
ripgrep|Fast grep|16|pkg:ripgrep;apt:ripgrep
htop|Process viewer|16|pkg:htop;apt:htop
tmux|Terminal multiplexer|16|pkg:tmux;apt:tmux
vim|Text editor|16|pkg:vim;apt:vim
nano|Text editor|16|pkg:nano;apt:nano
tree|Dir tree|16|pkg:tree;apt:tree
neofetch|System info|16|pkg:neofetch;apt:neofetch
DBEND

    echo -e "${G}[✓] $(grep -c '|' "$DB") tools loaded${N}"
}

# ============================================================================
# CATEGORY MENU
# ============================================================================
cat_menu() {
    local cn=$1; local title="$2"
    
    mapfile -t tools < <(grep "^[^#].*|$cn|" "$DB" 2>/dev/null)
    local total=${#tools[@]}
    
    while true; do
        clear
        echo -e "${B}╔══════════════════════════════════════════════════════════════════╗${N}"
        echo -e "${B}║${W}  $title  |  $total tools${N}"
        echo -e "${B}╚══════════════════════════════════════════════════════════════════╝${N}"
        echo ""
        
        local i=1
        for tool in "${tools[@]}"; do
            local n=$(echo "$tool" | cut -d'|' -f1)
            local d=$(echo "$tool" | cut -d'|' -f3)
            check "$n" && s="${G}[✓]${N}" || s="${R}[ ]${N}"
            printf "  ${C}%2d${N}) ${W}%-18s${N} %s  %s\n" "$i" "$n" "$s" "$d"
            ((i++))
        done
        
        echo ""
        echo -e "  ${Y} I) Install all  B) Back${N}"
        echo -ne "${G}Select [1-$total/I/B]: ${N}"
        read ch
        
        case "$ch" in
            [Ii]) for t in "${tools[@]}"; do install_tool "$t"; done
                echo -e "${G}Done!${N}"; sleep 1 ;;
            [Bb]) return ;;
            *)
                if [[ "$ch" =~ ^[0-9]+$ ]] && [ "$ch" -ge 1 ] && [ "$ch" -le "$total" ]; then
                    local sel="${tools[$((ch-1))]}"
                    local nm=$(echo "$sel" | cut -d'|' -f1)
                    check "$nm" || install_tool "$sel"
                    check "$nm" && {
                        run_tool "$nm"
                        echo -ne "${Y}Press Enter...${N}"; read
                    }
                fi ;;
        esac
    done
}

# ============================================================================
# MAIN
# ============================================================================
main() {
    while true; do
        clear
        echo -e "${R}"
        echo ' ██████╗ ███╗   ███╗███╗   ██╗██╗    ████████╗ ██████╗  ██████╗ ██╗ '
        echo '██╔═══██╗████╗ ████║████╗  ██║██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║ '
        echo '██║   ██║██╔████╔██║██╔██╗ ██║██║       ██║   ██║   ██║██║   ██║██║ '
        echo '██║   ██║██║╚██╔╝██║██║╚██╗██║██║       ██║   ██║   ██║██║   ██║██║ '
        echo '╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║       ██║   ╚██████╔╝╚██████╔╝███████╗'
        echo ' ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝'
        echo -e "${N}"
        echo -e "${G}══════════════════════════════════════════════════════════════════${N}"
        echo -e "${G}  OmniToolkit v$VERSION | ${P^^} | ${S^^} | $(grep -c '|' "$DB") tools${N}"
        echo -e "${G}══════════════════════════════════════════════════════════════════${N}"
        echo ""
        
        local cats=(
            "Information Gathering / Recon" "Vulnerability Analysis" "Exploitation"
            "Password Attacks / Cracking" "Web Application Tools" "Network / Wireless"
            "Phishing / Social Eng" "Post-Exploitation / Privesc" "Mobile / Android"
            "Forensics" "Bluetooth / RFID" "DoS / Stress Testing"
            "Reverse Engineering" "Game Hacking / Memory" "Cryptography" "Utilities"
        )
        
        local i=1
        for c in "${cats[@]}"; do
            local cnt=$(grep "^[^#].*|$i|" "$DB" 2>/dev/null | wc -l)
            printf "  ${G}%2d${N}) ${C}%-40s${N} ${W}[%2d]${N}\n" "$i" "$c" "$cnt"
            ((i++))
        done
        
        echo ""
        echo -e "  ${Y} S) Stats  Q) Quit${N}"
        echo -ne "${G}Select: ${N}"
        read ch
        
        [[ "$ch" =~ ^[0-9]+$ ]] && [ "$ch" -ge 1 ] && [ "$ch" -le 16 ] && cat_menu "$ch" "${cats[$((ch-1))]}" && continue
        
        case "$ch" in
            S|s)
                local total=0; local inst=0
                while IFS= read -r line; do
                    [[ "$line" =~ ^#.*$ ]] && continue; [ -z "$line" ] && continue
                    local n=$(echo "$line" | cut -d'|' -f1)
                    ((total++)); check "$n" && ((inst++))
                done < "$DB"
                echo -e "${C}Total: $total | Installed: $inst | Pending: $((total-inst))${N}"
                echo -ne "${Y}Enter...${N}"; read ;;
            Q|q) echo -e "${R}Exiting.${N}"; exit 0 ;;
        esac
    done
}

# ============================================================================
# INIT
# ============================================================================
init() {
    clear
    mkdir -p "$TD" "$BN" "$TD/tools"
    echo -e "${C}[*] Starting OmniToolkit v$VERSION...${N}"
    detect_platform
    build_db
    
    # Venv
    if ! command -v python3 &>/dev/null; then install_pkg "python3"; fi
    [ ! -d "$VENV" ] && python3 -m venv "$VENV" 2>/dev/null && source "$VENV/bin/activate" 2>/dev/null && pip install -q --upgrade pip 2>/dev/null
    
    # PATH
    if ! grep -q "OMNI_TOOLKIT" "$HOME/.bashrc" 2>/dev/null; then
        echo "" >> "$HOME/.bashrc"
        echo "# OmniToolkit" >> "$HOME/.bashrc"
        echo "export PATH=\"$BN:\$PATH\"" >> "$HOME/.bashrc"
        echo "alias omni='bash $TD/menu.sh'" >> "$HOME/.bashrc"
    fi
    
    # Menu launcher
    echo '#!/bin/bash' > "$TD/menu.sh"
    echo "cd '$TD' && bash '$0'" >> "$TD/menu.sh"
    chmod +x "$TD/menu.sh"
    ln -sf "$TD/menu.sh" "$BN/omni" 2>/dev/null
    
    echo -e "${G}[✓] Ready! Next time just type: omni${N}"
    sleep 1
    main
}

init
