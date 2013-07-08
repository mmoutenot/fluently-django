// String Constants

var PASSWORD_MISMATCH = "Passwords must match.";
var SERVER_ERROR = "Internal server error. Please try again.";

// Read a page's GET URL variables and return them as an associative array.
function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(
                 window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++)
    {
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

$(document).ready(function() {

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

  // Get email from join_id via server

  id = getUrlVars()["id"];
  if (typeof id == 'undefined') {
    id = "";
  }
  
  data = { join_id : id,
           csrfmiddlewaretoken: csrf_token 
  };

  $.ajax({
    type: "post",
    dataType: 'json',
    url: "/face/confirm/user/",
    data: data,
    success: function(dataJSON) {
      if (dataJSON["confirmed"]) {
        console.log("what")
        $('#register-account-form').load('confirm_blocks #already-confirmed');
      } else if (!dataJSON["success"]) {
        console.log(dataJSON)
        window.location.replace("/face/");
      }
      $('#account-email').val(dataJSON['email']);
    }
  });

  // On submit

  $('.account-form').live('submit', function () {

    // Clear errors

    errors = [];
    $('#invalid-wrap').text('');

    if ($('#account-password-a').val() != $('#account-password-b').val()) {
      errors.push(PASSWORD_MISMATCH);
      $('#account-password-a').val('');
      $('#account-password-b').val('');
    }

    if (errors.length == 0) {
      
      // Collect data from account form fields
    
      formData = {
        email: $('#account-email').val(),
        password: $('#account-password-a').val(),
        csrfmiddlewaretoken: csrf_token
      };  

      // Store form data and continue to space

      $.ajax({
        type: "post",
        dataType: "json",
        url: "/face/confirm/password/",
        data: formData,
        success: function(dataJSON) {
          if (dataJSON["status"] === "fail") {
            $('#account-email').val('');
            $('#account-password-a').val('');
            $('#account-password-b').val('');
            errors.push(SERVER_ERROR);
            displayErrors(errors);
          } else if (dataJSON["status"] === "success") {
            console.log("success");
            $('#register-account-form').load('confirm_blocks #confirmed');
          }
        }

      });
    }

    displayErrors(errors);

    return false;

  });

});
