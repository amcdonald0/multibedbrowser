// Authentication functions
function handleLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        // Basic form validation
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const urole = document.getElementById('urole').value;
        const errorMessage = document.getElementById('error-message');
        let isValid = true;

        // Clear previous error messages and validation states
        errorMessage.classList.add('d-none');
        form.querySelectorAll('.form-control').forEach(input => {
            input.classList.remove('is-invalid');
        });

        // Username validation
        if (!username) {
            errorMessage.textContent = 'Please enter your username';
            errorMessage.classList.remove('d-none');
            document.getElementById('username').classList.add('is-invalid');
            isValid = false;
        }

        // Email validation
        if (!email) {
            errorMessage.textContent = 'Please enter your email address';
            errorMessage.classList.remove('d-none');
            document.getElementById('email').classList.add('is-invalid');
            isValid = false;
        } else if (!isValidEmail(email)) {
            errorMessage.textContent = 'Please enter a valid email address';
            errorMessage.classList.remove('d-none');
            document.getElementById('email').classList.add('is-invalid');
            isValid = false;
        }

        // Password validation
        if (!password) {
            errorMessage.textContent = 'Please enter your password';
            errorMessage.classList.remove('d-none');
            document.getElementById('password').classList.add('is-invalid');
            isValid = false;
        }

        // Role validation
        if (!urole) {
            errorMessage.textContent = 'Please select your role';
            errorMessage.classList.remove('d-none');
            document.getElementById('urole').classList.add('is-invalid');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });

    // Real-time validation
    form.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('input', function() {
            document.getElementById('error-message').classList.add('d-none');
            this.classList.remove('is-invalid');
        });
    });
}

function continueAsGuest() {
    window.location.href = '/';
}

function isValidEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    handleLoginForm();
});