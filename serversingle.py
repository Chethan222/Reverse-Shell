import socket
import sys

# Creating socket /Connect to computer/


def create_socket():
    try:
        global host
        global port
        global soc
        host = ""

        port = 3000
        soc = socket.socket()

    except socket.error as msg:
        print("Scoket Creation Error: "+str(msg))

# Binding the socket and listening for connection


def bind_socket():
    try:
        global host
        global port
        global soc

        print("Binding the Port "+str(port))
        soc.bind((host, port))
        # Listening
        soc.listen(5)
    except socket.error as msg:
        print("Scoket Binding Error: "+str(msg)+"\n"+"Retrying...")
        create_socket()

# Send command


def send_command(connection):
    while True:
        command = input()
        if command == 'quit':
            connection.close()
            soc.close()
            sys.exit()

        if len(str.encode(command)) > 0:
            connection.send(str.encode(command))
            client_response = str(connection.recv(1024), "utf-8")
            print(client_response, end="")


# Establish connection with a client (socket must be listening )
def socket_accpt():
    connection, add = soc.accept()
    print("Connection Successfull..")
    print("Connected to "+add[0]+"| Port "+str(add[1]))

    send_command(connection)
    connection.close()


def main():
    create_socket()
    bind_socket()
    socket_accpt()


main()
