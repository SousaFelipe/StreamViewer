import asyncio
import socketio

from aiohttp import web

from core.Channel import Channel
from core.Connection import Connection


CONNECTIONS = []


def load_events(io: socketio.AsyncServer) -> socketio.AsyncServer:

    @io.event
    def connect(sid, data):
        print(f'[CONNECTED]: {sid}')

    @io.event
    def disconnect(data):
        if data is not None:
            msg = f'[DISCONNECTED]: {data}'
            conn: Connection = Connection.load(CONNECTIONS, sid=data)
            conn.task.cancel(msg=msg)
            CONNECTIONS.remove(conn)
            print(msg)

    @io.event
    async def client_accept(sid, data):
        if data is not None:
            CONNECTIONS.append(
                Connection(
                    sid=sid,
                    channel=Channel(data)
                ))
            await io.emit(event='server_accept', data={'data': sid}, to=sid)

    return io


async def loop(io: socketio.AsyncServer):

    app = web.Application()
    io.attach(app)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner=runner, host='127.0.0.1', port=8888)
    await site.start()

    while True:
        for conn in CONNECTIONS:
            if not conn.running:
                conn.task = asyncio.create_task(Connection.worker(io=io, connection=conn))
                conn.running = True
        await asyncio.sleep(0.001)
