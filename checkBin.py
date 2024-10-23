import requests
import sys
import os
from termcolor import colored

def get_gtfobins_data(binary_name):
    try:
        url = f"https://gtfobins.github.io/gtfobins/{binary_name}/"
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            return page_content
        else:
            return None
    except Exception as e:
        print(colored(f"[Error] No se pudo conectar a la página de GTFObin: {e}", "red"))
        return None

def check_vulnerabilities(binary_path):
    binary_name = os.path.basename(binary_path)
    page_content = get_gtfobins_data(binary_name)
    if page_content:
        sudo_vuln = "Sudo" if "sudo" in page_content.lower() else "No"
        suid_vuln = "SUID" if "suid" in page_content.lower() else "No"
        return binary_name, sudo_vuln, suid_vuln
    else:
        return binary_name, "No encontrado", "No encontrado"

def main():
    if len(sys.argv) != 2:
        print(colored("Uso: python3 checkbins.py <lista>", "yellow"))
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(colored("[Error] Archivo no encontrado", "red"))
        sys.exit(1)

    with open(input_file, "r") as file:
        binaries = file.readlines()

    for binary in binaries:
        binary = binary.strip()
        if binary:
            binary_name, sudo_vuln, suid_vuln = check_vulnerabilities(binary)
            if sudo_vuln == "Sudo":
                sudo_text = colored("Sudo(Vulnerable)", "green")
            else:
                sudo_text = colored("Sudo(No)", "red")

            if suid_vuln == "SUID":
                suid_text = colored("SUID(Vulnerable)", "green")
            else:
                suid_text = colored("SUID(No)", "red")

            print(f"\"{binary_name}\" {sudo_text} {suid_text}")

if __name__ == "__main__":
    main()
