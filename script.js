
function onSocketOpen() {
   
    mapRenderer=document.getElementById("map");
    console.log("WS client: Websocket opened.")

    ws.send(JSON.stringify({
        "loaded":"Notice me senpai ~UwU~",
        "refresh":true
    }))
}

function requestModelAndState(){
    console.log( document.getElementById("startState").value);
    ws.send(JSON.stringify({
        "command": {
            "model": document.getElementById("models").value,
            "state": document.getElementById("startState").value
        }
    }))
}
var mapRenderer;

function makeSelectOption(input){
    return "<option value='"+input.toLowerCase()+"'>" + input + "</option>"
}

function onBodyLoad() {
    //document.write('<head><script src = "./js/bootstrap.js"> </script>     <link rel="stylesheet" href="./css/bootstrap.css">    <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1">   <meta name="description" content="">   <script src="script.js" type="text/javascript"></script> </head>');
    const body = document.querySelector("body");
    body.innerHTML = "";
    body.innerHTML += "<div class= 'container' style = 'font-size:22px' id = 'controls'></div>";
    var controls = document.getElementById("controls"); 
    controls.innerHTML += "<label for = 'models'> Vyberte model: </label>";
    controls.innerHTML += "<select name='models' id='models'> </select> <br>";
    
    controls.innerHTML += "<label for = 'startState'> Počáteční stav: </label>";
    controls.innerHTML += '<input type="text" id="startState" name="startState" value="0">';
    controls.innerHTML += "<button onclick='requestModelAndState()' type='button'>Načti model</button>";
    //var selector = document.getElementById("models");
    //selector.innerHTML += 

    body.innerHTML += "<div  class = 'container' style='font-size:22px' id = 'map'>  </div>";

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
            mapRenderer=document.getElementById("map");
            mapRenderer.innerHTML = "";
            text = text["mapData"];
            //console.log(text)     
            arr=text["area"]
            //console.log(arr[102]);
            index = 0
            for (i = 0; i < text["rows"] ; i++){
                for (j = 0; j < text["columns"]; j++){
                    elementQuery =""
                    if(arr[index] == 0){elementQuery = '<img src="imgs/asphalt.png" class = "block" ';}
                    else if (arr[index] == 1){elementQuery = '<img src="imgs/asphalt.png" class = "vypln" ' ;}
                    else if (arr[index] == 2){elementQuery = '<img src="imgs/wall.png" class = "vypln" ' ;}
                    else if (arr[index] == 4){elementQuery = '<img src="imgs/wall.png" class = "block" ' ;}
                    else if (arr[index] == 8){elementQuery = '<img src="imgs/hotel.png" class = "block" ' ;}
                    else {elementQuery = "x"}
                    colorRot = 0x000000 | ( text["targetPos"] == index ? 0x0000FF:0 ) | (text["carPos"] == index ? 0xFFFF00:0 ) ^ (text["passengerPos"] == index ? 0xFF0000:0);
                    //console.log(colorRot)
                    if( text["targetPos"] == index ||text["carPos"] == index|| text["passengerPos"] == index ) { elementQuery +='style=" border: 5px solid #'+intToRGB(colorRot)+'; border-radius: 4px;"';
                        console.log(elementQuery)}
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
function hashCode(str) { // java String#hashCode
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
} 

function intToRGB(i){
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
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