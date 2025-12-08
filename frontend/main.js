const API_BASE_URL = 'http://localhost:8000';

// Tab switching functionality
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        
        // Remove active class from all tabs and buttons
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// Helper function to get username
function getUsername() {
    return document.getElementById('username').value.trim() || null;
}

// Helper function to show result
function showResult(resultBoxId, content) {
    const resultBox = document.getElementById(resultBoxId);
    resultBox.innerHTML = content;
    resultBox.classList.add('show');
}

// Helper function to show error
function showError(resultBoxId, message) {
    showResult(resultBoxId, `<div class="error-message"><strong>Error:</strong> ${message}</div>`);
}

// BMI Calculator
document.getElementById('bmi-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: getUsername(),
        age_years: parseInt(document.getElementById('bmi-age').value),
        gender: document.getElementById('bmi-gender').value === 'true',
        weight_kg: parseFloat(document.getElementById('bmi-weight').value),
        height_cm: parseFloat(document.getElementById('bmi-height').value)
    };

    try {
        const response = await fetch(`${API_BASE_URL}/calc/bmi`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Calculation failed');

        const result = await response.json();
        showResult('bmi-result', `
            <h3>Your BMI Results</h3>
            <p><strong>BMI Value:</strong> ${result.bmi_value}</p>
            <p><strong>Category:</strong> ${result.bmi_category}</p>
            ${formData.username ? '<p class="success-message">✓ Saved to history</p>' : ''}
        `);
    } catch (error) {
        showError('bmi-result', error.message);
    }
});

// Body Fat Calculator
document.getElementById('body-fat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: getUsername(),
        age_years: parseInt(document.getElementById('bf-age').value),
        gender: document.getElementById('bf-gender').value === 'true',
        weight_kg: parseFloat(document.getElementById('bf-weight').value),
        height_cm: parseFloat(document.getElementById('bf-height').value),
        neck_cm: parseFloat(document.getElementById('bf-neck').value),
        waist_cm: parseFloat(document.getElementById('bf-waist').value),
        hip_cm: parseFloat(document.getElementById('bf-hip').value)
    };

    try {
        const response = await fetch(`${API_BASE_URL}/calc/body-fat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Calculation failed');

        const result = await response.json();
        showResult('body-fat-result', `
            <h3>Your Body Fat Results</h3>
            <p><strong>Body Fat Percentage:</strong> ${result.body_fat_percentage}%</p>
            ${formData.username ? '<p class="success-message">✓ Saved to history</p>' : ''}
        `);
    } catch (error) {
        showError('body-fat-result', error.message);
    }
});

// Calorie Calculator
document.getElementById('calorie-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: getUsername(),
        age_years: parseInt(document.getElementById('cal-age').value),
        gender: document.getElementById('cal-gender').value === 'true',
        weight_kg: parseFloat(document.getElementById('cal-weight').value),
        height_cm: parseFloat(document.getElementById('cal-height').value),
        activity_factor: document.getElementById('cal-activity').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/calc/calorie`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Calculation failed');

        const result = await response.json();
        showResult('calorie-result', `
            <h3>Your Daily Calorie Needs</h3>
            <p><strong>Daily Calories:</strong> ${result.daily_calories} kcal</p>
            <p><strong>Activity Level:</strong> ${formData.activity_factor}</p>
            ${formData.username ? '<p class="success-message">✓ Saved to history</p>' : ''}
        `);
    } catch (error) {
        showError('calorie-result', error.message);
    }
});

// BMR Calculator
document.getElementById('bmr-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: getUsername(),
        age_years: parseInt(document.getElementById('bmr-age').value),
        gender: document.getElementById('bmr-gender').value === 'true',
        weight_kg: parseFloat(document.getElementById('bmr-weight').value),
        height_cm: parseFloat(document.getElementById('bmr-height').value)
    };

    try {
        const response = await fetch(`${API_BASE_URL}/calc/bmr`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Calculation failed');

        const result = await response.json();
        showResult('bmr-result', `
            <h3>Your BMR Results</h3>
            <p><strong>Basal Metabolic Rate:</strong> ${result.bmr_value} kcal/day</p>
            <p><em>This is the number of calories your body needs at rest.</em></p>
            ${formData.username ? '<p class="success-message">✓ Saved to history</p>' : ''}
        `);
    } catch (error) {
        showError('bmr-result', error.message);
    }
});

// Ideal Weight Calculator
document.getElementById('ideal-weight-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: getUsername(),
        age_years: parseInt(document.getElementById('iw-age').value),
        gender: document.getElementById('iw-gender').value === 'true',
        height_cm: parseFloat(document.getElementById('iw-height').value)
    };

    try {
        const response = await fetch(`${API_BASE_URL}/calc/ideal-weight`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Calculation failed');

        const result = await response.json();
        showResult('ideal-weight-result', `
            <h3>Your Ideal Weight Range</h3>
            <p><strong>Minimum Weight:</strong> ${result.min_weight_kg} kg</p>
            <p><strong>Maximum Weight:</strong> ${result.max_weight_kg} kg</p>
            <p><em>Based on your height and gender.</em></p>
            ${formData.username ? '<p class="success-message">✓ Saved to history</p>' : ''}
        `);
    } catch (error) {
        showError('ideal-weight-result', error.message);
    }
});

// Load History
document.getElementById('load-history-btn').addEventListener('click', async () => {
    const username = getUsername();
    
    if (!username) {
        showResult('history-result', '<div class="error-message">Please enter a username to view history.</div>');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/calc/history?username=${encodeURIComponent(username)}`);
        
        if (!response.ok) throw new Error('Failed to load history');

        const history = await response.json();
        
        if (history.length === 0) {
            showResult('history-result', '<p class="history-info">No calculation history found for this username.</p>');
            return;
        }

        const historyHTML = history.map(record => {
            const inputs = Object.entries(record.inputs)
                .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
                .join(', ');
            
            const results = Object.entries(record.result)
                .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
                .join(', ');

            return `
                <div class="history-item">
                    <button class="delete-btn" onclick="deleteRecord(${record.id}, '${username}')">Delete</button>
                    <h4>${record.calc_type} Calculation</h4>
                    <p><strong>Inputs:</strong> ${inputs}</p>
                    <p><strong>Results:</strong> ${results}</p>
                    <p class="timestamp">Calculated on: ${new Date(record.created_at).toLocaleString()}</p>
                </div>
            `;
        }).join('');

        showResult('history-result', historyHTML);
    } catch (error) {
        showError('history-result', error.message);
    }
});

// Delete Record Function
async function deleteRecord(recordId, username) {
    if (!confirm('Are you sure you want to delete this record?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/calc/history/${recordId}?username=${encodeURIComponent(username)}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete record');

        // Reload history after deletion
        document.getElementById('load-history-btn').click();
    } catch (error) {
        alert('Error deleting record: ' + error.message);
    }
}

// Utility: safe JSON parse
function tryParseJSON(text) {
    if (!text || !text.trim()) return null;
    try { return JSON.parse(text); } catch { return null; }
}

// Get single record by ID
document.getElementById('get-record-btn').addEventListener('click', async () => {
    const username = getUsername();
    const idStr = document.getElementById('history-record-id').value.trim();
    if (!username) {
        showError('single-record-result', 'Please enter a username.');
        return;
    }
    if (!idStr) {
        showError('single-record-result', 'Please enter a record ID.');
        return;
    }
    const recordId = parseInt(idStr, 10);
    try {
        const resp = await fetch(`${API_BASE_URL}/calc/history/${recordId}?username=${encodeURIComponent(username)}`);
        if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            throw new Error(err.detail || 'Failed to fetch record');
        }
        const record = await resp.json();
        const inputs = Object.entries(record.inputs || {}).map(([k, v]) => `<strong>${k}:</strong> ${v}`).join(', ');
        const results = Object.entries(record.result || {}).map(([k, v]) => `<strong>${k}:</strong> ${v}`).join(', ');
        showResult('single-record-result', `
            <h3>Record #${record.id}</h3>
            <p><strong>Type:</strong> ${record.calc_type}</p>
            <p><strong>Inputs:</strong> ${inputs || '-'}</p>
            <p><strong>Result:</strong> ${results || '-'}</p>
            <p class="timestamp">Created: ${record.created_at ? new Date(record.created_at).toLocaleString() : '-'}</p>
        `);
    } catch (e) {
        showError('single-record-result', e.message);
    }
});

// Update record by ID (PATCH)
document.getElementById('update-record-btn').addEventListener('click', async () => {
    const username = getUsername();
    const idStr = document.getElementById('history-record-id').value.trim();
    const inputsJSON = document.getElementById('update-inputs-json').value;
    const resultJSON = document.getElementById('update-result-json').value;

    if (!username) {
        showError('update-record-result', 'Please enter a username.');
        return;
    }
    if (!idStr) {
        showError('update-record-result', 'Please enter a record ID.');
        return;
    }
    const recordId = parseInt(idStr, 10);

    const inputs = tryParseJSON(inputsJSON);
    const result = tryParseJSON(resultJSON);
    if (inputsJSON && inputs === null) {
        showError('update-record-result', 'Invalid Inputs JSON.');
        return;
    }
    if (resultJSON && result === null) {
        showError('update-record-result', 'Invalid Result JSON.');
        return;
    }

    const payload = { username, inputs: inputs ?? null, result: result ?? null };
    try {
        const resp = await fetch(`${API_BASE_URL}/calc/history/${recordId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            throw new Error(err.detail || 'Failed to update record');
        }
        const updated = await resp.json();
        showResult('update-record-result', `
            <h3>Record Updated</h3>
            <p><strong>ID:</strong> ${updated.id}</p>
            <p><strong>Type:</strong> ${updated.calc_type}</p>
            <p><strong>Inputs:</strong> ${JSON.stringify(updated.inputs)}</p>
            <p><strong>Result:</strong> ${JSON.stringify(updated.result)}</p>
            <p class="timestamp">Updated: ${updated.created_at ? new Date(updated.created_at).toLocaleString() : '-'}</p>
        `);
        // Refresh history list
        document.getElementById('load-history-btn').click();
    } catch (e) {
        showError('update-record-result', e.message);
    }
});