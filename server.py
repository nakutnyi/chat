import pickle
import socket
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
        print("{} wrote:".format(self.data['sender']), self.data['text'])

        # just send back the same data, but upper-cased
        self.request.sendall(pickle.dumps(self.data))

# def serverRunner():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((HOST, PORT))
#     server.listen(5)
#     print(f'host: {HOST}, port {PORT}')
#
#     while True:
#         client, address = server.accept()
#         print(f'Success, client: {address}')
#         # Receive the data in small chunks and retransmit it
#         while True:
#             data = client.recv(1024)
#             if data:
#                 print(pickle.loads(data))
#                 client.sendall(data)
#             else:
#                 print('no data from', address)
#                 break


if __name__ == '__main__':
    HOST = "172.31.26.109"
    PORT = 443

    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
