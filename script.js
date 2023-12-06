
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
var oldStates = [0,0,0];

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
        jsonTxt = JSON.parse(text);
        // const {mapData} = text;
        // const h = text.hasOwnProperty("mapData");
        if(jsonTxt?.["mapData"]){     
            mapRenderer=document.getElementById("map");
            mapRenderer.innerHTML = "";
            text = jsonTxt["mapData"];
            //console.log(text)     
            arr=text["area"]
            //console.log(arr[102]);
            index = 0
            oldStates[0] = text["targetPos"];
            oldStates[1] = text["carPos"];
            oldStates[2] = text["passengerPos"];
            for (i = 0; i < text["rows"] ; i++){
                for (j = 0; j < text["columns"]; j++){
                    elementQuery =""
                    if((arr[index] & 4) > 0){elementQuery = '<img src="imgs/asphalt.png" class = "block" ';}
                    else if (arr[index] == 1){elementQuery = '<img src="imgs/asphalt.png" class = "vypln" ' ;}
                    else if (arr[index] == 2){elementQuery = '<img src="imgs/wall.png" class = "vypln" ' ;}
                    else if (arr[index] == 3){elementQuery = '<img src="imgs/wall.png" class = "block" ' ;}
                    else if ((arr[index] & 8) > 0){elementQuery = '<img src="imgs/hotel.png" class = "block" ' ;}
                    else {elementQuery = "x"}

                    elementQuery+=" id='"+index+"'"

                    //TODO: Rewrite back to use "normal" indexes of positions 
                    colorRot = 0x000000 | ( (arr[index] & 64) > 0 ? 0x0000FF:0x0 ) | ((arr[index] & 16) > 0 ? 0xFFFF00:0x0 ) ^ ((arr[index] & 32) > 0 ? 0xFF0000:0x0);
                    //console.log(colorRot)
                    //if((arr[index] & 0b11110000) > 0) { elementQuery +='style=" border: 5px solid #'+intToRGB(colorRot)+'; border-radius: 4px;"';
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
        if(jsonTxt?.["modelList"]){
            var selector = document.getElementById("models");
            selector.innerHTML = "";
            jsonTxt["modelList"].forEach(element => {
                selector.innerHTML += makeSelectOption(element);
            });
        }
        if(jsonTxt?.["states"]){
            oldStates.forEach(element => {
                byId = document.getElementById(element);
                byId.style.removeProperty("border");
                if(byId.src.includes("hotel")){
                    byId.style.filter = "grayscale(100%)";
                }
            });
            var selector = document.getElementById("models");
            selector.innerHTML = "";
            console.log(jsonTxt)
            x = jsonTxt["states"]
            count = 0;
            colors= {}
            Object.keys(x).forEach(element => {


                byId = document.getElementById(x[element]);
                byId.style.removeProperty("border");
                if(byId.src.includes("hotel")){
                    byId.style.filter = "";
                }
                oldStates[count] = x[element];
                count ++;
                console.log(colors)
                if(!colors?.[x[element]]){colors[x[element]] = 0x000000}

                if(element=="targetPos"){colors[x[element]] |= 0x0000FF}
                else if(element=="passengerPos"){colors[x[element]] |= 0xFFFF00}
                
                else if(element=="carPos"){colors[x[element]] ^= 0xFF0000}
                //console.log(""+x[element]);
                //console.log(document.getElementById(""+x[element]));
                //selector.innerHTML += makeSelectOption(element);
            });

            Object.keys(colors).forEach(element => {
                document.getElementById(element).style.border = '5px solid';
                document.getElementById(element).style.borderColor =  '#'+intToRGB(colors[element])
                document.getElementById(element).style.borderRadius = '4px;';
                console.log(element);
                console.log(colors[element]) ;               
            });
            console.log(oldStates);
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