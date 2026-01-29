import csv
import os


def generate_csv_report(events, output_path="reports/log_report.csv"):
    if not events:
        print("[WARNING] Raporlanacak olay yok.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "rule_id",
            "level",
            "description",
            "line_number",
            "log"
        ])

        for event in events:
            writer.writerow([
                event["rule_id"],
                event["level"],
                event["description"],
                event["line_number"],
                event["log"]
            ])

    print(f"[INFO] CSV raporu oluşturuldu: {output_path}")
