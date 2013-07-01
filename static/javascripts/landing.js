// String Constants
var EMAIL_REGEX = '^..*@.*.$';
var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "Email is already in use.";
var SERVER_ERROR = "Server error. Please try again.";

Shadowbox.init({
  handleOversize: "drag",
  modal: true    
});

$(document).ready(function () {

  // Disable submit button when a form field is blank

  $('.submit').prop('disabled', true);
  observeInterval = 100;
  setInterval(function () {
    noBlanks = true;
    $('.text_input').each(function () {
      if ($(this).val() == '') {
        noBlanks = false;
      }
    });
    $('.submit').prop('disabled', !noBlanks);
  }, observeInterval);

  // On submit
  
  $('.account-form').live('submit', function () {

    // Clear errors  

    errors = [];
    $('#invalid-wrap').text('');

    // Validate email

    if (!$('#student-email').val().match(EMAIL_REGEX)) {
      errors.push(INVALID_EMAIL);
      $('#student-email').val('');
    }

    if (errors.length == 0) {
    
    // Collect data from account form fields

    formData = {
      name: $('#student-name').val(),
      email: $('#student-email').val(),
      phone: $('#student-phone').val(),
      csrfmiddlewaretoken: csrf_token
    };



  }); 


});
