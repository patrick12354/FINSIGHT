document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('overall-form');
    const resultsDiv = document.getElementById('results');
    const submitButton = document.getElementById('submit-button');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        resultsDiv.innerHTML = '<p>Sedang menghitung prediksi gabungan...</p>';
        submitButton.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Konversi data numerik
        data['Price'] = parseFloat(data['Price']);
        data['Unit Cost'] = parseFloat(data['Unit Cost']);

        // --- INI BAGIAN PENTINGNYA ---
        // Kita akan membuat 2 API call terpisah

        // 1. Panggilan untuk Model Profit & Klasifikasi
        const fetchProfit = fetch('/predict/profit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data) // Model ini akan mengabaikan 'Price'
        }).then(res => {
            if (!res.ok) return res.json().then(err => { throw new Error(err.error) });
            return res.json();
        });

        // 2. Panggilan untuk Model Kuantitas
        const fetchQuantity = fetch('/predict/quantity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data) // Model ini akan MENGGUNAKAN 'Price'
        }).then(res => {
            if (!res.ok) return res.json().then(err => { throw new Error(err.error) });
            return res.json();
        });

        // 3. Jalankan keduanya secara paralel dan tunggu semua selesai
        Promise.all([fetchProfit, fetchQuantity])
            .then(([profitResults, qtyResults]) => {
                // 'profitResults' = { profit: ..., high_profit: ... }
                // 'qtyResults'    = { quantity: ... }
                
                // Format ke Dolar (USD)
                const profitUSD = profitResults.profit.toLocaleString('en-US', {
                    style: 'currency',
                    currency: 'USD'
                });
                
                const highProfitText = profitResults.high_profit === 1 
                    ? 'High Profit (Rekomendasi: YA)' 
                    : 'Low Profit (Rekomendasi: TIDAK)';

                // Tampilkan gabungan 3 hasil
                resultsDiv.innerHTML = `
                    <ul>
                        <li>
                            <strong>📈 Prediksi Profit:</strong> 
                            ${profitUSD}
                        </li>
                        <li>
                            <strong>🎯 Rekomendasi:</strong> 
                            ${highProfitText}
                        </li>
                        <li>
                            <strong>📦 Prediksi Kuantitas:</strong> 
                            ${qtyResults.quantity} unit
                        </li>
                    </ul>
                    <p style="font-size: 0.9em; color: #555; margin-top: 15px;">
                        Catatan: Prediksi Profit/Rekomendasi dihitung <strong>tanpa</strong> 'Price'/'Unit Cost' (anti-leakage), 
                        sedangkan Prediksi Kuantitas <strong>menggunakan</strong> 'Price'/'Unit Cost'.
                    </p>
                `;
                submitButton.disabled = false;
            })
            .catch(error => {
                // Tangkap error dari salah satu fetch
                resultsDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${error.message}</p>`;
                submitButton.disabled = false;
            });
    });
});