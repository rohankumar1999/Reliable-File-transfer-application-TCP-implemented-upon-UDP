from mySocket import mySocket
import socket
UDP_IP = socket.gethostname()
UDP_PORT = 5002
# print(pickle.dumps(pkt))
udpsocket=mySocket(socket.AF_INET,socket.SOCK_DGRAM)
udpsocket.custom_create(UDP_IP,UDP_PORT)
udpsocket.recv_from(4096)
print('closing server...')
udpsocket.close()