def analyze_log(log_content: str) -> dict:
    lines = log_content.splitlines()
    events = []

    for idx, line in enumerate(lines, start=1):
        if "error" in line.lower():
            events.append({
                "severity": "HIGH",
                "line": idx,
                "message": line.strip()
            })
        elif "warning" in line.lower():
            events.append({
                "severity": "MEDIUM",
                "line": idx,
                "message": line.strip()
            })

    return {
        "total_lines": len(lines),
        "events_detected": len(events),
        "events": events
    }
