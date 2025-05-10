// Main application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle flash message dismissal
    document.querySelectorAll('.alert .close').forEach(button => {
        button.addEventListener('click', (e) => {
            e.target.closest('.alert').remove();
        });
    });

    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            document.getElementById('navbarMenu').classList.toggle('show');
        });
    }
});