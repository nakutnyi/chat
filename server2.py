import pickle
import socket
from threading import Thread

def on_new_client(client):
    print('on_new_client')
    while True:
        data = client.recv(1024)
        if data:
            print(pickle.loads(data))
            client.sendall(data)
    # client.close()

def serverRunner(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f'host: {HOST}, port {PORT}')

    while True:
        client, address = server.accept()
        print(f'Success, client: {address}')
        # Receive the data in small chunks and retransmit it
        Thread(target=on_new_client, args=client)
    server.close()


if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 65432
    serverRunner(HOST, PORT)
