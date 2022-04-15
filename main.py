import asyncio
import socketio

from core.Server import loop, load_events


if __name__ == '__main__':

    sio = load_events(
        socketio.AsyncServer(
            async_mode='aiohttp',
            cors_allowed_origins='*',
        ))

    asyncio.run(loop(sio))

