import base64
import socketio
import asyncio
import threading
import concurrent.futures

import cv2 as cv

from aiohttp import web


sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


connections = []


@sio.event
async def connect(sid, environ):
    print(f'[CONNECTED]: { sid }')
    await sio.emit(event='server_connect', data={'data': sid}, to=sid)


@sio.event
async def client_accept(sid, data):
    print(f'[ACCEPTED]: { sid }')
    global connections
    connections.append({
        'id': sid,
        'device': data,
        'running': False
    })
    await sio.emit(event='server_accept', data={'data': sid}, to=sid)


def handle_connection(conn):
    device = conn['device']
    stream = cv.VideoCapture(f"rtsp://{device}/cam/realmonitor?channel=1&subtype=0")

    while True:
        frame = stream.read()
        encodedimg = base64.b64encode(frame[1])[1]
        sio.emit(event='image', data={'data': encodedimg}, to=conn['id'])
        asyncio.sleep(1/24)


async def main():
    global connections

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner=runner, host='127.0.0.1', port=8888)
    await site.start()

    while True:
        count_connections = len(connections)

        if count_connections > 0:
            loop = asyncio.get_running_loop()
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=count_connections+1)

            for conn in connections:
                if not conn['running']:
                    conn['running'] = True
                    asyncio.ensure_future(loop.run_in_executor(executor, handle_connection, conn))

        await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())
