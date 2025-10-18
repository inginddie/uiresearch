// Crossref Academic Search - Client-side JavaScript

// Store current search results
let currentResults = [];

// Auth functions
function getToken() {
    return localStorage.getItem('auth_token');
}

function isLoggedIn() {
    return !!getToken();
}

function logout() {
    localStorage.removeItem('auth_token');
    updateAuthUI();
    showStatus('Sesión cerrada exitosamente', 'success');
}

async function getCurrentUser() {
    const token = getToken();
    if (!token) return null;
    
    try {
        const response = await fetch('/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            // Token invalid, remove it
            localStorage.removeItem('auth_token');
            return null;
        }
    } catch (error) {
        console.error('Error getting current user:', error);
        return null;
    }
}

function updateAuthUI() {
    const authButtons = document.getElementById('auth-buttons');
    const userMenu = document.getElementById('user-menu');
    const userEmailText = document.getElementById('user-email-text');
    
    if (isLoggedIn()) {
        authButtons.style.display = 'none';
        userMenu.style.display = 'flex';
        userMenu.style.gap = '12px';
        userMenu.style.alignItems = 'center';
        
        // Get and display user info
        getCurrentUser().then(user => {
            if (user && userEmailText) {
                userEmailText.textContent = user.email;
            }
        });
    } else {
        authButtons.style.display = 'flex';
        userMenu.style.display = 'none';
    }
}

// Mobile menu toggle
function toggleMobileMenu() {
    const navLinks = document.getElementById('nav-links');
    const menuBtn = document.getElementById('mobile-menu-btn');
    const overlay = document.getElementById('menu-overlay');
    
    if (navLinks) {
        const isActive = navLinks.classList.contains('active');
        
        navLinks.classList.toggle('active');
        if (overlay) {
            overlay.classList.toggle('active');
        }
        
        // Update button icon
        if (menuBtn) {
            menuBtn.innerHTML = !isActive ? 
                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>' :
                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>';
        }
    }
}

// Close mobile menu when clicking overlay
document.addEventListener('click', (e) => {
    const overlay = document.getElementById('menu-overlay');
    const navLinks = document.getElementById('nav-links');
    const menuBtn = document.getElementById('mobile-menu-btn');
    
    if (overlay && e.target === overlay) {
        navLinks.classList.remove('active');
        overlay.classList.remove('active');
        if (menuBtn) {
            menuBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>';
        }
    }
});

// Initialize auth UI on page load
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    
    // Add logout button handler
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    // Add mobile menu button handler
    const menuBtn = document.getElementById('mobile-menu-btn');
    if (menuBtn) {
        menuBtn.addEventListener('click', toggleMobileMenu);
    }
    
    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-link, .btn-signup');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const menu = document.getElementById('nav-links');
            const overlay = document.getElementById('menu-overlay');
            const menuBtn = document.getElementById('mobile-menu-btn');
            
            if (menu) {
                menu.classList.remove('active');
            }
            if (overlay) {
                overlay.classList.remove('active');
            }
            if (menuBtn) {
                menuBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>';
            }
        });
    });
});

/**
 * Escape HTML to prevent XSS attacks
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show status message
 */
function showStatus(message, type = 'info') {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = message;
    statusDiv.className = `status status-${type}`;
    statusDiv.style.display = 'block';
}

/**
 * Hide status message
 */
function hideStatus() {
    const statusDiv = document.getElementById('status');
    statusDiv.style.display = 'none';
}

/**
 * Display search results as cards
 */
function displayResults(items) {
    const container = document.getElementById('results');
    
    if (!items || items.length === 0) {
        container.innerHTML = '<p class="no-results">No se encontraron resultados</p>';
        return;
    }
    
    const cardsHtml = items.map(item => `
        <article class="result-card">
            <h2 class="result-title">${escapeHtml(item.title)}</h2>
            
            <p class="result-authors">${escapeHtml(item.authors)}</p>
            
            <p class="result-metadata">
                <span class="journal">${escapeHtml(item.journal)}</span>
                ${item.year ? `<span class="year"> • ${item.year}</span>` : ''}
            </p>
            
            <p class="result-doi">
                <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">
                    ${escapeHtml(item.doi)}
                </a>
            </p>
            
            <details class="result-abstract">
                <summary>Ver abstract</summary>
                <p>${escapeHtml(item.abstract)}</p>
            </details>
        </article>
    `).join('');
    
    container.innerHTML = cardsHtml;
}

/**
 * Handle form submission
 */
document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(e.target);
    
    // Handle checkbox (not included in FormData if unchecked)
    if (!formData.has('has_abstract')) {
        formData.set('has_abstract', 'false');
    }
    
    // Build query params
    const params = new URLSearchParams(formData);
    
    // Show loading status
    showStatus('Buscando...', 'loading');
    
    // Hide export button
    document.getElementById('exportCsv').style.display = 'none';
    
    // Clear previous results
    document.getElementById('results').innerHTML = '';
    
    try {
        // Make API request
        const response = await fetch(`/search?${params}`);
        const data = await response.json();
        
        if (response.ok) {
            // Success
            currentResults = data.items;
            displayResults(data.items);
            showStatus(`${data.count} resultado${data.count !== 1 ? 's' : ''} encontrado${data.count !== 1 ? 's' : ''}`, 'success');
            
            // Show export button if there are results
            if (data.count > 0) {
                document.getElementById('exportCsv').style.display = 'block';
            }
        } else {
            // Error response from API
            const errorMessage = data.error?.message || 'Error desconocido';
            showStatus(`Error: ${errorMessage}`, 'error');
        }
    } catch (error) {
        // Network or other error
        console.error('Search error:', error);
        showStatus('Error de conexión. Por favor, intenta de nuevo.', 'error');
    }
});

/**
 * Handle CSV export
 */
document.getElementById('exportCsv').addEventListener('click', async () => {
    // Get current form data
    const form = document.getElementById('searchForm');
    const formData = new FormData(form);
    
    // Handle checkbox
    if (!formData.has('has_abstract')) {
        formData.set('has_abstract', 'false');
    }
    
    // Build query params
    const params = new URLSearchParams(formData);
    
    // Show status
    showStatus('Generando CSV...', 'loading');
    
    try {
        // Trigger download
        window.location.href = `/export/csv?${params}`;
        
        // Show success message after a short delay
        setTimeout(() => {
            showStatus('CSV descargado exitosamente', 'success');
        }, 1000);
    } catch (error) {
        console.error('Export error:', error);
        showStatus('Error al exportar CSV', 'error');
    }
});

/**
 * Set default dates on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    // Focus on search input
    document.getElementById('q').focus();
});
