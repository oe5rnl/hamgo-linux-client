#---------------------------------------------------------------------------------------------------------------
#  filename: hamgo_tcp.py
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3
 
# -*- coding: utf-8 -*-

import socket, select
import os, sys
import random
import threading
import com
import time
from gi.repository import GObject

from time import gmtime, strftime

#import prctl

#--------------------------------------------------
#--------------------------------------------------


class Tcp:

  #------------------------
  def TCPclose(self):
    self.__connected = False
    time.sleep(1)
    #self.sock.shutdown(socket.SHUT_RDWR) 
    self.sock.close()  
    print('TCP-socket closed !')
    
  #--------------------------------------------------
  def stop(self):
    self.chk_th_tcprx.go = False
    self.chk_th_tcprx.chkTerminated()
    self.TCPclose()
    #print('tcp:tc-rx: terminated !')


  #--------------------------------------------------
  def __init__(self, updfunc=None):
    self.ip = 'localhost'
    self.port = 9124

    self.chk_th_tcprx = com.CheckTerminated(go=True, text='tcp:tcp_rx ')

    self.updfunc = updfunc

    self.__connected = False
    self.sock = None

    self.th_tcprx = threading.Thread(target = self.tcp_rx)  
    self.th_tcprx.start() 

  #------------------------------------
  def getConnected(self):
    return self.__connected


  #-----------------------------------------
  def tag_search(self,tag,data,ldata):
    found = False
    p = data.find(tag)
    #if (p == -1): # nicht gefunden
    #  found = False
    #elif (p == 0): # eb im letzten buffer ?
    if (p == 0): # eb im letzten buffer ?
      if ldata[:-1] != 0xeb:
        found = True
    elif (p > 0):
      if (data[p-1] != 0xeb): # found
        return p, True

    return p, found


  # aa  00 01 aa aa 38 ab ab 77   ab
  #--------------------------------------------------------------
  def tcp_rx(self):
    print('rcp:tcp_rx start\n')
    #prctl.set_name("hgm:tcp_rx")
    time.sleep(3)

    start = False
    ldata = bytearray()

    while self.chk_th_tcprx.go:
      time.sleep(0.02)

      if self.__connected:
        inputs = [self.sock]
        outputs = [self.sock]
        urgent = []

        try:
          readable, writable, exceptional = select.select(inputs, outputs, urgent)
        except:
          print('hamgo_tcp: close bei select')
          self.TCPclose()
        else:

          for s in readable:
            data = s.recv(2048)
            #print('len(data)='+str(len(data)))
            if len(data)>0:
            
              sp, aa_found = self.tag_search(0xaa,data,ldata)
              ep, ab_found = self.tag_search(0xab,data,ldata)

              if aa_found and ab_found: # msg found
                #print('msg in data')
                msg_buf = data[sp:ep]    # ep+1 ???
                erg_buf, esc = com.deescape(msg_buf)
                if esc: 
                  #print('deescaped !')
                  #print('\n1-tcp_rx- ESC detected : '+str(esc))
                  #com.pb(msg_buf,'tcp_rx_th-1 ')
                  pass
                
                com.Com.queue_msg.put(erg_buf)
                #print('com.Com.queue_msg.put(erg_buf)')

              elif (not aa_found) and (not ab_found):  # nothing found
                #print('no aa and ab in data.. ', end='')
                if start:
                  #print('start found before - keep data ...')
                  msg_buf += data
                else:
                  #print()
                  pass
                                  
              elif aa_found and (not ab_found):  # found aa but not ab -> start tag
                #print('aa found not ab')
                start = True
                msg_buf = data[sp:]
                # next buffer

              elif (not aa_found) and (ab_found):  # found ende, start is in last buffer
                #print('no aa found but ab -> end tag')
                start = False
                msg_buf += data[:ep]
                erg_buf, esc = com.deescape(msg_buf)
                if esc: 
                  #print ('deescaped !')
                  #print('\n1-tcp_rx- ESC detected : '+str(esc))
                  #com.pb(msg_buf,'tcp_rx_th-1 ')
                  pass
                com.Com.queue_msg.put(erg_buf)
                #print('com.Com.queue_msg.put(erg_buf)')

              ldata = data
            else: # connection lost or closed by server or network problem
              self.TCPclose()

          for s in writable:

            if not com.Com.queue_b2s.empty(): 
                #print('TCP-send')
                b = com.Com.queue_b2s.get()
                b = com.escape(b)
                #com.pb(b,'tcp-w')
                totalsent = 0
                l = len(b)
                try:
                  while totalsent < l:
                    sent = self.sock.send(b[totalsent:])
                    if sent == 0:
                        raise RuntimeError("socket connection broken")
                    totalsent = totalsent + sent
                  #print('msg sent')
                except:
                  #print('hamgo_tcp: error tcp write !')
                  self.TCPclose()

          for s in exceptional:
            #print('tcp:urgent')
            s.close()  

    self.chk_th_tcprx.setTerminating()


  #------------------------
  def TCPconnect(self, ip='127.0.0.1', port=9124):
    #print('TCPconnect')

    self.ip = ip
    self.port = port
    print('try to connect: '+str(self.ip)+':'+str(self.port))

    self.__connected=False

    try:
      # Create a TCP/IP socket
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.settimeout(1)

      # Connect the socket to the port where the server is listening
      server_address = (self.ip, int(self.port))
      print('TCP-connecting to {} port {}'.format(*server_address))
      self.sock.connect(server_address)
      self.__connected = True
      print('TCP-connected !')  
      return True
    except:
      self.__connected=False
      print('TCP-connect: Error - not connected !') 
      return False


  #--------------------------------------------------------------
  def TCPsend(self,bmessage):
    #print('\n\nTCPsend: start')

    # reconnet 
    if self.__connected==False:
      self.TCPconnect(self.ip,self.port)

    if self.__connected==True:
      try:
        self.sock.sendall(bmessage)
      except:
        self.__connected=False
        self.sock.close()
        print('TCPsend: send error')
    else:
      print('TCPsend: connection is closed !!!')
    print('TCPsend: ende\n\n')


