import pickle
import socketserver


MSG_LOG = []


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global MSG_LOG
        self.latest_msg_idx_by_sender = getattr(self, "latest_msg_idx_by_sender", {})
        self.messages_counter = getattr(self, "messages_counter", 0)
        # self.request is the TCP socket connected to the client
        latest_message = pickle.loads(self.request.recv(1024).strip())
        sender = latest_message["sender"]
        MSG_LOG.append(latest_message)
        self.messages_counter += 1
        current_counter = self.latest_msg_idx_by_sender.get(sender, 0)
        self.latest_msg_idx_by_sender[sender] = current_counter + 1
        print("{} wrote: {}".format(sender, latest_message["text"]))

        # just send back the same data, but upper-cased

        messages = pickle.dumps(
            MSG_LOG[self.latest_msg_idx_by_sender[sender] - 1:]
        )
        self.request.sendall(messages)


if __name__ == "__main__":
    HOST = "172.31.26.109"
    PORT = 443
    print("Server started")

    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
