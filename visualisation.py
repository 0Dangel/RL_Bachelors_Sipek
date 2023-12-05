
import tornado.ioloop
import tornado.web
import asyncio
from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler
import socket, time
from os import path
from os.path import dirname
from async_timeout import asyncio
from tornado.ioloop import IOLoop
import tornado
import os
from threading import Thread
import tornado.escape as esc
import json


tornado.ioloop.IOLoop.configure("tornado.platform.asyncio.AsyncIOLoop")
io_loop = tornado.ioloop.IOLoop.current()
asyncio.set_event_loop(io_loop.asyncio_loop)

#ws_clients = []

#Creates a basic WebServer
class WebServer(tornado.web.Application):
   
    iol = IOLoop.current()
    tohle = ""
    ws_clients = []
    
    #Init it, som static handlers for files like .js and html
    #WSocket handler for WebSocket
    def __init__(self):
        
        global tohle
        tohle = self
        handlers = [
             (r"/", MainHandler),
             (r"/websocket",WSHandler,{"app":self}),
             (r'/(.*)', StaticFileHandler, {'path': dirname(__file__)})
             ]
        settings = {'debug':True}
        self.listen(8080)
        tornado.web.Application.__init__(self,handlers, **settings)
                
    #Function for sending a message over WebSocket
    def send_ws_message(self, message):
        for client in self.ws_clients:
            iol.spawn_callback(client.write_message, message)


        #print(len(self.ws_clients))


class AuthHandler():
    def on_message(self,msg):
        print(msg)

#Main file
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("main.html")

def makeMessage(message):
    splitted = message.split("\n")
    finalMsg = {}
    PlayArea = []
    alternatingBool = False
    rows = 0
    columns = 0
    #For every row in input sequence:
    for x in splitted:
        #This is just because of dashes at the top and botom - it has to intertwine a large wall with a small one for correct looks
        alternatingBool = False
        #Counting number of rows and columns - yes, as of now map is considered a long text seaquence
        rows += 1
        columns = 0
        #For ever char in the current line:
        for i in x:
            #Add a 1 to column counter 
            columns += 1
            #Conversion of chars into their numbered counterparts - i used binary progressing numbers - 1, 2, 4, 8 etc... 
            # this way it's possible to expand in the future
            if(i == " "):
                PlayArea.append(0)
            elif(i == ":"):
                PlayArea.append(1)
            elif(i == "|" or i =="+"):
                PlayArea.append(2)
            elif(i == "-"):
                #Yeee... the upper and lower parts... hate them, but it works
                if(alternatingBool):
                    alternatingBool = False
                    PlayArea.append(2)
                else:
                    alternatingBool = True
                    PlayArea.append(4)
            else:
                PlayArea.append(8)

        #print(1)

    #These numbers will be changed based on the current enviroment - targets to be seen, indexes based on "id = row*columns + column" equation
    finalMsg["targetPos"]=25
    finalMsg["passengerPos"]=12
    finalMsg["carPos"]=14

    #Add the map and stats
    finalMsg["area"] = PlayArea
    finalMsg["rows"] = rows
    finalMsg["columns"] = columns

    return {"mapData":finalMsg}


#All about Websocket
class WSHandler(WebSocketHandler):

    #Innit a connection
    def initialize(self, app):
        self.app = app
        self.app.ws_clients.append(self)

    #After opening a session, send this message:
    def open(self):
        #print('Webserver: Websocket opened.')
        # Message: [Rows, TargetPos, CarPos, [0 = ground, 1 = noWall, 2 = Wall, 4 = bigWall, 8 = Hotel (16 = car, 32 = passenger)], 
        # 
        # ]

        #Proof of concept - Character-based map in long string
        message  = "+---------+\n"+"|R: | : :G|\n"+"| : | : : |\n"+"| : : : : |\n"+"| | : | : |\n"+"|Y| : |B: |\n"+"+---------+"

        #Semi-Automatic conversion for all possible sizes
        
        #Send the message, encode it as Json - pbbly unnecesary
        self.write_message("test")

    #Ready handler for future control - e.g. changing the running version - BFS, DFS etc.
    def on_message(self, msg):
        modelsList = ["model", "model2", "model3"]
        print(msg)
        #return
        js = esc.json_decode(msg)
        #Needs to process the message
        if("loaded" in js):
            #self.app.ws_clients("")
            self.write_message(esc.json_encode({"modelList":modelsList}))
        elif(msg):
            self.write_message(esc.json_encode(makeMessage(msg)))
        print('Webserver: Received WS message:', msg)
        #If the message has propper format, go and render on client:
        

    #It's good to say goodbye at the end of transmissions!
    def on_close(self):
        self.application.ws_clients.remove(self)
        print('Webserver: Websocket client closed. Connected clients:', len(self.application.ws_clients))

#And start the server as asynchronous cycle 
def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    ws.run()

#worker.broadcast = Broadcast
 
if __name__ == "__main__":
    print(str(os.getcwd()))
    ws = WebServer()
    #t = Thread(target = start_server,args=())
    #t.start()
    settingFile = ""

    ##Zde přijde volání daného typu algoritmu, či nejlépe nějakého ovládacího scriptu
    # t = Thread(target=reader.main_function,daemon=True)
    # t.start()
  
 
 #START THE LOOOOOOOOOOOOOP:
    iol = IOLoop.current()
    iol.start()

#This should never happen:
    print("Err: How did I get here?!")
    #t.join()