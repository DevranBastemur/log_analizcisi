import csv
import io
import time
from flask import Flask, request, jsonify, render_template, send_file, Response, stream_with_context
from backend.log_reader import read_log_file
from backend.rule_engine import load_rules, apply_rules

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/health")
def health():
    return jsonify({"status": "ok"})



@app.route("/api/upload", methods=["POST"])
def upload_log():
    if "file" not in request.files:
        return jsonify({"error": "Dosya yok"}), 400

    file = request.files["file"]
    content = file.read().decode("utf-8", errors="ignore")

    lines = read_log_file(content)

    return jsonify({
        "message": "Log alındı",
        "total_lines": len(lines)
    })



@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "Dosya yok"}), 400

    file = request.files["file"]
    content = file.read().decode("utf-8", errors="ignore")

    lines = read_log_file(content)
    rules = load_rules()
    events = apply_rules(lines, rules)

    return jsonify({
        "total_lines": len(lines),
        "events_detected": len(events),
        "events": events
    })



@app.route("/api/export-csv", methods=["POST"])
def export_csv():
    if "file" not in request.files:
        return jsonify({"error": "Dosya yok"}), 400

    file = request.files["file"]
    content = file.read().decode("utf-8", errors="ignore")

    lines = read_log_file(content)
    rules = load_rules()
    events = apply_rules(lines, rules)

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["rule_id", "level", "description", "line_number", "log"])
    
    for event in events:
        cw.writerow([
            event["rule_id"],
            event["level"],
            event["description"],
            event["line_number"],
            event["log"]
        ])
    
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8-sig'))
    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="log_analiz_raporu.csv"
    )


@app.route("/api/stream")
def stream_logs():
    def generate():
        log_file = "logs/web_test.log"
        with open(log_file, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if line:
                    yield f"data: {line.strip()}\n\n"
                    time.sleep(0.1) # Okuma hızını simüle et
                else:
                    time.sleep(1)

    return Response(stream_with_context(generate()), mimetype="text/event-stream")



@app.route("/api/stats", methods=["POST"])
def stats():
    if "file" not in request.files:
        return jsonify({"error": "Dosya yok"}), 400

    file = request.files["file"]
    content = file.read().decode("utf-8", errors="ignore")
    lines = content.splitlines()

    return jsonify({
        "total_lines": len(lines),
        "empty_lines": sum(1 for l in lines if not l.strip()),
        "error_lines": sum(1 for l in lines if "error" in l.lower())
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
