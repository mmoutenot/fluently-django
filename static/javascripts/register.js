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
  if (stage == "account")
    $('#certification-step h2').addClass('next');
  else if (stage == "certification")
    $('#submit-step h2').addClass('next');
  inactive_step_text = $('.active').html();
  $('.active').text('');
  $('.active').addClass('iterator');
  $('.active').transition({x:175}, 500, 'ease', function() {
    $('<h2>' + inactive_step_text + '</h2>').insertBefore('.active');
    $('.next').prop('class', 'active');
    $('.iterator').remove();
  });
}

function hiddenInputsFromData(data) {
  html = "";
  $.each(data, function(key, value) {
    if (key != "csrfmiddlewaretoken") {
      html += '<input id="account-' + key + '" hidden="true" value="' + value + '"/>' 
    } 
  });
  return html;
}

$(document).ready(function() {

  id = getUrlVars()["id"];
  if (typeof id != 'undefined') {
    data = { join_id: id,
             csrfmiddlewaretoken: csrf_token };
    $.ajax({
      type : "post",
      dataType:'json',
      url : "/face/register/user_info/",
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

      if (!$('#account-email').val().match(EMAIL_REGEX)) {
        errors.push(INVALID_EMAIL);
        $('#account-email').val('');
      } 

    }
  
    if (errors.length == 0) {  

      formData = {
        name: $('#account-name').val(),
        email: $('#account-email').val(),
        phone: $('#account-phone').val(),
        csrfmiddlewaretoken: csrf_token 
      };

      if (stage == "account") {
        $.ajax({
          type : "post",
          dataType:'json',
          url : "/face/register/emailed/",
          data: formData,
          success: function(data) {
            dataJSON = jQuery.parseJSON(data);
            if (dataJSON['status'] === "DUP") {
              $('#account-email').val('');
              errors.push(EMAIL_TAKEN);
            } else if (dataJSON['status'] === 'OK') {
              $('#account-wrap').load('register_blocks #certification-block', function() {
                $('#account-wrap').append(hiddenInputsFromData(formData));
              });
              animate_step();
              stage = "certification";
            }
          }
        });

      } else if (stage == "certification") {

        formData = {
          name: $('#account-name').val(),
          email: $('#account-email').val(),
          phone: $('#account-phone').val(),
          state: $('#account-state').val(),
          specialties: $('#account-specialties').val(),
          csrfmiddlewaretoken: csrf_token 
        };

        $.ajax({
          type : "post",
          dataType:'json',
          url : "/face/register/account_handler/",
          data: formData,
          success:function(data){
            dataJSON = jQuery.parseJSON(data);
            if (dataJSON['status'] === "OK") {
              $('#account-wrap').load('register_blocks #submit-block');
              animate_step();
              stage = "submit";
            } else {
              errors.push(SERVER_ERROR);
            }
            display_errors(errors);          
          }
        });
      }
        
    }  

    display_errors(errors);

    return false;
  
  });

});




