import threading
import socket

# socket at the client side -> Internet socket (AF_INET) with TCP communication (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server with host ID and port number
client.connect(('127.0.0.1', 9000))

# ask the client for their username
client_name = input("Enter your preferred username: ")

# a function that receives messages from the server side  
def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            
            # send the server the username for first time login.
            if message == 'Username':
                client.send(client_name.encode())
            
            # for all other messages -> simply print in on screen
            else:
                print(message)
            
            # close the client if an error occurs
        except:
            print("An error was detected!")
            client.close()



# a function to write messages by the clients
def write():
    while True:
        
        # shows the username along with the message (Bob: Hello)
        message = f'{client_name}: {input("")}'
        
        # check to see if the message is a command or not -> command begins with /
        if message[(len(client_name)+2):].startswith("/"):
            
            # see if the command is '/quit' or not
            if message[(len(client_name)+2):].startswith("/quit"):
                
                # send a message to server saying to remove the client
                client.send(f'REMOVE {client_name}'.encode())
            
            # for any other command print the following
            else:   
                print("No other commands are allowed except: /quit")
        
        # for all other message, do nothing -> simply send it to be displayed
        else:
            client.send(message.encode())



# Starting two threads to execute the functions receive and write simultaneously  
t1 = threading.Thread(target=receive)
t1.start()

t2 = threading.Thread(target=write)
t2.start()
