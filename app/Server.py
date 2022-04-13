import base64
import threading
import socketio
import cv2 as cv


sio = socketio.AsyncServer()
app = socketio.WSGIApp(sio)


@sio.event
def image(sid, data):
    print(sid, f'image: {data}')


class Server(threading.Thread):

    def __init__(self, name, device_id):
        threading.Thread.__init__(self)
        self.name = name
        self.device_id = device_id

    def run(self):
        print(f'Starting... {self.name}')

        channel = cv.VideoCapture(self.device_id)

        if channel.isOpened():
            frame = channel.read()
            encodedimg = base64.encode(frame[1])

        sio.emit('image', {'data': encodedimg})


