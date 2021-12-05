import socket

# I used code from https://realpython.com/python-sockets/ used as general template for setting up the server
# modifying it as necessary for purpose of assignment. Also used https://docs.python.org/3/howto/sockets.html as
# a reference.

class Server:
    # Set HOST to localhost address.
    HOST = "127.0.0.1"
    PORT = 1094
    message_count = 0
    quit = False

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
                    # Receive message from client.
                    recvd = self.receive(conn)
                    
                    # Break and close connection if recvd is /q
                    if self.quit == True:
                        break
                    
                    # Send initial instructions only after first message is received.
                    if self.message_count == 1:
                        print("Please enter a response or enter '/q' to quit.")   
                    
                    # Send response to client.
                    self.send(conn)
                    
                    # Break and close connection if input is /q
                    if self.quit == True:
                        break 
            s.close
    

    def receive(self, conn):
        """Receive message from chat client. Returns received message string."""
        # Receive message length and message from client and print decoded (string version of bytes) message.
        recvd_len = int((conn.recv(124)).decode())
        #print(recvd_len, type(recvd_len))
        
        recvd = (conn.recv(24)).decode()

        # Set quit to true if message = /q
        if recvd == "/q":
            print("Them: " + recvd)
            self.quit = True
        
        # Call function to receive rest of message if all not received.
        if recvd_len > len(recvd):
            self.receive_additional(conn, recvd_len, len(recvd), recvd)
        
        # Else print message if full message has been received.
        else:
            print("Them: " + recvd)
            self.message_count += 1    
    

    def receive_additional(self, conn, expected_len, recvd_count, current_message):
        recvd = (conn.recv(24)).decode()
        current_message += recvd
        recvd_count += len(recvd)

        # Call function to receive rest of message if all not received.
        if expected_len > recvd_count:
            self.receive_additional(conn, expected_len, recvd_count, current_message)
        
        # Else print message if full message has been received.
        else:
            print("Them: " + current_message)
            self.message_count += 1    



    def send(self, conn):
        """Get response message from user and send to chat client. Returns user input string."""
        # Print prompt for user message.
        print("You: ", end='')
        # Send data to client.
        message = input()
        message_length = str(len(message))
       
        # Send length of message.
        conn.sendall(bytes(message_length, encoding= "utf-8" ))
        # Send message.
        conn.sendall(bytes(message, encoding= "utf-8" )) 

        # Set quit to true if message = /q
        if message == "/q":
            self.quit = True
        

if __name__ == '__main__':
    server = Server()
    server.start()
