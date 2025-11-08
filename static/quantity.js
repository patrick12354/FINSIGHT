document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('quantity-form');
    const resultsDiv = document.getElementById('results');
    const submitButton = document.getElementById('submit-button');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        resultsDiv.innerHTML = '<p>Sedang menghitung prediksi kuantitas...</p>';
        submitButton.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Model ini MEMBUTUHKAN Price & Unit Cost (dan 2 field baru)
        data['Price'] = parseFloat(data['Price']);
        data['Unit Cost'] = parseFloat(data['Unit Cost']);
        // 'date_month' and 'date_day_of_week' sudah otomatis 
        // diambil oleh Object.fromEntries() sebagai string, 
        // dan itu sudah benar (karena modelnya anggap sbg kategori).

        // Kirim data ke API /predict/quantity
        fetch('/predict/quantity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) return response.json().then(err => { throw new Error(err.error) });
            return response.json();
        })
        .then(results => {
            if (results.error) throw new Error(results.error);

            resultsDiv.innerHTML = `
                <ul>
                    <li>
                        <strong>📦 Prediksi Kuantitas:</strong> 
                        ${results.quantity} unit
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