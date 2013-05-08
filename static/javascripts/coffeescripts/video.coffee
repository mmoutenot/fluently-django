console.log "including video"

#stored in variables so that we can inject them into their proper zone
video_container_large_html = "<div id='video_large_container'><div id='video_large'></div></div>"
video_container_small_html = "<div id='video_small_container'><div id='video_small'></div></div>"

session_connect_handler = (event) ->
  subscribe_to_streams event.streams
  div = document.createElement 'div'
  div.setAttribute('id', 'publisher')

  publisher_container = $('video_small');
  publisher_container.appendChild div
  publisher_properties = {
    width  : '100%'
    height : '100%'
    name   : 'local stream'
  }
  publisher = TB.initPublisher (apiKey, 'publisher', publisher_properties)
  session.publish publisher

subscribe_to_streams = (streams) ->
  for stream in streams
    if stream.connection.connectionId != session.connection.connectionId
      display_stream stream

display_stream = (stream) ->
  div = document.createElement 'div'
  div.setAttribute ('id', 'stream'+stream.streamId)
  streams_container = document.getElementById 'video'
  streams_container.appendChild div
  subscriber = session.subscribe(stream, 'stream'+streamId)
  $('#stream'+stream.streamId).width('100%')
  $('#stream'+stream.streamId).height('100%');
  console.log 'added stream'

stream_created_handler = (event) ->
  console.log 'stream created'
  subscribe_to_streams event.streams

session = TB.initSession session_id
session.addEventListener("sessionConnected", session_connect_handler)
session.addEventListener("streamCreated", stream_created_handler)
session.connect(apiKey, tok_token)


