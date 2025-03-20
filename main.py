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
<<<<<<< HEAD:Be.py
aerator = Pin(16, Pin.OUT)  # Tambahkan aerator sebagai relay terpisah
=======
# Sensor gerak (opsional)
motion_sensor = Pin(14, Pin.IN)
>>>>>>> d3b1c4dcc6a87309a305bfa2d2cc6c8dc37ec55c:main.py

def read_sensor(sensor):
    return round(sensor.read_u16() / 65535 * 3.3, 2)

def get_status(value, low, high):
    if low <= value <= high:
        return "success"
    return "warning"

@app.route('/data')
def get_data(request):
    # Simulasi suhu dari sensor DS18B20
    temps = simulate_temperatures()

    # Baca sensor lainnya
    ph_value = read_sensor(adc_ph) * 3
    tds_value = read_sensor(adc_tds) * 5
    oxygen_value = read_sensor(adc_o2) * 2
    turbidity_value = read_sensor(adc_turbidity) * 4

    # Format data untuk setiap kamar
    data = []
    for i, temp_value in enumerate(temps):
        kamar_data = {
            "kamar": f"Kamar {i + 1}",  # Nama kamar sesuai indeks
            "tanggal_masuk": random_date(),
            "temperatur": { "value": temp_value, "status": get_status(temp_value, 20, 30) },
            "ph": { "value": ph_value, "status": get_status(ph_value, 6.5, 8.5) },
            "garam": { "value": tds_value, "status": get_status(tds_value, 10, 15) },
            "oksigen": { "value": oxygen_value, "status": get_status(oxygen_value, 7, 9) },
            "debit": { "value": turbidity_value, "status": get_status(turbidity_value, 5, 10) },
            "life": { "value": "ada", "status": "success" },
            "pompa": "on" if relay_pump.value() else "off",
            "aerator": "on" if aerator.value() else "off"
        }
        data.append(kamar_data)

    return json.dumps(data)

@app.route('/submit', methods=['POST'])
def submit(request):
    try:
        data = request.json  # Gunakan JSON sebagai format umum API
        
        kamar = data.get("kamar", "Kamar 1")
        tanggal_masuk = data.get("tanggal_masuk", "12-02-2025")
        
        temperatur = float(data.get("temperatur", 25.0))
        ph = float(data.get("ph", 7.0))
        garam = float(data.get("garam", 12.0))
        oksigen = float(data.get("oksigen", 7.5))
        debit = float(data.get("debit", 8.0))
        life = data.get("life", "ada")

        # Ambil status pompa & aerator dari request
        pompa_status = data.get("pompa", "off").lower()
        aerator_status = data.get("aerator", "off").lower()

        # Set status relay berdasarkan request
        relay_pump.value(1 if pompa_status == "on" else 0)
        aerator.value(1 if aerator_status == "on" else 0)

        response_data = {
            "kamar": kamar,
            "tanggal_masuk": tanggal_masuk,
            "temperatur": {"value": temperatur, "status": get_status(temperatur, 20, 30)},
            "ph": {"value": ph, "status": get_status(ph, 6.5, 8.5)},
            "garam": {"value": garam, "status": get_status(garam, 10, 15)},
            "oksigen": {"value": oksigen, "status": get_status(oksigen, 7, 9)},
            "debit": {"value": debit, "status": get_status(debit, 5, 10)},
            "life": {"value": life, "status": "success"},
            "pompa": "on" if relay_pump.value() else "off",
            "aerator": "on" if aerator.value() else "off"
        }

        return json.dumps({"status": "success", "message": "Data berhasil disimpan!", "data": response_data})
    
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 400

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
<<<<<<< HEAD:Be.py
app.run(host=ip_address, port=5000)
=======
app.run(host=ip_address, port=5000)
>>>>>>> d3b1c4dcc6a87309a305bfa2d2cc6c8dc37ec55c:main.py
