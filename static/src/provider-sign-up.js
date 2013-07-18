// String Constants
var EMAIL_REGEX = '^..*@.*.$';
var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "Email is already in use.";
var SERVER_ERROR = "Server error. Please try again.";

// Read GET URL variables and return them in associative array

function getUrlVars() {
  var vars = [], hash;
  var hashes = window.location.href.slice(
    window.location.href.indexOf('?') + 1).split('&');
  for (i = 0; i < hashes.length; i++) {
    hash = hashes[i].split('=');
    vars.push(hash[0]);
    vars[hash[0]] = hash[1];
  }
  return vars;
}

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

// Increment registration graphic with animation

function animateStep() {
  if (stage == "account")
    $('#certification-step h2').addClass('next');
  else if (stage == "certification")
    $('#submit-step h2').addClass('next');
  inactive_step_text = $('.active').html();
  $('.active').text('');
  $('.active').addClass('iterator');
  $('.active').transition({x: 175}, 500, 'ease', function () {
    $('<h2>' + inactive_step_text + '</h2>').insertBefore('.active');
    $('.next').prop('class', 'active');
    $('.iterator').remove();
  });
}

// Takes object literal of data and returns as hidden input html

function hiddenInputsFromData(data) {
  html = "";
  $.each(data, function (key, value) {
    if (key != "csrfmiddlewaretoken") {
      html += '<input id="account-' + key + '" hidden="true" value="' +
        value + '"/>'
    }
  });
  return html;
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


  // Begin with account stage

  stage = "account";
  $('#account-step h2').addClass('active');
  $('#account-wrap').load('blocks #account-block');

  // Disable submit button when a form field is blank

  $('.submit').prop('disabled', true);
  observeInterval = 100;
  setInterval(function () {
    var noBlanks = true;
    $('.text_input').each(function () {
      if ($(this).val() == '') {
        noBlanks = false;
      }
    });
    $('.submit').prop('disabled', !noBlanks);
  }, observeInterval);

  // On submit

  $('.account-form').live('submit', function () {

    //$('#sign-up-button').empty();
    var target = document.getElementById('sign-up-button');
    var spinner = new Spinner(opts).spin(target);

    // Clear errors  

    var errors = [];
    $('#invalid-wrap').text('');

    if (stage == "account") {

      // Validate email

      if (!$('#account-email').val().match(EMAIL_REGEX)) {
        errors.push(INVALID_EMAIL);
        spinner.stop();  
        $('#account-email').val('');
      }

      if (errors.length === 0) {

        // Collect data from account form fields

        var formData = {
          firstName: $('#account-first-name').val(),
          lastName: $('#account-last-name').val(),
          email: $('#account-email').val(),
          phone: $('#account-phone').val(),
          csrfmiddlewaretoken: csrf_token
        };

        // Validate email with server
        // Store form data and continue to certification stage
        
        $.ajax({
          type: "post",
          dataType: 'json',
          url: "/join/emailed/",
          data: formData,
          success: function (dataJSON) {
            if (dataJSON.status === "success") {
              if (dataJSON.emailed) {
                $('#account-email').val('');
                errors.push(EMAIL_TAKEN);
                console.log(errors);
              } else {
                $('#account-wrap').load(
                  'blocks #certification-block', function () {
                    $('#account-wrap').append(hiddenInputsFromData(formData));
                });
                animateStep();
                stage = "certification";
              }
            } else {
              $('#account-email').val('');
              spinner.stop();  
              errors.push(SERVER_ERROR);
            }
            console.log(errors);
            displayErrors(errors);
          }
        });
      }

    } else if (stage == "certification") {

      // Collect data from certification form fields

      var formData = {
        firstName: $('#account-firstName').val(),
        lastName: $('#account-lastName').val(),
        email: $('#account-email').val(),
        phone: $('#account-phone').val(),
        loc: $('#account-location').val(),
        specialties: $('#account-specialties').val(),
        csrfmiddlewaretoken: csrf_token
      };
      
      if (errors.length === 0) {

        // Send data to server, continue to submit stage

        $.ajax({
          type: "post",
          dataType: 'json',
          url: "/join/handler/",
          data: formData,
          success: function (dataJSON) {
            if (dataJSON.status === "success") {
              $('#account-wrap').load('blocks #submit-block', function () {
                spinner.stop();  
              });
              animateStep();
              stage = "submit";
            } else {
              spinner.stop();  
              errors.push(SERVER_ERROR);
            }
            displayErrors(errors);
          }
        });
      
      }

    }

    displayErrors(errors);

    return false;

  });

});
