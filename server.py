import threading
import socket

host = '127.0.0.1'    # defining IP address of the host 
port = 9000           # defining port number of the host


# staring the server by determining the socket
# Using the Internet socket (AF_INET) and the TCP communication (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))    # binding the server to the IP address and port 
server.listen()              # listening to the clients trying to connect    
print("The server is listening for connections.....")

# creating two lists to store connected clients and their username for chatting
clients = []
client_names = []


# a function to broadcast message to all connected clients
def broadcast(message):

    # for all clients in the list of connected clients -> send message to them
    for client in clients:
        client.send(message) 


# a function to handle client connectivity
def handle_client(client):
    
    # starting an endless loop to receive message from client continuously
    while True:
        
        # receives message when the client remains active
        try:
            msg = message = client.recv(1024)                                # receiving message from client
            if msg.decode().startswith('REMOVE'):                            # checking whether the clients wants to quit or not
                client_to_remove = msg.decode()[7:]                          # finding the client to be removed
                quit(client_to_remove)                                       # call function to to remove the user
            else: 
                broadcast(message)                                           # broadcast message to all clients  
        
        # removes the client after an error or lost connection
        except:
            if client in clients:
                index = clients.index(client)                              # finding the client from the clients list
                clients.remove(client)                                     # removing the client from the server
                client.close()                                             # closing the client connection
                client_name = client_names[index]                          # find the client name using the index
                broadcast(f'{client_name} left the chat'.encode())         # broadcast client leaving message to all
                client_names.remove(client_name)                           # remove client name from the client_names list
                print(f'{client_name} has left the chat')                  # sending info to the server
                break                                                      # break out of the loop


# remove the client that has quit the chat room
def quit(name):
    name_index = client_names.index(name)                       # finding the index of the client that quit
    quit_client = clients[name_index]                           # removing the client using the index
    clients.remove(quit_client)                                 # removing client from the clients list in server
    client_names.remove(name)                                   # removing the client from client_names list in server
    quit_client.close()                                         # closing the client connection
    print(f'{name} has quit the chat.')                         # sending the quit message for the server
    broadcast(f'{name} quit the chat'.encode())                 # broadcast quit message for all



# a function to combine all functions above -> accept clients, message, and broadcast them
def receive():
    while True:
        client, address = server.accept()                              # accepts the clients
        print(f'Connected with {str(address)}')                        # display connectivity in server side
        
        client.send('Username'.encode())                               # ask the client for username
        client_name = client.recv(1024).decode()                       # receive the username from the client
        client_names.append(client_name)                               # add the username into the client_names list
        clients.append(client)                                         # add the client to the clients list

        client.send("You are now connected.\n".encode())               # sending connection status to the client
        broadcast(f'{client_name} has joined the chat!\n'.encode())    # broadcast the joined message
        
        t1 = threading.Thread(target=handle_client, args=(client,))    # executing the handle_client function with a thread
        t1.start()                                                     # starting the thread



# calling the function receive to execute the program
receive()                        
