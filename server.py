import pickle
import socketserver


HOST = "172.31.26.109"
PORT = 443
# HOST = "127.0.0.1"
# PORT = 4321

MSG_LOG = []
MSG_COUNTER = len(MSG_LOG)
LATEST_MSG_IDX_BY_SENDER = {}


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
        # self.request is the TCP socket connected to the client
        latest_message = pickle.loads(self.request.recv(1024).strip())
        sender = latest_message["sender"]
        if latest_message["is_service"] and latest_message["msg"] == "get_update":
            if LATEST_MSG_IDX_BY_SENDER[sender] == MSG_COUNTER:
                return
            messages = []
            for msg in MSG_LOG[LATEST_MSG_IDX_BY_SENDER[sender]:]:
                if msg["sender"] != sender:
                    messages.append(msg)
            self.request.sendall(pickle.dumps(messages))
            LATEST_MSG_IDX_BY_SENDER[sender] = MSG_COUNTER

        elif not latest_message["is_service"]:
            MSG_COUNTER += 1
            MSG_LOG.append(latest_message)

            print("{} wrote: {}".format(sender, latest_message["msg"]))


if __name__ == "__main__":
    print("Server started")

    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
