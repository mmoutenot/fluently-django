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

  console.log('called');

  // Spin animation

  var opts = {
    lines: 9,
    length: 0,
    width: 8,
    radius: 10,
    corners: 1,
    color: '#ffffff'
  };  

  $('#contact-student-blocks-wrapper').load(
    '/consumer-contact/' + user_url + '/blocks #signup-block');

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
    
      // Collect data from account form fields

      formData = {
        name: $('#student-name').val(),
        email: $('#student-email').val(),
        zipCode: $('#student-zip-code').val(),
        needs: $('#student-needs').val(),
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
        url: "/consumer-contact/handler/",
        data: formData,
        success: function (dataJSON) {
          if (dataJSON['status'] === "success") {
            if (dataJSON['emailed'] === true) {
              $('#student-email').val('');
              spinner.stop();
              errors.push(EMAIL_TAKEN);
            } else {
              $('#contact-student-blocks-wrapper').load(
                '/consumer-contact/' + user_url + '/blocks #thankyou-block');
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


