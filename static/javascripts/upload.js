$(document).ready(function() {
  // $('#uploadModalContent').load('uploadModal.html');
  // console.log('loaded upload modal');
});

$(document).ready(function() {
  $('#uploadButton').click(function(e) {
    console.log('upload clicked');
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

$(document).ready(function() {
  var holder = document.getElementById('holder'),
  tests = {
    filereader: typeof FileReader != 'undefined',
    dnd: 'draggable' in document.createElement('span'),
    formdata: !!window.FormData,
    progress: "upload" in new XMLHttpRequest
  },
  support = {
    filereader: document.getElementById('filereader'),
    formdata: document.getElementById('formdata'),
    progress: document.getElementById('progress')
  },
  acceptedTypes = {
    'image/png': true,
    'image/jpeg': true,
    'image/gif': true
  },
  progress = document.getElementById('uploadprogress'),
  fileupload = document.getElementById('upload');

  "filereader formdata progress".split(' ').forEach(function (api) {
    if (tests[api] === false) {
      support[api].className = 'fail';
    } else {
      console.log('hiding '+api);
      // FFS. I could have done el.hidden = true, but IE doesn't support
      // hidden, so I tried to create a polyfill that would extend the
      // Element.prototype, but then IE10 doesn't even give me access
      // to the Element object. Brilliant.
      support[api].className = 'hidden';
    }
  });

  function previewfile(file) {
    if (tests.filereader === true && acceptedTypes[file.type] === true) {
      var reader = new FileReader();
      reader.onload = function (event) {
        var image = new Image();
        image.src = event.target.result;
        image.width = 250; // a fake resize
        holder.appendChild(image);
      };

      reader.readAsDataURL(file);
    }  else {
      holder.innerHTML += '<p>Uploaded ' + file.name + ' ' + (file.size ? (file.size/1024|0) + 'K' : '');
      console.log(file);
    }
  }

  function readfiles(files) {
    debugger;
    var formData = tests.formdata ? new FormData() : null;
    for (var i = 0; i < files.length; i++) {
      if (tests.formdata) formData.append('file', files[i]);
      previewfile(files[i]);
    }

    // now post a new XHR request
    if (tests.formdata) {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/upload/');
      xhr.onload = function() {
        progress.value = progress.innerHTML = 100;
      };

      if (tests.progress) {
        xhr.upload.onprogress = function (event) {
          if (event.lengthComputable) {
            var complete = (event.loaded / event.total * 100 | 0);
            progress.value = progress.innerHTML = complete;
          }
        }
      }

      xhr.send(formData);
    }
  }

  if (tests.dnd) {
    holder.ondragover = function () { this.className = 'hover'; return false; };
    holder.ondragend = function () { this.className = ''; return false; };
    holder.ondrop = function (e) {
      this.className = '';
      e.preventDefault();
      readfiles(e.dataTransfer.files);
    }
  } else {
    fileupload.className = 'hidden';
    fileupload.querySelector('input').onchange = function () {
      readfiles(this.files);
    };
  }
});
