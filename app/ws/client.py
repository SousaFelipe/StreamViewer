import websockets

from core.Channel import Channel
from app.ws.connection import Connection



class Client(object):


    def __init__(self, socket: websockets.WebSocketServerProtocol):
        self.__socket = socket
        self.__channel = None
        self.__connection = Connection()


    def uuid(self):
        return self.__socket.id


    def get_socket(self) -> websockets.WebSocketServerProtocol:
        return self.__socket


    def get_connection(self) -> Connection:
        return self.__connection


    def set_channel(self, ch: Channel) -> None:
        self.__channel = ch


    def get_channel(self) -> Channel:
        return self.__channel


    def has_channel(self) -> bool:
        return self.__channel is not None


