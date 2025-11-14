document.getElementById('loginForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  // Allowed public domains
  const publicDomains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"];

  if (!email || !password) {
    alert('Please enter both email and password.');
    return;
  }

  const emailDomain = email.split('@')[1];

  if (publicDomains.includes(emailDomain)) {
    // Redirect to landing page
    window.location.href = "../index.html";
  } else {
    alert('Please enter a valid public email domain (e.g., @gmail.com, @yahoo.com).');
  }
});
