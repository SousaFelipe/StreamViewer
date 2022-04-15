import asyncio

import cv2 as cv
import socketio
from aiohttp import web

from core.Connections import Connections


class Server(object):

    def __init__(self):
        self.connection_manager = None
        self.io = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
        self.webapp = web.Application()

    async def loop(self):
        runner = web.AppRunner(self.webapp)
        await runner.setup()

        site = web.TCPSite(runner=runner, host='127.0.0.1', port=8888)
        await site.start()

        while True:

            if self.connection_manager.is_not_empty():
                for conn in connections:
                    if not conn['running']:
                        conn['running'] = True
                        conn['task'] = asyncio.create_task(handle_connection(conn))
                        print(f"[USER]: {conn['id']} running...")
            await asyncio.sleep(1)
        pass

    def boot(self, connection_manager: Connections):
        self.connection_manager = connection_manager
        self.io.attach(self.webapp)
        pass

    def run(self):
        asyncio.run(self.loop())
