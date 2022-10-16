import asyncio
import socketio

from core.Server import loop, load_events
from app.http import server



def start_sockeio_server():

    sio = load_events(
        socketio.AsyncServer(
            async_mode='aiohttp',
            cors_allowed_origins='*',
        ))

    asyncio.run(loop(sio))



def start_raw_server():
    server.run(host='192.168.2.143', port=1010)



if __name__ == '__main__':
    # start_sockeio_server()
    start_raw_server()


