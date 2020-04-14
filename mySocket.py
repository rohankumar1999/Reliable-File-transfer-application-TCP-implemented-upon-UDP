import socket
import pickle
import pprint
class Packet:

  def __init__(self,payload,seq_no,isack):#if the packet is not an ack
    self.payload=payload
    self.isack=isack
    self.seq_no=seq_no
    
  def __init(self,seq_no,isack,ack_no):#if the packet is an ack
    self.isack=isack
    self.ack_no=ack_no
    self.seq_no=seq_no

class mySocket(socket.socket): #extends UDP socket
  
   
  # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
  def custom_create(self,localIP,port):
      self.bind((localIP,port))
      print('socket created')
  def __init__(self,arg1,arg2):
    super(mySocket,self).__init__(arg1,arg2)
    self.state=0
    print('constructor invoked')
  def send_to(self,arg1,arg2):
    pkt=Packet(arg1,self.state,False)
    self.sendto(pickle.dumps(pkt),arg2)
     #code for recieving ack.if no ack resend
    print('message sent')
  def recv_from(self,arg1):
    data,addr=self.recvfrom(arg1)
    pkt=pickle.loads(data)
    pprint.pprint(pkt.payload)
    #code to check if the recieved data has no errors
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
# print(pickle.dumps(pkt))
udpsocket=mySocket(socket.AF_INET,socket.SOCK_DGRAM)
udpsocket.custom_create(UDP_IP,UDP_PORT)
udpsocket.send_to("hello there!!",(UDP_IP,UDP_PORT))
udpsocket.recv_from(4096)
