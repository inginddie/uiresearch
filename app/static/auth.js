// Authentication JavaScript

// API Base URL
const API_URL = window.location.origin;

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');
    
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    successDiv.style.display = 'none';
    
    // Scroll to top to show error
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show success message
function showSuccess(message) {
    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');
    
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    errorDiv.style.display = 'none';
    
    // Scroll to top to show success
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Hide messages
function hideMessages() {
    document.getElementById('error-message').style.display = 'none';
    document.getElementById('success-message').style.display = 'none';
}

// Show loading state
function setLoading(isLoading) {
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnLoading = document.getElementById('btn-loading');
    
    if (isLoading) {
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'flex';
    } else {
        submitBtn.disabled = false;
        btnText.style.display = 'block';
        btnLoading.style.display = 'none';
    }
}

// Save token to localStorage
function saveToken(token) {
    localStorage.setItem('auth_token', token);
}

// Get token from localStorage
function getToken() {
    return localStorage.getItem('auth_token');
}

// Remove token from localStorage
function removeToken() {
    localStorage.removeItem('auth_token');
}

// Check if user is logged in
function isLoggedIn() {
    return !!getToken();
}

// Redirect to home if already logged in
function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        window.location.href = '/';
    }
}

// Handle Login Form
const loginForm = document.getElementById('login-form');
if (loginForm) {
    // Redirect if already logged in
    redirectIfLoggedIn();
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideMessages();
        setLoading(true);
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;
        
        try {
            // Create form data for OAuth2 format
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);
            
            const response = await fetch(`${API_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Save token
                saveToken(data.access_token);
                
                // Show success message
                showSuccess('¡Inicio de sesión exitoso! Redirigiendo...');
                
                // Redirect to home after 1 second
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                // Show error message
                const errorMessage = data.detail || 'Error al iniciar sesión. Verifica tus credenciales.';
                showError(errorMessage);
                setLoading(false);
            }
        } catch (error) {
            console.error('Login error:', error);
            showError('Error de conexión. Por favor, intenta de nuevo.');
            setLoading(false);
        }
    });
}

// Handle Signup Form
const signupForm = document.getElementById('signup-form');
if (signupForm) {
    // Redirect if already logged in
    redirectIfLoggedIn();
    
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideMessages();
        
        const fullName = document.getElementById('full_name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const terms = document.getElementById('terms').checked;
        
        // Validate passwords match
        if (password !== confirmPassword) {
            showError('Las contraseñas no coinciden');
            return;
        }
        
        // Validate password length
        if (password.length < 8) {
            showError('La contraseña debe tener al menos 8 caracteres');
            return;
        }
        
        // Validate terms
        if (!terms) {
            showError('Debes aceptar los términos y condiciones');
            return;
        }
        
        setLoading(true);
        
        try {
            const response = await fetch(`${API_URL}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                    full_name: fullName || null
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Show success message
                showSuccess('¡Cuenta creada exitosamente! Redirigiendo al inicio de sesión...');
                
                // Redirect to login after 2 seconds
                setTimeout(() => {
                    window.location.href = '/static/login.html';
                }, 2000);
            } else {
                // Show error message
                const errorMessage = data.detail || 'Error al crear la cuenta. Por favor, intenta de nuevo.';
                showError(errorMessage);
                setLoading(false);
            }
        } catch (error) {
            console.error('Signup error:', error);
            showError('Error de conexión. Por favor, intenta de nuevo.');
            setLoading(false);
        }
    });
}

// Password strength indicator (optional enhancement)
const passwordInput = document.getElementById('password');
if (passwordInput && signupForm) {
    passwordInput.addEventListener('input', (e) => {
        const password = e.target.value;
        const strength = calculatePasswordStrength(password);
        // You can add visual feedback here
    });
}

function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;
    return strength;
}
