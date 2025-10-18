// Pricing Page JavaScript

// Billing toggle (monthly/yearly)
const billingToggle = document.getElementById('billing-toggle');
const monthlyLabel = document.getElementById('monthly-label');
const yearlyLabel = document.getElementById('yearly-label');

// Update prices based on billing period
function updatePrices(isYearly) {
    const priceElements = document.querySelectorAll('.price-amount[data-monthly]');
    
    priceElements.forEach(element => {
        const monthly = element.getAttribute('data-monthly');
        const yearly = element.getAttribute('data-yearly');
        
        if (isYearly) {
            // Show yearly price (divided by 12 for monthly equivalent)
            const yearlyMonthly = (parseFloat(yearly) / 12).toFixed(2);
            element.textContent = `$${yearlyMonthly}`;
            
            // Update period text
            const periodElement = element.nextElementSibling;
            if (periodElement && periodElement.classList.contains('price-period')) {
                periodElement.textContent = '/mes (facturado anualmente)';
            }
        } else {
            // Show monthly price
            element.textContent = `$${monthly}`;
            
            // Update period text
            const periodElement = element.nextElementSibling;
            if (periodElement && periodElement.classList.contains('price-period')) {
                periodElement.textContent = '/mes';
            }
        }
    });
    
    // Update label styles
    if (isYearly) {
        monthlyLabel.classList.remove('active');
        yearlyLabel.classList.add('active');
    } else {
        monthlyLabel.classList.add('active');
        yearlyLabel.classList.remove('active');
    }
}

// Handle billing toggle
if (billingToggle) {
    billingToggle.addEventListener('change', (e) => {
        updatePrices(e.target.checked);
    });
    
    // Initialize with monthly pricing
    updatePrices(false);
    monthlyLabel.classList.add('active');
}

// Plan selection
function selectPlan(planName) {
    const isYearly = billingToggle ? billingToggle.checked : false;
    const period = isYearly ? 'yearly' : 'monthly';
    
    console.log(`Selected plan: ${planName} (${period})`);
    
    // Check if user is logged in
    const token = localStorage.getItem('auth_token');
    
    if (!token) {
        // Not logged in, redirect to signup with plan parameter
        window.location.href = `/static/signup.html?plan=${planName}&period=${period}`;
        return;
    }
    
    // User is logged in
    if (planName === 'free') {
        // Free plan - just show message
        alert('Ya estás en el plan gratuito. ¡Disfruta de UIResearch!');
        return;
    }
    
    // For paid plans, we'll implement Stripe checkout later
    // For now, show a message
    showPlanSelectionMessage(planName, period);
}

function showPlanSelectionMessage(planName, period) {
    const planNames = {
        'pro': 'Pro',
        'team': 'Team',
        'academic': 'Academic'
    };
    
    const prices = {
        'pro': { monthly: 9.99, yearly: 99 },
        'team': { monthly: 29.99, yearly: 299 },
        'academic': { monthly: 4.99, yearly: 49 }
    };
    
    const price = prices[planName][period];
    const periodText = period === 'yearly' ? 'año' : 'mes';
    
    const message = `
        ¡Excelente elección!
        
        Plan: ${planNames[planName]}
        Precio: $${price}/${periodText}
        
        La integración con Stripe estará disponible próximamente.
        Por ahora, puedes contactarnos para activar tu plan manualmente.
    `;
    
    alert(message);
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Highlight current plan if user is logged in
async function highlightCurrentPlan() {
    const token = localStorage.getItem('auth_token');
    if (!token) return;
    
    try {
        const response = await fetch('/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            // TODO: Get user's current plan from subscription endpoint
            // For now, we'll assume free plan
            console.log('User:', user);
        }
    } catch (error) {
        console.error('Error getting user info:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    highlightCurrentPlan();
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe pricing cards
document.querySelectorAll('.pricing-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Observe FAQ items
document.querySelectorAll('.faq-item').forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(20px)';
    item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(item);
});
