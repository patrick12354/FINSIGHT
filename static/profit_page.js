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

        // Kirim data ke API /predict/profit
        fetch('/predict/profit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) return response.json().then(err => { throw new Error(err.error) });
            return response.json();
        })
        .then(results => {
            // Format ke Dolar (USD)
            const profitUSD = results.profit.toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD'
            });

            resultsDiv.innerHTML = `
                <ul>
                    <li>
                        <strong>📈 Prediksi Profit:</strong> 
                        ${profitUSD}
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