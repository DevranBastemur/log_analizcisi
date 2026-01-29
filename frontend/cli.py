from rich.console import Console
from rich.table import Table

console = Console()


def show_menu():
    table = Table(title="LOG ANALİZCİSİ MENÜ")

    table.add_column("Seçim", style="cyan", justify="center")
    table.add_column("Açıklama", style="green")

    table.add_row("1", "Log dosyası analiz et")
    table.add_row("2", "Gerçek zamanlı log izleme")
    table.add_row("3", "CSV rapor üret")
    table.add_row("4", "Çıkış")

    console.print(table)


def get_choice():
    choice = console.input("\n[bold yellow]Seçiminizi girin (1-4): [/bold yellow]")
    return choice

def get_log_file_path():
    table = Table(title="LOG DOSYASI SEÇİMİ")
    table.add_column("No", style="cyan", justify="center")
    table.add_column("Dosya Yolu", style="green")

    logs = ["logs/sample.log", "logs/web_test.log", "/var/log/auth.log", "/var/log/syslog", "/var/log/nginx/access.log", "Manuel Giriş"]
    
    for idx, log in enumerate(logs, 1):
        table.add_row(str(idx), log)
    
    console.print(table)
    selection = console.input("\n[bold blue]Analiz edilecek log dosyasını seçin (Numara): [/bold blue]")
    
    if selection.isdigit() and 1 <= int(selection) < len(logs):
        return logs[int(selection)-1]
    elif selection == str(len(logs)):
        return console.input("[bold blue]Dosya yolunu girin: [/bold blue]")
    else:
        console.print("[red]Geçersiz seçim, varsayılan (logs/sample.log) kullanılıyor.[/red]")
        return "logs/sample.log"
