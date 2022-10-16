import threading
from socket import *

from app.http.request import Request
from app.http.response import Response



connections: list[str] = []
chunks: list[any] = []



def keep_alive(conn: socket, addr: any):
    host, port = addr

    print(f'\n[0]>> Client connected with: [{ host }:{ port }]\n')

    with conn:
        while True:
            try:
                data = conn.recv(4096).decode('UTF-8')
                if not data:
                    break
                chunks.append(data)
            except Exception as e:
                print('[1]>> {}'.format(e))
        print(f"\n[0]>> Client [{host}:{port}] disconnected")



def loop(host: str, port: int):

    with socket(AF_INET, SOCK_STREAM, IPPROTO_TCP) as service:

        service.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        service.bind((host, port))
        service.listen(1)

        while True:
            try:
                conn, addr = service.accept()
                t_alive = threading.Thread(target=keep_alive, args=(conn, addr))
                t_alive.start()
            except Exception as e:
                print(e)
                break



def run(host: str = '127.0.0.1', port: int = 8080):
    t_loop = threading.Thread(target=loop, args=(host, port))
    t_loop.start()
    pass
