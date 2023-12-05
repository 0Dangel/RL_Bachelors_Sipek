
function onSocketOpen() {
   
    mapRenderer=document.getElementById("map");
    console.log("WS client: Websocket opened.")

    ws.send(JSON.stringify({
        "loaded":"Notice me senpai ~UwU~",
        "refresh":true
    }))
}

function onBtnPress(){
    ws.send({
        command: 'BLS'
    })
}
var mapRenderer;

function makeSelectOption(input){
    return "<option value='"+input.toLowerCase()+"'>" + input + "</option>"
}

function onBodyLoad() {
    //document.write('<head><script src = "./js/bootstrap.js"> </script>     <link rel="stylesheet" href="./css/bootstrap.css">    <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1">   <meta name="description" content="">   <script src="script.js" type="text/javascript"></script> </head>');
    const body = document.querySelector("body");
    body.innerHTML = "";
    body.innerHTML += "<div  class = 'container' style='font-size:22px' id = 'map'>  </div>";
    body.innerHTML += "<div class= 'container' style = 'font-size:22px' id = 'controls'></div>";
    var controls = document.getElementById("controls"); 
    controls.innerHTML += "<label for = 'models'> Vyberte model: </label>"
    controls.innerHTML += "<select name='models' id='models'> </select>"
    var selector = document.getElementById("models");
    //selector.innerHTML += 

    //document.write(" <div  class = 'container' style='font-size:22px' id = 'textOutput'>  </div> ");
    //setInterval(fn60sec, 120 * 1000);
    mapRenderer=document.getElementById("map");

    ws = new WebSocket('ws://localhost:8080/websocket');     // ws is a global variable (index.html)
    ws.onopen = onSocketOpen;
    ws.onmessage = onSocketMessage;
    ws.onclose = onSocketClose;    

    //ws.send
}


function onSocketMessage(message) {
    console.log("WS message: ", message)
    //textOut.innerHTML = ""
    //here goes visualisation
    text = message.data;
    try {
        text = JSON.parse(text);
        // const {mapData} = text;
        // const h = text.hasOwnProperty("mapData");
        if(text?.["mapData"]){     
            text = text["mapData"]       
            arr=text["area"]
            index = 0
            for (i = 0; i < text["rows"] ; i++){
                for (j = 0; j < text["columns"]; j++){
                    elementQuery =""
                    if(arr[index] == 0){elementQuery = '<img src="imgs/asphalt.png" width="32" height="32"';}
                    else if (arr[index] == 1){elementQuery = '<img src="imgs/asphalt.png" width="8" height="32"' ;}
                    else if (arr[index] == 2){elementQuery = '<img src="imgs/wall.png" width="8" height="32"' ;}
                    else if (arr[index] == 4){elementQuery = '<img src="imgs/wall.png" width="32" height="32"' ;}
                    else if (arr[index] == 8){elementQuery = '<img src="imgs/hotel.png" width="32" height="32"' ;}
                    else {mapRenderer.innerHTML = "x"}
                    colorRot = 0+ ( text["targetPos"] == index ? 10:0 ) + (text["carPos"] == index ? 30:0 ) + (text["targetPos"] == index ? 60:0);

                    if(index == text["targetPos"] ||index == text["carPos"] || index == text["passengerPos"]) { elementQuery +=' style="filter:hue-rotate('+colorRot+' deg)"';}
                    else if (arr[index] == 8) {elementQuery +=' style="filter:grayscale(100%)"'}

                    elementQuery += ">";
                    mapRenderer.innerHTML += elementQuery
                    index +=1;
                }
                mapRenderer.innerHTML += "<br>"
            }    
        }
        else if(text?.["modelList"]){
            var selector = document.getElementById("models");
            selector.innerHTML = "";
            text["modelList"].forEach(element => {
                selector.innerHTML += makeSelectOption(element);
            });
        }                              
    }
    catch (e){
        console.log("onSocketMessage Error" + e)
        console.log("message.data = " + text)
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