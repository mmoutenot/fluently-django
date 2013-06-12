// String Constants

var EMAIL_REGEX = '^..*@.*.$';

var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "Email is already in use.";
var MISMATCH_PASSWORD = "Passwords must match.";
var TERMS_NOT_AGREED = "You must agree to the Terms of Service to proceed.";
var SERVER_ERROR = "Please try again.";

// Read a page's GET URL variables and return them as an associative array.
function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

$(document).ready(function() {

  id = getUrlVars()["id"];
  if (typeof id != 'undefined') {
    data = { stage: "confirmation", 
             join_id: id,
             csrfmiddlewaretoken: csrf_token };
    $.ajax({
      type : "post",
      dataType:'json',
      url : "/face/register/account_handler/",
      data: data, 
      success: function(data) {
        console.log(data);
        dataJSON = jQuery.parseJSON(data);
        console.log(dataJSON['status']);
        if (dataJSON['status'] === "OK") {
          email = dataJSON['email'];
          stage = "certification";
          $('#account-wrap').load('register_blocks #certification-block');
        }
      }
    });
  } else {
    stage = "account";
    $('#account-wrap').load('register_blocks #account-block');
  }

  $('.submit').prop('disabled', true);
  observeInterval = 100;
  setInterval(function() { 
    noBlanks = true;
    $('.text_input').each(function() {
      if ($(this).val() == '') {
        noBlanks = false;
      }
    });
    $('.submit').prop('disabled', !noBlanks);
  }, observeInterval);

  $('.account-form').live('submit', function() {

    errors = [];
    $('#invalid-wrap').text('');

    if (stage == "account") {

      first_name             = $('#account-first-name').val();
      last_name              = $('#account-last-name').val();
      email                  = $('#account-email').val();
      password_a             = $('#account-password-a').val();
      password_b             = $('#account-password-b').val();
      terms_check            = $('#account-terms').prop('checked'); 

      if (!email.match(EMAIL_REGEX)) {
        errors.push(INVALID_EMAIL);
        $('#account-email').val('');
      }
      
      if (password_a !== password_b) {
        errors.push(MISMATCH_PASSWORD);
        $('[id*=password]').val('');
      }
      
      if (!$('#account-terms').prop('checked')) {
        errors.push(TERMS_NOT_AGREED);
      }
  
      if (errors.length == 0) {
        data = {
          stage:               stage,
          firstName:           first_name,
          lastName:            last_name,
          email:               email,
          password:            password_a,
          csrfmiddlewaretoken: csrf_token
        };
      }
      
    } else if (stage == "certification") {   

      certification          = $('#account-certification').val();
      education              = $('#account-education').val();
      licensed_states        = $('#account-licensed-states').val();
      membership             = $('#account-membership').val();
      experience_specialties = $('#account-experience-specialties').val();
   
      if (errors.length == 0) {
        data = {
          stage:                 stage,
          email:                 email,
          certification:         certification,
          education:             education,
          licensedStates:        licensed_states,
          membership:            membership,
          experienceSpecialties: experience_specialties,
          csrfmiddlewaretoken:   csrf_token
        };
      }

    }
    
    if (errors.length == 0) {    
      $.ajax({
        type : "post",
        dataType:'json',
        url : "/face/register/account_handler/",
        data: data,
        success:function(data){
          dataJSON = jQuery.parseJSON(data);
          if(stage == "account" && dataJSON['status'] === "OK") {
            stage = "confirmation";
            $('#account-wrap').load('register_blocks #confirmation-block');
          } else if (stage == "account" && dataJSON['status'] === "DUP") {
            $('#account-email').val('');
            errors.push(EMAIL_TAKEN);
          } else if (stage == "certification" && dataJSON['status'] === "OK") {
            stage = "submit";
            $('#account-wrap').load('register_blocks #submit-block');
          } else {
            errors.push(SERVER_ERROR);
          }
        }
      });
    }  
    
    // Display errors if any
    $('#invalid-wrap').append(errors[0]);
    if (errors.length > 1) {
      $('#invalid-wrap').append('<br/>');
      for (i = 1; i < errors.length; i++) {
        $('#invalid-wrap').append(errors[i]);
      }
    }

    return false;
  
  });

});




