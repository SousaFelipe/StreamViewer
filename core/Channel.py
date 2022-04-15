import cv2 as cv


def decode_username(data: str):
    spl = data.split('@')[0].split(':')
    return spl[0]


def decode_password(data: str):
    spl = data.split('@')[0].split(':')
    return spl[1]


def decode_address(data: str):
    spl = data.split('@')[1].split(':')
    return spl[0]


def decode_port(data: str):
    spl = data.split('@')[1].split(':')
    return spl[1]


class Channel(object):


    def __init__(self, data: str):
        self.username = decode_username(data)
        self.password = decode_password(data)
        self.address = decode_address(data)
        self.port = decode_port(data)


    def video(self, channel: int = 1, subtype: int = 0) -> cv.VideoCapture:
        url = 'rtsp://{}:{}@{}:{}/cam/realmonitor?channel={}&subtype={}'\
            .format(
                self.username,
                self.password,
                self.address,
                self.port,
                channel,
                subtype)
        return cv.VideoCapture(url)
