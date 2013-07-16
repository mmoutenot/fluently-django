// String Constants

SERVER_ERROR = "Internal server error."

// Filepicker API for profile picture

var profile_data;

$(document).ready(function () {

  // Spin animation

  var opts = {
    lines: 13,
    length: 7,
    width: 4,
    radius: 10,
    corners: 1,
  };

  var target = document.getElementById('prof-pic');

  data = {
    csrfmiddlewaretoken: csrf_token
  };

  // Get profile picture

  $.ajax({
    type: "post",
    dataType: "json",
    url: "/space/picture/",
    data: data,
    success: function(dataJSON) {
      if (dataJSON['status'] === "success") {
        console.log("success");
        $('#prof-pic').css(
          'background-image', 
          'url("' + dataJSON.pic_url + '")'
        );
        console.log($('#prof-pic').css('background-image'));
      } 
    }
  });

  // Change profile picture

  filepicker.setKey('Ax3aLiPGtQJyyVSqNIiW2z');
  
  $('#change-prof-pic-btn').click(function () {
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
                               if (dataJSON.status === "success") {
                                 var spinner = new Spinner(opts).spin(target);
                                 $('#prof-pic').css(
                                   'background-image', 
                                   'url("' + pic.url + '")'
                                 );
                                 $('#prof-pic').waitForImages({
                                   finished: function () {
                                     spinner.stop();
                                   },
                                   waitForAll: true
                                 });
                               } else {
                                 $('#prof-pic-invalid-wrap').text(
                                   SERVER_ERROR);
                               } 
                             } 
                           });
                         });
    });
  });

  // Disable forms until save button clicked

  $('.user-field').attr('disabled', 'disabled');
  $('.text-field').attr('disabled', 'disabled');

  // Edit, save, cancel buttons

  $('.edit-btn').click(function () {
    $('.save-buttons-box').css('visibility', 'visible');
    $('.edit-btn').css('visibility', 'hidden');
    $('.user-field').removeAttr('disabled')
    $('.text-field').removeAttr('disabled')

    profile_data = {
      firstName: $('#first-name').val(),
      lastName: $('#last-name').val(),
      loc: $('#location').val(),
      aboutMe: $('#about-me').val(),
      certifications: $('#certifications').val(),
      experience: $('#experience').val(),
      therapyApproach: $('#therapy-approach').val()
    }

  });

  $('.save-btn').click(function () {
    $('.save-buttons-box').css('visibility', 'hidden');
    $('.edit-btn').css('visibility', 'visible');
    $('.user-field').attr('disabled', 'disabled');
    $('.text-field').attr('disabled', 'disabled');

    // Save user info

    data = {
      firstName: $('#first-name').val(),
      lastName: $('#last-name').val(),
      loc: $('#location').val(),
      aboutMe: $('#about-me').val(),
      certifications: $('#certifications').val(),
      experience: $('#experience').val(),
      therapyApproach: $('#therapy-approach').val(),
      csrfmiddlewaretoken: csrf_token
    };

    $.ajax({
      type: "post",
      dataType: "json",
      url: "/space/save_profile/",
      data: data,
      success: function(dataJSON) {
        if (dataJSON['status'] === "success") {
          $('html,body').scrollTop(0);
          $('#profile-status').text("Profile saved.");
          $('#info-name').text(data.firstName + " " + data.lastName);
        } 
      }
    });

  });

  $('.cancel-btn').click(function () {

    $('.save-buttons-box').css('visibility', 'hidden');
    $('.edit-btn').css('visibility', 'visible');
    $('.user-field').attr('disabled', 'disabled');
    $('.text-field').attr('disabled', 'disabled');
      
    $('#first-name').val(profile_data.firstName);
    $('#last-name').val(profile_data.lastName);
    $('#location').val(profile_data.loc);
    $('#about-me').val(profile_data.aboutMe);
    $('#certifications').val(profile_data.certifications);
    $('#experience').val(profile_data.experience);
    $('#therapy-approach').val(profile_data.therapyApproach);

  });


});
