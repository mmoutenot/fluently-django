$(function(){
  $('#chat_form').submit(function() {
    var value = $('#message').val();
    console.log('form submitted with message: ' + value);
    if (value) {
      data = {space: window.space, action: 'message', message: value};
      socket.send(data);
    }
    $('#message').val('').focus();
    return false;
  });
});
