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

  // Spin animation

  var opts = {
    lines: 9,
    length: 0,
    width: 8,
    radius: 10,
    corners: 1,
    color: '#ffffff'
  };  

  $('#register-student-blocks-wrapper').load(
    'blocks #signup-block');

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

    var target = document.getElementById('sign-up-button');
    var spinner = new Spinner(opts).spin(target);  

    console.log("submit");

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
    
      // Collect data from account form fields

      formData = {
        name: $('#student-name').val(),
        email: $('#student-email').val(),
        zip: $('#student-zip-code').val(),
        needs: $('#student-needs').val(),
        csrfmiddlewaretoken: csrf_token
      };

      // Validate email with server
      // Store form data
  
      console.log("ajaxing ");
      console.log(formData);

      $.ajax({
        type: "post",
        dataType: "json",
        url: "/consumer-request/handler/",
        data: formData,
        success: function (dataJSON) {
          if (dataJSON['status'] === "success") {
            if (dataJSON['emailed'] === true) {
              $('#student-email').val('');
              errors.push(EMAIL_TAKEN);
            } else {
              $('#register-student-blocks-wrapper').load(
                'blocks #thankyou-block');
            }
          } else {
            $('#student-email').val('');
            spinner.stop();
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

