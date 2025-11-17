import pandas as pd
import joblib
from flask import Flask, render_template, request, jsonify
import numpy as np
import os

# --- 1. SETUP PATH & APP ---
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

# DAFTAR FITUR FINAL (berdasarkan feature importance)
FEATURES_M1_CATEGORICAL = [
    'Product Sub Category', 'Manufacturer', 'City', 'Channel', 
    'date_month', 'Promotion Name', 'date_day_of_week'
]
FEATURES_M3_CATEGORICAL = [
    'Product Sub Category', 'City', 'Manufacturer', 'Product Category', 
    'date_month', 'date_day_of_week', 'Promotion Name'
]
FEATURES_M2_CATEGORICAL = [
    'Product Category', 'date_month', 'date_day_of_week', 'Promotion Name'
]

# Gabungkan semua fitur kategorikal unik yang perlu di-load
ALL_UNIQUE_CATEGORICAL = sorted(list(
    set(FEATURES_M1_CATEGORICAL + FEATURES_M3_CATEGORICAL + FEATURES_M2_CATEGORICAL)
))

# --- 2. FUNGSI LOAD DATA FORM ---
def load_form_options():
    try:
        csv_path = os.path.join(BASE_DIR, 'company_data.csv')
        df = pd.read_csv(csv_path)

        # Gunakan daftar fitur unik kita
        options = {}
        for col in ALL_UNIQUE_CATEGORICAL:
            if col in df.columns:
                unique_values = df[col].dropna().unique()
                unique_values.sort()
                options[col] = list(unique_values)

        # Tambahkan fitur tanggal/waktu secara manual
        options['date_month'] = [str(i) for i in range(1, 13)]
        options['date_day_of_week'] = [str(i) for i in range(0, 7)]

        print("Data dropdown/form berhasil di-load (Hanya Fitur Signifikan).")
        return options
    except FileNotFoundError:
        print(f"ERROR: 'company_data.csv' tidak ditemukan di {BASE_DIR}")
        return {}

# --- 3. LOAD MODEL & DATA FORM ---
model_profit_path = os.path.join(BASE_DIR, 'models', 'model_profit_predictor.pkl')
model_qty_path = os.path.join(BASE_DIR, 'models', 'model_quantity_predictor.pkl')
model_high_profit_path = os.path.join(BASE_DIR, 'models', 'model_high_profit_classifier.pkl')

print("Memuat model... Harap tunggu.")
try:
    model_profit = joblib.load(model_profit_path)
    model_qty = joblib.load(model_qty_path)
    model_high_profit = joblib.load(model_high_profit_path)
    print(f"Model berhasil di-load dari: {BASE_DIR}/models")
    ALL_FORM_OPTIONS = load_form_options()
except Exception as e:
    print(f"ERROR saat load: {e}")
    model_profit, model_qty, model_high_profit, ALL_FORM_OPTIONS = None, None, None, {}

# ===================================================================
# --- ROUTE UNTUK MENAMPILKAN HALAMAN HTML (FRONTEND) ---
# ===================================================================

@app.route('/')
def home():
    """Menampilkan halaman menu utama."""
    return render_template('index.html') # Menu akan di-update

@app.route('/profit')
def page_profit():
    """Halaman HANYA untuk Model 1 (Profit Regresi)."""
    # Filter: Kirim HANYA data yang dibutuhkan M1
    form_data_m1 = {feat: ALL_FORM_OPTIONS.get(feat, []) for feat in FEATURES_M1_CATEGORICAL}
    return render_template('profit_page.html', form_data=form_data_m1)

@app.route('/quantity')
def page_quantity():
    """Halaman untuk Model 2 (Kuantitas)."""
    # Filter: Kirim HANYA data yang dibutuhkan M2
    form_data_m2 = {feat: ALL_FORM_OPTIONS.get(feat, []) for feat in FEATURES_M2_CATEGORICAL}
    return render_template('quantity.html', form_data=form_data_m2)

@app.route('/classification')
def page_classification():
    """Halaman HANYA untuk Model 3 (Klasifikasi)."""
    form_data_m3 = {feat: ALL_FORM_OPTIONS.get(feat, []) for feat in FEATURES_M3_CATEGORICAL}
    return render_template('classification_page.html', form_data=form_data_m3)

@app.route('/overall')
def page_overall():
    """Halaman gabungan."""
    # Halaman overall perlu SEMUA opsi
    return render_template('overall.html', form_data=ALL_FORM_OPTIONS)

@app.route('/collaboration')
def page_collaboration():
    """Menampilkan halaman kerja sama."""
    return render_template('collaboration.html')


# ===================================================================
# --- ROUTE UNTUK API (BACKEND SERVICE) ---
# ===================================================================

@app.route('/predict/profit', methods=['POST'])
def predict_profit():
    """API ini HANYA menjalankan Model 1 (Profit)."""
    if not model_profit:
        return jsonify({'error': 'Model profit tidak ter-load.'}), 500
    try:
        data = request.get_json()
        sample_df = pd.DataFrame([data])
        pred_profit = model_profit.predict(sample_df)[0]
        return jsonify({'profit': float(pred_profit)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict/quantity', methods=['POST'])
def predict_quantity():
    """API ini HANYA menjalankan Model 2 (Kuantitas)."""
    if not model_qty:
        return jsonify({'error': 'Model kuantitas tidak ter-load.'}), 500
    try:
        data = request.get_json()
        sample_df = pd.DataFrame([data])
        pred_qty = model_qty.predict(sample_df)[0]
        return jsonify({'quantity': int(pred_qty)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict/classification', methods=['POST'])
def predict_classification():
    """API ini HANYA menjalankan Model 3 (Klasifikasi)."""
    if not model_high_profit:
        return jsonify({'error': 'Model klasifikasi tidak ter-load.'}), 500
    try:
        data = request.get_json()
        sample_df = pd.DataFrame([data])
        pred_high_profit = model_high_profit.predict(sample_df)[0]
        return jsonify({'high_profit': int(pred_high_profit)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# --- Menjalankan server ---
if __name__ == '__main__':
    app.run(debug=True)