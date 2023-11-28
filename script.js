
function onSocketOpen() {
   
    textOut=document.getElementById("textOutput");
    console.log("WS client: Websocket opened.")
}

function onBodyLoad() {
    document.write('<head><script src = "./js/bootstrap.js"> </script>     <link rel="stylesheet" href="./css/bootstrap.css">    <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1">   <meta name="description" content="">   <script src="script.js" type="text/javascript"></script> </head>');
    document.write(" <div  class = 'container' style='font-size:22px' id = 'textOutput'>  </div> ");
    //setInterval(fn60sec, 120 * 1000);
    textOut=document.getElementById("textOutput");

    ws = new WebSocket('ws://localhost:8080/websocket');     // ws is a global variable (index.html)
    ws.onopen = onSocketOpen;
    ws.onmessage = onSocketMessage;
    ws.onclose = onSocketClose;
    

}


function onSocketMessage(message) {
    console.log("WS message: ", message)
    //textOut.innerHTML = ""
    //here goes visualisation
    try { 
        
        text = message.data;
        text = JSON.parse(text)
        //Passenger, Target, Car
        // positions=[]
        // text = text.replaceAll("\n","<br>");

        
        // text = text.replaceAll(" ",'<img src="imgs/asphalt.png" width="32" height="32">')

        // text = text.replaceAll(":",'<img src="imgs/asphalt.png" width="8" height="32" >')
        // //text = text.replaceAll(":",'<img src="imgs/asphalt.png" width="32" height="32">')
        // text = text.replaceAll("|",'<img src="imgs/wall.png" width="8" height="32" >')
        // text = text.replaceAll("+",'<img src="imgs/wall.png" width="8" height="32" >')
        // text = text.replaceAll("--",'<img src="imgs/wall.png" width="32" height="32" ><img src="imgs/wall.png" width="8" height="32" >')
        // text = text.replaceAll("-",'<img src="imgs/wall.png" width="32" height="32" >')


        // text = text.replaceAll("R",'<img src="imgs/hotel.png" width="32" height="32" style = "filter:grayscale(100%)">')
        // text = text.replaceAll("G",'<img src="imgs/hotel.png" width="32" height="32" style = "filter:grayscale(100%)">')
        // text = text.replaceAll("Y",'<img src="imgs/hotel.png" width="32" height="32" style = "filter:grayscale(100%)">')
        // text = text.replaceAll("B",'<img src="imgs/hotel.png" width="32" height="32" style = "filter:grayscale(100%)">')

        //text["rows"]

        arr=text["area"]
        //textOut.innerHTML += text["column"];


        //# Message: [rows,column, targetPos, carPos, passengerPos. [0 = ground, 1 = noWall, 2 = Wall, 4 = bigWall, 8 = Hotel (16 = car, 32 = passenger)], 
        //# 
        index = 0
        for (i = 0; i < text["rows"] ; i++){
            for (j = 0; j < text["columns"]; j++){
                elementQuery =""
                if(arr[index] == 0){elementQuery = '<img src="imgs/asphalt.png" width="32" height="32"';}
                else if (arr[index] == 1){elementQuery = '<img src="imgs/asphalt.png" width="8" height="32"' ;}
                else if (arr[index] == 2){elementQuery = '<img src="imgs/wall.png" width="8" height="32"' ;}
                else if (arr[index] == 4){elementQuery = '<img src="imgs/wall.png" width="32" height="32"' ;}
                else if (arr[index] == 8){elementQuery = '<img src="imgs/hotel.png" width="32" height="32"' ;}
                else {textOut.innerHTML = "x"}
                colorRot = 0+ ( text["targetPos"] == index ? 10:0 ) + (text["carPos"] == index ? 30:0 ) + (text["targetPos"] == index ? 60:0);

                if(index == text["targetPos"] ||index == text["carPos"] || index == text["passengerPos"]) { elementQuery +=' style="filter:hue-rotate('+colorRot+'deg)"';}
                else if (arr[index] == 8) {elementQuery +=' style="filter:grayscale(100%)"'}
                
                

                elementQuery += ">";
                textOut.innerHTML += elementQuery
                index +=1;
            }
            textOut.innerHTML += "<br>"
        }
    }
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