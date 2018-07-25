#---------------------------------------------------------------------------------------------------------------
#  filename: server_connector.py
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3
# 
import threading, time, os, sys
import random
import com
import hamgo_tcp
import subprocess

#import prctl

#-----------------------------------------------------------
#-----------------------------------------------------------
class Server(com.Com):

  #--------------------------------------------------
  def stop(self):
    self.chk_th_rx.go = False
    self.chk_th_rx.chkTerminated()
    self.tcp.stop()
    print('server-connector:main terminated')
  

  #--------------------------------------------------
  def heartbeat(self):
    if  self.tcp.getConnected() == True:
      msg_text = self.config_data.name+'\t'+self.config_data.qth+'\t'+self.config_data.ip+'\t'+self.config_data.locator+'\t'+com.version
      #print('heartbeat:msg_text: '+msg_text)
      msg = MSG(payloadType=0, payload=msg_text, contactType=1, source=self.config_data.call,) #+++
      b = msg.buildBarray()
      com.Com.queue_b2s.put(b) 
      #msg.printIPmsg('HB')
    #else:
      #print('HB: Not Connected !')
      #pass
    pass  
 
  #--------------------------------------------------
  def reconnect(self, force=False):
    #print(time.strftime("%a, %d %b %Y %H:%M:%S")+ ' start method-reconnect')
    if force:
      self.tcp.TCPclose()
      return self.TCPconnect(self.config_data.server, self.config_data.port)
    else:  
      if self.tcp.getConnected():
        return True      
      else:
        #print('do reconnect')
        return self.TCPconnect(self.config_data.server, self.config_data.port)


  #--------------------------------------------------
  def setConfig_data(self,config_data):
    self.config_data = config_data
  
  #--------------------------------------------------
  def __init__(self): 
    print('INIT-server-connector')
    
    # for ip change reconnect
    self.ip = 'localhost'
    self.port = 9124
 
    self.chk_th_rx = com.CheckTerminated(go=True, text='server_connector:thrx')
    self.config_data = None                          
    self.tcp = hamgo_tcp.Tcp()
 
    #-------------------
    self.th_rx = threading.Thread(target = self.do_rx)  
    self.th_rx.start()  

   #-------------------
  def playSound(self,call,snd):
    if call != self.config_data.call:
      a = str(os.path.dirname(os.path.abspath(sys.argv[0])))+'/'+snd
      subprocess.Popen(["/usr/bin/aplay", '-D'+self.config_data.audio, a])
      
#--------------------------------------------------
  def do_rx(self):
    #print('server-connector: do_rx')
    #prctl.set_name("hgm:srv-con:do_rx")
   
    while self.chk_th_rx.go:

      time.sleep(0.1)
      msgmax = 700      
      
      if not com.Com.queue_msg.empty(): 
        msgbuf = com.Com.queue_msg.get()         
        if (len(msgbuf)<10):
          #print('len(msg) < 10 ->skipped !!!')
          continue

        lng = len(msgbuf)
        if (lng > msgmax):
          #print('len(msg) > '+str(msgmax)+' ->skipped !!!') 
          continue

        if ( (msgbuf[0]!=0xaa) and (msgbuf[1]!=0x00) and (msgbuf[2]!=0x00)  ): 
          #print('Bad msg rule: 6 STRONG ->skipped !!!')
          continue

        if ( (msgbuf[0]==0xaa) and (msgbuf[1]==0x01) and (msgbuf[2]==0x00)  ): 
          #print('\nserver_connector: valid \0xaa\0x01\0x00 detected !!!')
          #print(        'server_connector:rx-1: new message: msgbuf=\n'+str(msgbuf))
          #com.pb(msgbuf,'server_connector:rx-2: new message: msgbuf=\n')

          msg = MSG()
          msg.getMSGfromBuffer(msgbuf)
          #msg.printIPmsg('RX')  
            
          # HB PayloadType=0, contact=CQ, contacttype=1  -- maybe heartbeat
          if ((msg.PayloadType == msg.c_PayloadCQ_0) and (msg.ContactType==0x01)):
            #print('server_connector:rx: (HB)')
            info = msg.Payload.split('\t')
            #print('server_connector:rx: (HB) msg.Payload-splitted='+str(info))
            __call = msg_Call()
            if len(info) == 5:
              __call.SeqCounter = msg.SeqCounter 
              __call.call = str(msg.Source)
              __call.name = str(info[0])
              __call.info = str(info[1])
              __call.ip = str(info[2])
              __call.locator = str(info[3])
              __call.version = str(info[4])
              __call.lh = str(time.strftime("%H:%M:%S"))
              __call.path = str(msg.Path)
              com.Com.queue_s2o.put(__call)
              del __call
              continue
            else:
              #print('not HB . maybe CQ')    
              pass        

          # Type		PayloadType	ContactType	Contact	
          # CQ		    0           1           CQ
          # GroupCall	4		        1		        SELECT Ergebnis	
          # Broadcast 6           1           ALL
          # Emergency	7		        1		        EM  

            #print('check')

          if ( (msg.Contact=='CQ')  and (msg.ContactType==0x01) and (msg.PayloadType == msg.c_PayloadCQ_0) ):
            #print('server_connector:rx: (CQ)')
            cq_info = msg.Payload.split('\t')
            #print('server_connector:rx: (CQ) msg.Payload-splitted='+str(info))
            if len(info) >= 5:
              __h = msg_History()
              __h.SeqCounter = msg.SeqCounter
              __h.htype = msg.PayloadTypeString 
              __h.time = time.strftime("%H:%M:%S")         
              __h.src = msg.Source
              __h.dst = msg.Contact # msg.PayloadTypeString
              __h.text = str(' '.join(map(str, cq_info[5:]))) 
              __h.path = msg.Path
              com.Com.queue_s2h.put(__h)
              #print('server_connector:rx: CQ queue_s2h.put(h)')
              self.playSound(__h.src,'hinweis.wav')
              del __h
              continue

          # BC contact=ALL,  contacttype=1, PayloadType=6
          elif ( (msg.Contact=='ALL') and (msg.ContactType==0x01) and (msg.PayloadType == msg.c_PayloadBroadcastMessage_6) ):
              #print('server_connector:rx: received: ALL(=BC)')
              __h = msg_History()
              __h.SeqCounter = msg.SeqCounter
              __h.htype = msg.PayloadTypeString 
              __h.time = time.strftime("%H:%M:%S")         
              __h.src = msg.Source
              __h.dst = msg.Contact #msg.PayloadTypeString
              __h.text = msg.Payload
              __h.path = msg.Path
              com.Com.queue_s2h.put(__h)
              #print('server_connector:rx: ALL(=BC) queue_s2h.put(h)')
              #print('server_connector:rx: s2o.put(call)')
              self.playSound(__h.src,'hinweis.wav')
              del __h
              continue

          elif ( (msg.Contact=='EM')  and (msg.ContactType==0x01) and (msg.PayloadType == msg.c_PayloadEMCOMMessage_7) ):
              #print('server_connector:rx: received: EM')
              __h = msg_History()
              __h.SeqCounter = msg.SeqCounter
              __h.htype = msg.PayloadTypeString 
              __h.time = time.strftime("%H:%M:%S")         
              __h.src = msg.Source
              __h.dst = msg.Contact #msg.PayloadTypeString
              __h.text = msg.Payload
              __h.path = msg.Path
              com.Com.queue_s2h.put(__h)
              #print('server_connector:rx: EM queue_s2h.put(h)')
              #print('server_connector:rx: s2o.put(call)')
              self.playSound(__h.src,'buzzer_x.wav')
              del __h
              continue

          # GC PayloadType=4, contact=GROUP, contacttype=1
          elif ((msg.PayloadType == msg.c_PayloadGroupMessage_4) and (msg.ContactType==0x01)):
              #print('server_connector:rx: received: GC')
              __h = msg_History()
              __h.SeqCounter = msg.SeqCounter
              __h.payloadType = msg.PayloadType
              __h.htype = msg.PayloadTypeString # ???????????? 
              __h.time = time.strftime("%H:%M:%S")         
              __h.src = msg.Source
              __h.dst = msg.Contact
              __h.text = msg.Payload
              __h.path = msg.Path
              com.Com.queue_s2h.put(__h)
              #print('server_connector:rx: GC queue_s2h.put(h)')
              self.playSound(__h.src,'hinweis.wav')
              del __h
              continue

          #  Transfer
          # elif ((msg.PayloadType == msg.PayloadCQ_0) and (msg.ContactType==0x01)):
          #   pass      

          else:
            print('server_connector:rx: ERROR:MSG Type')
            print('msg.PayloadType='+str(msg.PayloadType)+' msg.ContactType='+str(msg.ContactType))
            msg.printIPmsg('server_connector: ERROR:\n') 

          del msg 

        else:
          print('wrong msg version - Why ???')
          #com.pb(msgbuf,'server_connector:rx: wrong message\n')

    self.chk_th_rx.setTerminating()


  #--------------------------------------------------
  def TCPconnect(self, ip='localhost', port=9124):
    r = self.tcp.TCPconnect(self.config_data.server, int(self.config_data.port))
    print('server_connector:TCPconnect: '+str(r))
    return r

  def getTCPconnected(self):
    return self.tcp.getConnected()


#--------------------------------------------------
#--------------------------------------------------
class msg_Call():
  SeqCounter = 0
  call = ''
  group = ''
  name = ''
  info = ''
  locator = ''
  ip = ''
  version = ''
  lh = ''
  path = ''

#--------------------------------------------------
#--------------------------------------------------
class msg_History():
  SeqCounter = 0
  payloadType = 0
  htype = ''
  time = ''
  src = '--'
  dst = '--'
  Text = ''
  path = ''
  

#--------------------------------------------------
#--------------------------------------------------
class MSG:

  # Payload types
  c_PayloadCQ_0                = 0
  c_PayloadDebug_1             = 1
  c_PayloadUpd_2               = 2
  c_PayloadAck_3               = 3
  c_PayloadGroupMessage_4      = 4
  c_PayloadPrivateMessage_5    = 5
  c_PayloadBroadcastMessage_6  = 6
  c_PayloadEMCOMMessage_7      = 7
  c_PayloadFile_10             = 10
  c_PayloadFileresponse_11     = 11
   

  def __init__(self, version=1, ttl=0xfe, flags=0x00,source='', contactType=0x01, contact='CQ', path='', payloadType=0x00, payload='' ):

    self.Version = version          # 2 Byte  big-endian
    self.SeqCounter = os.urandom(8) # 8 Byte  
    self.TTL = ttl                  # 1 Byte
    self.Flags=flags                # 1 Byte
    self.SourceLength=0             # 2 Byte  big-endian
    self.Source = source            # 0-n Byte
    self.ContactType = contactType  # 1 Byte
    self.ContactLength=0             # 2 Byte  big-endian
    self.Contact = contact          # 0-n Byte
    self.PathLength=0                # 2 Byte  big-endian
    self.Path = path                # 0-n Byte
    self.PayloadType = payloadType  # 1 Byte
    self.PayloadLength=0             # 4 Byte  little-endian
    self.Payload = payload          # 0-n Byte

    self.PayloadTypeString=''

    self.PayloadText = ''

    self.SourceLength =  len(self.Source)
    self.ContactLength =  len(self.Contact)  
    self.PathLength =  len(self.Path)     
    self.PayloadLength =  len(self.Payload)


  #--------------------------------
  def buildBarray(self): 
    #print('buildBarray: start... ', end='')

    # Start Frame
    b = 0xaa.to_bytes(1, byteorder='little')
    
    # Version
    b +=  self.Version.to_bytes(2, byteorder='little')
    # Sequence Counter
    b += self.SeqCounter
    # TTL
    b += self.TTL.to_bytes(1, byteorder='little')
    # Flags
    b += self.Flags.to_bytes(1, byteorder='little')
    
    #Source = call
    t = self.Source.encode(encoding='UTF-8')
    l = len(t)
    # Source length
    b += l.to_bytes(2, byteorder='big')
    # Source
    if l > 0:
      b += t
  
    # Contact Type
    b += self.ContactType.to_bytes(1, byteorder='little')
    
    # Contact 
    t = self.Contact.encode(encoding='UTF-8')
    l = len(t)    
    # Contact length
    b += l.to_bytes(2, byteorder='big')
    if l > 0:
      # contact
      b += t

    # Path
    t = self.Path.encode(encoding='UTF-8')
    l = len(t)
    # Path length
    b += l.to_bytes(2, byteorder='little')
    if l > 0:
      # path
      b += t

    # Payloadtype
    b += self.PayloadType.to_bytes(1, byteorder='little')

    if self.PayloadType == b'\x02':
      self.PayloadLength = 7
      self.Payload = b'\x00\x04\x00\x00\x00\x00\x00'

    # payload 
    t = self.Payload.encode(encoding='UTF-8')
    l = len(t)
    # payload length
    b += l.to_bytes(4, byteorder='little')
    # payload
    if l > 0:
      # payload value
      b += t
    
    # end frame
    b += 0xab.to_bytes(1, byteorder='little')
    
    #print('buildBarray: ende')
    return b

  #--------------------------------------------------
  def getMSGfromBuffer(self, msgbuf):
    #print('getMSGfromBuffer:lng='+str(lng))
    ibp = 1

    try:

      #print('getMSGfromBuffer:'+str(msgbuf))
      if ( (msgbuf[1]==0x00) and (msgbuf[2]==0x00) ):
        #print('getMSGfromBuffer:problem')
        return 'x'

      # Version
      self.Version = int.from_bytes(msgbuf[ibp:ibp+2],byteorder='little')
      ibp = ibp + 2

      if self.Version == 0:
        return

      self.SeqCounter = int.from_bytes(msgbuf[ibp:ibp+8],byteorder='little')
      ibp = ibp + 8

      self.TTL = int.from_bytes(msgbuf[ibp:ibp+1],byteorder='little')
      ibp = ibp + 1

      self.Flags = int.from_bytes(msgbuf[ibp:ibp+1],byteorder='little')
      ibp = ibp + 1

      self.SourceLength = int.from_bytes(msgbuf[ibp:ibp+2],byteorder='big')
      ibp = ibp + 2

      self.Source = msgbuf[ibp:ibp+self.SourceLength].decode('ascii')
      ibp = ibp + self.SourceLength

      self.ContactType = int.from_bytes(msgbuf[ibp:ibp+1],byteorder='little')
      ibp = ibp + 1

      self.ContactLength = int.from_bytes(msgbuf[ibp:ibp+2],byteorder='big')
      ibp = ibp + 2

      self.Contact = msgbuf[ibp:ibp+self.ContactLength].decode('ascii')
      ibp = ibp + self.ContactLength
              
      self.PathLength = int.from_bytes(msgbuf[ibp:ibp+2],byteorder='little')
      ibp = ibp + 2

      self.Path = msgbuf[ibp:ibp+self.PathLength].decode('ascii')
      ibp = ibp + self.PathLength

      self.PayloadType = int.from_bytes(msgbuf[ibp:ibp+1],byteorder='little')
      ibp = ibp + 1    

      self.PayloadLength = int.from_bytes(msgbuf[ibp:ibp+4],byteorder='little')
      ibp = ibp + 4

      self.Payload = msgbuf[ibp:ibp+self.PayloadLength].decode('ascii')

      self.PayloadTypeString = "CQ"
      if (self.PayloadType == 1): self.PayloadTypeString = "DEBUG"
      if (self.PayloadType == 2): self.PayloadTypeString = "FIL"
      if (self.PayloadType == 3): self.PayloadTypeString = "ACK"
      if (self.PayloadType == 4): self.PayloadTypeString = "GC"
      if (self.PayloadType == 5): self.PayloadTypeString = "PC"
      if (self.PayloadType == 6): self.PayloadTypeString = "BC"
      if (self.PayloadType == 7): self.PayloadTypeString = "EM"

    except ValueError:
      self.PayloadTypeString = "ER"
      self.Source = self.Source
      self.Contact = "MSG"
      self.PayloadText = "Protocol-Error in the last received message"

    return self

  #--------------------------------------------
  def printIPmsg(self, title='', dir='h'):

    if dir == 'h':

      print(title+': '
        + ' Version='+str(self.Version)
        + ' SeqCounter='+str(self.SeqCounter)
        + ' TTL='+str(self.TTL)
        + ' Flags='+str(self.Flags)
        + ' SourceLength='+str(self.SourceLength)
        + ' Source='+str(self.Source)
        + ' ContactType='+str(self.ContactType)
        + ' ContactLength='+str(self.ContactLength)
        + ' Contact='+str(self.Contact)
        + ' PathLength='+str(self.PathLength)
        + ' Path='+str(self.Path)
        + ' PayloadType='+str(self.PayloadType)
        + ' PayloadLength='+str(self.PayloadLength)
        + ' Payload='+str(self.Payload)
        + ' PayloadTypeString='+str(self.PayloadTypeString)
      )
        
    else:

      print('Version='+str(self.Version))
      print('SeqCounter='+str(self.SeqCounter))
      print('TTL='+str(self.TTL))
      print('Flags='+str(self.Flags))
      print('SourceLength='+str(self.SourceLength))
      print('Source='+str(self.Source))
      print('ContactType='+str(self.ContactType))
      print('ContactLength='+str(self.ContactLength))
      print('Contact='+str(self.Contact))
      print('PathLength='+str(self.PathLength))
      print('Path='+str(self.Path))
      print('PayloadType='+str(self.PayloadType))
      print('PayloadLength='+str(self.PayloadLength))
      print('Payload='+str(self.Payload))      
      print('PayloadTypeString='+str(self.PayloadTypeString))
      
#--------------------------------------------------
if __name__ == "__main__":

  msgbuf=b'\xaa\x01\x00\xe9\x34\xa6\x0a\x00\x00\x00\x00\xfd\x00\x00\x06\x4f\x45\x35\x4e\x56\x4c\x01\x00\x02\x43\x51\x07\x00\x3b\x4f\x45\x35\x58\x4c\x4c\x00\x2d\x00\x00\x00\x4d\x61\x6e\x66\x72\x65\x64\x09\x4c\x69\x6e\x7a\x09'

  msg = MSG()
  msg.getMSGfromBuffer(msgbuf)
  print(msg.Source) 
