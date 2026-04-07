import socket
import os
from datetime import datetime
# Importa a função do arquivo reporter.py
from reporter import generate_dev_report 

# Cores para o terminal
BLUE, GREEN, YELLOW, RED, RESET = '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{BLUE}
   ____                      ____                                  
  |  _ \ ___  _ __ ___  ___ / ___|  ___ __ _ _ __  _ __   ___ _ __ 
  | |_) / _ \| '__/ __|/ _ \\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
  |  __/ (_) | |  \__ \  __/ ___) | (_| (_| | | | | | | |  __/ |   
  |_|   \___/|_|  |___/\___|____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                                   
  -> Scanner de Rede & Gerador de Relatórios Técnicos v2.5 <-
{RESET}
    """
    print(banner)

def run_scan():
    log_file = "scan_report.txt"
    
    while True:
        clear_screen()
        print_banner()
        
        target = input(f"{YELLOW}[?] Digite o IP ou Host para escanear:{RESET} ") or "127.0.0.1"
        ports = [21, 22, 23, 80, 443, 3306, 8080]
        
        print(f"\n{BLUE}[!] Iniciando varredura em {target}...{RESET}")
        
        try:
            with open(log_file, "a") as file:
                # Marcação de início de sessão para a Timeline
                timestamp_inicio = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                file.write(f"\n--- SESSAO_INICIO: {timestamp_inicio} ---\n")
                file.write(f"Alvo: {target}\n")
                
                for port in ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    result = s.connect_ex((target, port))
                    
                    if result == 0:
                        print(f"{GREEN}[+] Porta {port}: ABERTA{RESET}")
                        hora_detecao = datetime.now().strftime('%H:%M:%S')
                        file.write(f"[{hora_detecao}] Porta {port} ABERTA\n")
                    s.close()
                
                file.write(f"--- SESSAO_FIM ---\n")
        except Exception as e:
            print(f"{RED}[!] Erro durante o scan: {e}{RESET}")

        if input(f"\n{YELLOW}[?] Deseja escanear outro alvo? (y/n):{RESET} ").lower() != 'y':
            print(f"\n{BLUE}[*] Finalizando sessão...{RESET}")
            ans = input(f"{YELLOW}[?] Deseja gerar o relatório técnico de Timeline? (y/n):{RESET} ").lower()
            
            if ans == 'y':
                if generate_dev_report(log_file):
                    print(f"{GREEN}[V] Relatório 'RELATORIO_TECNICO_DETALHADO.md' atualizado com sucesso!{RESET}")
            
            print(f"{BLUE}\n[!] Encerrando. Até logo, Eduardo!{RESET}")
            break

if __name__ == "__main__":
    run_scan()