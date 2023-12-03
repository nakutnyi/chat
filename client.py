import pickle
import argparse
import getpass
import socket
import time
import threading


HOST = '18.184.170.176'  # The server's hostname or IP address
PORT = 443        # The port used by the server
# HOST = "127.0.0.1"
# PORT = 4321
USERNAME = getpass.getuser()


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", default=USERNAME)
args = parser.parse_args()


def make_message(msg="", sender="", is_service=False):
    return {"msg": msg, "sender": sender, "is_service": is_service}


def picker():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            data = pickle.dumps(make_message(
                is_service=True,
                msg="get_update",
                sender=args.name,
            ))
            sock.sendall(data)
            time.sleep(1)
            messages = pickle.loads(sock.recv(1024))

            for message in messages:
                print(repr(f"{message['sender']}: {message['msg']};"))
        time.sleep(2)


def pusher():
    while True:
        msg = input()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            data = pickle.dumps(make_message(msg=msg, sender=args.name))
            sock.sendall(data)


if __name__ == "__main__":
    picker_thread = threading.Thread(target=picker)
    pusher_thread = threading.Thread(target=pusher)

    picker_thread.start()
    pusher_thread.start()
