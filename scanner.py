import socket
from datetime import datetime
import sys
import os

# Cores para o terminal
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def clear_screen():
    # Limpa o terminal dependendo do Sistema Operacional
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{BLUE}
   ____                      ____                                  
  |  _ \ ___  _ __ ___  ___ / ___|  ___ __ _ _ __  _ __   ___ _ __ 
  | |_) / _ \| '__/ __|/ _ \\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
  |  __/ (_) | |  \__ \  __/ ___) | (_| (_| | | | | | | |  __/ |   
  |_|   \___/|_|  |___/\___|____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                                   
  -> Uma ferramenta simples para reconhecimento rápido de rede <-
{RESET}
    """
    print(banner)

def run_scan():
    while True:
        clear_screen()
        print_banner()
        
        target = input(f"{YELLOW}[?] Digite o IP ou Host para escanear:{RESET} ")
        if not target:
            target = "127.0.0.1"
        
        ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
        log_file = "scan_report.txt"

        print(f"\n{BLUE}[!] Iniciando scan em:{RESET} {target}")
        print("-" * 50)

        open_ports = 0

        try:
            with open(log_file, "a") as file:
                file.write(f"\n--- Relatório de Scan: {datetime.now()} ---\n")
                file.write(f"Alvo: {target}\n")

                for port in ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5) 
                    result = s.connect_ex((target, port))
                    
                    if result == 0:
                        status = f"{GREEN}[+] Porta {port}: ABERTA{RESET}"
                        print(status)
                        file.write(f"- Porta {port} ABERTA\n")
                        open_ports += 1
                    s.close()
                
                if open_ports == 0:
                    print(f"{RED}[-] Nenhuma porta aberta comum encontrada.{RESET}")
                    file.write("- Nenhuma porta encontrada.\n")

        except KeyboardInterrupt:
            print(f"\n{RED}[!] Interrompido.{RESET}")
            break
        except Exception as e:
            print(f"{RED}[!] Erro: {e}{RESET}")

        print("-" * 50)
        print(f"{GREEN}[V] Scan finalizado e salvo em {log_file}{RESET}")
        
        # --- NOVA FUNÇÃO: CONTINUAR OU SAIR ---
        choice = input(f"\n{YELLOW}[?] Deseja escanear outro IP? (y/n):{RESET} ").lower()
        if choice != 'y':
            print(f"{BLUE}\n[!] Encerrando ferramenta... Até logo!{RESET}")
            break

if __name__ == "__main__":
    run_scan()