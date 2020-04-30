import sys
sys.path.append('../')
import socket
import tqdm
import os
from mySocket import mySocket

# device's IP address
def receive_file(host,port):
    IP = host
    PORT = int(port)
    # receive 4096 bytes each time
    BUFFER_SIZE = 1024 * 4
    SEPARATOR = "<SEPARATOR>"
    # create the server socket
    udpsocket=mySocket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind the socket to our local address
    udpsocket.custom_create(IP,PORT)
    print(f"[*] Listening as {IP}:{PORT}")

    # receive the file infos
    # receive using client socket, not server socket
    received = udpsocket.recv_from(BUFFER_SIZE)
    # print(received)
    received = received.decode()
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
            # read 1024*4 bytes from the socket (receive)
            bytes_read = udpsocket.recv_from(BUFFER_SIZE)
            # print('in')
            if bytes_read == 'bye'.encode():    
                # file transmitting is done
                progress.close()
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
            progress.refresh(nolock=False, lock_args=None)
    udpsocket.close()
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("port", help="Port to use")
    args = parser.parse_args()
    host = args.host
    port = args.port
    receive_file(host, port)    