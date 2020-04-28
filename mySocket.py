import socket
import pickle
import pprint
import time
import threading
import hashlib
class Packet:

  def __init__(self,args):#if the packet is not an ack
    if len(args)==4:
      self.payload=args[0]
      self.isack=args[2]
      self.seq_no=args[1]
      self.checksum=args[3]
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
      s=0
      # print('sending..')
      start = time.perf_counter()
      self.sendto(arg1,arg2)
      while True:
        if self.t2.is_alive() is False:
          # print('message sent')
          s=1
          break
        tout = time.perf_counter()
        if((tout-start) > 5 ):
          s=0
          break
      if(s==1):
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
      if data.isack and data.ack_no==self.state:
        # print('ack recieved!!')
        self.state=abs(1-self.state)
        break
  #   while True:
  #     pkt,addr=self.recvfrom(4096)
  #     data=pickle.loads(pkt)
  #     if data.isack :
  #       print('ack recieved!!')
  #       break

    
  def send_to(self,arg1,arg2):
    m=hashlib.md5()
    m.update(arg1)
    checksum = m.hexdigest()
    pkt=Packet([arg1,self.state,False,checksum])
    send_data = pickle.dumps(pkt)
    # print(send_data)
    self.t1 = threading.Thread(target=self.run_send, args=(send_data,arg2)) 
      # self.sendto(pickle.dumps(pkt),arg2)
    self.t2=threading.Thread(target=self.terminate_send,args=())
    self.t1.start()
    self.t2.start()
    self.t1.join()
     
  def recv_from(self,arg1):
    # print(arg1)
    while True:
      s=0
      data,addr=self.recvfrom(arg1)
      # print((data))
      pkt=pickle.loads(data)
      received = pkt.payload
      m=hashlib.md5()
      m.update(received)
      checksum = m.hexdigest()
      if pkt.seq_no==self.state & checksum==pkt.checksum:
        # print('message recieved: ')
      # pprint.pprint(received)
        self.state=abs(1-self.state)
        ack_pkt=Packet([pkt.seq_no,True])
        print('addr: ',addr)
        self.sendto(pickle.dumps(ack_pkt),addr)
        s=1
      if(s==1):
        break
    return received  
    #code to check if the recieved data has no errors

