import socket
import pickle
import pprint
import time
import threading
import hashlib
from datetime import datetime
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
  
  def write_log(self,log_str):	
    file_object = open('./../log.txt', 'a')
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    file_object.write(date_time+':'+log_str + '\n')
    file_object.close() 
  # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
  def custom_create(self,localIP,port):
      self.bind((localIP,port))
      
  def __init__(self,arg1,arg2,unreliable = 0):
    super(mySocket,self).__init__(arg1,arg2)
    self.state=0
    self.unreliable = unreliable
    
  def run_send(self,arg1,arg2):
    # print('in run send')
    while True:
      s=0
      # print('sending..')
      # sendpacket = pickle.loads(arg1)
      # print(sendpacket.seq_no)
      start = time.perf_counter()
      self.sendto(arg1,arg2)
      while True:
        if self.t2.is_alive() is False:
          # print('message sent')
          s=1
          break
        tout = time.perf_counter()
        if((tout-start) > 2 ):
          self.write_log('Ack drop')
          # print('in')
          s=0
          break
      if(s==1):
        self.state=abs(1-self.state)
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
        break
  #   while True:
  #     pkt,addr=self.recvfrom(4096)
  #     data=pickle.loads(pkt)
  #     if data.isack :
  #       print('ack recieved!!')
  #       break

    
  def send_to(self,arg1,arg2):
    if(self.unreliable == 1):
      self.sendto(arg1,arg2)
      return
    pkt=Packet([arg1,self.state,False,0])  
    check_str = str(pkt.payload)+str(pkt.isack)+str(pkt.seq_no)  
    m=hashlib.md5()
    m.update(check_str.encode())
    checksum = m.hexdigest()
    pkt.checksum = checksum
    send_data = pickle.dumps(pkt)
    # print(send_data)
    self.t1 = threading.Thread(target=self.run_send, args=(send_data,arg2)) 
      # self.sendto(pickle.dumps(pkt),arg2)
    self.t2=threading.Thread(target=self.terminate_send,args=())
    self.t2.start()
    self.t1.start()
    self.t1.join()
     
  def recv_from(self,arg1):
    if(self.unreliable == 1):
      data, addr = self.recvfrom(arg1)
      return data.decode()
    # print(arg1)
    while True:
      s=0
      data,addr=self.recvfrom(arg1)
      # print((data))
      pkt=pickle.loads(data)
      received = str(pkt.payload) + str(pkt.isack) + str(pkt.seq_no)
      m=hashlib.md5()
      m.update(received.encode())
      checksum = m.hexdigest()
      # print(checksum, pkt.checksum)
      # print(self.state,(pkt.seq_no),checksum==pkt.checksum )
      if(checksum == pkt.checksum):
        ack_pkt=Packet([pkt.seq_no,True])
        self.sendto(pickle.dumps(ack_pkt),addr)
        if (pkt.seq_no==self.state):
          # print('message recieved: ')
          # pprint.pprint(received)
          self.state=abs(1-self.state)
          # ack_pkt=Packet([pkt.seq_no,True])                  
          # print('addr: ',addr)
          s=1
        else:
          self.write_log('Packet Drop')  
      else:
        self.write_log('Packet Corrupt')    
      if(s==1):
        break
    return pkt.payload 

