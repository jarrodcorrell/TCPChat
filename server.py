import socket
import threading

#Defining Constants
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#defining server type/family
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



#Handling the individual clients that have connected to the server
def handle_client(conn, addr):
    #Server has found a new conection from the start function and displays this message
    print(f"[NEW CONNECTION] {addr} connected.")

    #Starting the Handling of the client loop
    connected = True
    while connected:
        #Receiving the message from the client ONLY STARTS WHEN CLIENTS SENDS A MESSAGE (BLOCKING LINE OF CODE)
        #Format is utf-8
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg==DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            messag = f"[{addr}] {msg}"

            conn.send(messag.encode(FORMAT))
    conn.close()

#Listens and defines the clients
def start():

    #listening for clients to connect to the server
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} on port {PORT}")

    while True:
        #when client has connected it will make an object with the information of the connection
        conn, addr = server.accept()
        #when a client connects it will hand it to the handle_client function
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        #displays the #of clients connected to the server
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()