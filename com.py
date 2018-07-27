#---------------------------------------------------------------------------------------------------------------
#  filename: com.py
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3
 
import time, queue 
from gi.repository import GObject

#fname = 'file_tcp.txt'
version = 'L.0.5.2'

#--------------------------------------------------
class Com():

  queue_msg = queue.Queue() # Data from msg_dispatcher to serverconnetor
  queue_s2h = queue.Queue() # Data from msg_dispatcher to history
  queue_s2o = queue.Queue() # Server sendet zu online 
  queue_b2s = queue.Queue() # Broadcast to server


#------------------------------------------------------
class CheckTerminated():

  def __init__(self, go=False, stime=0.05, wait_time=10, text=''):

    self.__stime = stime
    self.__wait_time= wait_time
    self.__text = text
    self.__go = go
    self.__wait = True

  def set_go(self,v):
      self.__go = v

  def get_go(self):
      return self.__go

  def setTerminating(self):
    print(self.__text+ ' terminating...', end='')
    self.__wait = False

  def status(self):
    return self.__wait

  def chkTerminated(self):
    #time.(self.__stime)
    GObject.timeout_add(self.__wait_time, self.status)
    print(self.__text+ ' terminated !')

  go = property(get_go, set_go)

#------------------------
def isascii(c):
  return ( (c >= 0x20) and (c<=0x7f) )

#------------------------  
def p(c):
  if isascii(c):
    return(chr(c))
  else:
    return(hex(c))

#------------------------  
def pb(buf, h=''):
  print(h+'len='+str(len(buf)))
  for i in buf:
    x = str(hex(i))
    x = x.replace("0x", "")
    if len(x) == 1:
      x='0'+x
    else:
      x= ''+x
    print(x+' ', end='')
print('')

#--------------------------------------------
def escape(inbuf):

  outbuf = bytearray()
  outbuf.append(0xaa) 

  for iesc in range(1,len(inbuf)-1):  

    if ( (inbuf[iesc] == 0xaa) or (inbuf[iesc] == 0xab) or (inbuf[iesc] == 0xeb) ):
      outbuf.append(0xeb)
    outbuf.append(inbuf[iesc])

  outbuf.append(0xab)
  return outbuf

#--------------------------------------------
def deescape(msgbuf):

  descape = False
  ebaa = b'\xEB\xAA' in msgbuf
  ebab = b'\xEB\xAB' in msgbuf
  ebeb = b'\xEB\xEB' in msgbuf
  if ( (ebaa) or (ebab) or (ebeb) ):
    descape = True  
  msgbuf = msgbuf.replace(b'\xEB\xAA',b'\xAA')
  outbuf = msgbuf.replace(b'\xEB\xAB',b'\xAB')
  outbuf = outbuf.replace(b'\xEB\xEB',b'\xEB')

  return outbuf, descape
