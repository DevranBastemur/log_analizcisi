import time
import re
from frontend.cli import console

def follow_log(file_path, rules):
    console.print(f"\n[bold blue][INFO] {file_path} izleniyor... (Çıkış için CTRL+C)[/bold blue]\n")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                line = line.strip()
                if not line:
                    continue

                for rule in rules:
                    if re.search(rule["pattern"], line, re.IGNORECASE):
                        level_style = "green"
                        if rule["level"] == "HIGH": level_style = "bold yellow"
                        if rule["level"] == "CRITICAL": level_style = "bold red"
                        
                        console.print(f"[{level_style}][{rule['level']}] {rule['description']}: {line}[/{level_style}]")

    except KeyboardInterrupt:
        console.print("\n[bold yellow][INFO] İzleme durduruldu.[/bold yellow]")
    except FileNotFoundError:
        console.print(f"[bold red][ERROR] Dosya bulunamadı: {file_path}[/bold red]")
    except Exception as e:
        console.print(f"[bold red][ERROR] Hata: {e}[/bold red]")