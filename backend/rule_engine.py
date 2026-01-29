import re
import os
import yaml


def load_rules():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(base_dir, "rules", "rules.yaml")

    try:
        with open(rules_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("rules", [])
    except Exception as e:
        print(f"[ERROR] Kurallar yüklenirken hata oluştu ({rules_path}): {e}")
        return []


def apply_rules(log_lines, rules):
    events = []

    for idx, line in enumerate(log_lines, start=1):
        if isinstance(line, dict):
            text = line.get("text", "")
            line_number = line.get("line", idx)
        else:
            text = str(line)
            line_number = idx

        for rule in rules:
            if re.search(rule["pattern"], text, re.IGNORECASE):
                events.append({
                    "rule_id": rule["id"],
                    "description": rule["description"],
                    "level": rule["level"],
                    "line_number": line_number,
                    "log": text
                })

    return events
