var pins = {},
  stage = null,
  layer = null,
  mouseDown = false,
  itemSelected = false,
  colors = ["red", "green", "black", "blue"],
  myColor = colors[Math.floor(Math.random()*3)];
  widthInc = window.innerWidth,
  heightInc = window.innerHeight,
  pointBatch = [];

var PADDING = 10;

/** ima hide shit in pinboard **/
var pinboard = {};

$(document).ready(function() {
  socket.onmessage = handleMessage;
});

function updateBoardName(name) {
  pinboard.name = name || "Pinboard";
  $("#pinners").html(pinboard.name);
}

function handleMessage(message) {
  var data = $.parseJSON(message.data);
  if ("users_connected" in data) {
    UserDisplay.render(data);
  }

  if ("board" in data) {
    var items = data["board"]["items"];
    updateBoardName(data["board"]["name"]);
    addItems(items);
  } else if ("update_type" in data) {
    if (data["update_type"] == "add_item") {
      addItem(data["item"]);
    } else if (data["update_type"] == "remove_item") {
      removeItem(data["item_id"]);
    } else if (data["update_type"] == "draw") {
      var points = data["points"];
      for (var i = 0; i < points.length; i++) {
        var point = points[i];
        var line = new Kinetic.Line({
          points: [point.x - point.dx, point.y - point.dy, point.x, point.y],
          stroke: point.color,
          strokeWidth: 8,
          lineCap: 'round',
          lineJoin: 'round'
        });
        layer.add(line);
        stage.draw();
      }
    } else if (data["update_type"] == "board_name_update") {
      updateBoardName(data["name"]);
    } else {
      var updatedItem = data["item"];
      var itemGroup = pins[updatedItem.id].group;
      var originalItem = pins[updatedItem.id].item;

      // Update position and scale.
      itemGroup.setPosition(updatedItem.pos_x, updatedItem.pos_y);
      var scale = updatedItem.scale;

      var newWidth = originalItem.original_width * scale;
      var newHeight = originalItem.original_height * scale;
      resizeItemGroup(itemGroup, newWidth, newHeight, true);

      stage.draw();
    }
  }

}

function resizeItemGroup(itemGroup, newWidth, newHeight, shouldUpdateDragger) {
  var fullWidth = newWidth + PADDING * 2;
  var fullHeight = newHeight + PADDING * 2;
  itemGroup.get(".image")[0].setSize(newWidth, newHeight);
  itemGroup.get(".rect")[0].setSize(fullWidth, fullHeight);
  itemGroup.get(".resizeWidget")[0].setPosition(fullWidth, fullHeight);
  itemGroup.get(".image")[0].setPosition(PADDING, PADDING);

  if (shouldUpdateDragger) {
    itemGroup.get(".bottomRight")[0].setPosition(fullWidth, fullHeight);
  }
}

function update(group, activeAnchor, item) {
  var topLeft = group.get(".topLeft")[0];
  var topRight = group.get(".topRight")[0];
  var bottomRight = group.get(".bottomRight")[0];
  var bottomLeft = group.get(".bottomLeft")[0];
  var resizeWidget = group.get(".resizeWidget")[0];

  var image = group.get(".image")[0];

  // update anchor positions
  switch (activeAnchor.getName()) {
    case "topLeft":
      topRight.attrs.y = activeAnchor.attrs.y;
      bottomLeft.attrs.x = activeAnchor.attrs.x;
      break;
    case "topRight":
      topLeft.attrs.y = activeAnchor.attrs.y;
      bottomRight.attrs.x = activeAnchor.attrs.x;
      break;
    case "bottomRight":
      bottomLeft.attrs.y = activeAnchor.attrs.y;
      topRight.attrs.x = activeAnchor.attrs.x;
      break;
    case "bottomLeft":
      bottomRight.attrs.y = activeAnchor.attrs.y;
      topLeft.attrs.x = activeAnchor.attrs.x;
      break;
  }

  image.setPosition(topLeft.attrs.x, topLeft.attrs.y);

  var imageSize = image.getSize();
  var aspectRatio = imageSize.width / imageSize.height;

  var width = topRight.attrs.x - topLeft.attrs.x;
  var height = width / aspectRatio;
  if(width && height) {
    item.scale = width / item.original_width;
    resizeItemGroup(group, width, height, false);
  }
}

function addAnchor(group, x, y, name, item) {
  var stage = group.getStage();
  var layer = group.getLayer();

  var anchor = new Kinetic.Circle({
    x: x,
    y: y,
    stroke: "#000",
    fill: "#000",
    opacity: 0,
    strokeWidth: 2,
    radius: 4,
    name: name,
    draggable: true
  });

  anchor.on("dragmove", function() {
    update(group, this, item);
    var currentTime = new Date()
    if (currentTime.getTime() % 2 == 0) {
      sendItemUpdate(group, item);
    }
    layer.draw();
  });
  anchor.on("mousedown touchstart", function() {
    group.setDraggable(false);
    this.moveToTop();
  });
  anchor.on("dragstart", function() {
    itemSelected = true;
  });

  anchor.on("dragend", function() {
    group.setDraggable(true);
    var size = group.get(".image")[0].getSize();
    resizeItemGroup(group, size.width, size.height, true);
    layer.draw();
    itemSelected = false;
  });
  // add hover styling
  anchor.on("mouseover", function() {
    var layer = this.getLayer();
    document.body.style.cursor = "se-resize";
    this.setStrokeWidth(4);
    layer.draw();
  });
  anchor.on("mouseout", function() {
    var layer = this.getLayer();
    document.body.style.cursor = "default";
    this.setStrokeWidth(2);
    layer.draw();
  });

  group.add(anchor);
}

function addResizeWidget(group, x, y) {
  var anchor = new Kinetic.Circle({
    x: x,
    y: y,
    stroke: "#000",
    fill: "#000",
    strokeWidth: 2,
    radius: 4,
    name: "resizeWidget",
  });

  group.add(anchor);
}

function addPinImage(group, tooltip) {
  var img = new Image();

  img.onload = function() {
    var kineticImage = new Kinetic.Image({
      x: -10,
      y: -20,
      image: img,
      width: 30,
      height: 30,
      name: "pin_image",
    });

    kineticImage.on('click', function(evt) {
        if (tooltip.attrs.visible == true) {
          tooltip.attrs.visible = false;
        }
        else {
          tooltip.attrs.visible = true;
        }
    });

    group.add(kineticImage);
    stage.draw();
  };
  img.src = "/static/images/pin_green.png";
}


function sendItemUpdate(group, item) {
  var position = group.getPosition();
  item.pos_x = position.x;
  item.pos_y = position.y;

  var width = group.get(".image")[0].getSize().width;
  item.scale = width / item.original_width;

  var data = {
    "board_id": boardId,
    "item": item
  };

  socket.send(JSON.stringify(data));
}

function addGroupForItem(item, image) {
  // Update the item's data.
  item.original_width = image.width;
  item.original_height = image.height;

  var itemGroup = new Kinetic.Group({
    x: item.pos_x,
    y: item.pos_y,
    draggable: true
  });

  // Map the item id to the data.
  pins[item.id] = {
    "item": item,
    "group": itemGroup
  };

  (function(image, item) {
    itemGroup.on("dragstart", function(evt) {
      itemSelected = true;
    });

    itemGroup.on("dragend", function(evt) {
      sendItemUpdate(this, item);
      pinboard.current_image = this.getChildren()[0];
      pinboard.current_item = item;
      itemSelected = false;
    });

    itemGroup.on("dragmove", function() {
      var currentTime = new Date()
      if (currentTime.getTime() % 2 == 0) {
        sendItemUpdate(this, item);
      }
    });
  })(image, item);

  layer.add(itemGroup);

  var imageWidth = image.width * item.scale;
  var imageHeight = image.height * item.scale;

  // Rect padding for the item.
  var rect = new Kinetic.Rect({
    x: 0,
    y: 0,
    width: imageWidth + PADDING * 2,
    height: imageHeight + PADDING * 2,
    fill: 'black',
    stroke: 'black',
    cornerRadius: 5,
    opacity: 0.5,
    strokeWidth: 1,
    name: "rect"
  });
  itemGroup.add(rect);

  // Main image content for the item.
  var img = new Kinetic.Image({
    x: PADDING,
    y: PADDING,
    image: image,
    width: image.width * item.scale,
    height: image.height * item.scale,
    name: "image",
  });
  itemGroup.add(img);

  img.on('click', function(evt) {
      // Store this image if we need to delete.
      pinboard.current_image = img;
      pinboard.current_item = item;
  });

  img.on('dblclick', function(evt) {
      var url = item.url
      window.open(url, '_blank');
      window.focus();
  });



  var tooltip = new Kinetic.Text({
      x: 2 * PADDING,
      y: -2 * PADDING,
      text: item.tags,
      fontFamily: "Helvetica Neue",
      fontSize: 15,
      fontStyle: "bold",
      padding: 0,
      textFill: "white",
      fill: "#232323",
      visible: false
  });
  itemGroup.add(tooltip);


  var size = rect.getSize();
  addResizeWidget(itemGroup, size.width, size.height);
  addAnchor(itemGroup, 0, 0, "topLeft", item);
  addAnchor(itemGroup, size.width, 0, "topRight", item);
  addAnchor(itemGroup, size.width, size.height, "bottomRight", item);
  addAnchor(itemGroup, 0, size.height, "bottomLeft", item);
  addPinImage(itemGroup, tooltip);

  itemGroup.on("dragstart", function() {
    this.moveToTop();
  });
  itemGroup.moveToTop();
  stage.draw();
}

function addItems(items) {
  for (var i = 0; i < items.length; i++) {
    addItem(items[i]);
  }
}

function addItem(item) {
  var img = new Image();

  (function(item, img) {
    img.onload = function() {
      addGroupForItem(item, img);
    };
  })(item, img);
  img.src = item["image_url"];
}

function removeItem(item_id) {
    var itemGroup = pins[item_id].group;
    itemGroup.remove();
    stage.draw()
}

function setupLastObjectTracking(stage) {
}

$(document).keyup(function (e) {
  if (e.keyCode == 46) {
      if (pinboard.current_image) {
          var image = pinboard.current_image;
          var group = image.getParent();
          var item = pinboard.current_item;
          group.removeChildren()
          pinboard.current_image = undefined;
          stage.draw();
          $.ajax({
            url: "/remove_item/",
            type: 'PUT',
            data: {board_id: boardId, id:item.id}}).done(function() { console.log("Really deleted."); });
      } else {
          console.log('Nothing to delete');
      }
  }
});

function initStage() {
  stage = new Kinetic.Stage({
    container: "container",
    width: window.innerWidth,
    height: window.innerHeight
  });
  layer = new Kinetic.Layer();
  stage.add(layer);

  var imageObj = new Image();
  imageObj.onload = function() {
    var cork = new Kinetic.Image({
      x: 0,
      y: 0,
      image: imageObj,
      width: window.innerWidth,
      height: window.innerHeight
    });
    layer.add(cork);
    stage.draw();
  };

  imageObj.src = '/static/images/cork.jpg';
  setupLastObjectTracking(stage);

  stage.on('mousedown', function(evt) {
    mouseDown = true;
  });

  stage.on('mouseup', function(evt) {
    mouseDown = false;
  });

  stage.on('mousemove', function(evt) {
    if (mouseDown && !itemSelected) {
      var line = new Kinetic.Line({
        points: [evt.layerX - evt.webkitMovementX, evt.layerY - evt.webkitMovementY, evt.layerX, evt.layerY],
        stroke: myColor,
        strokeWidth: 8,
        lineCap: 'round',
        lineJoin: 'round'
      });
      layer.add(line);
      stage.draw();
      data = {
        "x": evt.layerX,
        "y": evt.layerY,
        "dx": evt.webkitMovementX,
        "dy": evt.webkitMovementY,
        "color": myColor
      }
      pointBatch.push(data)
      if (pointBatch.length == 5) {
        sendDrawMessage();
      }
    }
  });
}

function sendDrawMessage() {
  var data = {"update_type": "draw", "points": pointBatch, "board_id": boardId};
  socket.send(JSON.stringify(data));
  pointBatch = [];
}

window.onload = initStage;

$(document).scroll(function(){
  // if(> stage.getWidth() - 200){
  //   console.log('increase stage width');
  //   stage.setWidth(stage.getWidth()+ widthInc);

  //   layer = new Kinetic.Layer();
  //   stage.add(layer);

  //   var imageObj = new Image();
  //   imageObj.onload = function() {
  //     var cork = new Kinetic.Image({
  //       x: stage.getWidth()-widthInc,
  //         y: 0,
  //         image: imageObj,
  //         width: window.innerWidth,
  //         height: window.innerHeight
  //     });
  //     layer.add(cork);
  //     stage.draw();
  //   };

  //   imageObj.src = '/static/images/cork.jpg';

  //   $('document').scrollLeft = $('.left').width()
  // }
  if($(document).scrollTop() + $(window).height() > stage.getHeight() - 200){
    stage.setHeight(stage.getHeight()+heightInc);

    layer = new Kinetic.Layer();
    stage.add(layer);

    var imageObj = new Image();
    imageObj.onload = function() {
      var cork = new Kinetic.Image({
        x: 0,
          y: stage.getHeight()-heightInc,
          image: imageObj,
          width: window.innerWidth,
          height: window.innerHeight
      });
      layer.add(cork);
      layer.moveToBottom();
      stage.draw();
    };

    imageObj.src = '/static/images/cork.jpg';
  }
});
