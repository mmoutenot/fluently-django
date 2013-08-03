// String Constants
var EMAIL_REGEX = '^..*@.*.$';
var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "You have already contacted this SLP.";
var SERVER_ERROR = "Server error. Please try again.";

// Display all error strings from *errors array in *invalid-wrap element

function displayErrors(errors) {
  $('#invalid-wrap').append(errors[0]);
  if (errors.length > 1) {
    $('#invalid-wrap').append('<br/>');
    for (i = 1; i < errors.length; i++) {
      $('#invalid-wrap').append(errors[i]);
    }
  }
}

$(document).ready(function () {

  // Spin animation

  var opts = {
    lines: 9,
    length: 0,
    width: 8,
    radius: 10,
    corners: 1,
    color: '#ffffff'
  };  

  $('#example-contact-blocks-wrapper').load(
    '/example-consumer-contact/blocks #signup-block', function () {
     
    $('#student-modal-title').text('Contact Susan J.');
    $('#student-needs').attr(
      'placeholder', "I'm contacting Susan J. because...");  
    
  });

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
    if (!$('#student-needs').val()) {
      noBlanks = false;
    }
    $('.submit').prop('disabled', !noBlanks);
    console.log(noBlanks);
  }, observeInterval);

  // On submit
  
  $('#student-signup-form').live('submit', function () {

    var target = document.getElementById('sign-up-button');
    var spinner = new Spinner(opts).spin(target);   

    // Clear errors  

    errors = [];
    $('#invalid-wrap').text('');

    // Validate email

    if (!$('#student-email').val().match(EMAIL_REGEX)) {
      errors.push(INVALID_EMAIL);
      spinner.stop();
      $('#student-email').val('');
    }

    if (errors.length == 0) {

      $('#example-contact-blocks-wrapper').load(
          '/example-consumer-contact/blocks #thankyou-block', 
          function() {
            console.log('thanks?');
          });
      spinner.stop();

    }

    displayErrors(errors);

    return false;


  }); 


});


