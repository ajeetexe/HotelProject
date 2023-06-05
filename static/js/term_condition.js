var declineButton = document.getElementById('declineButton');
var agreeButton = document.getElementById('agreeButton');

declineButton.addEventListener('click', function() {
  // Action to perform when the decline button is clicked
  let tmp = confirm("You have declined the terms and conditions.");
});

agreeButton.addEventListener('click', function() {
  // Action to perform when the agree button is clicked
  let tmp = confirm("You have agreed to the terms and conditions.");
  
});