import asyncio
import socketio

from core.Server import loop, load_events
from app.http import server as http_server
from app.ws import server as ws_server



def start_sockeio_server():

    sio = load_events(
        socketio.AsyncServer(
            async_mode='aiohttp',
            cors_allowed_origins='*',
        ))

    asyncio.run(loop(sio))



def start_raw_server():
    http_server.run(host='192.168.2.143', port=6666)



def start_websockets():
    asyncio.run(ws_server.run())



if __name__ == '__main__':
    # start_sockeio_server()
    # start_raw_server()
    start_websockets()
