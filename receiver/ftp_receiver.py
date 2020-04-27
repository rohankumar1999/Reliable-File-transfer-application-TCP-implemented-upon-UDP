import sys
sys.path.append('../')
import socket
import tqdm
import os
from mySocket import mySocket

# device's IP address
IP = "127.0.0.1"
PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 1024 * 4
SEPARATOR = "<SEPARATOR>"
# create the server socket
# TCP socket
udpsocket=mySocket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to our local address
udpsocket.custom_create(IP,PORT)
# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
print(f"[*] Listening as {IP}:{PORT}")
# accept connection if there is any
# if below code is executed, that means the sender is connected

# receive the file infos
# receive using client socket, not server socket
received = udpsocket.recv_from(BUFFER_SIZE)
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)
# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        # read 1024 bytes from the socket (receive)
        bytes_read = udpsocket.recv_from(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

udpsocket.close()