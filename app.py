from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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
    
    '''data = {
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
    }'''

    # Kembalikan respons JSON
    return jsonify({"status": "success", "message": "Data berhasil disimpan!", "data": data})

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