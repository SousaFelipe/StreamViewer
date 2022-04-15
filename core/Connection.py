import asyncio
import socketio

import cv2 as cv

from core.Channel import Channel


class Connection(object):


    def __init__(self, sid, channel: Channel):
        self.sid = sid
        self.channel = channel
        self.task = None
        self.running = False


    @staticmethod
    async def worker(io: socketio.AsyncServer, connection):

        ch: Channel = connection.channel
        video: cv.VideoCapture = ch.video(channel=3)

        if video.isOpened():
            while True:
                (ok, frame) = video.read()
                if ok:
                    (_, image) = cv.imencode('.jpg', frame)
                    await io.emit(event='image', data={'image': image.tobytes()}, to=connection.sid)
                    await asyncio.sleep(0.01666)
                else:
                    print('Erro on read frame')
        else:
            print('Error on open connection with channel.')


    @staticmethod
    def load(connections, sid):
        for connection in connections:
            if connection.sid == sid:
                return connection
        return False
