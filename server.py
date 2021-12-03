import socket

# I used code from https://realpython.com/python-sockets/ used as general template for setting up the server
# modifying it as necessary for purpose of assignment. Also used https://docs.python.org/3/howto/sockets.html as
# a reference.

class Server:
    # Set HOST to localhost address.
    HOST = "127.0.0.1"
    PORT = 1094
    message_count = 0

    def start(self):
        # Establish socket.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Establish server on localhost and port.
            s.bind((self.HOST, self.PORT))
            # Listen for connections.
            s.listen()
            print("Listening.")
            conn, addr = s.accept()

            with conn:
                print("Connected by "+ self.HOST +",", self.PORT)
                print("Waiting for a message.")
                
                while True:
                    # Receive request from client and print decoded (string version of bytes) request.
                    recvd = (conn.recv(2048)).decode()
                    print("Them: " + recvd)
                    self.message_count += 1

                    # Break and close connection if input is /q
                    if recvd == "/q":
                        break
                    
                    # Send initial instructions after first message is received.
                    if self.message_count == 1:
                        print("Please enter a response or enter '/q' to quit.")   
                    
                    # Print prompt for user message.
                    print("You: ", end='')
                    # Send data to client.
                    message = input()
                    conn.sendall(bytes(message, encoding= "utf-8" )) 
                    
            s.close

if __name__ == '__main__':
    server = Server()
    server.start()
