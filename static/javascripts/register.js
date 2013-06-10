// String Constants

var EMAIL_REGEX = '^..*@.*.$';
var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "Email is already in use.";
var MISMATCH_PASSWORD = "Passwords must match.";
var TERMS_NOT_AGREED = "You must agree to the Terms of Service to proceed.";

$(document).ready(function() {

  $('#account-wrap').load('register_blocks #account-block');
  stage = "account";

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

});

$(function() {

  $('#register-account-form').live('submit', function() {

    validInputClient = true;
    validInputServer = true;
    client_error_strs = [];
    server_error_strs = [];
    $('#invalid-wrap').text('');

    if (stage == "account") {

      first_name             = $('#account-first-name').val();
      last_name              = $('#account-last-name').val();
      email                  = $('#account-email').val();
      password_a             = $('#account-password-a').val();
      password_b             = $('#account-password-b').val();
      terms_check            = $('#account-terms').prop('checked'); 

      if (!email.match(EMAIL_REGEX)) {
        validInputClient = false;
        client_error_strs.push(INVALID_EMAIL);
        $('#account-email').val('');
      }
      
      if (password_a !== password_b) {
        validInputClient = false;
        client_error_strs.push(MISMATCH_PASSWORD);
        $('[id*=password]').val('');
      }
      
      if (!$('#account-terms').prop('checked')) {
        validInputClient = false;
        client_error_strs.push(TERMS_NOT_AGREED);
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
            $('#account-wrap').load('register_blocks #confirmation-block');
            // TODO: SLLlllliidde to the right, yo!
          } else if (stage == "account" && dataJSON['status'] === "DUP") {
            validInputServer = false;
            $('#account-email').val('');
            server_error_strs.push(EMAIL_TAKEN);
            $('#invalid-wrap').append(server_error_strs[0]);
            if (server_error_strs.length > 1) {
              $('#invalid-wrap').append('<br/>');
              for (i = 1; i < server_error_strs.length; i++) {
                $('#invalid-wrap').append(server_error_strs[i]);
              }
            }
          }
        }
      });
    } else { 
      $('#invalid-wrap').append(client_error_strs[0]);
      if (error_strs.length > 1) {
        $('#invalid-wrap').append('<br/>');
        for (i = 1; i < client_error_strs.length; i++) {
          $('#invalid-wrap').append(client_error_strs[i]);
        }
      }
    }

    return false;
  
  });

});




