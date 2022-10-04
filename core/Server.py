import asyncio
import socketio

from aiohttp import web

from core.Channel import Channel
from core.Connection import Connection



CONNECTIONS: list[Connection] = []



def load_events(io: socketio.AsyncServer) -> socketio.AsyncServer:


    @io.event
    def connect(sid, data):
        if hasattr(data, '_size'):
            print(data)
        print(f'[CONNECTION STARTED WITH]: {sid}')

    @io.event
    async def client_connect(sid, data):
        if hasattr(data, '_size'):
            print(data)
        print(f'[CONNECTION REQUESTED BY CLIENT]: {sid}')
        if any(c.sid == sid for c in CONNECTIONS):
            await io.emit(event='server_refuse', data={'data': False}, to=sid)
        else:
            await io.emit(event='server_accept', data={'data': sid}, to=sid)

    @io.event
    def client_accept(sid, data):
        if data is not None:
            print(f'[CONNECTION ACCEPTED BY SERVER WITH]: {sid}')
            CONNECTIONS.append(
                Connection(
                    sid=sid,
                    channel=Channel(data, sid[0:16])
                ))

    @io.event
    def disconnect(data):
        if data is not None:
            msg = f'[DISCONNECTED]: {data}'
            conn: Connection = Connection.load(CONNECTIONS, sid=data)
            conn.task.cancel(msg=msg)
            CONNECTIONS.remove(conn)
            print(msg)


    return io



async def loop(io: socketio.AsyncServer):

    app = web.Application()
    io.attach(app)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner=runner, host='127.0.0.1', port=3333)
    await site.start()

    while True:
        for conn in CONNECTIONS:
            if not conn.running:
                conn.task = asyncio.create_task(Connection.worker(io=io, connection=conn))
                conn.running = True
        await asyncio.sleep(0.0166666666666667)
