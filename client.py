import socket

 # Set HOST to localhost address.
HOST = "127.0.0.1"
PORT = 1094
 
 # Establish socket.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Client connected.")
    print('Enter "/q" to quit.')
    print("Please enter a message.")
    print("-------------------------")

    while True:
        # Print prompt for user message.
        print("You: ", end='')
        # Get user input and then send message.
        message = input() + ""
        s.sendall(bytes(message, encoding= "utf-8" ))
        
        # Break and close connection if input is /q
        if message == "/q":
            break

        data = s.recv(1024)
        print('Them:', data.decode())

    s.close
