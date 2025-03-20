from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API Key untuk OpenWeatherMap (GANTI DENGAN API KEY MILIKMU)
API_KEY = "0e789f2f130b02441ed2b9cd27b0201f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# URL API eksternal
API_URL = "http://192.168.57.87:5000/data"

# Data dummy untuk simulasi
dummyData = [
    {
        "kamar": "Kamar 1",
        "tanggal_masuk": "12-02-2025",
        "temperatur": {"value": 25.15, "status": "success"},
        "ph": {"value": 7.4, "status": "warning"},
        "garam": {"value": 14, "status": "success"},
        "oksigen": {"value": 7.4, "status": "warning"},
        "debit": {"value": 9, "status": "success"},
        "life": {"value": "ada", "status": "success"},
        "pompa": "on",
        "aerator": "on"
    }
]

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk menerima data dari form
@app.route('/submit', methods=['POST'])
def submit():
    # Ambil data dari form
    data = request.get_json()
    kamar = data.get('kamar')
    jenis = data.get('jenis')
    status = data.get('status')

    # Lakukan sesuatu dengan data (misalnya simpan ke database)
    print(f"Data diterima: Kamar {kamar}, {jenis} = {status}")

    # Kembalikan respons JSON
    return jsonify({"status": "success", "message": "Data berhasil disimpan!", "data": data})

# Route untuk mengambil data kamar
@app.route('/data', methods=['GET'])
def get_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Cek jika ada error pada response
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route untuk mengambil data cuaca
@app.route('/cuaca', methods=['GET'])
def get_weather():
    kota = request.args.get('kota', 'Jakarta')  # Default ke Jakarta jika tidak ada input
    params = {
        "q": kota,
        "appid": API_KEY,
        "units": "metric",
        "lang": "id"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        hasil = {
            "kota": data["name"],
            "suhu": data["main"]["temp"],
            "cuaca": data["weather"][0]["description"]
        }
        return jsonify(hasil)
    else:
        return jsonify({"error": "Kota tidak ditemukan"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
