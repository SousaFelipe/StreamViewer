import socket
import threading
import time

SERVER_ADDR = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5050
SERVER_HOST = (SERVER_ADDR, SERVER_PORT)
SERVER_FORM = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)

connections = []
mssgs_queue = []


def send_message_to(conn):
    pass


def broadcast_message():
    pass


def handle_clients(conn, addr):
    print(f'[CONNECTION] => Client: {addr}')

    global connections

    while True:
        msg: str = conn.recv(2048).decode(SERVER_FORM)
        if msg and msg.startswith('token='):
            connections.append({
                'token': msg.split('=')[1],
                'connection': conn,
                'ipaddress': addr
            })


def start():
    print('[SERVER] => Starting...')
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()
