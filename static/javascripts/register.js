// String Constants

var EMAIL_REGEX = '^..*@.*.$';

var INVALID_EMAIL = "Please provide valid email.";
var EMAIL_TAKEN = "Email is already in use.";
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

function display_errors(errors) {
  $('#invalid-wrap').append(errors[0]);
  if (errors.length > 1) {
    $('#invalid-wrap').append('<br/>');
    for (i = 1; i < errors.length; i++) {
      $('#invalid-wrap').append(errors[i]);
    }
  }
}

function animate_step() {
  inactive_step_text = $('.active').html();
  $('.active').text('');
  $('.active').addClass('iterator');
  $('.active').transition({x:175}, 500, 'ease', function() {
    $('<h2>' + inactive_step_text + '</h2>').insertBefore('.active');
    $('.next').prop('class', 'active');
    $('.iterator').remove();
  });
}

$(document).ready(function() {

  id = getUrlVars()["id"];
  if (typeof id != 'undefined') {
    data = { join_id: id,
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
          $('#account-email').val(email);
          $('#account-email').prop('disabled', true);
        }
      }
    });
  }
  stage = "account";
  $('#account-step h2').addClass('active');
  $('#certification-step h2').addClass('next');
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

  $('.account-form').live('submit', function() {

    errors = [];
    $('#invalid-wrap').text('');

    if (stage == "account") {

      first_name             = $('#account-first-name').val();
      email                  = $('#account-email').val();
      password               = $('#account-password').val();

      if (!email.match(EMAIL_REGEX)) {
        errors.push(INVALID_EMAIL);
        $('#account-email').val('');
      }
      
      if (errors.length == 0) {
        data = {
          stage:               stage,
          firstName:           first_name,
          email:               email,
          password:            password,
          csrfmiddlewaretoken: csrf_token
        };
      }
      
    } else if (stage == "certification") {   
      
      company     = $('#account-company').val();
      phone       = $('#account-phone').val();
      terms_check = $('#account-terms').prop('checked'); 

      if (!$('#account-terms').prop('checked')) {
        errors.push(TERMS_NOT_AGREED);
      }

      if (errors.length == 0) {
        data = {
          stage:                 stage,
          email:                 email,
          company:               $('#account-company').val(),
          phone:                 $('#account-phone').val(),
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
            stage = "certification";
            $('#account-wrap').load('register_blocks #certification-block');
            $('#account-company').val(dataJSON['company']);
            $('#account-company').prop('disabled', 'true');
            animate_step();
          } else if (stage == "account" && dataJSON['status'] === "DUP") {
            $('#account-email').val('');
            errors.push(EMAIL_TAKEN);
          } else if (stage == "certification" && dataJSON['status'] === "OK") {
            stage = "submit";
            $('#account-wrap').load('register_blocks #submit-block');
            animate_step();
          } else {
            errors.push(SERVER_ERROR);
          }
          display_errors(errors);          
        }
      });
    }  

    display_errors(errors);

    return false;
  
  });

});




