import pickle
import argparse
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", default=1)
args = parser.parse_args()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        mes = input('Your message: ')

        data = pickle.dumps({'text': mes, 'sender': args.name})
        # print('my data', pickle.loads(data))
        s.sendall(data)
        data = s.recv(1024)
        new_data = pickle.loads(data)

        print(repr(f"{new_data['sender']}: {new_data['text']};"))
