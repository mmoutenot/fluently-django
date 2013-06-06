// String Constants

var EMAIL_REGEX = '^..*@.*.$';
var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "Email is already in use.";
var MISMATCH_PASSWORD = "Passwords must match.";

$(document).ready(function() {
  
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
    if (!$('#termsCheck').prop('checked')) {
      noBlanks = false;
    }
    $('.submit').prop('disabled', !noBlanks);
    console.log(noBlanks);
  }, observeInterval);

  $('#register-account-form').live('submit', function() {

    validInputClient = true;
    display_strs = [];
    $('#invalid-wrap').text('');

    first_name = $('#account-first-name').val();
    last_name = $('#account-last-name').val();
    email = $('#account-email').val();
    password_a = $('#account-password-a').val();
    password_b = $('#account-password-b').val();
    
    if (!email.match(email_regex)) {
      validInputClient = false;
      display_strs.push(INVALID_EMAIL);
      $('#account-email').val('');
    }

    if (password_a !== password_b){
      validInputClient = false;
      display_strs.push(MISMATCH_PASSWORD);
      $('[id*=password]').val('');
    }

    if (validInputClient) {
      // data_string = 'stage=account'
      // data_string += '&firstName=' + first_name;
      // data_string += '&lastName=' + last_name;
      // data_string += '&email=' + email;
      // data_string += '&password=' + password_a;
      data = {
        stage:"account",
        firstName:first_name,
        lastName:last_name,
        email: email,
        password: password_a,
        // and with every ajax post, we need the csrf_token
        csrfmiddlewaretoken:csrf_token
      };

      $.ajax({
        type : "post",
        dataType:'json',
        url : "/face/register/account_handler/",
        data: data,
        success:function(data){
          dataJSON = jQuery.parseJSON(data);
          if(dataJSON['status'] === "OK"){
            console.log('account registered. stage 1 complete');
            $('#account-wrap').load('register_blocks #confirmation-block');
            // TODO: SLLlllliidde to the right, yo!
          } else if (dataJSON['status'] === "DUP") {
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

  $('#certify-account-form').live('submit', function() {
    console.log("submitted-cert");
    // TODO: validate form items
    certification          = $('#account-certification').val();
    education              = $('#account-education').val();
    licensed_states        = $('#account-licensed-states').val();
    membership             = $('#account-membership').val();
    experience_specialties = $('#account-experience-specialties').val();
    
    data = {
      stage: "certification",
      certification: certification,
      education: education,
      licensedStates: licensed_states,
      membership: membership,
      experienceSpecialties: experience_specialties,
      // and with every ajax post, we need the csrf_token
      csrfmiddlewaretoken: csrf_token
    };
    
    $.ajax({
      type : "post",
      dataType:'json',
      url : "/face/register/account_handler/",
      data: data,
      success:function(data){
      dataJSON = jQuery.parseJSON(data);
        if(dataJSON['status'] === "OK"){
          console.log('account certified. stage 3 complete');
          // TODO: SLLlllliidde to the right, yo!
        }
      }
    });
    
    $('#account-wrap').load('register_blocks #submit-block');

  });

});




