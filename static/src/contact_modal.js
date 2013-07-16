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

  $('#contact-student-blocks-wrapper').load(
    '/space/contact/contact_student_blocks #contactform-block', function () {
     
    $('#student-modal-title').text('Contact ' + firstName + ' ' + lastName);
    $('#student-needs').attr(
      'placeholder', "I'm contacting " + firstName + " "  + lastName + " because...");  
    
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
    $('.submit').prop('disabled', !noBlanks);
  }, observeInterval);

  // On submit
  
  $('#contact-signup-form').live('submit', function () {

    // Clear errors  

    errors = [];
    $('#invalid-wrap').text('');

    // Validate email

    if (!$('#contact-email').val().match(EMAIL_REGEX)) {
      errors.push(INVALID_EMAIL);
      $('#contact-email').val('');
    }

    if (errors.length == 0) {
    
      // Collect data from account form fields

      formData = {
        name: $('#contact-name').val(),
        email: $('#contact-email').val(),
        loc: $('#contact-location').val(),
        needs: $('#contact-needs').val(),
        slp: slp,
        csrfmiddlewaretoken: csrf_token
      };

      // Validate email with server
      // Store form data
  
      console.log("ajaxing ");
      console.log(formData);

      $.ajax({
        type: "post",
        dataType: "json",
        url: "/space/contact/SLP/",
        data: formData,
        success: function (dataJSON) {
          if (dataJSON['status'] === "success") {
            if (dataJSON['emailed'] === true) {
              $('#contact-email').val('');
              errors.push(EMAIL_TAKEN);
            } else {
              $('#contact-student-blocks-wrapper').load(
                '/space/contact/contact_student_blocks #thankyou-block');
            }
          } else {
            $('#contact-email').val('');
            errors.push(SERVER_ERROR);
          }
          displayErrors(errors);
        }
      });
    
    }

    displayErrors(errors);

    return false;


  }); 


});


