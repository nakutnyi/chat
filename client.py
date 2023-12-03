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
        data = s.recv(1024)
        new_data = pickle.loads(data)

        print(repr(f"{new_data['sender']}: {new_data['text']};"))
