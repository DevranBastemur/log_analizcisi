# Log Analizcisi Projesi

Bu proje, sistem log dosyalarını analiz ederek şüpheli aktiviteleri (SSH brute-force, yetkisiz erişim, sistem hataları vb.) tespit eden, kural tabanlı bir güvenlik aracıdır. Hem komut satırı (CLI) hem de Web arayüzü üzerinden kullanılabilir.

## Özellikler

*   **Dosya Bazlı Analiz:** `/var/log/auth.log`, `syslog`, `nginx/access.log` gibi dosyaları okur.
*   **Kural Tabanlı Tespit:** YAML formatında tanımlanmış kurallar ile (Regex) tehditleri yakalar.
*   **Gerçek Zamanlı İzleme:** Log dosyalarını anlık olarak takip eder.
*   **Raporlama:** Analiz sonuçlarını CSV formatında dışa aktarır.
*   **Web Arayüzü:** Dosya yükleme ve canlı izleme imkanı sunar.
*   **Docker Desteği:** Tüm bağımlılıkları ile birlikte konteyner içinde çalışır.

## Kurulum ve Çalıştırma

Proje Dockerize edilmiştir. Çalıştırmak için bilgisayarınızda Docker'ın yüklü olması yeterlidir.

### 1. İmajı Oluşturma

Terminali proje dizininde açın ve şu komutu çalıştırın:

```bash
docker build -t log-analizcisi .
```

### 2. Projeyi Çalıştırma

**Web Arayüzü İçin (Önerilen):**

```bash
docker run -it --rm -p 5000:5000 log-analizcisi
```

Tarayıcınızdan **http://localhost:5000** adresine gidin.

**Komut Satırı (CLI) Modu İçin:**

```bash
docker run -it --rm log-analizcisi python backend/menu.py


 Notlar
 Web arayüzündeki "Canlı İzleme" demosu, proje içindeki `logs/web_test.log` dosyasını simüle eder.
Sistem loglarını (örn: `/var/log`) okumak için Docker'ı `-v /var/log:/var/log` parametresi ile çalıştırmanız gerekir.