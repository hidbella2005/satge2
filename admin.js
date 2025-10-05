// Admin Dashboard JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert && alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });

    // Form validation helpers
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const message = button.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Hotel image preview
    const imageUrlInput = document.getElementById('image_url');
    if (imageUrlInput) {
        imageUrlInput.addEventListener('input', function() {
            const url = this.value;
            let preview = document.getElementById('image-preview');
            
            if (!preview) {
                preview = document.createElement('div');
                preview.id = 'image-preview';
                preview.className = 'mt-2';
                this.parentNode.appendChild(preview);
            }
            
            if (url) {
                preview.innerHTML = `
                    <img src="${url}" alt="Preview" class="img-thumbnail" style="max-width: 200px; max-height: 150px;">
                `;
            } else {
                preview.innerHTML = '';
            }
        });
    }

    // Auto-refresh dashboard data (if on dashboard page)
    if (window.location.pathname.includes('/admin') && window.location.pathname.endsWith('/admin')) {
        // Refresh dashboard data every 5 minutes
        setInterval(function() {
            // You can implement AJAX refresh here if needed
            console.log('Dashboard auto-refresh (placeholder)');
        }, 300000); // 5 minutes
    }

    // Search functionality enhancement
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    searchInputs.forEach(function(input) {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                // Auto-submit search after 500ms of no typing
                if (input.form && input.value.length > 2) {
                    // You can implement auto-search here if needed
                }
            }, 500);
        });
    });

    // Price formatting
    const priceInputs = document.querySelectorAll('input[name="price_per_night"], input[name="min_price"], input[name="max_price"]');
    priceInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });

    // Rating input validation
    const ratingInputs = document.querySelectorAll('input[name="rating"], input[name="min_rating"]');
    ratingInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value > 5) {
                this.value = 5;
            } else if (value < 0) {
                this.value = 0;
            }
        });
    });

    // Table row highlighting
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(13, 110, 253, 0.1)';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Mobile menu handling
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const target = document.querySelector(this.getAttribute('data-bs-target'));
            if (target) {
                // Add mobile menu animation classes if needed
                target.classList.toggle('show');
            }
        });
    }

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

// Utility functions
function showToast(message, type = 'info') {
    // Create toast notification
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

// Chart helper functions
function createChart(ctx, type, data, options = {}) {
    return new Chart(ctx, {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            ...options
        }
    });
}

// Export functions for global use
window.AdminUtils = {
    showToast,
    formatCurrency,
    formatDate,
    createChart
};
