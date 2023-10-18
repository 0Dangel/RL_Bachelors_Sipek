
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


tornado.ioloop.IOLoop.configure("tornado.platform.asyncio.AsyncIOLoop")
io_loop = tornado.ioloop.IOLoop.current()
asyncio.set_event_loop(io_loop.asyncio_loop)

#ws_clients = []


class WebServer(tornado.web.Application):
   
    iol = IOLoop.current()
    tohle = ""
    ws_clients = []
    
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
                
    def send_ws_message(self, message):
        for client in self.ws_clients:
            iol.spawn_callback(client.write_message, message)


        #print(len(self.ws_clients))


class AuthHandler():
    def on_message(self,msg):
        print(msg)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("main.html")

class WSHandler(WebSocketHandler):

    def initialize(self, app):
        self.app = app
        self.app.ws_clients.append(self)

    def open(self):
        print('Webserver: Websocket opened.')
        self.write_message('Server ready.')

    def on_message(self, msg):
        print('Webserver: Received WS message:', msg)

    def on_close(self):
        self.application.ws_clients.remove(self)
        print('Webserver: Websocket client closed. Connected clients:', len(self.application.ws_clients))

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
  
 
    iol = IOLoop.current()
    iol.start()


    print("Err: How did I get here?!")
    t.join()