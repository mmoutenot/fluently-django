// String Constants
var EMAIL_REGEX = '^..*@.*.$';
var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "Email is already in use.";
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
        phone: $('#student-location').val(),
        csrfmiddlewaretoken: csrf_token
      };

      // Validate email with server
      // Store form data

      $.ajax({
        type: "post",
        dataType: "json",
        url: "/face/register/student/",
        data: formData,
        success: function (dataJSON) {
          if (dataJSON['status'] === "success") {
            if (dataJSON['emailed'] === true) {
              $('#student-email').val('');
              errors.push(EMAIL_TAKEN);
            } else {
              $('#student-wrap').load('student_blocks #emailed-block');
            }
          } else {
            $('#student-email').val('');
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


