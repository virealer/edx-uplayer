/* Javascript for edx-uplayer. */
function uplayerXBlockInitView(runtime, element) {
    /* Weird behaviour :
     * In the LMS, element is the DOM container.
     * In the CMS, element is the jQuery object associated*
     * So here I make sure element is the jQuery object */
     //get params from studio
     get_params(runtime, element);
     console.log("mytest");
}
function get_params(runtime, element){
	$.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'get_params'),
            data: JSON.stringify({a: 'a'}),
            success: function(result) {
                console.log(result);
                service = result.service;
                vid = result.vid;
                app_id = result.app_id;
                width = result.width;
                height = result.height;
                show_player(service,vid,app_id,width,height);
                //watched_status.text(result.watched);
            }
        });

}

function show_player(service,vid,app_id,width,height){
    if (service === "polyv"){
	console.log("polyv");
      var player = polyvObject('#uplayer').videoPlayer({
        'width': width,
        'height': height,
        'vid' : vid,
      });
    }
    else if(service === "qcloud"){
      var player = new qcVideo.Player("uplayer",{
     	"file_id": vid,
        "app_id": app_id,
        "auto_play": "1",
        "width": width,
        "height": height,
     },{});
    }
}
