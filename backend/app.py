from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

# LOAD MODEL
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '..', 'company_data.csv')

try:
    print("Memuat model...")
    model_profit = joblib.load(os.path.join(BASE_DIR, 'models/model_profit_predictor.pkl'))
    model_qty = joblib.load(os.path.join(BASE_DIR, 'models/model_quantity_predictor.pkl'))
    model_high = joblib.load(os.path.join(BASE_DIR, 'models/model_high_profit_classifier.pkl'))
    print("✅ Backend: Semua Model Berhasil Di-load.")
except Exception as e:
    print(f"❌ Backend Error Loading Model: {e}")
    model_profit, model_qty, model_high = None, None, None

# HELPER: FUNGSI TRANSLATOR
def fix_column_names(df):
    """
    Mengubah nama kolom dari format MySQL/JSON (Underscore)
    kembali ke format asli Model (Spasi).
    """
    mapping = {
        'Product_Category': 'Product Category',
        'Product_Sub_Category': 'Product Sub Category',
        'Promotion_Name': 'Promotion Name',
        'Product_Name': 'Product Name',
        'Unit_Cost': 'Unit Cost',
    }
    
    df_renamed = df.rename(columns=mapping)
    
    return df_renamed

# API 1: OPTIONS
@app.route('/api/options', methods=['GET'])
def get_options():
    try:
        cols_query = [
            'Channel', 'Promotion_Name', 'Product_Name', 'Manufacturer', 
            'Product_Sub_Category', 'Product_Category', 'Region', 'City', 'Country'
        ]
        
        # Langsung baca dari CSV
        df = pd.read_csv(CSV_PATH)
        # Ganti spasi di nama kolom dengan underscore agar konsisten
        df.columns = [c.replace(' ', '_') for c in df.columns]
        
        options = {}
        for col in cols_query:
            if col in df.columns:
                options[col] = sorted(df[col].dropna().unique().tolist())
            else:
                options[col] = []
        
        options['date_month'] = [str(i) for i in range(1, 13)]
        options['date_day_of_week'] = [str(i) for i in range(0, 7)]
        
        return jsonify(options)
    except Exception as e:
        print(f"Error di /api/options: {e}")
        return jsonify({'error': str(e)}), 500

# API 2: PREDICT PROFIT
@app.route('/api/predict/profit', methods=['POST'])
def predict_profit():
    if not model_profit: return jsonify({'error': 'Model Profit Failed Load'}), 500
    try:
        data = request.get_json()
        df_input = pd.DataFrame([data])
        
        df_ready = fix_column_names(df_input)
        
        pred = model_profit.predict(df_ready)[0]
        return jsonify({'result': float(pred)})
    except Exception as e:
        print(f"Error Profit: {e}")
        return jsonify({'error': str(e)}), 400

# API 3: PREDICT QUANTITY
@app.route('/api/predict/quantity', methods=['POST'])
def predict_quantity():
    if not model_qty: return jsonify({'error': 'Model Quantity Failed Load'}), 500
    try:
        data = request.get_json()
        df_input = pd.DataFrame([data])
        
        df_ready = fix_column_names(df_input)
        
        if 'Price' in df_ready.columns: df_ready['Price'] = pd.to_numeric(df_ready['Price'])
        if 'Unit Cost' in df_ready.columns: df_ready['Unit Cost'] = pd.to_numeric(df_ready['Unit Cost'])

        pred = model_qty.predict(df_ready)[0]
        return jsonify({'result': int(pred)})
    except Exception as e:
        print(f"Error Quantity: {e}")
        return jsonify({'error': str(e)}), 400

# API 4: PREDICT CLASSIFICATION
@app.route('/api/predict/high_profit_classifier', methods=['POST'])
def predict_classifier():
    if not model_high: return jsonify({'error': 'Model Class Failed Load'}), 500
    try:
        data = request.get_json()
        df_input = pd.DataFrame([data])
        
        df_ready = fix_column_names(df_input)
        
        pred = model_high.predict(df_ready)[0]
        return jsonify({'result': int(pred)})
    except Exception as e:
        print(f"Error Classification: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Host 0.0.0.0 agar bisa diakses dari IP lain jika perlu
    app.run(port=5000, debug=True, host='0.0.0.0')
