import pickle
import socketserver


HOST = "172.31.26.109"
PORT = 443
# HOST = "127.0.0.1"
# PORT = 4321

MSG_LOG = []
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
        global LATEST_MSG_IDX_BY_SENDER
        # self.request is the TCP socket connected to the client
        latest_message = pickle.loads(self.request.recv(1024).strip())
        sender = latest_message["sender"]
        if latest_message["is_service"] and latest_message["msg"] == "get_update":
            if sender in LATEST_MSG_IDX_BY_SENDER:
                messages = pickle.dumps(
                    MSG_LOG[LATEST_MSG_IDX_BY_SENDER[sender]:]
                )
            else:
                messages = pickle.dumps([])
            self.request.sendall(messages)
            self.update_counters(sender, update_for_all=False)

        elif not latest_message["is_service"]:
            MSG_LOG.append(latest_message)
            self.update_counters(sender)

            print("{} wrote: {}".format(sender, latest_message["msg"]))

    @staticmethod
    def update_counters(sender, update_for_all=True):
        current_user_counter = LATEST_MSG_IDX_BY_SENDER.get(sender, 0)
        LATEST_MSG_IDX_BY_SENDER[sender] = current_user_counter
        if update_for_all:
            keys = list(LATEST_MSG_IDX_BY_SENDER)
        else:
            keys = [sender]
        for sender in keys:
            LATEST_MSG_IDX_BY_SENDER[sender] += 1


if __name__ == "__main__":
    print("Server started")

    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
