from mySocket import mySocket
import socket
UDP_IP = socket.gethostname()
UDP_PORT = 5000
# print(pickle.dumps(pkt))
udpsocket=mySocket(socket.AF_INET,socket.SOCK_DGRAM)
udpsocket.custom_create(UDP_IP,UDP_PORT)
udpsocket.send_to("hello mondii inka paduko!!",(UDP_IP,5002))
print('closing client...')
udpsocket.close()