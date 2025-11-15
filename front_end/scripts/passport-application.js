document.getElementById("passport-application-form").addEventListener("submit", function(e) {
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
    showMessage('success', 'Application submitted successfully! You will receive a confirmation email with your application reference number shortly.');
    
    document.getElementById("passport-application-form").reset();

    submitBtn.textContent = originalText;
    submitBtn.disabled = false;

    window.scrollTo({ top: 0, behavior: 'smooth' });

    setTimeout(() => {
    }, 3000);
  }, 2000);
});

function validateForm() {
  const nationalId = document.getElementById('national-id').value;
  const phone = document.getElementById('phone').value;
  const email = document.getElementById('email').value;

  if (!/^\d{16}$/.test(nationalId)) {
    showMessage('error', 'National ID must be exactly 16 digits.');
    return false;
  }

if (!/^\+?257\s?\d{8}$/.test(phone.replace(/\s/g, ''))) {
  showMessage('error', 'Please enter a valid Burundian phone number (e.g., +257 XX XXX XXX).');
  return false;
}

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
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

document.getElementById('reason').addEventListener('change', function() {
  const reason = this.value;
});

