// Authentication related JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const submitBtn = loginForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Logging in...';

            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: loginForm.username.value,
                        password: loginForm.password.value
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    // Store token and redirect
                    localStorage.setItem('authToken', data.token);
                    window.location.href = data.redirect || '/dashboard';
                } else {
                    showAuthError(data.message || 'Login failed. Please try again.');
                }
            } catch (error) {
                showAuthError('Network error. Please try again later.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Login';
            }
        });
    }

    // Handle registration form submission
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            if (registerForm.password.value !== registerForm.confirm_password.value) {
                showAuthError('Passwords do not match');
                return;
            }

            const submitBtn = registerForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Registering...';

            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: registerForm.username.value,
                        email: registerForm.email.value,
                        password: registerForm.password.value
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    // Store token and redirect
                    localStorage.setItem('authToken', data.token);
                    window.location.href = data.redirect || '/dashboard';
                } else {
                    showAuthError(data.message || 'Registration failed. Please try again.');
                }
            } catch (error) {
                showAuthError('Network error. Please try again later.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Register';
            }
        });
    }

    // Function to display authentication errors
    function showAuthError(message) {
        // Remove any existing error messages
        const existingErrors = document.querySelectorAll('.auth-error');
        existingErrors.forEach(el => el.remove());

        // Create new error element
        const errorEl = document.createElement('div');
        errorEl.className = 'auth-error alert alert-danger';
        errorEl.textContent = message;

        // Insert error message
        const authContainer = document.querySelector('.auth-container');
        if (authContainer) {
            authContainer.insertBefore(errorEl, authContainer.firstChild);

            // Auto-remove after 5 seconds
            setTimeout(() => {
                errorEl.remove();
            }, 5000);
        }
    }

    // Password visibility toggle
    document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const passwordField = this.previousElementSibling;
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    });
});