document.getElementById("id-card-replacement-form").addEventListener("submit", function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const reason = document.getElementById('replacement-reason').value;

  if (!validateForm()) {
    return;
  }

  const submitBtn = document.querySelector('.btn-primary');
  const originalText = submitBtn.textContent;
  submitBtn.textContent = 'Submitting...';
  submitBtn.disabled = true;

  setTimeout(() => {
    showMessage('success', 'ID Card replacement request submitted successfully! You will be contacted within 5 business days regarding the next steps.');

    document.getElementById("id-card-replacement-form").reset();

    document.getElementById('police-report-group').style.display = 'none';

    submitBtn.textContent = originalText;
    submitBtn.disabled = false;

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, 2000);
});

function validateForm() {
  const idNumber = document.getElementById('current-id-number').value;
  const phone = document.getElementById('phone').value;
  const email = document.getElementById('email').value;
  const reason = document.getElementById('replacement-reason').value;
  const policeReport = document.getElementById('police-report').value;
  
  if (!/^\d{16}$/.test(idNumber)) {
    showMessage('error', 'National ID must be exactly 16 digits.');
    return false;
  }

  if ((reason === 'lost' || reason === 'stolen') && !policeReport) {
    showMessage('error', 'Police report number is required for lost or stolen ID cards.');
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

document.getElementById('replacement-reason').addEventListener('change', function() {
  const reason = this.value;
  const policeReportGroup = document.getElementById('police-report-group');
  const policeReportInput = document.getElementById('police-report');
  const damagedIdGroup = document.getElementById('damaged-id-group');
  const damagedIdInput = document.getElementById('damaged-id-photo');
  
  if (reason === 'lost' || reason === 'stolen') {
    policeReportGroup.style.display = 'block';
    policeReportInput.required = true;
    damagedIdGroup.style.display = 'none';
    damagedIdInput.required = false;
  } else if (reason === 'damaged') {
    policeReportGroup.style.display = 'none';
    policeReportInput.required = false;
    damagedIdGroup.style.display = 'block';
    damagedIdInput.required = true;
  } else {
    policeReportGroup.style.display = 'none';
    policeReportInput.required = false;
    damagedIdGroup.style.display = 'none';
    damagedIdInput.required = false;
  }
});

