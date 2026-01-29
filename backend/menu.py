from frontend.cli import show_menu, get_choice, get_log_file_path, console
from backend.log_reader import read_log_file
from backend.rule_engine import load_rules, apply_rules
from backend.report import generate_csv_report
from backend.tailer import follow_log


def run_menu():
    rules = load_rules()
    last_events = []

    while True:
        show_menu()
        choice = get_choice()

        if choice == "1":
            print("\n[INFO] Log dosyası analiz ediliyor...\n")

            log_path = get_log_file_path()
            try:
                with open(log_path, "r", encoding="utf-8") as f:
                    content = f.read()
                lines = read_log_file(content)
            except Exception as e:
                print(f"[ERROR] Dosya okunamadı: {e}")
                lines = []

            if not lines:
                print("[WARNING] Okunacak log satırı yok.\n")
            else:
                last_events = apply_rules(lines, rules)

                print(f"[INFO] Toplam {len(lines)} satır okundu.\n")
                print("[INFO] Tespit edilen olaylar:\n")

                if not last_events:
                    print("Hiçbir şüpheli olay tespit edilmedi.\n")
                else:
                    for event in last_events:
                        print(
                            f"[{event['level']}] "
                            f"{event['description']} | "
                            f"Satır {event['line_number']} | "
                            f"{event['log']}"
                        )

                print("\n[INFO] Log analizi tamamlandı.\n")

        elif choice == "2":
            log_path = get_log_file_path()
            follow_log(log_path, rules)

        elif choice == "3":
            if not last_events:
                console.print("\n[bold red][UYARI] Rapor oluşturulacak veri yok. Lütfen önce log analizi yapın (Seçenek 1).[/bold red]\n")
            else:
                print("\n[INFO] CSV raporu üretiliyor...\n")
                generate_csv_report(last_events)

        elif choice == "4":
            print("\nÇıkış yapılıyor...")
            break

        else:
            print("\nGeçersiz seçim! Tekrar deneyin.\n")

if __name__ == "__main__":
    run_menu()
