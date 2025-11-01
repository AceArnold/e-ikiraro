document.addEventListener('DOMContentLoaded', function() {
    setCurrentYear();
    setupFormHandling();
    setupFileValidation();
});

function setCurrentYear() {
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        const currentYear = new Date().getFullYear();
        yearElement.textContent = currentYear;
    }
}

function setupFormHandling() {
    const forms = document.querySelectorAll('.application-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
}

function handleFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Submitting...';
    submitButton.disabled = true;

    setTimeout(() => {
        console.log('Form submitted with data:', Object.fromEntries(formData));

        showSuccessMessage();

        submitButton.textContent = originalText;
        submitButton.disabled = false;

        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
        
    }, 1500);
}

function showSuccessMessage() {

    const successDiv = document.createElement('div');
    successDiv.className = 'success-message show';
    successDiv.innerHTML = `
        <strong>✓ Application Submitted Successfully!</strong><br>
        Your application has been received. You will receive a confirmation email shortly.
    `;

    const form = document.querySelector('.application-form');
    form.insertBefore(successDiv, form.firstChild);

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setupFileValidation() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                validateFile(file, input);
            }
        });
    });
}

function validateFile(file, input) {
    const maxSize = 5 * 1024 * 1024; 
    const photoMaxSize = 2 * 1024 * 1024; 
    

    const isPhoto = input.id.toLowerCase().includes('photo');
    const sizeLimit = isPhoto ? photoMaxSize : maxSize;
    

    if (file.size > sizeLimit) {
        const sizeMB = isPhoto ? '2MB' : '5MB';
        alert(`File size exceeds ${sizeMB}. Please choose a smaller file.`);
        input.value = '';
        return false;
    }
    

    const allowedTypes = input.accept.split(',').map(type => type.trim());
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    const mimeType = file.type;
    
    const isValidType = allowedTypes.some(type => {
        if (type.startsWith('.')) {
            return fileExtension === type;
        }
        return mimeType.match(type.replace('*', '.*'));
    });
    
    if (!isValidType) {
        alert(`Invalid file type. Please upload: ${input.accept}`);
        input.value = '';
        return false;
    }
    
    return true;
}


function setupConditionalFields() {

    const medicalRadios = document.querySelectorAll('input[name="medicalConditions"]');
    const medicalDetailsGroup = document.querySelector('#medicalDetails')?.closest('.form-group');
    
    if (medicalRadios.length > 0 && medicalDetailsGroup) {
        medicalRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'yes') {
                    medicalDetailsGroup.style.display = 'block';
                    document.getElementById('medicalDetails').required = true;
                } else {
                    medicalDetailsGroup.style.display = 'none';
                    document.getElementById('medicalDetails').required = false;
                }
            });
        });
        
        medicalDetailsGroup.style.display = 'none';
    }
}

setupConditionalFields();

function saveFormData(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (form.elements[key].type !== 'file') {
            data[key] = value;
        }
    }
    
    localStorage.setItem(formId + '_draft', JSON.stringify(data));
}

function loadFormData(formId) {
    const savedData = localStorage.getItem(formId + '_draft');
    if (!savedData) return;
    
    const data = JSON.parse(savedData);
    const form = document.getElementById(formId);
    if (!form) return;
    
    for (let [key, value] of Object.entries(data)) {
        const field = form.elements[key];
        if (field && field.type !== 'file') {
            field.value = value;
        }
    }
}


const form = document.querySelector('.application-form');
if (form && form.id) {

    loadFormData(form.id);
    

    setInterval(() => {
        saveFormData(form.id);
        console.log('Form data auto-saved');
    }, 30000);
}

function clearSavedFormData(formId) {
    localStorage.removeItem(formId + '_draft');
}

const originalHandleSubmit = handleFormSubmit;
handleFormSubmit = function(event) {
    originalHandleSubmit(event);
    const form = event.target;
    if (form.id) {
        clearSavedFormData(form.id);
    }
};

