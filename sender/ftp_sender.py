import sys
sys.path.append('../')
from mySocket import mySocket
import tqdm
import os
import argparse
import socket
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4 #4KB

def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    udpsocket=mySocket(socket.AF_INET, socket.SOCK_DGRAM)
    # send the filename and filesize
    fname = f"{filename}{SEPARATOR}{filesize}"
    encoded_filename = fname.encode()
    udpsocket.send_to(encoded_filename,(host,port))
    
    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE-400)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            udpsocket.send_to(bytes_read,(host,port))
            # print('sent')
            # update the progress bar
            progress.update(len(bytes_read))

    # close the socket
    udpsocket.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("file", help="File name to send")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=5001)
    args = parser.parse_args()
    filename = args.file
    host = args.host
    port = args.port
    send_file(filename, host, port)