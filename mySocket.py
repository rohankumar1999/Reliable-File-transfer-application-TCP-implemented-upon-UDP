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
      s=0
      print('sending..')
      start = time.perf_counter()
      self.sendto(arg1,arg2)
      # time.sleep(5)
      # if self.t2.is_alive() is False:
      #   print('message sent')
      #   break
      while True:
        pkt,addr=self.recvfrom(4096)
        data=pickle.loads(pkt)
        if data.isack and data.ack_no==self.state:
          print('ack recieved!!')
          self.state=abs(1-self.state)
          s=1
          break
        tout = time.perf_counter()
        if((tout-start) > 5 ):
          s=1
          break
      if(s==1):
        break    
      # data,addr=self.recvfrom(4096)
      # pkt=pickle.loads(data)
      # print(pkt.isack)
      # if pkt.isack:
      #   print('ack recieved!!')
      #   break
        
      
  # def terminate_send(self):
    
  #   while True:
  #     pkt,addr=self.recvfrom(4096)
  #     data=pickle.loads(pkt)
  #     if data.isack :
  #       print('ack recieved!!')
  #       break

    
  def send_to(self,arg1,arg2):
    pkt=Packet([arg1,self.state,False])
    send_data = pickle.dumps(pkt)
    # print(send_data)
    self.t1 = threading.Thread(target=self.run_send, args=(send_data,arg2)) 
      # self.sendto(pickle.dumps(pkt),arg2)
    # self.t2=threading.Thread(target=self.terminate_send,args=())
    self.t1.start()
    # self.t2.start()
    self.t1.join()
     #code for recieving ack.if no ack resend
     
  def recv_from(self,arg1):
    print(arg1)
    data,addr=self.recvfrom(arg1)
    # print((data))
    pkt=pickle.loads(data)
    
    if pkt.seq_no==self.state:
      received = pkt.payload
      print('message recieved: ')
    # pprint.pprint(received)
      self.state=abs(1-self.state)
      ack_pkt=Packet([pkt.seq_no,True])
      print('addr: ',addr)
      self.sendto(pickle.dumps(ack_pkt),addr)
      return received
    #code to check if the recieved data has no errors

