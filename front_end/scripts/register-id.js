// document.getElementById('registerForm').addEventListener('submit', function(e) {
//   e.preventDefault();

//   const fullname = document.getElementById('fullname').value.trim();
//   const email = document.getElementById('email').value.trim();
//   const password = document.getElementById('password').value.trim();
//   const confirmPassword = document.getElementById('confirmPassword').value.trim();

//   const publicDomains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"];
//   const emailDomain = email.split('@')[1];

//   // Validation checks
//   if (!fullname || !email || !password || !confirmPassword) {
//     alert('Please fill in all fields.');
//     return;
//   }

//   if (!publicDomains.includes(emailDomain)) {
//     alert('Please enter a valid public email domain (e.g., @gmail.com, @yahoo.com).');
//     return;
//   }

//   if (password.length < 6) {
//     alert('Password must be at least 6 characters.');
//     return;
//   }

//   if (password !== confirmPassword) {
//     alert('Passwords do not match.');
//     return;
//   }

//   // Registration success (frontend demo)
//   alert('Registration successful! You can now log in.');
//   window.location.href = "login.html";
// });
