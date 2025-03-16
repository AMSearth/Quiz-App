// Main JavaScript file for Quiz App

document.addEventListener('DOMContentLoaded', function() {
    // Add Bootstrap classes to form fields
    const formFields = document.querySelectorAll('input, select, textarea');
    formFields.forEach(field => {
        if (!field.classList.contains('form-control') && 
            field.type !== 'checkbox' && 
            field.type !== 'radio' && 
            field.type !== 'hidden' &&
            field.type !== 'submit') {
            field.classList.add('form-control');
        }
    });
}); 