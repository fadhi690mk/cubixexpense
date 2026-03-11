/**
 * Button Loader Script
 * Prevents duplicate form submissions by disabling buttons during form submission
 * and displaying a loading spinner
 */

document.addEventListener('DOMContentLoaded', function() {
    // Handle all form submissions
    const forms = document.querySelectorAll('form[method="post"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Find all submit buttons in the form
            const submitButtons = form.querySelectorAll('button[type="submit"]');
            
            submitButtons.forEach(button => {
                // Store the original button text
                const originalHTML = button.innerHTML;
                const originalText = button.textContent.trim();
                
                // Disable the button to prevent duplicate submissions
                button.disabled = true;
                
                // Add spinner and loading text
                button.innerHTML = `
                    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    <span>Processing...</span>
                `;
                
                // Add Bootstrap spinner styles if not already present
                if (!document.querySelector('style[data-spinner-styles]')) {
                    const style = document.createElement('style');
                    style.setAttribute('data-spinner-styles', 'true');
                    style.textContent = `
                        .spinner-border-sm {
                            width: 1rem;
                            height: 1rem;
                            border-width: 0.2em;
                        }
                        
                        button[type="submit"]:disabled {
                            cursor: not-allowed;
                            opacity: 0.8;
                        }
                    `;
                    document.head.appendChild(style);
                }
                
                // Store original state for potential restoration
                button.dataset.originalHtml = originalHTML;
            });
        });
    });
    
    // Optional: Reset button state if form encounters an error
    // This allows users to try again without page reload
    window.resetFormButtons = function(formSelector = 'form[method="post"]') {
        const forms = document.querySelectorAll(formSelector);
        forms.forEach(form => {
            const submitButtons = form.querySelectorAll('button[type="submit"]');
            submitButtons.forEach(button => {
                if (button.dataset.originalHtml) {
                    button.innerHTML = button.dataset.originalHtml;
                    button.disabled = false;
                }
            });
        });
    };
});
