Untuk versi Bahasa Indonesia, silakan scroll ke bawah.


# FINSIGHT: Business Analysis and Prediction Web App

FINSIGHT is a web application for business analysis and prediction that uses machine learning. This application is capable of performing three main predictions:
1.  **Profit Prediction**: Estimates the profit from a future transaction.
2.  **Quantity Prediction**: Estimates the number of items that will be ordered.
3.  **High Profit Classification**: Determines whether a transaction has the potential to generate high profits.

This application aims to assist in business decision-making based on historical data.

---

## Architecture

This application uses a microservices architecture, which means the frontend (user interface) and backend (application logic) operate as two separate services.

### 1. Backend (Port 5000)
- Built with Python and the Flask framework.
- Serves as an API (Application Programming Interface).
- Handles all business logic, connection to the database (MySQL), and machine learning computations.
- Loads `.pkl` models when run to make predictions.

### 2. Frontend (Port 8000)
- Built with Python and the Flask framework, specifically for serving web pages.
- Responsible for displaying the user interface (UI) through HTML pages.
- Communicates with the backend to get data and send prediction requests.

---

## Folder Structure

Here is an explanation of the important files in this project:

-   `FINSIGHT/`
    -   `overview.txt`: This file contains a general explanation of the project.
    -   `cara run.txt`: Instructions for running the frontend and backend servers.
    -   `company_data.csv`: The raw dataset used to train the machine learning models.
    -   `prototype.ipynb`: Jupyter Notebook containing the entire experimental process, from data cleaning, feature engineering, to training and saving the machine learning models.
    -   `migrate_db.py`: A script to migrate data from `company_data.csv` into a MySQL database.
    -   `backend/`:
        -   `app.py`: The core of the backend. It is a Flask API server that receives, processes requests with ML models, and provides responses.
        -   `requirements.txt`: A list of Python libraries required by the backend.
        -   `models/`: A directory containing the pre-trained and ready-to-use machine learning models (`.pkl`).
    -   `frontend/`:
        -   `app.py`: A Flask web server responsible for displaying HTML pages (templates) to the user.
        -   `templates/`: Contains HTML files that make up the application's interface.
        -   `static/`: Contains static files such as CSS for styling (`style.css`) and images (`images/`).

---

## API Workflow (GET & POST)

Interaction between the frontend and backend occurs through two main types of requests:

### 1. GET Flow (Fetching Options for Forms)

This flow occurs when the user first loads a prediction page (e.g., the "Profit Prediction" page). The purpose is to populate the options in the form (e.g., a list of countries, product categories, etc.).

1.  The user opens a page in the browser, for example, `http://127.0.0.1:8000/profit`.
2.  The Frontend Server (`frontend/app.py`) receives this request.
3.  Before displaying the HTML page, the Frontend Server sends a `GET` request to the Backend API at `http://127.0.0.1:5000/api/options`.
4.  The Backend API (`backend/app.py`) receives the `GET` request, retrieves unique data from the database (such as a list of countries, cities, categories), then sends it back to the Frontend Server in JSON format.
5.  The Frontend Server receives this JSON data and injects it into the HTML template (`profit_page.html`), so the form can display all available options.
6.  The complete HTML page is displayed in the user's browser.

### 2. POST Flow (Sending Data for Prediction)

This flow occurs when the user has filled out the form and presses the "Predict" button.

1.  The user fills in the data on the form in the browser and presses the "Predict" button.
2.  JavaScript in the User's Browser retrieves all the data from the form.
3.  JavaScript in the User's Browser sends a `POST` request directly to the corresponding Backend API endpoint (e.g., `http://127.0.0.1:5000/api/predict/profit`). The form data is sent in JSON format.
4.  The Backend API (`backend/app.py`) receives the JSON data, processes it, and feeds it into the appropriate machine learning model.
5.  The ML model generates a prediction (e.g., a profit figure).
6.  The Backend API sends the prediction result back to the User's Browser in JSON format.
7.  JavaScript in the User's Browser receives the prediction result and displays it on the page without needing to reload the entire page.

---

## Prerequisites

- Python 3.x
- XAMPP
- Virtual environment (recommended)

## Dependencies

### Backend
```
Flask
pandas
scikit-learn
```

### Frontend
```
Flask
```

---

## How to Run the Project

1.  **Start the database server**: Make sure the XAMPP application is open and the "MySQL Database" module is started (Running).
2.  **Migrate the database**: If the `finsight_db` database has not been created, run the `migrate_db.py` script.
3.  **Run the backend**:
    - Open a new terminal.
    - Navigate to the `backend` directory.
    - Activate the virtual environment.
    - Run the command: `python app.py`
    - Wait until you see the message: "Running on http://127.0.0.1:5000"
4.  **Run the frontend**:
    - Open a new terminal tab or window.
    - Navigate to the `frontend` directory.
    - Activate the virtual environment.
    - Run the command: `python app.py`
    - Wait until you see the message: "Running on http://127.0.0.1:8000"
5.  **Access the application**:
    - Open a browser and go to `http://127.0.0.1:8000`.


---

# FINSIGHT: Aplikasi Web Analisis dan Prediksi Bisnis

FINSIGHT adalah aplikasi web untuk analisis dan prediksi bisnis yang menggunakan machine learning. Aplikasi ini mampu melakukan tiga prediksi utama:
1.  **Prediksi Profit**: Memperkirakan keuntungan dari transaksi di masa depan.
2.  **Prediksi Kuantitas**: Memperkirakan jumlah barang yang akan dipesan.
3.  **Klasifikasi Profit Tinggi**: Menentukan apakah sebuah transaksi berpotensi menghasilkan keuntungan tinggi.

Aplikasi ini bertujuan untuk membantu pengambilan keputusan bisnis berdasarkan data historis.

---

## Arsitektur

Aplikasi ini menggunakan arsitektur microservices, yang berarti frontend (antarmuka pengguna) dan backend (logika aplikasi) berjalan sebagai dua layanan terpisah.

### 1. Backend (Port 5000)
- Dibangun dengan Python dan framework Flask.
- Berperan sebagai API (Application Programming Interface).
- Menangani semua logika bisnis, koneksi ke database (MySQL), dan komputasi machine learning.
- Memuat model `.pkl` saat dijalankan untuk melakukan prediksi.

### 2. Frontend (Port 8000)
- Dibangun dengan Python dan framework Flask, khusus untuk menyajikan halaman web.
- Bertanggung jawab untuk menampilkan antarmuka pengguna (UI) melalui halaman HTML.
- Berkomunikasi dengan backend untuk mendapatkan data dan mengirim permintaan prediksi.

---

## Struktur Folder

Berikut adalah penjelasan mengenai file-file penting dalam proyek ini:

-   `FINSIGHT/`
    -   `overview.txt`: File ini berisi penjelasan umum mengenai proyek.
    -   `cara run.txt`: Petunjuk untuk menjalankan server frontend dan backend.
    -   `company_data.csv`: Dataset mentah yang digunakan untuk melatih model machine learning.
    -   `prototype.ipynb`: Jupyter Notebook yang berisi seluruh proses eksperimen, mulai dari pembersihan data, rekayasa fitur, hingga pelatihan dan penyimpanan model machine learning.
    -   `migrate_db.py`: Skrip untuk memigrasikan data dari `company_data.csv` ke dalam database MySQL.
    -   `backend/`:
        -   `app.py`: Inti dari backend. Ini adalah server API Flask yang menerima, memproses permintaan dengan model ML, dan memberikan respons.
        -   `requirements.txt`: Daftar pustaka Python yang dibutuhkan oleh backend.
        -   `models/`: Direktori yang berisi model-model machine learning yang sudah dilatih dan siap pakai (`.pkl`).
    -   `frontend/`:
        -   `app.py`: Server web Flask yang bertanggung jawab untuk menampilkan halaman HTML (template) kepada pengguna.
        -   `templates/`: Berisi file-file HTML yang membentuk antarmuka aplikasi.
        -   `static/`: Berisi file-file statis seperti CSS untuk styling (`style.css`) dan gambar (`images/`).

---

## Alur Kerja API (GET & POST)

Interaksi antara frontend dan backend terjadi melalui dua jenis permintaan utama:

### 1. Alur GET (Mengambil Opsi untuk Formulir)

Alur ini terjadi saat pengguna pertama kali memuat halaman prediksi (misalnya, halaman "Prediksi Profit"). Tujuannya adalah untuk mengisi opsi-opsi dalam formulir (misalnya, daftar negara, kategori produk, dll.).

1.  Pengguna membuka halaman di browser, misalnya `http://127.0.0.1:8000/profit`.
2.  Server Frontend (`frontend/app.py`) menerima permintaan ini.
3.  Sebelum menampilkan halaman HTML, Server Frontend mengirimkan permintaan `GET` ke API Backend di `http://127.0.0.1:5000/api/options`.
4.  API Backend (`backend/app.py`) menerima permintaan `GET`, mengambil data unik dari database (seperti daftar negara, kota, kategori), lalu mengirimkannya kembali ke Server Frontend dalam format JSON.
5.  Server Frontend menerima data JSON ini dan menyuntikkannya ke dalam template HTML (`profit_page.html`), sehingga formulir dapat menampilkan semua opsi yang tersedia.
6.  Halaman HTML yang lengkap ditampilkan di browser pengguna.

### 2. Alur POST (Mengirim Data untuk Prediksi)

Alur ini terjadi saat pengguna telah mengisi formulir dan menekan tombol "Prediksi".

1.  Pengguna mengisi data pada formulir di browser dan menekan tombol "Prediksi".
2.  JavaScript di Browser Pengguna mengambil semua data dari formulir.
3.  JavaScript di Browser Pengguna mengirimkan permintaan `POST` langsung ke endpoint API Backend yang sesuai (misalnya, `http://127.0.0.1:5000/api/predict/profit`). Data formulir dikirim dalam format JSON.
4.  API Backend (`backend/app.py`) menerima data JSON, memprosesnya, dan memasukkannya ke dalam model machine learning yang sesuai.
5.  Model ML menghasilkan prediksi (misalnya, angka profit).
6.  API Backend mengirimkan hasil prediksi kembali ke Browser Pengguna dalam format JSON.
7.  JavaScript di Browser Pengguna menerima hasil prediksi dan menampilkannya di halaman tanpa perlu memuat ulang seluruh halaman.

---

## Prasyarat

- Python 3.x
- XAMPP
- Lingkungan virtual (disarankan)

## Ketergantungan

### Backend
```
Flask
pandas
scikit-learn
```

### Frontend
```
Flask
```

---

## Cara Menjalankan Proyek

1.  **Mulai server database**: Pastikan aplikasi XAMPP terbuka dan modul "MySQL Database" sudah dimulai (Running).
2.  **Migrasikan database**: Jika database `finsight_db` belum dibuat, jalankan skrip `migrate_db.py`.
3.  **Jalankan backend**:
    - Buka terminal baru.
    - Arahkan ke direktori `backend`.
    - Aktifkan lingkungan virtual.
    - Jalankan perintah: `python app.py`
    - Tunggu hingga muncul pesan: "Running on http://127.0.0.1:5000"
4.  **Jalankan frontend**:
    - Buka tab atau jendela terminal baru.
    - Arahkan ke direktori `frontend`.
    - Aktifkan lingkungan virtual.
    - Jalankan perintah: `python app.py`
    - Tunggu hingga muncul pesan: "Running on http://127.0.0.1:8000"
5.  **Akses aplikasi**:
    - Buka browser dan pergi ke `http://127.0.0.1:8000`.