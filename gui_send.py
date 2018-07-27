#---------------------------------------------------------------------------------------------------------------
#  filename: send_messages.py
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux
#               based on OE1KBs Windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from gi.repository import Pango
from abc import ABC, abstractmethod

from server_connector import MSG

import com


#------------------------------------------------------
class Sm(ABC):

  def __init__(self, btn_label='button', max_len=10, config_data=None):
    print('Hallo')

    self.config_data = config_data   
    self.max_len = max_len

    self.msg_i = 1
    self.shift = False
    self.lock = True

    self.grid = Gtk.Grid()
    self.grid.set_column_spacing(10) 
    self.grid.set_row_spacing(10)

    self.content = Gtk.Box()
    self.content.set_border_width(10)        
    self.content.add(self.grid)

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    # start-textview
    self.txt_buf = Gtk.TextBuffer()
    self.txt_buf.set_text("Text")
    textview = Gtk.TextView(buffer=self.txt_buf)

    textview.set_wrap_mode(Gtk.WrapMode.WORD)
    scrolledwindow.add(textview)
    # end-textview
      
    send = Gtk.Button(btn_label)        

    # 0 for gc
    self.grid.attach(scrolledwindow, 0, 1, 1, 1)
    self.grid.attach(Gtk.Label("") , 0, 2, 2, 1)
    self.grid.attach(send          , 0, 3, 2, 1)

    textview.connect("key_press_event", self.on_key_pressed)
    textview.connect("key_release_event", self.on_key_release)
    send.connect("clicked", self.on_send_clicked) 

  #--------------------------------------------------
  def setConfig_data(self,config_data):
    self.config_data = config_data
  
  #------------------------------------------
  def on_key_pressed(self, widget, event, user_data=None):
    key = Gdk.keyval_name(event.keyval)
    print('pressed: '+str(key))
    if ((key == "Shift_L") or (key=="Shift_R")):
      self.shift = True

    cnt = self.txt_buf.get_char_count()
    print('p-cnt='+str(cnt))

    if (key=="BackSpace"):
      print('BS')
      self.lock = False
    else:
      self.lock = True
 
    if ((cnt>=self.max_len) and self.lock):
      return True

    return False

  #------------------------------------------
  def on_key_release(self, widget, event, user_data=None):

    cnt = self.txt_buf.get_char_count()
    #print('cnt='+str(cnt))

    #print('1:'+str(self.shift))
    key = Gdk.keyval_name(event.keyval)
    if not self.shift:
      if key=='Return':
        print('SEND cr?????????????????????')

    if ((key == "Shift_L") or (key=="Shift_R")):
      self.shift = False

    return True

  @abstractmethod
  def do_it(self):
    pass

  def dialog_response(self,widget, response_id):
    if response_id == Gtk.ResponseType.OK:
      #print("OK") 
      pass               
    widget.destroy()   


  #---- send callback ----------------------------------
  def on_send_clicked(self,widget):  
    #print('on_bc_send_clicked')  
    

    if ((self.config_data.call=='your call') or (self.config_data.name=='your name')):
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Please check Setup: call, name, server, your IP, etc !")
      md2.connect("response", self.dialog_response)
      md2.run()
      return False 

    start = self.txt_buf.get_start_iter()
    end   = self.txt_buf.get_end_iter()
    self.text  = self.txt_buf.get_text(start, end, True)
    
    #print('on_bc_text[-1]='+on_bc_text[-1])

    #if on_bc_text[-1]=='\n':  on_bc_text = on_bc_text[:-1]

    if len(self.text)==0:
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Text is needed")
      md2.connect("response", self.dialog_response)
      md2.run()
      return False

    self.do_it()

    return True

#-------------------------------------------------
class send_bc(Sm):

  def __init__(self, btn_label='button', max_len=10, config_data=None):
    Sm.__init__(self, btn_label, max_len, config_data)

  #-----------------
  def do_it(self):  

    msg_text   = '('+str(self.msg_i)+') '+self.text
    msg = MSG(payloadType=6, payload=msg_text, contactType=1, contact='ALL', source=self.config_data.call)   
    b = msg.buildBarray()   
    com.Com.queue_b2s.put(b)         
    self.msg_i += 1

#-------------------------------------------------
class send_cq(Sm):

  def __init__(self, btn_label='button', max_len=10, config_data=None):
    Sm.__init__(self, btn_label, max_len, config_data)

  #---------------
  def do_it(self):

    msg_text =  self.config_data.name+'\t' \
              + self.config_data.qth+'\t' \
              + self.config_data.ip+'\t' \
              + self.config_data.locator+'\t' \
              + com.version+'\t(' \
              + str(self.msg_i)+') '+self.text 
    msg = MSG(payloadType=0, payload=msg_text, contactType=1, contact='CQ', source=self.config_data.call)   
    b = msg.buildBarray()   
    com.Com.queue_b2s.put(b)         
    self.msg_i += 1

# #-------------------------------------------------
class send_gc(Sm):

  def __init__(self, btn_label='button', max_len=10, config_data=None):
    Sm.__init__(self, btn_label, max_len, config_data)

    # ComboBox for GC 
    self.gc_liststore = Gtk.ListStore(str)
    self.gc_group_combo  = Gtk.ComboBox()
    self.gc_group_combo.set_model(self.gc_liststore)

    #gc_group_combo.connect("changed", gc_cbx_changed)

    gc_group_cell = Gtk.CellRendererText()
    self.gc_group_combo.pack_start(gc_group_cell, True)
    self.gc_group_combo.add_attribute(gc_group_cell, "text", 0)

    self.gc_liststore.append(("'OE5RNL fake !'",))
    self.gc_liststore.append(("OE1",))
    self.gc_liststore.append(("OE2",))             
    self.gc_liststore.append(("OE3",))             
    self.gc_liststore.append(("OE4",))             
    self.gc_liststore.append(("OE5",))             
    self.gc_liststore.append(("OE6",))             
    self.gc_liststore.append(("OE7",))             
    self.gc_liststore.append(("OE8",))             
    self.gc_liststore.append(("OE9",))             
    self.gc_liststore.append(("DVINTERN",))             

    # select ComboBox entry from config
    gc_iter = self.gc_liststore.get_iter_first()      #+++
    while self.gc_liststore is not None:
      if (self.gc_liststore.get_value(gc_iter,0)==self.config_data.gc):  #'default'
        break
      gc_iter = self.gc_liststore.iter_next(gc_iter) 
    self.gc_group_combo.set_active_iter(gc_iter) 

    self.grid.attach(self.gc_group_combo, 0, 0, 1, 1)


  #-----------------------------------
  def do_it(self):  

    msg_text = '('+str(self.msg_i)+') '+self.text 
    gc_text = self.gc_liststore.get_value(self.gc_group_combo.get_active_iter(),0)
    msg = MSG(payloadType=4, payload=msg_text, contactType=1, contact=gc_text, source=self.config_data.call)   
    b = msg.buildBarray()   
    com.Com.queue_b2s.put(b)         
    self.msg_i += 1

    pass

#-------------------------------------------------
class send_em(Sm):

  def __init__(self, btn_label='button', max_len=10, config_data=None):
    Sm.__init__(self, btn_label, max_len, config_data)

    self.em_ok = False

  #---------------
  def do_it(self):

    def dialog_response(widget, response_id):
      if response_id == Gtk.ResponseType.YES:
        #print("OK")     
        self.em_ok = True 
      else:
        self.em_ok = False       
      widget.destroy()  

    md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.YES_NO, 
          message_format="Are you sure to send this Mergency-Message:\n"+self.text)
    md2.connect("response", dialog_response)
    md2.run()
    if self.em_ok==False:
      #print('em not sent')
      return

    msg_text = '('+str(self.msg_i)+') '+self.text 

    msg = MSG(payloadType=7, payload=msg_text, contactType=1, contact='EM', source=self.config_data.call)   
    b = msg.buildBarray()   
    com.Com.queue_b2s.put(b)         
    self.msg_i += 1
