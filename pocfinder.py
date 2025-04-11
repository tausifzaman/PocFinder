import requests
import json
import time
import os
import re

# Terminal colors
R = '\033[91m'  # Red
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
B = '\033[94m'  # Blue
C = '\033[96m'  # Cyan
W = '\033[97m'  # White
END = '\033[0m'

# Colorful Logo
logo = f"""{C}

   _______      ________      _____   ____   _____ 
  / ____\ \    / /  ____|    |  __ \ / __ \ / ____|
 | |     \ \  / /| |__ ______| |__) | |  | | |     
 | |      \ \/ / |  __|______|  ___/| |  | | |     
 | |____   \  /  | |____     | |    | |__| | |____ 
  \_____|   \/   |______|    |_|     \____/ \_____|
                                                   

{END}"""

# Developer Info
developer_info = f"""
{G}CVE PoC Finder | Developed by Tausif Zaman
GitHub    : https://github.com/tausifzaman
Instagram : @_tausif_zaman
"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def normalize_cve(input_str):
    match = re.match(r"(?:CVE-)?(\d{4})-(\d{4,7})", input_str, re.IGNORECASE)
    if match:
        return f"CVE-{match.group(1)}-{match.group(2)}"
    return None

def fetch_cve_pocs(cve_id):
    try:
        print(f"\n{B}[+] Fetching data for: {cve_id}{END}")
        url = f"https://poc-in-github.motikan2010.net/api/v1/?cve_id={cve_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("pocs"):
            print(f"{Y}[!] No PoCs found for this CVE.{END}")
            return

        print(f"\n{G}[+] Found {len(data['pocs'])} PoC(s):{END}\n")
        for idx, poc in enumerate(data["pocs"], start=1):
            print(f"{C}{'='*60}{END}")
            print(f"{Y}[{idx}] CVE ID        :{W} {poc.get('cve_id', 'N/A')}")
            print(f"{Y}     Name         :{W} {poc.get('name', 'N/A')}")
            print(f"{Y}     Owner        :{W} {poc.get('owner', 'N/A')}")
            print(f"{Y}     GitHub Link  :{W} {poc.get('html_url', 'N/A')}")
            print(f"{Y}     Description  :{W} {poc.get('description', 'N/A')}")
            print(f"{Y}     Stars        :{W} {poc.get('stargazers_count', '0')}")
            print(f"{Y}     Created At   :{W} {poc.get('created_at', 'N/A')}")
            print(f"{Y}     Updated At   :{W} {poc.get('updated_at', 'N/A')}")
            print(f"{C}{'='*60}{END}\n")
            time.sleep(0.2)

    except requests.exceptions.RequestException as err:
        print(f"{R}[Error] {err}{END}")
    except json.decoder.JSONDecodeError:
        print(f"{R}[!] Failed to decode JSON response.{END}")
    except Exception as e:
        print(f"{R}[!] Unexpected Error: {e}{END}")

def main():
    clear_screen()
    print(logo)
    print(developer_info)
    while True:
        user_input = input(f"{B}Enter CVE ID (e.g. 2024-13346 ) or 'exit': {END}").strip()
        if user_input.lower() == 'exit':
            break
        cve_id = normalize_cve(user_input)
        if not cve_id:
            print(f"{R}[!] Invalid CVE format. Try again.{END}")
            continue
        fetch_cve_pocs(cve_id)

if __name__ == "__main__":
    main()
