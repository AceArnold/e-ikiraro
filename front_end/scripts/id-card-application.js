document.getElementById("id-card-application-form").addEventListener("submit", function(e) {
  e.preventDefault();

  const formData = new FormData(this);

  if (!validateForm()) {
    return;
  }

  const submitBtn = document.querySelector('.btn-primary');
  const originalText = submitBtn.textContent;
  submitBtn.textContent = 'Submitting...';
  submitBtn.disabled = true;

  setTimeout(() => {
    showMessage('success', 'ID Card application submitted successfully! Please visit your local registration office within 30 days to complete biometric enrollment.');

    document.getElementById("id-card-application-form").reset();

    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, 2000);
});

function validateForm() {
  const phone = document.getElementById('phone').value;
  const dateOfBirth = new Date(document.getElementById('date-of-birth').value);
  const today = new Date();

  let age = today.getFullYear() - dateOfBirth.getFullYear();
  const monthDiff = today.getMonth() - dateOfBirth.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dateOfBirth.getDate())) {
    age--;
  }

  if (age < 16) {
    showMessage('error', 'You must be at least 16 years old to apply for a National ID Card.');
    return false;
  }
if (!/^\+?257\s?\d{8}$/.test(phone.replace(/\s/g, ''))) {
  showMessage('error', 'Please enter a valid Burundian phone number (e.g., +257 XX XXX XXX).');
  return false;
}
  const email = document.getElementById('email').value;
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showMessage('error', 'Please enter a valid email address.');
    return false;
  }
  
  if (!document.getElementById('declaration').checked) {
    showMessage('error', 'You must accept the declaration to proceed.');
    return false;
  }
  
  return true;
}

function showMessage(type, message) {
  const existingMessages = document.querySelectorAll('.message');
  existingMessages.forEach(msg => msg.remove());
  
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  messageDiv.textContent = message;
  
  const formContainer = document.querySelector('.form-container');
  formContainer.insertBefore(messageDiv, formContainer.firstChild);
  
  if (type === 'error') {
    setTimeout(() => {
      messageDiv.remove();
    }, 5000);
  }
}

document.getElementById('marital-status').addEventListener('change', function() {
  const spouseField = document.getElementById('spouse-name');
  if (this.value === 'married') {
    spouseField.required = true;
    spouseField.parentElement.querySelector('label').innerHTML = 'Spouse\'s Full Name *';
  } else {
    spouseField.required = false;
    spouseField.parentElement.querySelector('label').innerHTML = 'Spouse\'s Full Name (if married)';
  }
});

