import pickle
import argparse
import socket
import getpass


HOST = '18.184.170.176'  # The server's hostname or IP address
PORT = 443        # The port used by the server
USERNAME = getpass.getuser()


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", default=USERNAME)
args = parser.parse_args()


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        mes = input('Your message: ')

        data = pickle.dumps({'text': mes, 'sender': args.name})
        s.sendall(data)
        messages = pickle.loads(s.recv(1024))

        for message in messages:
            print(repr(f"{message['sender']}: {message['text']};"))
