from flask import Flask, render_template, request, jsonify  # Import modul Flask untuk web API
import requests  # Import modul requests untuk mengakses API eksternal

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# API Key untuk OpenWeatherMap (GANTI DENGAN API KEY MILIKMU)
API_KEY = "0e789f2f130b02441ed2b9cd27b0201f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# URL API Pico W (Pastikan IP benar)
API_URL = "http://192.168.57.87/data"

# Data dummy jika tidak bisa terhubung ke Pico W
dummy_data = [
    {
        "kamar": "Kamar 1",
        "tanggal_masuk": "10-02-2025",
        "temperatur": {"value": 31.5, "status": "warning", "message": "Kepiting Stres"},
        "ph": {"value": 6.8, "status": "warning", "message": "Kepiting Stres"},
        "garam": {"value": 14, "status": "warning", "message": "Resiko Infeksi Bakteri"},
        "oksigen": {"value": 4.8, "status": "warning", "message": "Kepiting Kurang Oksigen"},
        "debit": {"value": 8, "status": "warning", "message": "Kepiting Kurang Oksigen"},
        "life": {"value": "ada", "status": "success"},
        "pompa": "off",
        "aerator": "off"
    },
    {
        "kamar": "Kamar 2",
        "tanggal_masuk": "12-02-2025",
        "temperatur": {"value": 27.5, "status": "success", "message": "Kondisi Normal"},
        "ph": {"value": 7.8, "status": "success", "message": "Kondisi Normal"},
        "garam": {"value": 20, "status": "success", "message": "Kondisi Normal"},
        "oksigen": {"value": 6.2, "status": "success", "message": "Kondisi Normal"},
        "debit": {"value": 15, "status": "success", "message": "Kondisi Normal"},
        "life": {"value": "ada", "status": "success"},
        "pompa": "on",
        "aerator": "on"
    },
    {
        "kamar": "Kamar 3",
        "tanggal_masuk": "15-02-2025",
        "temperatur": {"value": 25.5, "status": "warning", "message": "Tidak Nafsu Makan"},
        "ph": {"value": 8.9, "status": "warning", "message": "Cangkang Rusak"},
        "garam": {"value": 26, "status": "warning", "message": "Kepiting Dehidrasi"},
        "oksigen": {"value": 4.5, "status": "warning", "message": "Kepiting Kurang Oksigen"},
        "debit": {"value": 35, "status": "warning", "message": "Kepiting Stres"},
        "life": {"value": "ada", "status": "success"},
        "pompa": "on",
        "aerator": "off"
    },
    {
        "kamar": "Kamar 4",
        "tanggal_masuk": "18-02-2025",
        "temperatur": {"value": 28.5, "status": "success", "message": "Kondisi Normal"},
        "ph": {"value": 7.5, "status": "success", "message": "Kondisi Normal"},
        "garam": {"value": 18, "status": "success", "message": "Kondisi Normal"},
        "oksigen": {"value": 5.5, "status": "success", "message": "Kondisi Normal"},
        "debit": {"value": 20, "status": "success", "message": "Kondisi Normal"},
        "life": {"value": "ada", "status": "success"},
        "pompa": "on",
        "aerator": "on"
    }
]

# ================== ROUTE UTAMA (RENDER HALAMAN HTML) ==================
@app.route('/')
def index():
    """
    Menampilkan halaman utama aplikasi.
    HTML file `index.html` harus tersedia di folder `templates`.
    """
    return render_template('index.html')

# ================== ROUTE UNTUK MENERIMA DATA DARI FORM ==================
@app.route('/submit', methods=['POST'])
def submit():
    """
    Menerima data JSON dari form input, mencetaknya ke terminal, 
    dan mengembalikan respons JSON.
    """
    try:
        data = request.get_json()  # Mengambil data yang dikirim dalam format JSON
        if not data:  # Jika tidak ada data yang dikirim
            return jsonify({"status": "error", "message": "Data tidak ditemukan"}), 400

        # Mengambil nilai dari JSON dengan default jika tidak ada
        kamar = data.get('kamar', 'Tidak Diketahui')
        jenis = data.get('jenis', 'Tidak Diketahui')
        status = data.get('status', 'Tidak Diketahui')

        # Cetak data ke terminal (untuk debugging)
        print(f"Data diterima: Kamar {kamar}, {jenis} = {status}")

        # Mengembalikan respons JSON ke klien
        return jsonify({"status": "success", "message": "Data berhasil disimpan!", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ================== ROUTE UNTUK MENGAMBIL DATA DARI PICO W ATAU DUMMY ==================
@app.route('/data', methods=['GET'])
def get_data():
    """
    Mengambil data dari server Pico W. Jika gagal, mengembalikan data dummy.
    """
    try:
        response = requests.get(API_URL, timeout=5)  # Coba ambil data dari Pico W
        response.raise_for_status()  # Periksa error pada respons HTTP
        data = response.json()  # Konversi respons ke JSON

        # Pastikan data dari Pico W berupa list
        if not isinstance(data, list):
            return jsonify({"status": "error", "message": "Format data dari Pico W tidak valid"}), 500

        return jsonify(data)  # Kirim data dari Pico W jika sukses
    except requests.exceptions.Timeout:
        print("Timeout: Menggunakan data dummy.")
    except requests.exceptions.RequestException as e:
        print(f"Kesalahan saat mengambil data dari Pico W: {str(e)}")

    return jsonify(dummy_data)  # Jika gagal, kirim data dummy

# ================== ROUTE UNTUK MENGAMBIL DATA CUACA ==================
@app.route('/cuaca', methods=['GET'])
def get_weather():
    """
    Mengambil data cuaca dari OpenWeatherMap berdasarkan kota yang diminta.
    """
    kota = request.args.get('kota', 'Malang')  # Default ke Jakarta jika tidak ada input dari user
    params = {
        "q": kota,        # Nama kota yang diminta
        "appid": API_KEY,  # API Key OpenWeatherMap
        "units": "metric", # Menggunakan satuan Celcius
        "lang": "id"       # Bahasa Indonesia
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)  # Mengirim permintaan dengan batas waktu 5 detik
        response.raise_for_status()  # Memeriksa apakah ada kesalahan HTTP

        data = response.json()  # Konversi respons ke JSON
        hasil = {
            "kota": data.get("name", "Tidak diketahui"),
            "suhu": data["main"].get("temp", "Tidak tersedia"),
            "cuaca": data["weather"][0].get("description", "Tidak tersedia")
        }

        return jsonify(hasil)  # Mengembalikan data dalam format JSON
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Timeout saat mengambil data cuaca"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Kesalahan saat mengambil data cuaca: {str(e)}"}), 500

# ================== MENJALANKAN SERVER FLASK ==================
if __name__ == '__main__':
    """
    Menjalankan server Flask di semua alamat jaringan (0.0.0.0)
    pada port 5000 dengan mode debug aktif.
    """
    app.run(debug=True, port=5000, host='0.0.0.0')
