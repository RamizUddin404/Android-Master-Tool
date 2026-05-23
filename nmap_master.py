import os
import sys
import time
import datetime
import urllib.request
import json

# Configuration
USER_NAME = "Ramiz Uddin"
TOOL_NAME = "NMAP ELITE"
VERSION = "13.0.0 (Omni Edition)"

# Global Colors
C_R = "\033[38;5;196m"  # Red
C_G = "\033[38;5;82m"   # Green
C_Y = "\033[38;5;226m"  # Yellow
C_B = "\033[38;5;21m"   # Blue
C_P = "\033[38;5;201m"  # Pink
C_C = "\033[38;5;51m"   # Cyan
C_O = "\033[38;5;208m"  # Orange
C_W = "\033[38;5;255m"  # White
C_D = "\033[2m"         # Dim
C_RS = "\033[0m"        # Reset

LOG_DIR = os.path.expanduser("~/nmap_logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def is_root():
    return os.getuid() == 0

def clear_screen():
    os.system('clear')

def banner():
    clear_screen()
    status = f"{C_G}ROOT{C_RS}" if is_root() else f"{C_R}NON-ROOT{C_RS}"
    print(f"{C_O}╔════════════════════════════════════════════════════════════╗{C_RS}")
    print(f"{C_O}║{C_C}   ███╗   ██╗███╗   ███╗ █████╗ ██████╗ {C_R}                   {C_O}║{C_RS}")
    print(f"{C_O}║{C_C}   ████╗  ██║████╗ ████║██╔══██╗██╔══██╗{C_R}    {C_W}OMNI EDITION{C_R}   {C_O}║{C_RS}")
    print(f"{C_O}║{C_C}   ██╔██╗ ██║██╔████╔██║███████║██████╔╝{C_R}    {C_G}v{VERSION}{C_R} {C_O}║{C_RS}")
    print(f"{C_O}║{C_C}   ██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝ {C_R}                   {C_O}║{C_RS}")
    print(f"{C_O}║{C_C}   ██║ ╚████║██║ ╚═╝ ██║██║  ██║██║     {C_R}     {C_Y}ULTIMATE{C_R}      {C_O}║{C_RS}")
    print(f"{C_O}╚════════════════════════════════════════════════════════════╝{C_RS}")
    print(f"{C_G}  [{C_W}♛{C_G}] {C_Y}Dev: {C_W}{USER_NAME}  {C_G}[{C_W}♛{C_G}] {C_Y}Status: {status}  {C_G}[{C_W}♛{C_G}] {C_Y}{datetime.datetime.now().strftime('%H:%M:%S')}{C_RS}")
    print(f"{C_C}  {'━'*56}{C_RS}")

def run_nmap_omni(args, target, scan_name):
    banner()
    safe_target = target.replace(".", "_").replace("/", "_")
    log_name = f"scan_{safe_target}.txt"
    log_path = os.path.join(LOG_DIR, log_name)
    
    # Global Verbosity
    if "-v" not in args: args += " -v"
    if "-Pn" not in args: args += " -Pn"
    
    if not is_root():
        if "-O" in args: args = args.replace("-O", "-sV")
        if "-sS" in args: args = args.replace("-sS", "-sT")
        if "--unprivileged" not in args: args += " --unprivileged"

    command = f"nmap {args} {target} -oN {log_path}"
    
    print(f"{C_O}  [+]{C_W} Target: {C_G}{target}{C_RS}")
    print(f"{C_O}  [+]{C_W} Mode:   {C_P}{scan_name}{C_RS}")
    print(f"{C_O}  [+]{C_W} Command: {C_D}{command}{C_RS}")
    print(f"{C_C}  {'━'*56}{C_RS}\n")

    os.system(command)
    
    print(f"\n{C_C}  {'━'*56}{C_RS}")
    print(f"{C_G}  [✔] Scan Finished. Results saved.{C_RS}")
    input(f"\n{C_Y}  [#] Press Enter to return...{C_RS}")

def advanced_menu():
    while True:
        banner()
        print(f"  {C_C}┌──{C_W} STEALTH & SPECIALS {C_C}──────┬──{C_W} TIMING & SPEED {C_C}────────┐{C_RS}")
        print(f"  {C_C}│ {C_G}[21]{C_W} NULL SCAN  {C_D}(-sN)     {C_C}│ {C_G}[26]{C_W} T0-PARANOID  {C_D}(Slow)   {C_C}│{C_RS}")
        print(f"  {C_C}│ {C_G}[22]{C_W} FIN SCAN   {C_D}(-sF)     {C_C}│ {C_G}[27]{C_W} T2-POLITE    {C_D}(Safe)   {C_C}│{C_RS}")
        print(f"  {C_C}│ {C_G}[23]{C_W} XMAS SCAN  {C_D}(-sX)     {C_C}│ {C_G}[28]{C_W} T4-AGGRESSIVE {C_D}(Fast)   {C_C}│{C_RS}")
        print(f"  {C_C}│ {C_G}[24]{C_W} IDLE SCAN  {C_D}(-sI)     {C_C}│ {C_G}[29]{C_W} T5-INSANE     {C_D}(Max)    {C_C}│{C_RS}")
        print(f"  {C_C}│ {C_G}[25]{C_W} ACK SCAN   {C_D}(-sA)     {C_C}│ {C_G}[30]{C_W} PACKET FRAG.  {C_D}(-f)     {C_C}│{C_RS}")
        print(f"  {C_C}├──────────────────────────┴──────────────────────────┤{C_RS}")
        print(f"  {C_C}│ {C_G}[31]{C_W} RANDOM TARGETS {C_D}(-iR)   {C_P}[0]{C_W} BACK TO MAIN MENU       {C_C}│{C_RS}")
        print(f"  {C_C}└────────────────────────────────────────────────────┘{C_RS}")
        
        choice = input(f"\n{C_P}  Ramiz@Omni ~# {C_W}").strip()
        if choice == '0': break
        
        target = ""
        if choice != '31':
            target = input(f"{C_P}  [+]{C_W} Target IP/Domain > {C_W}").strip()
            if not target: continue

        if choice == '21': run_nmap_omni("-sN", target, "NULL SCAN")
        elif choice == '22': run_nmap_omni("-sF", target, "FIN SCAN")
        elif choice == '23': run_nmap_omni("-sX", target, "XMAS SCAN")
        elif choice == '24': run_nmap_omni("-sI", target, "IDLE SCAN")
        elif choice == '25': run_nmap_omni("-sA", target, "ACK SCAN")
        elif choice == '26': run_nmap_omni("-T0", target, "PARANOID SCAN")
        elif choice == '27': run_nmap_omni("-T2", target, "POLITE SCAN")
        elif choice == '28': run_nmap_omni("-T4", target, "AGGRESSIVE TIMING")
        elif choice == '29': run_nmap_omni("-T5", target, "INSANE TIMING")
        elif choice == '30': run_nmap_omni("-f", target, "FRAGMENTED SCAN")
        elif choice == '31':
            num = input(f"{C_P}  [+]{C_W} How many random targets? > {C_W}").strip()
            run_nmap_omni(f"-iR {num} -sL", "RandomTargets", "RANDOM TARGET SCAN")

def script_menu():
    while True:
        banner()
        print(f"  {C_C}┌──{C_W} NSE SCRIPT CATEGORIES {C_C}─────────────────────────────┐{C_RS}")
        print(f"  {C_C}│ {C_G}[41]{C_W} DISCOVERY SCAN   {C_C}│ {C_G}[45]{C_W} MALWARE CHECK    {C_C}│{C_RS}")
        print(f"  {C_C}│ {C_G}[42]{C_W} VULN SCAN        {C_C}│ {C_G}[46]{C_W} EXPLOIT SCAN     {C_C}│{C_RS}")
        print(f"  {C_C}│ {C_G}[43]{C_W} BRUTE FORCE      {C_C}│ {C_G}[47]{C_W} FUZZER SCAN      {C_C}│{C_RS}")
        print(f"  {C_C}│ {C_G}[44]{C_W} AUTH SCAN        {C_C}│ {C_G}[48]{C_W} INTRUSIVE SCAN   {C_C}│{C_RS}")
        print(f"  {C_C}├────────────────────────────────────────────────────┤{C_RS}")
        print(f"  {C_C}│ {C_P}[0]{C_W} BACK TO MAIN MENU                                 {C_C}│{C_RS}")
        print(f"  {C_C}└────────────────────────────────────────────────────┘{C_RS}")
        
        choice = input(f"\n{C_P}  Ramiz@Scripts ~# {C_W}").strip()
        if choice == '0': break
        
        target = input(f"{C_P}  [+]{C_W} Target IP/Domain > {C_W}").strip()
        if not target: continue

        if choice == '41': run_nmap_omni("--script discovery", target, "DISCOVERY SCAN")
        elif choice == '42': run_nmap_omni("--script vuln", target, "VULN SCAN")
        elif choice == '43': run_nmap_omni("--script brute", target, "BRUTE FORCE SCAN")
        elif choice == '44': run_nmap_omni("--script auth", target, "AUTH SCAN")
        elif choice == '45': run_nmap_omni("--script malware", target, "MALWARE SCAN")
        elif choice == '46': run_nmap_omni("--script exploit", target, "EXPLOIT SCAN")
        elif choice == '47': run_nmap_omni("--script fuzzer", target, "FUZZER SCAN")
        elif choice == '48': run_nmap_omni("--script intrusive", target, "INTRUSIVE SCAN")

def main_menu():
    while True:
        banner()
        C, G, W, D, RS, Y, P, R = C_C, C_G, C_W, C_D, C_RS, C_Y, C_P, C_R
        print(f"  {C}┌──{W} BASIC SCANS {C}──────────────┬──{W} NETWORK TOOLS {C}───────┐{RS}")
        print(f"  {C}│ {G}[01]{W} QUICK SCAN  {D}(-F)     {C}│ {G}[05]{W} SERVICE SCAN {D}(-sV)    {C}│{RS}")
        print(f"  {C}│ {G}[02]{W} STEALTH SCAN {D}(-sS)    {C}│ {G}[06]{W} OS DETECTOR  {D}(-O)     {C}│{RS}")
        print(f"  {C}│ {G}[03]{W} AGGRESSIVE   {D}(-A)     {C}│ {G}[07]{W} LAN SCANNER  {D}(-sn)    {C}│{RS}")
        print(f"  {C}│ {G}[04]{W} UDP SCAN     {D}(-sU)    {C}│ {G}[08]{W} PORT SNIPER  {D}(-p)     {C}│{RS}")
        print(f"  {C}├──────────────────────────┴──────────────────────────┤{RS}")
        print(f"  {C}│ {G}[A]{W} ADVANCED FLAGS  {G}[S]{W} SCRIPT ENGINE  {G}[C]{W} CUSTOM COMMAND {C}│{RS}")
        print(f"  {C}├────────────────────────────────────────────────────┤{RS}")
        print(f"  {C}│ {Y}[L]{W} VIEW LOGS    {G}[H]{W} FLAG GUIDE    {R}[00]{W} SHUTDOWN SYSTEM   {C}│{RS}")
        print(f"  {C}└────────────────────────────────────────────────────┘{RS}")
        
        choice = input(f"\n{P}  Ramiz@Omni ~# {W}").strip().upper()
        
        if choice in ['00', '0']: sys.exit()
        if choice == 'L': os.system(f"ls {LOG_DIR}"); input("\nPress Enter..."); continue
        if choice == 'A': advanced_menu(); continue
        if choice == 'S': script_menu(); continue
        if choice == 'H':
            banner()
            print(f"{Y}  -v : Verbose (Scan er details dekhay)\n  -iR: Random targets scan kore\n  -sS: Stealth scan\n  -sV: Version detection\n  -O : OS detection\n  -Pn: No Ping check{RS}")
            input("\nEnter chapun..."); continue
        
        if choice == 'C':
            cust_args = input(f"{P}  [+]{W} Enter Nmap Flags (e.g. -sS -v -p 80) > {W}").strip()
            target = input(f"{P}  [+]{W} Target > {W}").strip()
            run_nmap_omni(cust_args, target, "CUSTOM SCAN")
            continue

        target = input(f"{P}  [+]{W} Target IP/Domain > {W}").strip()
        if not target: continue

        if choice == '01' or choice == '1': run_nmap_omni("-F -T4", target, "QUICK SCAN")
        elif choice == '02' or choice == '2': run_nmap_omni("-sS", target, "STEALTH SCAN")
        elif choice == '03' or choice == '3': run_nmap_omni("-A", target, "AGGRESSIVE SCAN")
        elif choice == '04' or choice == '4': run_nmap_omni("-sU", target, "UDP SCAN")
        elif choice == '05' or choice == '5': run_nmap_omni("-sV", target, "SERVICE SCAN")
        elif choice == '06' or choice == '6': run_nmap_omni("-O", target, "OS DETECTOR")
        elif choice == '07' or choice == '7': run_nmap_omni("-sn", target, "LAN SCANNER")
        elif choice == '08' or choice == '8':
            p = input(f"{P}  [+]{W} Ports > "); run_nmap_omni(f"-p {p}", target, "PORT SNIPER")

if __name__ == "__main__":
    try: main_menu()
    except KeyboardInterrupt: sys.exit()
