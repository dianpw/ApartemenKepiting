from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

    # Tambahkan data ke dummyData
    dummyData.append(data)

    # Kembalikan respons JSON
    return jsonify({"status": "success", "message": "Data berhasil disimpan!", "data": data})


# Route untuk mengambil data kamar
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(dummyData)


if __name__ == '__main__':
    app.run(debug=True)