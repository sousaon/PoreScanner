import os
import platform
import getpass
from datetime import datetime

def generate_dev_report(log_file="scan_report.txt"):
    report_file = "RELATORIO_TECNICO_DETALHADO.md"
    
    if not os.path.exists(log_file):
        return False

    # Informações da máquina do analista
    sys_info = {
        "user": getpass.getuser(),
        "node": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "date": datetime.now().strftime("%d/%m/%Y"),
        "time": datetime.now().strftime("%H:%M:%S")
    }

    with open(log_file, "r") as f:
        lines = f.readlines()
    
    # Inverte as linhas para que o scan mais recente apareça no topo (Timeline Reversa)
    lines.reverse()

    with open(report_file, "w", encoding="utf-8") as r:
        # Cabeçalho do Relatório
        r.write(f"# 🛡️ PORESCANNER | TIMELINE DE AUDITORIA TÉCNICA\n")
        r.write(f"**Relatório Atualizado em:** {sys_info['date']} às {sys_info['time']}\n\n")
        r.write("> Este documento contém o histórico acumulado de varreduras. Os eventos mais recentes aparecem primeiro.\n\n")
        
        r.write("--- \n\n")

        # Seção de Auditoria
        r.write("### 🛠️ INFORMAÇÕES DO ANALISTA\n")
        r.write(f"| Atributo | Detalhe |\n| :--- | :--- |\n")
        r.write(f"| **Analista Responsável** | `{sys_info['user']}` |\n")
        r.write(f"| **Estação de Trabalho** | `{sys_info['node']}` |\n")
        r.write(f"| **Sistema Operacional** | {sys_info['os']} |\n\n")

        # Tabela de Histórico
        r.write("## 🔍 HISTÓRICO DE EXPOSIÇÃO (TIMELINE)\n\n")
        r.write("| DATA/HORA SESSÃO | ALVO | PORTA | RISCO | RECOMENDAÇÃO TÉCNICA |\n")
        r.write("| :--- | :--- | :--- | :--- | :--- |\n")

        sessao_atual = "Data Desconhecida"
        alvo_atual = "IP Desconhecido"

        for line in lines:
            # Identifica a sessão (Invertido: FIM aparece antes do INICIO no loop)
            if "SESSAO_INICIO:" in line:
                sessao_atual = line.split("INICIO:")[1].strip().replace(" ---", "")
            
            if "Alvo:" in line:
                alvo_atual = line.split(":")[1].strip()

            if "ABERTA" in line:
                porta = "".join(filter(str.isdigit, line.split("Porta")[1]))
                
                # Matriz de Risco e Remediação Profissional
                risk, sev, rec = "🟡", "MÉDIO", "Revisar firewall."
                if porta == "21": risk, sev, rec = "🔴", "**ALTO**", "FTP sem criptografia. Migrar para **SFTP**."
                if porta == "23": risk, rec = "⚫", "**CRÍTICO**", "Telnet detectado. **Desativar serviço imediatamente.**"
                if porta == "22": risk, sev, rec = "🟢", "BAIXO", "Porta SSH segura. Verificar atualizações."
                if porta == "80": risk, sev, rec = "🟡", "MÉDIO", "HTTP exposto. Implementar **HTTPS (443)**."
                if porta == "3306": risk, sev, rec = "🔴", "**ALTO**", "Banco MySQL exposto. Bloquear acesso externo."

                r.write(f"| {sessao_atual} | {alvo_atual} | `{porta}` | {risk} {sev} | {rec} |\n")

        r.write("\n\n---\n")
        r.write(f"**Nota:** Este relatório é gerado automaticamente para fins de monitoramento contínuo.")
    
    return True

# Permite que o reporter seja testado sozinho se houver um log
if __name__ == "__main__":
    generate_dev_report()