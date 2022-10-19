import asyncio
import json
import logging
import websockets

from app.ws.client import Client
from app.ws.connection import Connection
from core.Channel import Channel



# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("asyncio").setLevel(logging.WARNING)



CLIENTS: list[Client] = []



async def await_connections(wssp: websockets.WebSocketServerProtocol):

    while True:

        try:
            client = Client(wssp)
            data = await client.get_socket().recv()
            load = json.loads(data)

            if 'event' in load:

                if load['event'] == 'connect':
                    if not [c.uuid() == wssp.id for c in CLIENTS]:
                        event = {'event': 'uuid', 'uuid': client.uuid().hex}
                        await client.get_socket().send(json.dumps(event))
                        CLIENTS.append(client)

                if load['event'] == 'stream':
                    for client in CLIENTS:
                        if load['uuid'] == client.uuid().hex and client.get_connection().unplugged():
                            channel = Channel(load['data'], client.uuid().hex[:16])
                            client.set_channel(channel)
                            client.get_connection().set_task(asyncio.create_task(coro=Connection.worker(client)))

        except websockets.ConnectionClosedOK as e:
            print(e)
            break

        await asyncio.sleep(0)



async def run():
    async with websockets.serve(ws_handler=await_connections, host='192.168.2.143', port=6666):
        await asyncio.Future()
