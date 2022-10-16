import json
import socket

from app.http.request import Request



def get_raw_body(body: str | dict) -> str:
    if isinstance(body, str):
        raw_body = body
    else:
        raw_body = json.dumps(body)
    return raw_body



class Response(object):



    def __init__(self, req: Request):
        self.req: Request = req
        self.conn: socket = req.socket
        self.status_code: int = 200
        self.body: str | None = None
        self.payload: bytes = b''
        self.headers = {
            'Content-Type': 'text/plain; encoding=utf8',
            'Content-Length': 0,
            'Connection': 'keep-alive'
        }



    def raw(self, body: any = None) -> bytes:
        head_line = '{} {} {}'.format(self.req.proto, self.status_code, 'OK')
        header_line = ''.join('%s: %s\n' % (k, v) for k, v in self.headers.items())
        return '{}\r\n{}\r\n{}'.format(head_line, header_line, body).encode('UTF-8')



    def send(self, body: any = None):
        if body is None:
            raw_body = get_raw_body(self.body)
        else:
            raw_body = get_raw_body(body)
        self.headers['Content-Length'] = len(raw_body)
        self.conn.send(self.raw(body=raw_body))
        return self
