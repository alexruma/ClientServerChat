import socket

# I used code from https://realpython.com/python-sockets/ used as general template for setting up the socket connection,
# modifying it as necessary for purpose of assignment. Also used https://docs.python.org/3/howto/sockets.html as
# a reference.

class Client:

    # Set HOST to localhost address.
    HOST = "127.0.0.1"
    PORT = 1094
    quit = False
 
    def start(self):
        # Establish socket.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            print("> Client connected.")
            print('> Enter "/q" to quit.')
            print("> Please enter a message.")
            print("-------------------------")

            while True:
                # Send message.
                self.send(s)
                 # Break and close connection if input is /q
                if self.quit == True:
                    break 
            
                # Receive message.
                self.receive(s)
                # Break and close connection if input is /q
                if self.quit == True:
                    break

            s.close


    def send(self, s):
        """Uses socket to send message to server."""
        # Print prompt for user message.
        print("You: ", end='')
        # Get user input and then determine length of message.
        message = input()
        message_length = str(len(message))

        # Send length of message.
        s.sendall(bytes(message_length, encoding= "utf-8" ))
        # Send message.
        s.sendall(bytes(message, encoding= "utf-8" ))

        if message == "/q":
            self.quit = True
    
    
    def receive(self, s):
        """Uses socket to receive message from chat server. Prints received message."""
        # Receive message length and message from client and print decoded (string version of bytes) message.
        recvd_len = int((s.recv(1024)).decode())
        # Receive and print response.
        recvd = s.recv(1024).decode()
        
        # Break and close connection if recvd is /q
        if recvd == "/q":
            print('Them:', recvd)
            self.quit = True
            return
        
        # Call function to receive rest of message if all not received.
        if recvd_len > len(recvd):
            self.receive_additional(s, recvd_len, len(recvd), recvd)

        # Else print message if full message has been received.
        else:
            print('Them:', recvd)
    

    def receive_additional(self, conn, expected_len, recvd_count, current_message):
        """Function to receive remainder of message if server message length exceeds receive window.
        Will be called as many time as necessary and then print the full message once it has been received."""
        recvd = (conn.recv(1024)).decode()
        current_message += recvd
        recvd_count += len(recvd)

        # Call function to receive rest of message if all not received.
        if expected_len > recvd_count:
            self.receive_additional(conn, expected_len, recvd_count, current_message)
        
        # Else print message if full message has been received.
        else:
            print("Them: " + current_message)



if __name__ == '__main__':
    client = Client()
    client.start()