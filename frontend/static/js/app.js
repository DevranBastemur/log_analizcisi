async function analyzeLog() {
    const fileInput = document.getElementById("logFile");
    if (!fileInput.files.length) {
        alert("Lütfen bir log dosyası seç");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    document.getElementById("results").innerHTML = " Analiz ediliyor...";

    const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("stats").innerHTML = `
        <h3> İstatistikler</h3>
        <p>Toplam Satır: ${data.total_lines}</p>
        <p>Tespit Edilen Olay: ${data.events_detected}</p>
    `;

    if (data.events_detected === 0) {
        document.getElementById("results").innerHTML = " Şüpheli olay yok";
        return;
    }

    let html = "<h3> Olaylar</h3>";
    data.events.forEach(e => {
        html += `
            <div class="event ${e.level.toLowerCase()}">
                <b>[${e.level}]</b> ${e.description}<br>
                <small>${e.log}</small>
            </div>
        `;
    });

    document.getElementById("results").innerHTML = html;
}
