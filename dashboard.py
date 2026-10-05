import json
import time
import pandas as pd
import plotly.express as px
import streamlit as st
import paho.mqtt.client as mqtt

st.set_page_config(page_title="Motor Dijital İkizi", layout="wide")
st.title("🏭 Fabrika Motoru #01 - Canlı Dijital İkiz")

# Streamlit önbelleğinde global bir veri listesi ve istemci tutuyoruz.
# @st.cache_resource sayesinde sayfa yeniden yüklense bile bağlantı kopmaz ve veriler kaybolmaz.
@st.cache_resource
def mqtt_baglantisini_baslat():
    veriler = []
    
    def on_message(client, userdata, message):
        try:
            gelen = json.loads(message.payload.decode("utf-8"))
            veriler.append(gelen)
            if len(veriler) > 20:
                veriler.pop(0)
        except Exception as e:
            pass

    # paho-mqtt v2 ve v1 uyumlu istemci
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2 if hasattr(mqtt, "CallbackAPIVersion") else None)
    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883, 60)
    client.subscribe("fabrikam/motor_01/telemetri")
    client.loop_start()
    
    return veriler

# Listeyi al
canli_veriler = mqtt_baglantisini_baslat()

# Ekranı dinamik yenileme alanı
placeholder = st.empty()

with placeholder.container():
    if len(canli_veriler) > 0:
        df = pd.DataFrame(canli_veriler)
        en_son = df.iloc[-1]

        # Metrik Kartları
        col1, col2, col3 = st.columns(3)
        col1.metric("Anlık Sıcaklık", f"{en_son['sicaklik']} °C")
        col2.metric("Anlık Titreşim", f"{en_son['titresim']} mm/s")
        
        durum_renk = "🔴 TEHLİKE (Anomali)" if en_son["durum"] == "Kritik Anomali" else "🟢 NORMAL"
        col3.metric("Motor Durumu", durum_renk)

        # Grafikler
        fig_temp = px.line(df, x="zaman", y="sicaklik", title="Canlı Sıcaklık Grafiği (°C)", markers=True)
        fig_vib = px.line(df, x="zaman", y="titresim", title="Canlı Titreşim Grafiği (mm/s)", markers=True)

        c1, c2 = st.columns(2)
        c1.plotly_chart(fig_temp, use_container_width=True)
        c2.plotly_chart(fig_vib, use_container_width=True)
    else:
        st.warning("Sensörden telemetri verisi bekleniyor... 'sensor.py' dosyasının çalıştığından emin ol.")

# 1 saniye bekle ve arayüzü güncelle
time.sleep(1)
st.rerun()