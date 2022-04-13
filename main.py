import base64
import socketio
import asyncio
import threading

import cv2 as cv

from time import sleep
from aiohttp import web


sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


connections = []


@sio.event
async def connect(sid, environ):
    await sio.emit(event='server_connect', data={'data': sid}, to=sid)


@sio.event
async def client_accept(sid, data):
    global connections

    conn = {
        'id': sid,
        'device': data,
        'task': None,
        'running': False
    }

    conn['task'] = threading.Thread(target=handle_connection, args=(conn,))

    connections.append(conn)

    await sio.emit(event='server_accept', data={'data': sid}, to=sid)


async def handle_connection(connection):

    device = connection['device']
    wCap = cv.VideoCapture(f"rtsp://{device}/cam/realmonitor?channel=1&subtype=0")

    while True:
        frame = wCap.read()
        encodedimg = base64.b64encode(frame[1])[1]
        await sio.emit(event='image', data={'data': encodedimg}, to=connection['id'])
        await asyncio.sleep(1/24)


async def main():
    global connections

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner=runner, host='127.0.0.1', port=8888)
    await site.start()

    while True:
        if len(connections) > 0:
            for conn in connections:
                if not conn['running']:
                    conn['running'] = True
                    conn['task'].run()


if __name__ == '__main__':
    # web.run_app(app=app, host='127.0.0.1', port=8888, loop=main())
    asyncio.run(main())

