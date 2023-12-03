import pickle
import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = pickle.loads(self.request.recv(1024).strip())
        print("{} wrote:".format(self.data["sender"]), self.data["text"])

        # just send back the same data, but upper-cased
        self.request.sendall(pickle.dumps(self.data))


if __name__ == "__main__":
    HOST = "172.31.26.109"
    PORT = 443
    print("Server started")

    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
