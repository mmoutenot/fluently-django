// String Constants

var EMAIL_REGEX = '^..*@.*.$';
var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "Email is already in use.";
var MISMATCH_PASSWORD = "Passwords must match.";
var TERMS_NOT_AGREED = "You must agree to the Terms of Service to proceed.";

// Stage functions
// account -> confirmation -> certification -> submit

// Returns a string corresponding to current registration stage
function checkStage() {
  if ($('#account-block').exists()) { 
    return "account"; 
  } else if ($('#confirmation-block').exists()) {
    return "confirmation";
  } else if ($('#certification-block').exists()) { 
    return "certification"; 
  } else if ($('#submit-block').exists()) {
    return "submit";
  } else {
    return null;
  }
}

// Advances front end registration stage and returns string corresponding
// to new registration stage
function advanceStage() {
  if (checkStage() == "account") {
    $('#account-wrap').load('register-blocks #confirmation-block');
  } else if (checkStage() == "certification") {
    $('#account-wrap').load('register-blocks #submit-block');
  }
  return checkStage();
}

$(document).ready(function() {

  stage = checkStage();  
  $('#account-wrap').load('register_blocks #account-block');
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

  $('.submit').live('submit', function() {

    validInputClient = true;
    validInputServer = true;
    display_strs = [];
    $('#invalid-wrap').text('');

    if (stage == "account") {

      first_name             = $('#account-first-name').val();
      last_name              = $('#account-last-name').val();
      email                  = $('#account-email').val();
      password_a             = $('#account-password-a').val();
      password_b             = $('#account-password-b').val();
      terms_check            = $('#account-terms').prop('checked'); 

      if (!email.match(email_regex)) {
        validInputClient = false;
        display_strs.push(INVALID_EMAIL);
        $('#account-email').val('');
      }
      
      if (password_a !== password_b) {
        validInputClient = false;
        display_strs.push(MISMATCH_PASSWORD);
        $('[id*=password]').val('');
      }
      
      if (!$('#account-terms').prop('checked')) {
        validInputClient = false;
        display_strs.push(TERMS_NOT_AGREED);
      }
  
      if (validInputClient) {
        data = {
          stage:               stage,
          firstName:           first_name,
          lastName:            last_name,
          email:               email,
          password:            password_a,
          // and with every ajax post, we need the csrf_token
          csrfmiddlewaretoken: csrf_token
        };
      }
      
    } else if (stage == "certification") {   
    
      certification          = $('#account-certification').val();
      education              = $('#account-education').val();
      licensed_states        = $('#account-licensed-states').val();
      membership             = $('#account-membership').val();
      experience_specialties = $('#account-experience-specialties').val();
   
      if (validInputClient) {
        data = {
          stage:                 stage,
          certification:         certification,
          education:             education,
          licensedStates:        licensed_states,
          membership:            membership,
          experienceSpecialties: experience_specialties,
          // and with every ajax post, we need the csrf_token
          csrfmiddlewaretoken:   csrf_token
        };
      }

    }
    
    if (validInputClient) {    
      $.ajax({
        type : "post",
        dataType:'json',
        url : "/face/register/account_handler/",
        data: data,
        success:function(data){
          dataJSON = jQuery.parseJSON(data);
          if(dataJSON['status'] === "OK") {
            stage = advanceStage();
            // TODO: SLLlllliidde to the right, yo!
          } else if (stage == "account" && dataJSON['status'] === "DUP") {
            validInputServer = false;
            $('#account-email').val('');
            display_strs.push(EMAIL_TAKEN);
          }
        }
      });
    }
    
    if (!validInputClient || !validInputServer) {  
      $('#invalid-wrap').append(display_strs[0]);
      if (display_strs.length > 1) {
        $('#invalid-wrap').append('<br/>');
        for (i = 1; i < display_strs.length; i++) {
          $('#invalid-wrap').append(display_strs[i]);
        }
      }
    }

    return false;
  });
});




