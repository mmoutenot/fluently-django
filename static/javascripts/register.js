$(document).ready(function() {
  $('.submit').prop('disabled', true);
  observeInterval = 100;
    setInterval(function() { 
      isValid = true;
      $('.text_input').each(function() {
        if ($(this).val() == '') {
          isValid = false;
        }
      });
      if (!$('#check').prop('checked')) {
        isValid = false;
      }
      $('.submit').prop('disabled', !isValid);
    }, observeInterval);
  });
});

$(function(){
  $('#register-account-form').submit(function() {
    console.log("submitted");
    // TODO:validate form items
    first_name = $('#account-first-name').val();
    last_name = $('#account-first-name').val();
    email = $('#account-first-name').val();
    password_a = $('#account-first-name').val();
    password_b = $('#account-first-name').val();

    if (password_a === password_b){
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
            // TODO:mmoutenot or TODO:dporterlance
            // SLLlllliidde to the right, yo!
          }
        }
      });
    }
    return false;

  });

});




