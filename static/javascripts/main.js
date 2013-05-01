$(document).ready(function() {
  var btn = $('#nav li a');

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
