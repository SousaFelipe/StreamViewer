import cv2 as cv

from core.Secret import decrypt



def decode_username(data: str, iv: str):
    dec = decrypt(data, iv)
    spl = dec.split('@')[0].split(':')
    return spl[0]


def decode_password(data: str, iv: str):
    dec = decrypt(data, iv)
    spl = dec.split('@')[0].split(':')
    return spl[1]


def decode_address(data: str, iv: str):
    dec = decrypt(data, iv)
    spl = dec.split('@')[1].split(':')
    return spl[0]


def decode_port(data: str, iv: str):
    dec = decrypt(data, iv)
    spl = dec.split('@')[1].split(':')
    return spl[1]


def decode_channel(data: str, iv: str):
    dec = decrypt(data, iv)
    spl = dec.split('@')[2]
    return spl



class Channel(object):


    def __init__(self, data: str, iv: str):
        self.username = decode_username(data, iv)
        self.password = decode_password(data, iv)
        self.address = decode_address(data, iv)
        self.port = decode_port(data, iv)
        self.channel = decode_channel(data, iv)


    def video(self, subtype: int = 0) -> cv.VideoCapture:
        url = 'rtsp://{}:{}@{}:{}/cam/realmonitor?channel={}&subtype={}' \
            .format(
                self.username,
                self.password,
                self.address,
                self.port,
                self.channel,
                subtype
            )
        return cv.VideoCapture(url)
