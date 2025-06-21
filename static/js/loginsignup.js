// Wait for DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if login form exists on the current page
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Get form data
            const formData = new FormData();
            formData.append('email', document.getElementById('loginEmail').value);
            formData.append('password', document.getElementById('loginPassword').value);
            
            // Send POST request to backend
            fetch('/api/login', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    window.location.href = '/';  // Redirect to home page instead of profile
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during login');
            });
        });
    }
    
    // Check if signup form exists on the current page
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Validate passwords match
            const password = document.getElementById('signupPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (password !== confirmPassword) {
                alert('Passwords do not match!');
                return;
            }
            
            // Get form data - create it manually instead of from form
            const formData = new FormData();
            formData.append('fullName', document.getElementById('fullName').value);
            formData.append('signupEmail', document.getElementById('signupEmail').value);
            formData.append('signupPassword', document.getElementById('signupPassword').value);
            
            // Send POST request to backend
            fetch('/api/signup', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    window.location.href = '/login_page';  // Redirect to login page
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during signup');
            });
        });
    }
});