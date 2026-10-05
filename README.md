# 🏭 Endüstriyel Motor Dijital İkizi & Canlı Telemetri Takip Sistemi

Gerçek zamanlı sensör verileriyle çalışan, MQTT tabanlı haberleşme mimarisine sahip ve operasyonel anomalileri anlık olarak tespit eden uçtan uca bir dijital ikiz simülasyonu.

## 📌 Proje Mimarisi

```text
[Fiziksel Sensör Simülatörü (sensor.py)]
                  │
                  ▼ (MQTT - JSON Telemetri)
        [test.mosquitto.org]
                  │
                  ▼ (Subscribed Stream)
    [Canlı Streamlit & Plotly Dashboard]