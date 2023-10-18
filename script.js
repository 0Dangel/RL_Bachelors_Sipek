
function onSocketOpen() {
    console.log("WS client: Websocket opened.")
}

function onBodyLoad() {
    ws = new WebSocket('ws://localhost:8080/websocket');     // ws is a global variable (index.html)
    ws.onopen = onSocketOpen;
    ws.onmessage = onSocketMessage;
    ws.onclose = onSocketClose;
    document.write('<head><script src = "./js/bootstrap.js"> </script>     <link rel="stylesheet" href="./css/bootstrap.css">    <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1">   <meta name="description" content="">   <script src="script.js" type="text/javascript"></script> </head>');
    document.write(" <div  class = 'container' style='font-size:3px' id = 'textOutput'>  </div> ");
    //setInterval(fn60sec, 120 * 1000);
    textOut=document.getElementById("textOutput");

}


function onSocketMessage(message) {
    console.log("WS message: ", message)
    textOut.innerHTML = ""
    //here goes visualisation
    try {JSON.parse(message.data).forEach(element => {
        textOut.innerHTML += "<div>  </div>"+element+"<br>"
    })}
    catch (e){
        console.log("onSocketMessage Error" + e)
    }
}


function getMessage(data){
	if(!data.hasOwnProperty("message"))
	{ return 'x'}
	return +data["name"]


}

function onSocketClose() {
    console.log("WS client: Websocket closed.")
    ws = new WebSocket('ws://localhost:8080/websocket'); 
    ws.onopen = onSocketOpen;
    ws.onmessage = onSocketMessage;
    ws.onclose = onSocketClose;
}