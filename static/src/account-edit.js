$(document).ready(function () {   

  // Spin animation

  var opts = {
    lines: 9,
    length: 0,
    width: 8,
    radius: 10,
    corners: 1,
    color: '#ffffff'
  };

  $.ajax({
    type: "post",
    dataType: "json",
    url: "/account-edit/handler/",
    data: {csrfmiddlewaretoken: csrf_token},
    success: function(dataJSON) {
      if (!dataJSON['viewed']) {
        $('#edit-specialties-block').css('display', '');
        $('#select-to').prop('selectedIndex', -1);
        $('#select-to').selectize({
          maxItems: 6,
          hideSelected: true
        });
        $('#select-to1').selectize({
          hideSelected: true,
          maxItems: 5,
        });
      } else {
        $('edit-advanced-specialties-block').css('display', '');
      }
    }
  });

  $('#edit-specialties-form').on('submit', function () {
   
    certs = []; 
    $('#select-to1 option').each(
      function () {
        certs.push($(this).val());
      }
    ); 

    specs = [];
    $('#select-to option').each(
      function () {
        specs.push($(this).val());
      }
    ); 
  
    formData = {
      city: $('#city-input').val(),
      state: $('#state-input').val(),
      certifications: certs.toString(),
      specialties: specs.toString(),
      csrfmiddlewaretoken: csrf_token
    };

    console.log(formData);

    $.ajax({
      type: "post",
      dataType: "json",
      url: "/account-edit/options-handler-1/",
      data: formData,
      success: function(dataJSON) {
        console.log('1st page to server');
      }
    });

    $('#edit-specialties-block').css('display', 'none');
    $('#edit-advanced-specialties-block').css('display', '');
    return false;
  });

  $('#edit-advanced-specialties-form').on('submit', function () {

    ages = [];
    $('.age').each(
      function () {
        if ($(this).is(':checked')) {
          ages.push($(this).val());
        }
      }
    );
    if (ages[0] == 'all') {
      ages.splice(0, 1);
    } 

    locs = [];
    $('.loc').each(
      function() {
        if ($(this).is(':checked')) {
          locs.push($(this).val());
        }
      }
    ); 

    pays = [];
    $('.pay').each(
      function() {
        if ($(this).is(':checked')) {
          pays.push($(this).val());
        }
      }
    ); 
 
    formData = {
      age: ages.toString(),
      loc: locs.toString(),
      pay: pays.toString(),
      test: "test",
      csrfmiddlewaretoken: csrf_token
    };
    
    console.log(formData);

    $.ajax({
      type: "post",
      dataType: "json",
      url: "/account-edit/options-handler-2/",
      data: formData,
      success: function(dataJSON) {
        console.log('2nd page to server');
      }
    });

    $('#edit-advanced-specialties-block').css('display', 'none');
    $('#welcome-block').css('display', '');
    return false;
  });

  $('#select-all').click(function() {
    $('.age').prop('checked', $('#select-all').is(':checked'));
  });

});


