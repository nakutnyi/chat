import pickle
import socketserver
import threading


HOST = "172.31.26.109"
PORT = 443
# HOST = "127.0.0.1"
# PORT = 4321

MSG_LOG = []
MSG_COUNTER = len(MSG_LOG)
LATEST_MSG_IDX_BY_SENDER = {}
lock = threading.Lock()


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global MSG_LOG
        global MSG_COUNTER
        global LATEST_MSG_IDX_BY_SENDER

        try:
            received = self.request.recv(1024)
            latest_message = pickle.loads(received)
        except pickle.UnpicklingError:
            latest_message = {
                "sender": "system", "is_service": True, "msg": "control_flow"
            }
            print(received)
        sender = latest_message["sender"]
        if latest_message["is_service"] and latest_message["msg"] == "get_update":
            messages = []
            if LATEST_MSG_IDX_BY_SENDER.get(sender) != MSG_COUNTER:
                for msg in MSG_LOG[LATEST_MSG_IDX_BY_SENDER.get(sender, 0):]:
                    if msg["sender"] != sender:
                        messages.append(msg)
            self.request.sendall(pickle.dumps(messages))
            lock.acquire()
            LATEST_MSG_IDX_BY_SENDER[sender] = MSG_COUNTER
            lock.release()

        elif not latest_message["is_service"]:
            lock.acquire()
            MSG_COUNTER += 1
            MSG_LOG.append(latest_message)
            lock.release()

            print("{} wrote: {}".format(sender, latest_message["msg"]))


if __name__ == "__main__":
    print("Server started")

    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
