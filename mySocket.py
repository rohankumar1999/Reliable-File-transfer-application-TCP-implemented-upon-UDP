import socket
import pickle
import pprint
import time
import threading
class Packet:

  def __init__(self,args):#if the packet is not an ack
    if len(args)==3:
      self.payload=args[0]
      self.isack=args[2]
      self.seq_no=args[1]
    elif len(args)==2:
      self.isack=args[1]
      self.ack_no=args[0]
    
  
class mySocket(socket.socket): #extends UDP socket
  
   
  # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
  def custom_create(self,localIP,port):
      self.bind((localIP,port))
      
  def __init__(self,arg1,arg2):
    super(mySocket,self).__init__(arg1,arg2)
    self.state=0
    
  def run_send(self,arg1,arg2):
    # print('in run send')
    while True:
      print('sending..')
      self.sendto(arg1,arg2)
      time.sleep(5)
      if self.t2.is_alive() is False:
        print('message sent')
        break
      # data,addr=self.recvfrom(4096)
      # pkt=pickle.loads(data)
      # print(pkt.isack)
      # if pkt.isack:
      #   print('ack recieved!!')
      #   break
        
      
  def terminate_send(self):
    
    while True:
      pkt,addr=self.recvfrom(4096)
      data=pickle.loads(pkt)
      if data.isack :
        print('ack recieved!!')
        break

    
  def send_to(self,arg1,arg2):
    pkt=Packet([arg1,self.state,False])
    self.t1 = threading.Thread(target=self.run_send, args=(pickle.dumps(pkt),arg2)) 
      # self.sendto(pickle.dumps(pkt),arg2)
    self.t2=threading.Thread(target=self.terminate_send,args=())
    self.t1.start()
    self.t2.start()
    self.t1.join()
     #code for recieving ack.if no ack resend
     
  def recv_from(self,arg1):
    data,addr=self.recvfrom(arg1)
    pkt=pickle.loads(data)
    print('message recieved: ')
    pprint.pprint(pkt.payload)
    ack_pkt=Packet([pkt.seq_no,True])
    print('addr: ',addr)
    self.sendto(pickle.dumps(ack_pkt),addr)
    #code to check if the recieved data has no errors

