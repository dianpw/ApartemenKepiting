from microdot import Microdot, Response
from machine import Pin, ADC
import network
import time
import json
import random

# ---- Setup WiFi ----
ssid = "BOE-"  # Ganti dengan SSID WiFi Anda
password = ""   # Ganti dengan password WiFi Anda

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("Menghubungkan ke WiFi...")
timeout = 10  # Waktu maksimal menunggu koneksi (detik)
start_time = time.time()

while not wifi.isconnected():
    if time.time() - start_time > timeout:
        print("Gagal terhubung ke WiFi. Periksa SSID/Password!")
        break
    time.sleep(1)
    print("Menghubungkan...")

if wifi.isconnected():
    print("Terhubung ke WiFi")
    ip_address = wifi.ifconfig()[0]
else:
    ip_address = "0.0.0.0"

print("IP Address:", ip_address)

# ---- Inisialisasi Microdot ----
app = Microdot()
Response.default_content_type = 'application/json'

# ---- Simulasi Sensor DS18B20 ----
sensors = ["Sensor_1", "Sensor_2", "Sensor_3", "Sensor_4", "Sensor_5", "Sensor_6"]

def simulate_temperatures():
    return [round(random.uniform(26, 30), 2) for _ in sensors]

def random_date():
    year = 2025
    month = random.randint(1, 3)
    day = random.randint(1, 15 if month == 3 else 28)
    return f"{day:02d}-{month:02d}-{year}"

# ---- Inisialisasi Sensor ----
adc_ph = ADC(Pin(26))         # pH Sensor
adc_tds = ADC(Pin(27))        # TDS Sensor
adc_o2 = ADC(Pin(28))         # Oksigen Sensor
adc_turbidity = ADC(Pin(29))  # Turbidity Sensor

# ---- Relay & Sensor Gerak ----
relay_pump = Pin(15, Pin.OUT)
aerator = Pin(16, Pin.OUT)
motion_sensor = Pin(14, Pin.IN)

# ---- Fungsi Status Sensor ----
def get_status(value, sensor_type):
    status_ranges = {
        "temperatur": (26, 30),
        "ph": (7.5, 8.5),
        "garam": (15, 25),
        "debit": (10, 30),
        "oksigen": (5, 7)
    }

    if sensor_type in status_ranges:
        low, high = status_ranges[sensor_type]
        
        if value < low:
            return {
                "status": "warning",
                "message": {
                    "temperatur": "Tidak Nafsu Makan",
                    "ph": "Kepiting Stres",
                    "garam": "Resiko Infeksi Bakteri",
                    "debit": "Kepiting Kurang Oksigen",
                    "oksigen": "Kepiting Kurang Oksigen"
                }[sensor_type]
            }
        elif value > high:
            return {
                "status": "warning",
                "message": {
                    "temperatur": "Kepiting Stres",
                    "ph": "Cangkang Rusak",
                    "garam": "Kepiting Dehidrasi",
                    "debit": "Kepiting Stres",
                    "oksigen": "Kepiting Stres"
                }[sensor_type]
            }

    return {"status": "success", "message": "Kondisi Normal"}

@app.route('/data')
def get_data(request):
    # Simulasi suhu dari sensor DS18B20
    temps = simulate_temperatures()

    # Status pompa dan aerator
    pump_status = relay_pump.value() == 1
    aerator_status = aerator.value() == 1

    # Simulasi pembacaan sensor lainnya
    ph_value = round(random.uniform(7.5, 8.5), 2)
    tds_value = round(random.uniform(15, 25), 2)
    
    # Jika pompa mati, debit dan oksigen di bawah range
    turbidity_value = round(random.uniform(5, 10), 2) if pump_status else round(random.uniform(3, 5), 2)
    oxygen_value = round(random.uniform(5, 7), 2) if pump_status and aerator_status else round(random.uniform(3, 5), 2)

    # Format data untuk setiap kamar
    data = []
    for i, temp_value in enumerate(temps):
        kamar_data = {
            "kamar": f"Kamar {i + 1}",
            "tanggal_masuk": random_date(),
            "temperatur": { "value": temp_value, **get_status(temp_value, "temperatur") },
            "ph": { "value": ph_value, **get_status(ph_value, "ph") },
            "garam": { "value": tds_value, **get_status(tds_value, "garam") },
            "oksigen": { "value": oxygen_value, **get_status(oxygen_value, "oksigen") },
            "debit": { "value": turbidity_value, **get_status(turbidity_value, "debit") },
            "life": { "value": "ada", "status": "success" },
            "pompa": "on" if pump_status else "off",
            "aerator": "on" if aerator_status else "off"
        }
        data.append(kamar_data)

    return json.dumps(data)

@app.route('/pump/<action>')
def control_pump(request, action):
    if action == 'on':
        relay_pump.value(1)
    elif action == 'off':
        relay_pump.value(0)
    return json.dumps({"pump_status": "on" if relay_pump.value() else "off"})

@app.route('/aerator/<action>')
def control_aerator(request, action):
    if action == 'on':
        aerator.value(1)
    elif action == 'off':
        aerator.value(0)
    return json.dumps({"aerator_status": "on" if aerator.value() else "off"})

# ---- Menjalankan Server ----
if ip_address != "0.0.0.0":
    print(f"Server berjalan di http://{ip_address}:80")
    app.run(host='0.0.0.0', port=80)  # Gunakan port 80
else:
    print("Server tidak bisa dijalankan karena gagal terhubung ke WiFi")
