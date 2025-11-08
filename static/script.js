// Menunggu sampai seluruh halaman HTML selesai di-load
document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('prediction-form');
    const resultsDiv = document.getElementById('results');
    const submitButton = document.getElementById('submit-button');

    // Menjalankan fungsi ini saat tombol 'submit' (Prediksi) ditekan
    form.addEventListener('submit', (e) => {
        // 1. Mencegah form me-refresh halaman (ini kuncinya!)
        e.preventDefault();

        // 2. Tampilkan status "Loading"
        resultsDiv.innerHTML = '<p>Sedang menghitung prediksi...</p>';
        submitButton.disabled = true;

        // 3. Kumpulkan semua data dari form
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // 4. Konversi data angka dari string ke number
        // (Semua input form adalah string, tapi model butuh angka)
        data['Price'] = parseFloat(data['Price']);
        data['Unit Cost'] = parseFloat(data['Unit Cost']);
        // (Tambahkan konversi lain jika ada input numerik baru)

        // 5. Kirim data ke API (service) di /predict menggunakan fetch()
        fetch('/predict', {
            method: 'POST', // Metode POST untuk mengirim data
            headers: {
                'Content-Type': 'application/json' // Bilang ke server kita kirim JSON
            },
            body: JSON.stringify(data) // Ubah objek JavaScript jadi string JSON
        })
        .then(response => response.json()) // Ambil balasan JSON dari server
        .then(results => {
            // 6. Tampilkan hasil prediksi di 'resultsDiv'
            
            // Cek jika server mengembalikan error
            if (results.error) {
                throw new Error(results.error);
            }

            // Ubah hasil 'high_profit' (1/0) jadi teks
            const highProfitText = results.high_profit === 1 
                ? 'High Profit (Rekomendasi: YA)' 
                : 'Low Profit (Rekomendasi: TIDAK)';

            // Format profit jadi mata uang Rupiah
            const profitIDR = results.profit.toLocaleString('id-ID', {
                style: 'currency',
                currency: 'IDR'
            });

            // Buat HTML baru untuk ditampilkan
            resultsDiv.innerHTML = `
                <ul>
                    <li>
                        <strong>📈 Prediksi Profit:</strong> 
                        ${profitIDR}
                    </li>
                    <li>
                        <strong>📦 Prediksi Kuantitas:</strong> 
                        ${results.quantity} unit
                    </li>
                    <li>
                        <strong>🎯 Rekomendasi:</strong> 
                        ${highProfitText}
                    </li>
                </ul>
            `;
            submitButton.disabled = false;
        })
        .catch(error => {
            // 7. Tampilkan jika terjadi error
            resultsDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${error.message}</p>`;
            submitButton.disabled = false;
        });
    });
});