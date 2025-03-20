from microdot import Microdot, Response
from machine import Pin, ADC
import onewire, ds18x20
import network
import time
import json
import random

# Setup koneksi WiFi
ssid = "BOE-"  # Ganti dengan SSID WiFi Anda
password = ""  # Ganti dengan password WiFi Anda

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("Menghubungkan ke WiFi...")
while not wifi.isconnected():
    time.sleep(1)
    print("Menghubungkan...")

print("Terhubung ke WiFi")
ip_address = wifi.ifconfig()[0]
print("IP Address:", ip_address)

# Inisialisasi Microdot
app = Microdot()
Response.default_content_type = 'application/json'

# Simulasi sensor DS18B20 dengan 6 data suhu
sensors = ["Sensor_1", "Sensor_2", "Sensor_3", "Sensor_4", "Sensor_5", "Sensor_6"]

def simulate_temperatures():
    return [round(random.uniform(20, 30), 2) for _ in sensors]

def random_date():
    month = random.randint(1, 3)
    if month == 3:
        day = random.randint(1, 15)  # Hanya sampai pertengahan Maret
    else:
        day = random.randint(1, 28)  # Untuk Januari dan Februari
    year = 2025
    return "{:02d}-{:02d}-{}".format(day, month, year)

# Inisialisasi sensor lainnya (1 sensor per jenis)
adc_ph = ADC(Pin(26))  # Pin ADC untuk pH
adc_tds = ADC(Pin(27))  # Pin ADC untuk TDS
adc_o2 = ADC(Pin(28))  # Pin ADC untuk Oksigen
adc_turbidity = ADC(Pin(26))  # Pin ADC untuk Turbiditas

# Relay untuk pompa
relay_pump = Pin(15, Pin.OUT)
# Sensor gerak (opsional)
motion_sensor = Pin(14, Pin.IN)

def read_sensor(sensor):
    return round(sensor.read_u16() / 65535 * 3.3, 2)

def get_status(value, sensor_type):
    # Aturan status berdasarkan jenis sensor
    if sensor_type == "debit":
        if value > 30 or value < 10:
            return "warning"
    elif sensor_type == "ph":
        if value > 8.5 or value < 7.5:
            return "warning"
    elif sensor_type == "temperatur":
        if value > 30 or value < 26:
            return "warning"
    elif sensor_type == "garam":
        if value > 25 or value < 15:
            return "warning"
    # Default status success jika dalam rentang
    return "success"

@app.route('/data')
def get_data(request):
    # Simulasi suhu dari sensor DS18B20
    temps = simulate_temperatures()

    # Baca sensor lainnya (hanya sekali untuk semua kamar)
    '''ph_value = read_sensor(adc_ph) * 3
    tds_value = read_sensor(adc_tds) * 5
    oxygen_value = read_sensor(adc_o2) * 2
    turbidity_value = read_sensor(adc_turbidity) * 4
    '''
    ph_value = round(random.uniform(7.5, 8.5), 2)  # Rentang pH real
    tds_value = round(random.uniform(15, 25), 2)  # Rentang garam real
    oxygen_value = round(random.uniform(5, 7), 2)  # Rentang oksigen real
    turbidity_value = round(random.uniform(5, 10), 2)  # Rentang turbiditas real

    # Format data untuk setiap kamar
    data = []
    for i, temp_value in enumerate(temps):
        kamar_data = {
            "kamar": f"Kamar {i + 1}",  # Nama kamar sesuai indeks
            "tanggal_masuk": random_date(),
            "temperatur": { "value": temp_value, "status": get_status(temp_value, "temperatur") },
            "ph": { "value": ph_value, "status": get_status(ph_value, "ph") },
            "garam": { "value": tds_value, "status": get_status(tds_value, "garam") },
            "oksigen": { "value": oxygen_value, "status": get_status(oxygen_value, "oksigen") },
            "debit": { "value": turbidity_value, "status": get_status(turbidity_value, "debit") },
            "life": { "value": "ada", "status": "success" },
            "pompa": "on" if relay_pump.value() else "off",
            "aerator": "on"
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

print("Server berjalan di http://{}:5000".format(ip_address))
app.run(host=ip_address, port=5000)
