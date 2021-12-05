import socket

# I used code from https://realpython.com/python-sockets/ used as general template for setting up the server,
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
            print("> Listening.")
            conn, addr = s.accept()

            with conn:
                print("> Connected by "+ self.HOST +",", self.PORT)
                print("> Waiting for a message.")
                print("-------------------------")

                while True:
                    # Receive message from client.
                    recvd = self.receive(conn)
                    
                    # Break and close connection if recvd is /q
                    if self.quit == True:
                        break
                    
                    # Send initial instructions only after first message is received.
                    if self.message_count == 1:
                        print("> Please enter a response or enter '/q' to quit.")   
                    
                    # Send response to client.
                    self.send(conn)
                    
                    # Break and close connection if input is /q
                    if self.quit == True:
                        break 
            s.close
    

    def receive(self, conn):
        """Uses socket to receive message from chat client. Prints received message."""
        # Receive message length and message from client and print decoded (string version of bytes) message.
        recvd_len = int((conn.recv(1024)).decode())
        #print(recvd_len, type(recvd_len))
        
        recvd = (conn.recv(1024)).decode()

        # Set quit to true if message = /q
        if recvd == "/q":
            print("Them: " + recvd)
            self.quit = True
            return
        
        # Enter hangman mode upon client request.
        if recvd.lower() == "hangman":
           self.hangman(conn)
           self.receive(conn)
           return

        # Call function to receive rest of message if all not received.
        if recvd_len > len(recvd):
            self.receive_additional(conn, recvd_len, len(recvd), recvd)
        
        # Else print message if full message has been received.
        else:
            print("Them: " + recvd)
            self.message_count += 1    
    

    def receive_additional(self, conn, expected_len, recvd_count, current_message):
        """Function to receive remainder of message if client message length exceeds receive window.
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
            self.message_count += 1    



    def send(self, conn):
        """Get response message from user and send to chat client."""
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


################## Hangman Functions #############################
    
    def hangman(self, conn):
        """Hangman game mode."""
        print("Hangman mode started. Please enter a word to play with.")
        # Word the client player must guess.
        word = input().lower()
        # Number of wrong guesses by the client player.
        wrong_guesses = 0
        # List of letters that have been entered by client player.
        guess_bank = []
        # Revealed word to be displayed to client player.
        revealed = self.calculate_revealed(word, guess_bank)
        
        message = "The word is: " + revealed + " Please enter a single character."
        self.send_hangman_message(conn, message)

        # Bulk of the game happens here.
        while True:
            recvd_len = (conn.recv(1024)).decode()
            recvd = (conn.recv(1024)).decode()
            
            # If guess is more than one character.
            if len(recvd) > 1:
                message = "Please enter only a single character."
                # Send length of message and message.
                self.send_hangman_message(conn, message)
            
            # Else if guess is just one character.
            else:
                print("Them:", recvd)

                # Increment wrong guesses if recvd character not in word.
                if recvd.lower() not in word:
                    wrong_guesses += 1
                
                # Get hangman
                hangman = self.calculate_hangman(wrong_guesses)

                # End game if man is hanged.
                if wrong_guesses >= 6:
                    message = "Game Over" + hangman
                   
                    # Update server console.
                    print("You: ", message)

                    # Send length of message and message.
                    self.send_hangman_message(conn, message)
                    return

                # Update guess bank and revealed
                guess_bank.append(recvd.lower())
                revealed = self.calculate_revealed(word, guess_bank)

                # End game if word is guessed.
                if "_" not in revealed:
                    message = "The word is: " + revealed + "! You won!"
                    
                    # Update server console.
                    print("You: ", message)

                    # Send length of message and message.
                    self.send_hangman_message(conn, message)
                    return
                
                else: 
                    message = "The word is: " + revealed + " The man is: " + hangman + " Please enter a single character."

                    # Update server console.
                    print("You: ", message)

                    # Send length of message and message.
                    self.send_hangman_message(conn, message)
 
    
    def calculate_revealed(self, word, guess_bank):
        """Hangman game function.
        Calculate the response to send to client player based on characters guessed."""
        revealed = ""
        for char in word:
            if char in guess_bank:
                revealed += char
            else:
                revealed += "_"
        
        return revealed
    
    
    def calculate_hangman(self, wrong_guesses):
        """Hangman game function."""
        hang_dict = {0: "--",
        1: "--O",
        2: "--O-",
        3: "--O-(",
        4: "--O-(-",
        5: "--O-(--",
        6: "--O-(--<",
        7: "--O-(--<",
        }
        
        return hang_dict[wrong_guesses]
    

    def send_hangman_message(self, conn, message):
        conn.sendall(bytes(str(len(message)), encoding= "utf-8" ))
        conn.sendall(bytes(message, encoding= "utf-8" ))

################## End Hangman Functions #############################


if __name__ == '__main__':
    server = Server()
    server.start()
