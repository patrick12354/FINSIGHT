import pandas as pd
from sqlalchemy import create_engine
import os

# Path file CSV (otomatis mengikuti lokasi script)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(BASE_DIR, 'company_data.csv')

print(f"Mencoba membaca CSV dari: {csv_path}")


# Load CSV
df = pd.read_csv(csv_path)
print("Berhasil membaca CSV!")

# Rapikan nama kolom (hindari spasi untuk MySQL)
df.columns = [c.replace(' ', '_') for c in df.columns]

# Koneksi ke MySQL (XAMPP)
db_connection_str = 'mysql+pymysql://root:@localhost/finsight_db'
db_connection = create_engine(db_connection_str)

# Input ke database
print("Memasukkan data ke MySQL...")
df.to_sql('sales_data', con=db_connection, if_exists='replace', index=False)

print("-" * 30)
print("SUKSES! Data berhasil dipindah ke tabel 'sales_data'.")
print("-" * 30)
