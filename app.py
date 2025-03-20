from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

<<<<<<< HEAD
# API Key untuk OpenWeatherMap (GANTI DENGAN API KEY MILIKMU)
API_KEY = "0e789f2f130b02441ed2b9cd27b0201f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

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

=======
>>>>>>> d3b1c4dcc6a87309a305bfa2d2cc6c8dc37ec55c
# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk menerima data dari form
@app.route('/submit', methods=['POST'])
def submit():
    data = {
        "kamar": request.form.get('kamar'),
        "tanggal_masuk": request.form.get('tanggal_masuk'),
        "temperatur": {"value": float(request.form.get('temperatur')), "status": "success"},
        "ph": {"value": float(request.form.get('ph')), "status": "success"},
        "garam": {"value": float(request.form.get('garam')), "status": "success"},
        "oksigen": {"value": float(request.form.get('oksigen')), "status": "success"},
        "debit": {"value": float(request.form.get('debit')), "status": "success"},
        "life": {"value": request.form.get('life'), "status": "success"},
        "pompa": request.form.get('pompa'),
        "aerator": request.form.get('aerator')
    }

    # Kembalikan respons JSON
    return jsonify({"status": "success", "message": "Data berhasil disimpan!", "data": data})

<<<<<<< HEAD
# Route untuk mengambil data kamar
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(dummyData)

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
    app.run(debug=True)
=======
# URL API eksternal
API_URL = "http://192.168.57.87:5000/data"

@app.route('/data', methods=['GET'])
def get_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Cek jika ada error pada response
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
>>>>>>> d3b1c4dcc6a87309a305bfa2d2cc6c8dc37ec55c
