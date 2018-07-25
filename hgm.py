#!/usr/bin/python3

#---------------------------------------------------------------------------------------------------------------
#  filename: hgm.py 
#  date: 2018-07-23
#  function:
# 
#  author:      oe5rnl@oevsv.at, oe5nvl@oevsv.at
#  description: HAMNET Messenger client für Linux
#               based on OE1KBCs windows .NET Client
#  license:     GNU_GENERAL_PUBLIC_LICENSE_V3
# 
# ==========================-===================-=======-=====================================
# ii  libgtk-3-0:amd64       3.18.9-1ubuntu3.3   amd64   GTK+ graphical user interface library
# ii  libgtk2.0-0:amd64      2.24.30-1ubuntu1.16 amd64   GTK+ graphical user interface library
#
# dpkg -l libgtk2.0-0 libgtk-3-0 
#
# usefull links:
#
# https://wiki.gnome.org/Projects/PyGObject/Threading
# PyGObject
# https://pygobject.readthedocs.io/en/latest/
# https://pygobject.readthedocs.io/en/latest/guide/threading.html?highlight=thread%20
# http://zetcode.com/gui/pygtk/
# https://www.programcreek.com/python/example/88440/gi.repository.Gtk.CssProvider
# https://www.programcreek.com/python/example/88416/gi.repository.Gtk.ComboBox
# https://developer.gnome.org/gtk3/stable/chap-css-overview.html
# https://thegnomejournal.wordpress.com/2011/03/15/styling-gtk-with-css/
# https://stackoverflow.com/questions/40761906/python-3-and-gtk3-issue-with-treeview-and-alternate-colors-of-rows
# https://lzone.de/blog/Media%20Player%20with%20GStreamer%20and%20PyGI
# https://www.reddit.com/r/gnome/comments/3owhp6/python_help_critique_my_application_design_home/
# https://wiki.gnome.org/Attic/GnomeArt/Tutorials/GtkThemes/GtkComboBox
# https://developer.sugarlabs.org/src/gtk3-porting-guide.md.html
# https://wiki.pythonde.pysv.org/Import
#
# for gui debuging
# gsettings set org.gtk.Settings.Debug enable-inspector-keybinding true
# GTK_DEBUG=interactive ./hgm.py
#
# https://de.wikipedia.org/wiki/GNU_General_Public_License



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from gi.repository import Pango

import time,threading,sys,os, subprocess
from datetime import datetime 
#import prctl

import com
import server_connector
from gui_debug_info import debug_info_tab, debug_info_osname
import gui_config
from gui_online import online_scrolledwindow, online_liststore

from gui_send_messages import bc_content, bc_txt_buf, bc_send
from gui_send_messages import cq_content, cq_txt_buf, cq_send
from gui_send_messages import gc_content, gc_txt_buf, gc_send, gc_liststore, gc_group_combo
from gui_send_messages import em_content, em_txt_buf, em_send

from gui_about import about_tab
from gui_history import history_frame, history_liststore
from gui_log import log_tab, log_liststore


#------ MAIN Class------------------------------------------------------------
class hgm():

  #---------------------------------------------------------------------------
  def __init__(self):

    self.winTitle = "HAMNET-Messanger by ÖVSV/OE1KBC - Linux (Version: "+com.version+") by OE5RNL, OE5NVL   "

    self.bc_i = 1
    self.cq_i = 1
    self.gc_i = 1
    self.em_i = 1
    self.em_ok = False
    self.go = True

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    # --- App_Main ----
    
    self.app_server_connector = server_connector.Server()
    self.app_server_connector.setConfig_data(gui_config.setup_config_data)

    # create main window
    self.win = Gtk.Window()
    self.win.resize(1000,600)
    self.win.set_position(Gtk.WindowPosition.CENTER)
    self.update_winTitle()
    #self.win.set_title(self.winTitle + time.strftime("%a, %d %b %Y %H:%M:%S")     )
    self.win.set_border_width(10)
    self.win.connect("destroy", self.end)

    #disable drag and drop
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-dnd-drag-threshold", 10000)

    # Set Application Theme
    # WORK: https://blogs.gnome.org/mclasen/2014/05/06/tweaking-a-the-gtk-theme-using-css/
    #settings.set_property("gtk-theme-name", "Numix")
    settings.set_property("gtk-theme-name", "Ambiance")
    #settings.set_property("gtk-theme-name", "Emacs")
    #settings.set_property("gtk-theme-name", "Metabox")
    settings.set_property("gtk-application-prefer-dark-theme", True)  # if you want use dark theme, set second arg to True

    # load proper css file
    css_provider = Gtk.CssProvider()
    #('OS-NAME===>'+dbg.osname)
    if debug_info_osname.find('Raspbian')!=-1:
     ('Raspbian css loaded')
     css_provider.load_from_path(os.path.dirname(os.path.abspath(sys.argv[0]))+'/application-raspi.css')
    else:
      print('ubuntu css loaded')
      css_provider.load_from_path(os.path.dirname(os.path.abspath(sys.argv[0]))+'/application-ubuntu.css')
      Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    #--------------------------------------------------------------------------
    #----- Build Gui widgets --------------------------------------------------
    #--------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------
    # --- Messages ----
    messagestabs = Gtk.Notebook() 
    messagestabs.append_page(bc_content, Gtk.Label('Broadcast'))
    messagestabs.append_page(cq_content, Gtk.Label('CQ'))
    messagestabs.append_page(gc_content, Gtk.Label('Group Call'))
    messagestabs.append_page(em_content, Gtk.Label('Emergency'))
    messagestabs.append_page(Gtk.Label('not implementet yet'), Gtk.Label('Transfer'))

    # --- Messenger ----
    # content of tab "Messenger"
    # left "online" right "Messages" bottom "History"
    messenger_pan_hor = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
    messenger_pan_hor.set_position(500)

    messenger_pan_ver = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
    messenger_pan_ver.set_position(300)

    # Frame: online
    messenger_frame_online = Gtk.Frame()
    messenger_frame_online.set_label(" Online ")
    messenger_frame_online.add(online_scrolledwindow) 

    #Frame: messages
    messenger_frame_messages = Gtk.Frame()
    messenger_frame_messages.set_label(" Messages ")
    messenger_frame_messages.add(messagestabs)

    messenger_pan_hor.add1(messenger_frame_online)
    messenger_pan_hor.add2(messenger_frame_messages) 

    messenger_pan_ver.add1(messenger_pan_hor)
    messenger_pan_ver.add2(history_frame) 
    
    # Build the gui from widgets
    main_grid = Gtk.Grid()
    main_grid.set_column_spacing(10) 
    main_grid.set_row_spacing(10) 

    # add grid to mainwindow
    self.win.add(main_grid)

    self.main_header = AppHeaderLabel()

    # --- Add mainmenu-Tabs  ---
    main_tabs = Gtk.Notebook()
    main_tabs.append_page(messenger_pan_ver, Gtk.Label('Messenger')) # START tab1: Messenger   
    main_tabs.append_page(log_tab, Gtk.Label('Log')) # tab2: Log   
    main_tabs.append_page(gui_config.setup_tab, Gtk.Label('Setup')) # Tab3: config    
    main_tabs.append_page(about_tab, Gtk.Label('About')) # tab4: About   
    main_tabs.append_page(debug_info_tab, Gtk.Label('Debug-Info')) # tab5: debug-info
    
    # place elements
    main_grid.attach(self.main_header ,0,0,1,1)
    main_grid.attach(main_tabs,0,1,1,1)
    
    # set header info
    self.main_header.setText(gui_config.setup_config_data.call+'  '+gui_config.setup_config_data.name+'  '+gui_config.setup_config_data.qth+'  '+gui_config.setup_config_data.locator)
    #self.main_header.setStatus(self.app_server_connector.getTCPconnected())
    self.main_header.setStatus(True) 

    # connect Callbacks for buttons
    gui_config.setup_save.connect("clicked", self.on_save_config_clicked)
    gui_config.setup_btn_audio_test.connect("clicked", self.on_audio_test_clicked)

    bc_send.connect("clicked", self.on_bc_send_clicked) 
    cq_send.connect("clicked", self.on_cq_send_clicked) 
    gc_send.connect("clicked", self.on_gc_send_clicked)
    em_send.connect("clicked", self.on_em_send_clicked)

    # start the main thread for update GUI widgets
    self.to = threading.Thread(target = self.do_main)  
    self.to.start() 

    # connect to hamgo server
    print('main:Tcp-connect')
    print('IP='+gui_config.setup_config_data.server)
    print('port='+str(gui_config.setup_config_data.port))
    co = self.app_server_connector.TCPconnect(gui_config.setup_config_data.server, int(gui_config.setup_config_data.port))
    self.main_header.setStatus(co)

    # show all and start Gtk main loop
    self.win.show_all() 
    Gtk.main() 

    # end init

  #--------------------------------------------------
  # quit the application
  def end(self, e):
    self.go  = False
    time.sleep(1)
    self.app_server_connector.stop()
    Gtk.main_quit()
    print('vy 73')

  #-------------------------------------------------
  #--- Update Gui from thread ----------------------
  #-------------------------------------------------
  def do_main(self):
    lhmycall = datetime.now()
    while self.go == True:
      #prctl.set_name("hgm:do_main")
      #print('do_main go='+str(self.go))

      # if necessery try reconnect 
      s = int(time.strftime("%S")) 
      if ((s % 5)==0):
        r = self.app_server_connector.reconnect()
        self.main_header.setStatus(r)

      # Heardbeat
      if ((s % 20)==0):
      #if (s==0):
        #print('')
        self.app_server_connector.heartbeat()

      GLib.idle_add(self.update_winTitle)

      # Update online users
      if not com.Com.queue_s2o.empty(): 
        call = com.Com.queue_s2o.get()
        #print('--------------------->call Update-Online !' +call.call+' '+str(call.SeqCounter))
        GLib.idle_add(self.UpdateOnlineCall, call)
        # last time i received my own call from hamgo server
        if call.call == gui_config.setup_config_data.call:
          lhmycall = datetime.now()
    
      # check if no reply for my call last in the 160 secounds
      # if yes -> network or hamgo server down.
      akt=datetime.now()

      # print('AKT:'+str(d.total_seconds()))
      if (akt-lhmycall).total_seconds()>160:
        print("NETWORK PROBLEM ?")
        # set offline  ?
        GLib.idle_add(self.SetOfflineCall)
        
        h = server_connector.msg_History()
        h.SeqCounter = 0
        h.htype = 'ERr'
        h.time = time.strftime("%H:%M:%S")         
        h.src = '--'
        h.dst = '--'
        h.text = 'Connection to the HAMGO module not possible\nHAMGO nodule offline or check Setup please' 
        h.path = ' '
        GLib.idle_add(self.InsertHistoryCall, h)
        GLib.idle_add(self.InsertLogCall,  h)
      
      time.sleep(0.5)

      # insert incomming messages into history and log
      if not com.Com.queue_s2h.empty(): 
        hist = com.Com.queue_s2h.get()
        #print('---------------------->call insert-History !'+hist.src+' '+str(hist.SeqCounter))
        GLib.idle_add(self.InsertHistoryCall, hist)
        GLib.idle_add(self.InsertLogCall,  hist)

      time.sleep(0.5)  
    print('online terminated')  

  #-------------------------------------------------
  #---- Update GUI widgets--------------------------
  #-------------------------------------------------
  def UpdateOnlineCall(self, call):

    #self.liststore.append([setup_config_data.call, 'Hugo', '1234 Ort', 'JN00AA','18.06.00','44.143.97.20','1.5.4',12345])

    found = False
    b = online_liststore.get_iter_first()      
    # skip online info line IF NOT NONE  
    online_liststore.set_value(b,7,time.time()+300)
    b = online_liststore.iter_next(b) 
    
    while b is not None:
       
      # delete 'OFFLINE' row
      if (online_liststore.get_value(b,0)=='OFFLINE'):
        online_liststore.remove(b)

      old = (online_liststore.get_value(b,7) < (time.time()-80))        
      if old:   
        online_liststore.set_value(b,8,'#f55e5e') # background: red  
        online_liststore.set_value(b,9,'#000000') # foregrounf: black           
      else:
        online_liststore.set_value(b,8,'#98f887') # foreground: green
        online_liststore.set_value(b,9,'#000000') # foreground: black 
        
      if online_liststore.get_value(b,0) == call.call:
        #print('online: update user: '+str(call.call))
        found = True   

        if old:
          online_liststore.set_value(b,8,'#98f887') # reactivate call -> green
          online_liststore.set_value(b,9,'#000000') # foreground: black

        online_liststore.set_value(b,1,str(call.name))
        online_liststore.set_value(b,2,str(call.info))
        online_liststore.set_value(b,3,str(call.locator))
        online_liststore.set_value(b,4,str(call.lh))
        online_liststore.set_value(b,5,str(call.ip))
        online_liststore.set_value(b,6,str(call.version))
        online_liststore.set_value(b,7,time.time())
        
      b = online_liststore.iter_next(b) 
    # end while

    if found == False:
      #print('online: insert user: '+str(call.call))
      online_liststore.append([call.call, call.name, call.info, call.locator ,str(call.lh), call.ip, call.version, time.time(),'#98f887', '#000000'])
    
    # Insert 'OFFLINE' row, if needed
    b = online_liststore.get_iter_first()   
    online_liststore.set_value(b,7,time.time()+300)
    b = online_liststore.iter_next(b)      
    while b is not None:
      if online_liststore.get_value(b,8) == '#f55e5e': # red
        online_liststore.insert_before(b,['OFFLINE', '', '', '','','','',online_liststore.get_value(b,7)+1, '#ffffff','#000000']) # whilte        
        break
      b = online_liststore.iter_next(b) 

  #-------------------------------------------------
  def SetOfflineCall(self):
    b = online_liststore.get_iter_first()      
    # skip online info line IF NOT NONE  
    online_liststore.set_value(b,7,time.time()+300)
    b = online_liststore.iter_next(b) 
    while b is not None:
      online_liststore.set_value(b,8,'#f55e5e')
      b = online_liststore.iter_next(b) 
    pass

  #-------------------------------------------------
  def InsertLogCall(self, call): 
    #print('InsertLogCall: '+str(call.src))
    log_liststore.insert(0,[time.strftime("%a, %d %b %Y %H:%M:%S"), str(call.htype), str(call.src), str(call.dst), str(call.text), str(call.path),time.time(),'#ffffff', '#000000' ])

  #-------------------------------------------------
  def InsertHistoryCall(self,hist): 
    if   hist.dst == 'ALL':
      backgroundColor = '#ffffff' # white
      foregroundColor = '#0000ff' # blue
    elif hist.dst == 'CQ':
      backgroundColor = '#faf86a' # yellow
      foregroundColor = '#000000' # black      
    elif hist.dst == 'EM':
      backgroundColor = '#ff0000' # red
      foregroundColor  = '#ffffff'       
    elif hist.payloadType == 4:   #GC
      backgroundColor = '#00ff00' # green
      foregroundColor = '#000000' # green       
    else:
      backgroundColor = '#ffffff'
      foregroundColor  = '#000000'        

    history_liststore.insert(0,[str(hist.htype), str(hist.time), str(hist.src), str(hist.dst), str(hist.text), time.time(), backgroundColor, foregroundColor]) 


  #-------------------------------------------------
  def update_winTitle(self):
    self.win.set_title(self.winTitle + time.strftime("%a, %d %b %Y %H:%M:%S"))    


  #-------------------------------------------------
  #---- Callbacks ----------------------------------
  #-------------------------------------------------

  def on_save_config_clicked(self,button):

    server_tmp = gui_config.setup_config_data.server
    port_tmp   = gui_config.setup_config_data.port

    # config_data = Config_data
    gui_config.setup_config_data.call    = gui_config.setup_call.get_text()
    gui_config.setup_config_data.name    = gui_config.setup_name.get_text()
    gui_config.setup_config_data.qth     = gui_config.setup_qth.get_text()
    gui_config.setup_config_data.locator = gui_config.setup_locator.get_text()
    gui_config.setup_config_data.rig1    = gui_config.setup_rig1.get_text()
    gui_config.setup_config_data.rig2    = gui_config.setup_rig2.get_text()
    gui_config.setup_config_data.rig3    = gui_config.setup_rig3.get_text()
    gui_config.setup_config_data.server  = gui_config.setup_server.get_text()
    gui_config.setup_config_data.port    = gui_config.setup_port.get_text()
    gui_config.setup_config_data.ip      = gui_config.setup_ip.get_text()
    gui_config.setup_config_data.log     = gui_config.setup_log.get_text()
    gui_config.setup_config_data.audio   = gui_config.setup_audio_ls.get_value(gui_config.setup_audio_cbx.get_active_iter(),0)
    gui_config.setup_config_data.gc      = gc_liststore.get_value(gc_group_combo.get_active_iter(),0)

    gui_config.app_config.save_ini(gui_config.setup_config_data) 
    self.app_server_connector.setConfig_data(gui_config.setup_config_data)

    if ((server_tmp  != gui_config.setup_server.get_text()) or (port_tmp    != gui_config.setup_port.get_text()) ):
      self.app_server_connector.reconnect(True)

    self.main_header.setText(gui_config.setup_config_data.call+'  '+gui_config.setup_config_data.name+'  '+gui_config.setup_config_data.qth+'  '+gui_config.setup_config_data.locator)
    
  #---- setup_btn_audio_test ----------------------------------  
  def on_audio_test_clicked(self,w):
    #print('button: Audio test')
    a = str(os.path.dirname(os.path.abspath(sys.argv[0])))+'/buzzer_x.wav'
    subprocess.Popen(["/usr/bin/aplay", '-D'+gui_config.setup_config_data.audio, a])


  #---- BC callback ----------------------------------
  def on_bc_send_clicked(self,widget):  
    #print('on_bc_send_clicked')  
    
    def dialog_response(widget, response_id):
      if response_id == Gtk.ResponseType.OK:
        #print("OK") 
        pass               
      widget.destroy()   

    if ((gui_config.setup_config_data.call=='your call') or (gui_config.setup_config_data.name=='your name')):
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Please check Setup: call, name, server, your IP, etc !")
      md2.connect("response", dialog_response)
      md2.run()
      return   

    on_bc_start = bc_txt_buf.get_start_iter()
    on_bc_end   = bc_txt_buf.get_end_iter()
    on_bc_text  = bc_txt_buf.get_text(on_bc_start, on_bc_end, True)

    if len(on_bc_text)==0:
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Text is needed")
      md2.connect("response", dialog_response)
      md2.run()
      return

    on_bc_msg_text   = '('+str(self.bc_i)+') '+on_bc_text

    msg = server_connector.MSG(payloadType=6, payload=on_bc_msg_text, contactType=1, contact='ALL', source=gui_config.setup_config_data.call)   
    b = msg.buildBarray()   
    com.Com.queue_b2s.put(b)         
    self.bc_i += 1

  # --- CQ callback ----------------------------------
  def on_cq_send_clicked(self,widget): 

    def dialog_response(widget, response_id):
      if response_id == Gtk.ResponseType.OK:
        pass
        #print("OK")                
      widget.destroy()   

    if ((gui_config.setup_config_data.call=='your call') or (gui_config.setup_config_data.name=='your name')):
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Please check Setup: call, name, server, your IP, etc !")
      md2.connect("response", dialog_response)
      md2.run()
      return   

    on_cq_start = cq_txt_buf.get_start_iter()
    on_cq_end   = cq_txt_buf.get_end_iter()
    on_cq_text  = cq_txt_buf.get_text(on_cq_start, on_cq_end, True) #+++

    if len(on_cq_text)==0:
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Text is needed")
      md2.connect("response", dialog_response)
      md2.run()
      return

    msg_text = gui_config.setup_config_data.name+'\t' \
              + gui_config.setup_config_data.qth+'\t' \
              + gui_config.setup_config_data.ip+'\t' \
              + gui_config.setup_config_data.locator+'\t' \
              + com.version+'\t(' \
              + str(self.cq_i)+') '+on_cq_text 
    msg = server_connector.MSG(payloadType=0, payload=msg_text, contactType=1, contact='CQ', source=gui_config.setup_config_data.call)   
    b = msg.buildBarray()   
    com.Com.queue_b2s.put(b)         
    self.cq_i += 1

  # --- GC callback ----------------------------------
  def on_gc_send_clicked(self,widget):     
    #print('gc clicked')

    def dialog_response(widget, response_id):
      if response_id == Gtk.ResponseType.OK:
        pass
        #print("OK")                
      widget.destroy()

    if ((gui_config.setup_config_data.call=='your call') or (gui_config.setup_config_data.name=='your name')):
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, 
            message_format="Please check Setup: call, name, server, your IP, etc !") 
      md2.connect("response", dialog_response)
      md2.run()
      return   

    on_gc_start = gc_txt_buf.get_start_iter()
    on_gc_end   = gc_txt_buf.get_end_iter()
    on_gc_text  = gc_txt_buf.get_text(on_gc_start, on_gc_end, True)

    if len(on_gc_text)==0:
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Text is needed")
      md2.connect("response", dialog_response)
      md2.run()
      return

    msg_text = '('+str(self.gc_i)+') '+on_gc_text 

    gc_co_text = gc_liststore.get_value(gc_group_combo.get_active_iter(),0)
    msg = server_connector.MSG(payloadType=4, payload=msg_text, contactType=1, contact=gc_co_text, source=gui_config.setup_config_data.call)   
    b = msg.buildBarray()   
    com.Com.queue_b2s.put(b)         
    self.gc_i += 1

  # --- EM callback ----------------------------------
  def on_em_send_clicked(self,widget):   
    #print('em clicked')

    def dialog_response(widget, response_id):
      if response_id == Gtk.ResponseType.YES:
        #print("OK")     
        self.em_ok = True 
      else:
        self.em_ok = False       
      widget.destroy()  

    if ((gui_config.setup_config_data.call=='your call') or (gui_config.setup_config_data.name=='your name')):
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Please check Setup: call, name, server, your IP, etc !")
      md2.connect("response", dialog_response)
      md2.run()
      return   

    on_em_start = em_txt_buf.get_start_iter()
    on_em_end   = em_txt_buf.get_end_iter()
    on_em_text  = em_txt_buf.get_text(on_em_start, on_em_end, True)

    if len(on_em_text)==0:
      md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.OK, message_format="Text is needed")
      md2.connect("response", dialog_response)
      md2.run()
      return

    md2 = Gtk.MessageDialog(flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.YES_NO, 
          message_format="Are you sure to send this Mergency-Message:\n"+on_em_text)
    md2.connect("response", dialog_response)
    md2.run()
    if self.em_ok==False:
      #print('em not sent')
      return

    msg_text = '('+str(self.em_i)+') '+on_em_text 

    msg = server_connector.MSG(payloadType=7, payload=msg_text, contactType=1, contact='EM', source=gui_config.setup_config_data.call)   
    b = msg.buildBarray()   
    com.Com.queue_b2s.put(b)         
    self.em_i += 1

#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
class AppHeaderLabel(Gtk.Label):

  def __init__(self, text='Header', tcpStatus=False):
    super().__init__()

    self.text = text
    self.tcpStatus = tcpStatus 
    self.txt_status = 'OFFLINE'
    self.set_name('offline')
    self.setStatus(self.tcpStatus)

  def setText(self,text):
    self.text = text
    self.set_text(self.text+' '+self.txt_status) 

  def setStatus(self,tcpStatus):
    self.tcpStatus = tcpStatus
    if self.tcpStatus == True:
      self.txt_status = 'ONLINE'
      self.set_name('online') # color
    else:
      self.txt_status = 'OFFLINE'
      self.set_name('offline') # color

    self.set_text(self.text+' '+self.txt_status) 


#-----------------------------------------------------
if __name__ == "__main__":
   GObject.threads_init()
   a = hgm()
  