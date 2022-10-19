import asyncio
import base64
import json

import cv2 as cv



class Connection(object):


    def __init__(self):
        self.__task = None
        self.__plugged = False


    def set_task(self, task) -> None:
        self.__task = task
        self.__plugged = True


    def unplugged(self) -> bool:
        return not self.__plugged


    @staticmethod
    async def worker(client):

        channel = client.get_channel()
        socket = client.get_socket()
        video: cv.VideoCapture = channel.video()

        if video.isOpened():
            while True:

                try:
                    (ok, frame) = video.read()
                    if ok:
                        (_, image) = cv.imencode('.jpg', frame)
                        event = {'event': 'image', 'image': base64.b64encode(image.tobytes()).decode('utf-8')}
                        await socket.send(json.dumps(event))
                    else:
                        print('Erro on read frame')
                    await asyncio.sleep(0)

                except Exception as e:
                    print(e)
        else:
            print('Error on open connection with channel.')
