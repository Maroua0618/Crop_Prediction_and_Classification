// Form submission handler for both prediction and classification pages
document.addEventListener('DOMContentLoaded', function() {
    // Handle prediction form submission
    const predictionForm = document.getElementById('environmentForm');
    if (predictionForm && window.location.pathname.includes('prediction')) {
        predictionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitButton = this.querySelector('input[type="submit"]');
            const originalValue = submitButton.value;
            
            // Show loading state
            submitButton.value = 'Processing...';
            submitButton.disabled = true;
            
            // Validate form data
            const requiredFields = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Ph', 'Rainfall'];
            let isValid = true;
            
            for (let field of requiredFields) {
                const value = formData.get(field);
                if (!value || isNaN(value)) {
                    alert(`Please enter a valid value for ${field}`);
                    isValid = false;
                    break;
                }
            }
            
            if (!isValid) {
                submitButton.value = originalValue;
                submitButton.disabled = false;
                return;
            }
            
            // Submit to prediction API
            fetch('/api/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Redirect to results page
                    window.location.href = data.redirect || '/prediction-results';
                } else {
                    alert('Error: ' + (data.message || 'Prediction failed'));
                    submitButton.value = originalValue;
                    submitButton.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your request. Please try again.');
                submitButton.value = originalValue;
                submitButton.disabled = false;
            });
        });
    }
    
    // Handle classification form submission
    if (predictionForm && window.location.pathname.includes('classification')) {
        predictionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitButton = this.querySelector('input[type="submit"]');
            const originalValue = submitButton.value;
            
            // Show loading state
            submitButton.value = 'Classifying...';
            submitButton.disabled = true;
            
            // Validate form data
            const requiredFields = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Ph', 'Rainfall'];
            let isValid = true;
            
            for (let field of requiredFields) {
                const value = formData.get(field);
                if (!value || isNaN(value)) {
                    alert(`Please enter a valid value for ${field}`);
                    isValid = false;
                    break;
                }
            }
            
            // Additional validation
            const ph = parseFloat(formData.get('Ph'));
            const humidity = parseFloat(formData.get('Humidity'));
            const rainfall = parseFloat(formData.get('Rainfall'));
            
            if (ph < 0 || ph > 14) {
                alert('pH value must be between 0 and 14');
                isValid = false;
            }
            
            if (humidity < 0 || humidity > 100) {
                alert('Humidity value must be between 0 and 100%');
                isValid = false;
            }
            
            if (rainfall < 0) {
                alert('Rainfall cannot be negative');
                isValid = false;
            }
            
            if (!isValid) {
                submitButton.value = originalValue;
                submitButton.disabled = false;
                return;
            }
            
            // Submit to classification API
            fetch('/api/classify', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Redirect to results page
                    window.location.href = data.redirect || '/classification-results';
                } else {
                    alert('Error: ' + (data.message || 'Classification failed'));
                    submitButton.value = originalValue;
                    submitButton.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your request. Please try again.');
                submitButton.value = originalValue;
                submitButton.disabled = false;
            });
        });
    }
    
    // Add input validation and formatting
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove any non-numeric characters except decimal point
            this.value = this.value.replace(/[^0-9.]/g, '');
            
            // Ensure only one decimal point
            if ((this.value.match(/\./g) || []).length > 1) {
                this.value = this.value.replace(/\.+$/, '');
            }
            
            // Add visual feedback for valid/invalid inputs
            if (this.value && !isNaN(this.value)) {
                this.style.borderColor = '#4CAF50';
            } else if (this.value) {
                this.style.borderColor = '#F44336';
            } else {
                this.style.borderColor = '';
            }
        });
        
        // Format on blur
        input.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                const value = parseFloat(this.value);
                this.value = value.toFixed(1);
            }
        });
    });
    
    // Add loading spinner styles
    const style = document.createElement('style');
    style.textContent = `
        .loading {
            position: relative;
            pointer-events: none;
        }
        
        .loading::after {
            content: '';
            position: absolute;
            width: 16px;
            height: 16px;
            margin: auto;
            border: 2px solid transparent;
            border-top-color: #ffffff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        input[type="number"]:focus {
            outline: none;
            box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
        }
        
        .form-error {
            border-color: #F44336 !important;
            box-shadow: 0 0 5px rgba(244, 67, 54, 0.3) !important;
        }
        
        .form-success {
            border-color: #4CAF50 !important;
            box-shadow: 0 0 5px rgba(76, 175, 80, 0.3) !important;
        }
    `;
    document.head.appendChild(style);
});

// Utility functions for form handling
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#F44336' : '#2196F3'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add animation styles for notifications
const animationStyle = document.createElement('style');
animationStyle.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(animationStyle);