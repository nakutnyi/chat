import pickle
import argparse
import getpass
import time
import threading


HOST = '18.184.170.176'  # The server's hostname or IP address
PORT = 443        # The port used by the server
USERNAME = getpass.getuser()


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", default=USERNAME)
args = parser.parse_args()


def make_message(msg="", sender="", is_service=False):
    return {"msg": msg, "sender": sender, "service": is_service}


def picker():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
            socket.connect((HOST, PORT))
            data = pickle.dumps(make_message(is_service=True, msg="get_update"))
            socket.sendall(data)
            messages = pickle.loads(socket.recv(1024))

            for message in messages:
                print(repr(f"{message['sender']}: {message['text']};"))
        time.sleep(0.2)


def pusher():
    while True:
        msg = input()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
            socket.connect((HOST, PORT))
            data = pickle.dumps(make_message(msg=msg, sender=args.name))
            socket.sendall(data)


if __name__ == "__main__":
    picker_thread = threading.Thread(picker)
    pusher_thread = threading.Thread(pusher)

    picker_thread.start()
    pusher_thread.start()
