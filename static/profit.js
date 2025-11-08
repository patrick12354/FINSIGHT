document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('profit-form');
    const resultsDiv = document.getElementById('results');
    const submitButton = document.getElementById('submit-button');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        resultsDiv.innerHTML = '<p>Sedang menghitung prediksi profit...</p>';
        submitButton.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Model ini TIDAK butuh konversi Price/Unit Cost
        
        // Kirim data ke API /predict/profit
        fetch('/predict/profit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                // Tangkap error 400/500 dari server
                return response.json().then(err => { throw new Error(err.error) });
            }
            return response.json();
        })
        .then(results => {
            // Format ke Dolar (USD)
            const profitUSD = results.profit.toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD'
            });

            const highProfitText = results.high_profit === 1 
                ? 'High Profit (Rekomendasi: YA)' 
                : 'Low Profit (Rekomendasi: TIDAK)';

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
                </ul>
            `;
            submitButton.disabled = false;
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${error.message}</p>`;
            submitButton.disabled = false;
        });
    });
});