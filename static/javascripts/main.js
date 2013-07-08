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
  var btn = $('#nav li a');

  id = getUrlVars()["id"];
  if (typeof id != 'undefined') {

    data = { join_id: id,
             csrfmiddlewaretoken: csrf_token };

    $.ajax({
      type: "post",
      dataType: "json",
      url: "/face/signin_user/",
      data: data
    )};

  }

  // $(btn).click(function() {
  //   $(this).parent('li').addClass('active');
  //   $(btn).not(this).parent('li').removeClass('active');

  //   if ($('#btn1').hasClass('active')) {
  //     $('#slider').animate({
  //       marginLeft:1
  //     });
  //   } else if ($('#btn2').hasClass('active')) {
  //     $('#slider').animate({
  //       marginLeft:77
  //     });
  //   }
  // });

});

$(window).bind('beforeunload', function(){
  // return 'Are you sure you want to leave this session?';
});
