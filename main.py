import asyncio

import cv2 as cv
import socketio
from aiohttp import web


sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()


connections = []


@sio.event
async def connect(sid, data):
    if hasattr(data, '_size'):
        print(f'[CONNECTED]: {sid} - {data}')
    else:
        print(f'[CONNECTED]: {sid}')


@sio.event
def disconnect(data):
    msg = f'[DISCONNECTED]: => {data}'
    if data is not None:
        global connections
        for conn in connections:
            if conn['id'] == data:
                conn['task'].cancel(msg=msg)
                connections.remove(conn)
                break
        print(msg)
    else:
        print(f'[DISCONNECTED]: => None')


@sio.event
async def client_accept(sid, data):
    device = cv.VideoCapture(f"rtsp://{data}:554/cam/realmonitor?channel=3&subtype=0")
    global connections
    connections.append({
        'id': sid,
        'device': device,
        'task': None,
        'running': False
    })
    await sio.emit(event='server_accept', data={'data': sid}, to=sid)


async def handle_connection(conn):
    device: cv.VideoCapture = conn['device']
    if device.isOpened():
        while True:
            (frame_ok, frame) = device.read()
            if frame_ok:
                (_, image) = cv.imencode('.jpg', frame)
                await sio.emit(event='image', data={'image': image.tobytes()}, to=conn['id'])
                await asyncio.sleep(0.01666)
            else:
                print('Error on open connection with device.')
                await sio.emit(event='error', data={'data': 'Error on open connection with device.'})


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
                    print(f"[USER]: { conn['id'] } running...")
        await asyncio.sleep(1)


if __name__ == '__main__':
    sio.attach(app)
    asyncio.run(main())
