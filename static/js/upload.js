$(document).ready(function() {
  $('#uploadModalContent').load('/static/uploadModal.html');
});

$(document).ready(function() {
  $('#uploadButton').click(function(e) {
    e.preventDefault();
    $('#uploadModal').reveal();
  });
});

function formSubmit()
{
  url = document.getElementById("url").value;
  link = '/image/?url=' + url;
  $("#images").html("");
  $.getJSON(link, function(data) {
    $.each(data, function(i,item){
      $("<img/>").attr("src", item).attr('class', 'selectable-image').appendTo("#images");
    });
    $(".selectable-image").click(function(event) {
      $(".selected-image").removeClass('selected-image');
      $(this).addClass('selected-image');
    });
    $('.tags-input').show();
    $('#error-message').hide();
    document.getElementById('error-message').innerHTML = "";

    $("#select-button").unbind('click');
    $("#select-button").click(function() {
      var image_url = $('.selected-image').attr('src');
      var tags = document.getElementById('tag').value.split(" ");
      $.ajax({
        url: "/add_item/",
        type: 'PUT',
        data: {board_id: boardId, url: url,
          image_url: image_url, tags: tags, pos_x: 100, pos_y: 200,
        scale: 1, locked: true
        }}).done(function() {
          $("#add-image-modal").trigger('reveal:close');
        });
    });
  })
  .error(function() {
    document.getElementById('error-message').innerHTML = "Image not found!";
    $('.tags-input').hide();
    $('#error-message').show();
  });
}
