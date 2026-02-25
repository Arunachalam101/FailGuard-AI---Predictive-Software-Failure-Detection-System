// FailGuard AI - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

async function handleFormSubmit(event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(document.getElementById('predictionForm'));
    const data = {
        loc: parseFloat(formData.get('loc')),
        wmc: parseFloat(formData.get('wmc')),
        rfc: parseFloat(formData.get('rfc')),
        cbo: parseFloat(formData.get('cbo')),
        lcom: parseFloat(formData.get('lcom')),
        code_churn: parseFloat(formData.get('code_churn')),
        num_developers: parseFloat(formData.get('num_developers')),
        past_defects: parseFloat(formData.get('past_defects'))
    };

    // Validate input
    if (!validateInput(data)) {
        alert('Please fill in all fields with valid numbers.');
        return;
    }

    try {
        // Show loading state
        const submitBtn = document.querySelector('.btn-submit');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="btn-text">⏳ Analyzing...</span>';
        submitBtn.disabled = true;

        // Make prediction request
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Restore button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;

        if (result.success) {
            // Store result and prediction ID
            sessionStorage.setItem('lastPrediction', JSON.stringify(result));
            sessionStorage.setItem('lastPredictionId', result.prediction_id);
            
            // Redirect to dashboard
            window.location.href = '/dashboard';
        } else {
            showError(result.error || 'Prediction failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to server. Make sure Flask app is running.');
        
        // Restore button
        const submitBtn = document.querySelector('.btn-submit');
        submitBtn.innerHTML = '<span class="btn-text">🔍 Analyze Module Risk</span>';
        submitBtn.disabled = false;
    }
}

function validateInput(data) {
    for (const [key, value] of Object.entries(data)) {
        if (isNaN(value) || value < 0) {
            return false;
        }
    }
    if (data.num_developers < 1) {
        return false;
    }
    if (data.lcom > 1) {
        return false;
    }
    return true;
}

function displayResult(result, inputData) {
    const riskColor = result.risk_color;
    const riskEmoji = result.risk_level === 'HIGH' ? '⚠️' : 
                     result.risk_level === 'MEDIUM' ? '⚡' : '✅';

    const resultHTML = `
        <div class="result-card" style="background-color: ${riskColor}20; border-left: 6px solid ${riskColor};">
            <div class="result-header">
                <span class="risk-emoji">${riskEmoji}</span>
                <div class="result-title">
                    <h2>Risk Level: ${result.risk_level}</h2>
                    <p class="result-subtitle">Module Failure Prediction</p>
                </div>
            </div>

            <div class="result-metrics">
                <div class="metric-item">
                    <div class="metric-label">Failure Probability</div>
                    <div class="metric-widget">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${result.probability}%; background-color: ${riskColor};"></div>
                        </div>
                        <div class="metric-value">${result.probability}%</div>
                    </div>
                </div>

                <div class="metric-item">
                    <div class="metric-label">Model Confidence</div>
                    <div class="metric-value">${result.confidence}%</div>
                </div>

                <div class="metric-item">
                    <div class="metric-label">Prediction Status</div>
                    <div class="metric-value">${result.prediction}</div>
                </div>
            </div>
        </div>

        <div class="input-summary">
            <h3>Input Module Metrics</h3>
            <div class="metrics-table">
                <div class="metric-row">
                    <span class="metric-key">Lines of Code (LOC):</span>
                    <span class="metric-val">${inputData.loc}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-key">Weighted Methods per Class (WMC):</span>
                    <span class="metric-val">${inputData.wmc}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-key">Response for a Class (RFC):</span>
                    <span class="metric-val">${inputData.rfc}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-key">Coupling Between Objects (CBO):</span>
                    <span class="metric-val">${inputData.cbo}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-key">Lack of Cohesion (LCOM):</span>
                    <span class="metric-val">${inputData.lcom}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-key">Code Churn:</span>
                    <span class="metric-val">${inputData.code_churn}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-key">Number of Developers:</span>
                    <span class="metric-val">${inputData.num_developers}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-key">Past Defects:</span>
                    <span class="metric-val">${inputData.past_defects}</span>
                </div>
            </div>
        </div>
    `;

    document.getElementById('resultContent').innerHTML = resultHTML;
    document.getElementById('resultSection').style.display = 'block';

    // Display recommendations
    displayRecommendations(result.risk_level, result.probability);

    // Scroll to results
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });

    // Store result for result page
    sessionStorage.setItem('lastPrediction', JSON.stringify(result));
}

function displayRecommendations(riskLevel, probability) {
    let recommendations = [];

    if (riskLevel === 'HIGH') {
        recommendations = [
            '🔴 Perform thorough code review before deployment',
            '🔴 Increase test coverage for this module',
            '🔴 Consider refactoring to reduce complexity',
            '🔴 Schedule security audit and penetration testing',
            '🔴 Plan additional debugging and QA time',
            '🔴 Prioritize this module for immediate attention'
        ];
    } else if (riskLevel === 'MEDIUM') {
        recommendations = [
            '🟡 Standard code review recommended',
            '🟡 Ensure adequate test coverage is present',
            '🟡 Monitor during initial deployment phase',
            '🟡 Consider minor refactoring if feasible',
            '🟡 Implement runtime monitoring and logging',
            '🟡 Have rollback plan ready'
        ];
    } else {
        recommendations = [
            '🟢 Standard QA process sufficient',
            '🟢 Proceed with normal code review',
            '🟢 Maintain current test coverage levels',
            '🟢 Low risk for deployment',
            '🟢 Continue monitoring for performance issues',
            '🟢 Safe to include in sprint deliverable'
        ];
    }

    const html = recommendations.map(rec => `<div class="recommendation-item">${rec}</div>`).join('');
    
    const recommendationsSection = document.querySelector('.recommendations');
    if (recommendationsSection) {
        const contentDiv = recommendationsSection.querySelector('#recommendationsContent') 
                         || document.createElement('div');
        if (!contentDiv.id) {
            contentDiv.id = 'recommendationsContent';
            recommendationsSection.appendChild(contentDiv);
        }
        contentDiv.innerHTML = html;
    } else {
        // Create recommendations section if not exists
        const newSection = document.createElement('section');
        newSection.className = 'recommendations';
        newSection.innerHTML = `<h3>📋 Recommendations</h3><div id="recommendationsContent">${html}</div>`;
        document.querySelector('main').appendChild(newSection);
    }
}

function showError(message) {
    const resultHTML = `
        <div class="error-box">
            <p><strong>❌ Error:</strong> ${message}</p>
        </div>
    `;
    
    document.getElementById('resultContent').innerHTML = resultHTML;
    document.getElementById('resultSection').style.display = 'block';
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
}

// Pre-fill example data function
function fillExampleData() {
    document.getElementById('loc').value = 450;
    document.getElementById('wmc').value = 14;
    document.getElementById('rfc').value = 22;
    document.getElementById('cbo').value = 7;
    document.getElementById('lcom').value = 0.55;
    document.getElementById('code_churn').value = 12;
    document.getElementById('num_developers').value = 4;
    document.getElementById('past_defects').value = 3;
}

// Utility: Copy results to clipboard
function copyResults(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const text = element.innerText;
        navigator.clipboard.writeText(text).then(() => {
            alert('Results copied to clipboard!');
        });
    }
}

// Initialize tooltips on page load
function initializeTooltips() {
    const tooltips = document.querySelectorAll('.tooltip');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            this.querySelector('.tooltip-text').style.visibility = 'visible';
        });
        tooltip.addEventListener('mouseleave', function() {
            this.querySelector('.tooltip-text').style.visibility = 'hidden';
        });
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', initializeTooltips);
