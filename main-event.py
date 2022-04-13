import base64

import cv2
import socketio
import asyncio

import cv2 as cv

from aiohttp import web


sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


connections = []


@sio.event
async def connect(sid, data):
    print(f'[CONNECTED]: {sid}')
    await sio.emit(event='server_connect', data={'data': sid}, to=sid)


@sio.event
async def disconnect(sid, data):
    global connections
    connections.remove(__value={'id': sid,})


@sio.event
async def client_accept(sid, data):
    device = cv.VideoCapture(f"rtsp://{data}/cam/realmonitor?channel=1&subtype=0")
    global connections
    connections.append({
        'id': sid,
        'device': device,
        'task': None,
        'running': False
    })
    await sio.emit(event='server_accept', data={'data': sid}, to=sid)


async def handle_connection(conn):
    device: cv2.VideoCapture = conn['device']
    if device.isOpened():
        while True:
            (success, frame) = device.read()
            encodedimg = base64.b64encode(frame)
            await sio.emit(event='image', data={'image': encodedimg}, to=conn['id'])
            await asyncio.sleep(2)


async def main():
    global connections

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner=runner, host='127.0.0.1', port=8888)
    await site.start()

    while True:
        count_connections = len(connections)
        if count_connections > 0:
            for conn in connections:
                if not conn['running']:
                    conn['running'] = True
                    conn['task'] = asyncio.create_task(handle_connection(conn))
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
