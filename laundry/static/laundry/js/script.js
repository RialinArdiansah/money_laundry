// Money Laundry - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initializeNavigation();
    initializeCards();
    initializeForms();
    initializeTables();
    initializeAnimations();
    initializeTooltips();
    initializeNotifications();
});

// Navigation interactions
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // Mobile menu toggle (if needed)
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            navbarCollapse.classList.toggle('show');
        });
    }
}

// Card interactions
function initializeCards() {
    const cards = document.querySelectorAll('.card, .dashboard-card');
    
    cards.forEach(card => {
        // Add hover sound effect (visual feedback)
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });

        // Add click effect for clickable cards
        if (card.tagName === 'A' || card.onclick) {
            card.addEventListener('click', function(e) {
                // Create ripple effect
                createRipple(e, this);
            });
        }
    });
}

// Form interactions
function initializeForms() {
    const forms = document.querySelectorAll('form');
    const inputs = document.querySelectorAll('.form-control');
    
    // Form submission with loading state
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Add loading state
                const originalText = submitBtn.textContent;
                submitBtn.innerHTML = '<span class="loading"></span> Memproses...';
                submitBtn.disabled = true;
                
                // Re-enable button after 3 seconds (or when form is processed)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });

    // Input field interactions
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focused');
        });

        // Real-time validation feedback
        if (input.hasAttribute('required')) {
            input.addEventListener('input', function() {
                validateField(this);
            });
        }
    });
}

// Table interactions
function initializeTables() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            row.addEventListener('click', function() {
                // Highlight selected row
                rows.forEach(r => r.classList.remove('table-active'));
                this.classList.add('table-active');
            });
        });
    });

    // Add search functionality for tables
    const searchInputs = document.querySelectorAll('input[data-table-search]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const tableId = this.getAttribute('data-table-search');
            const table = document.getElementById(tableId);
            if (table) {
                searchTable(table, this.value);
            }
        });
    });
}

// Animations
function initializeAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe cards and sections
    const animatedElements = document.querySelectorAll('.card, .dashboard-card, section');
    animatedElements.forEach(el => observer.observe(el));

    // Counter animation for statistics
    const counters = document.querySelectorAll('[data-count]');
    counters.forEach(counter => {
        animateCounter(counter);
    });
}

// Tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = element.getAttribute('data-tooltip');
        document.body.appendChild(tooltip);

        element.addEventListener('mouseenter', function() {
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            tooltip.classList.add('show');
        });

        element.addEventListener('mouseleave', function() {
            tooltip.classList.remove('show');
        });
    });
}

// Notifications
function initializeNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
}

// Utility functions
function createRipple(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name || field.placeholder;
    
    if (value === '') {
        showFieldError(field, `${fieldName} tidak boleh kosong`);
        return false;
    } else {
        clearFieldError(field);
        return true;
    }
}

function showFieldError(field, message) {
    const formGroup = field.closest('.form-group') || field.parentElement;
    let errorElement = formGroup.querySelector('.field-error');
    
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        formGroup.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    field.classList.add('is-invalid');
}

function clearFieldError(field) {
    const formGroup = field.closest('.form-group') || field.parentElement;
    const errorElement = formGroup.querySelector('.field-error');
    
    if (errorElement) {
        errorElement.remove();
    }
    
    field.classList.remove('is-invalid');
}

function searchTable(table, searchTerm) {
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const isVisible = text.includes(searchTerm.toLowerCase());
        row.style.display = isVisible ? '' : 'none';
    });
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-count'));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// Show notification function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Add show class
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
    
    // Close button
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
}

// Add CSS for dynamic elements
const dynamicStyles = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .input-focused {
        transform: translateY(-2px);
    }
    
    .field-error {
        color: #ef4444;
        font-size: 0.875rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    .is-invalid {
        border-color: #ef4444 !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }
    
    .custom-tooltip {
        position: absolute;
        background: #1f2937;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
        pointer-events: none;
    }
    
    .custom-tooltip.show {
        opacity: 1;
        visibility: visible;
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        min-width: 300px;
        z-index: 1000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid #10b981;
    }
    
    .notification-error {
        border-left: 4px solid #ef4444;
    }
    
    .notification-info {
        border-left: 4px solid #3b82f6;
    }
    
    .notification-warning {
        border-left: 4px solid #f59e0b;
    }
    
    .notification-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .notification-close {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: #6b7280;
        padding: 0;
        margin-left: 1rem;
    }
    
    .notification-close:hover {
        color: #374151;
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease;
    }
    
    .table-active {
        background-color: #dbeafe !important;
        border-left: 4px solid #2563eb;
    }
`;

// Add dynamic styles to head
const styleSheet = document.createElement('style');
styleSheet.textContent = dynamicStyles;
document.head.appendChild(styleSheet);

// Export functions for global use
window.MoneyLaundry = {
    showNotification,
    validateField,
    searchTable,
    animateCounter
};