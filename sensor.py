import json
import random
import time
import paho.mqtt.client as mqtt

# 1. IoT Haberleşme Parametreleri
# test.mosquitto.org, dünya çapında geliştiricilerin kullandığı ücretsiz bir MQTT sunucusudur (broker).
# Topic (Kanal): Radyo frekansı gibi çalışır. Alıcı (dashboard) ve verici (sensör) bu isimde buluşur.
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "fabrikam/motor_01/telemetri"

# 2. MQTT İstemcisini Başlatma ve Bağlanma
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Sensör simülasyonu başlatıldı... Durdurmak için: Ctrl + C")

# Motorun ideal çalışma değerleri
normal_sicaklik = 50.0  # °C
normal_titresim = 1.5   # mm/s

try:
    while True:
        # Fiziksel ortamdaki doğal küçük dalgalanmalar (+/-)
        sicaklik = normal_sicaklik + random.uniform(-1.5, 1.5)
        titresim = normal_titresim + random.uniform(-0.2, 0.2)
        durum = "Normal"

        # %10 olasılıkla aşırı ısınma ve şiddetli sarsıntı (Arıza / Anomali Senaryosu)
        if random.random() < 0.10:
            sicaklik += random.uniform(20.0, 35.0)
            titresim += random.uniform(3.0, 5.0)
            durum = "Kritik Anomali"

        # Telemetri paketini JSON formatına çevirme
        paket = {
            "zaman": time.strftime("%H:%M:%S"),
            "sicaklik": round(sicaklik, 2),
            "titresim": round(titresim, 2),
            "durum": durum
        }

        # Veriyi MQTT kanalına yayınla (Publish)
        client.publish(TOPIC, json.dumps(paket))
        print(f"Sensör Verisi Yollandı -> {paket}")

        # Her 1 saniyede bir yeni ölçüm gönder
        time.sleep(1)

except KeyboardInterrupt:
    print("\nSensör durduruldu.")
    client.disconnect()
    