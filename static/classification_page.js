document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('classification-form');
    const resultsDiv = document.getElementById('results');
    const submitButton = document.getElementById('submit-button');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        resultsDiv.innerHTML = '<p>Sedang menghitung prediksi rekomendasi...</p>';
        submitButton.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Kirim data ke API /predict/classification
        fetch('/predict/classification', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) return response.json().then(err => { throw new Error(err.error) });
            return response.json();
        })
        .then(results => {
            
            const highProfitText = results.high_profit === 1 
                ? 'High Profit (Rekomendasi: YA)' 
                : 'Low Profit (Rekomendasi: TIDAK)';

            resultsDiv.innerHTML = `
                <ul>
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