// String Constants

SERVER_ERROR = "Internal server error."

// Filepicker API for profile picture

$(document).ready(function () {

  // Spin animation

  var opts = {
    lines: 13,
    length: 7,
    width: 4,
    radius: 10,
    corners: 1,
  };

  var target = document.getElementById('profile-picture');

  data = {
    csrfmiddlewaretoken: csrf_token
  };

  $.ajax({
    type: "post",
    dataType: "json",
    url: "/space/picture/",
    data: data,
    success: function(dataJSON) {
      if (dataJSON['status'] === "success") {
        $('#profile-picture').attr('src', dataJSON['pic_url']);
      } else {
        $('#profile-picture').attr('src', "/static/images/default_profile.jpg");
      }
    } 
  });

  filepicker.setKey('Ax3aLiPGtQJyyVSqNIiW2z');

  $('#profile-picture-button').click(function () {
    filepicker.pick({'mimetype':"image/*"}, function(InkBlob) {
      filepicker.convert(InkBlob, 
                         {width: 200, height: 220, fit: 'crop', 
                          align: "faces"},
                         function (pic) {
                           data = {
                             pic_url: pic.url,
                             csrfmiddlewaretoken: csrf_token
                           };
                           $.ajax({
                             type: "post",
                             dataType: "json",
                             url: "/space/picture/",
                             data: data,
                             success: function (dataJSON) {
                               if (dataJSON['status'] === "success") {
                                 var spinner = new Spinner(opts).spin(target);
                                 $('#profile-picture').attr('src', pic.url);
                                 $('#profile-picture').load(function () {
                                   spinner.stop();
                                 });
                               } else {
                                 $('#profile-picture-invalid-wrap').text(
                                   SERVER_ERROR);
                               } 
                             } 
                           });
                         });
    });
  });

});
