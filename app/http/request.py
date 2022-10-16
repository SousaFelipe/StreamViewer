import socket



def normalize_line_endings(b: bytes) -> str:
    r"""Converte string contendo várias terminações de linha como \n, \r or \r\n,
    para uniform \n."""
    s = b.decode('UTF-8')
    return ''.join((line + '\n') for line in s.splitlines())



class Request(object):


    def __init__(self, conn: socket):
        self.socket = conn

        request = normalize_line_endings(conn.recv(4096))
        head, body = request.split('\n\n', 1)

        request_head = head.splitlines()
        request_head_line = request_head[0]
        request_method, request_uri, request_proto = request_head_line.split(' ', 3)

        self.method = request_method
        self.uri = request_uri
        self.proto = request_proto
        self.headers = dict(x.split(': ', 1) for x in request_head[1:])
        self.key = self.headers['Sec-WebSocket-Key']
        self.body = body



    def verb(self):
        print('\n')
        for key, value in self.headers.items():
            print('{}: {}'.format(key, value))
