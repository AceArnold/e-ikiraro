document.getElementById("provisional-btn").addEventListener("click", function() {
  window.location.href = "./wDL.html"; // or create a new dedicated provisional page
});

document.getElementById("practical-btn").addEventListener("click", function() {
  const code = prompt("Enter your provisional license code:");
  if (code && code.trim().length >= 5) {
    alert("Code verified! Redirecting to Practical Exam Registration...");
    window.location.href = "./PDL.html"; // can later point to a 'practical-registration.html'
  } else {
    alert("Invalid or empty code. Please try again.");
  }
});
