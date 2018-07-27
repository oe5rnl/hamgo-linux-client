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
# https://www.tutorialspoint.com/pygtk/pygtk_quick_guide.htm
# http://eccentric.slavery.cx/misc/pygtk/pygtkfaq.html
#
# https://valadoc.org/gdk-3.0/Gdk.EventKey.html
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

import time,threading,sys,os #, subprocess
from datetime import datetime 
#import prctl

import com
import server_connector
import gui_debug_info
import gui_config
import gui_about
import gui_online
import gui_history
import gui_log
import gui_send

#------ MAIN Class------------------------------------------------------------
class hgm():

  #---------------------------------------------------------------------------
  def __init__(self):

    self.winTitle = "HAMNET-Messanger by ÖVSV/OE1KBC - Linux (Version: "+com.version+") by OE5RNL, OE5NVL   "
    self.go = True

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    # --- App_Main ----

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

    self.setup = gui_config.Setup()
    self.debug_info = gui_debug_info.Debug_info()

    # load proper css file
    css_provider = Gtk.CssProvider()
    #('OS-NAME===>'+dbg.osname)
    if self.debug_info.osname.find('Raspbian')!=-1:
     ('Raspbian css loaded')
     css_provider.load_from_path(os.path.dirname(os.path.abspath(sys.argv[0]))+'/application-raspi.css')
    else:
      print('ubuntu css loaded')
      css_provider.load_from_path(os.path.dirname(os.path.abspath(sys.argv[0]))+'/application-ubuntu.css')
      Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    #--------------------------------------------------------------------------
    #----- Build Gui widgets --------------------------------------------------
    #--------------------------------------------------------------------------
    self.main_header = AppHeaderLabel()
       
    self.app_server_connector = server_connector.Server()
    self.app_server_connector.setConfig_data(self.setup.app_config.config_data)

    len = 20
    self.bc = gui_send.send_bc(max_len=len, btn_label='send Broadcast', config_data=self.setup.app_config.config_data)
    self.cq = gui_send.send_cq(max_len=len, btn_label='send CQ', config_data=self.setup.app_config.config_data)
    self.gc = gui_send.send_gc(max_len=len, btn_label='send Group', config_data=self.setup.app_config.config_data)
    self.em = gui_send.send_em(max_len=len, btn_label='send Emergency', config_data=self.setup.app_config.config_data)
    self.about = gui_about.About()
    self.history = gui_history.History()
    self.online = gui_online.Online()
    self.log = gui_log.Log()
 
    self.setup.set_GcGroup(self.gc)
    self.setup.set_Reconnect(self.app_server_connector)
    self.setup.set_mainHeader(self.main_header)

    #--------------------------------------------------------------------------
    # --- Messages ----
    messagestabs = Gtk.Notebook() 
    messagestabs.append_page(self.bc.content, Gtk.Label('Broadcast'))
    messagestabs.append_page(self.cq.content, Gtk.Label('CQ'))
    messagestabs.append_page(self.gc.content, Gtk.Label('Group Call'))
    messagestabs.append_page(self.em.content, Gtk.Label('Emergency'))
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
    messenger_frame_online.add(self.online.scrolledwindow) 

    #Frame: messages
    messenger_frame_messages = Gtk.Frame()
    messenger_frame_messages.set_label(" Messages ")
    messenger_frame_messages.add(messagestabs)

    messenger_pan_hor.add1(messenger_frame_online)
    messenger_pan_hor.add2(messenger_frame_messages) 

    messenger_pan_ver.add1(messenger_pan_hor)
    messenger_pan_ver.add2(self.history.frame) 
    
    # Build the gui from widgets
    main_grid = Gtk.Grid()
    main_grid.set_column_spacing(10) 
    main_grid.set_row_spacing(10) 

    # add grid to mainwindow
    self.win.add(main_grid)

    # --- Add mainmenu-Tabs  ---
    main_tabs = Gtk.Notebook()
    main_tabs.append_page(messenger_pan_ver, Gtk.Label('Messenger')) # START tab1: Messenger   
    main_tabs.append_page(self.log.tab, Gtk.Label('Log')) # tab2: Log   
    main_tabs.append_page(self.setup.tab, Gtk.Label('Setup')) # Tab3: config    
    main_tabs.append_page(self.about.tab, Gtk.Label('About')) # tab4: About   
    main_tabs.append_page(self.debug_info.tab, Gtk.Label('Debug-Info')) # tab5: debug-info
    
    # place elements
    main_grid.attach(self.main_header ,0,0,1,1)
    main_grid.attach(main_tabs,0,1,1,1)
    
    # set header info
    self.main_header.setText(self.setup.app_config.config_data.call+'  '+self.setup.app_config.config_data.name+'  '+self.setup.app_config.config_data.qth+'  '+self.setup.app_config.config_data.locator)
    #self.main_header.setStatus(self.app_server_connector.getTCPconnected())
    self.main_header.setStatus(True) 

    # start the main thread for update GUI widgets
    self.to = threading.Thread(target = self.do_main)  
    self.to.start() 

    # connect to hamgo server
    print('main:Tcp-connect')
    print('IP='+self.setup.app_config.config_data.server)
    print('port='+str(self.setup.app_config.config_data.port))
    co = self.app_server_connector.TCPconnect(str(self.setup.app_config.config_data.server), int(self.setup.app_config.config_data.port))
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

      if ((s % 1)==0):
        # Update WindowTitle with info and time
        GLib.idle_add(self.update_winTitle)

      if ((s % 5)==0):
        r = self.app_server_connector.reconnect()
        self.main_header.setStatus(r)

      # Heardbeat
      if ((s % 20)==0):
      #if (s==0):
        #print('')
        self.app_server_connector.heartbeat()

      # Update online users
      if not com.Com.queue_s2o.empty(): 
        call = com.Com.queue_s2o.get()
        #print('--------------------->call Update-Online !' +call.call+' '+str(call.SeqCounter))
        GLib.idle_add(self.online.UpdateOnlineCall, call)

        # last time i received my own call from hamgo server
        if call.call == self.setup.app_config.config_data.call:
          lhmycall = datetime.now()
    
      # insert incomming messages into history and log
      if not com.Com.queue_s2h.empty(): 
        hist = com.Com.queue_s2h.get()
        #print('---------------------->call insert-History !'+hist.src+' '+str(hist.SeqCounter))
        GLib.idle_add(self.history.InsertHistoryCall, hist)
        GLib.idle_add(self.log.InsertLogCall,  hist)

      time.sleep(0.5)

      # check if no reply for my call last in the 160 secounds
      # if yes -> network or hamgo server down.
      akt=datetime.now()
      # print('AKT:'+str(d.total_seconds()))
      if (akt-lhmycall).total_seconds()>160:
        print("NETWORK PROBLEM ?")
        # set offline  ?
        GLib.idle_add(self.online.SetOfflineCall)
        
        h = server_connector.msg_History()
        h.SeqCounter = 0
        h.htype = 'ERr'
        h.time = time.strftime("%H:%M:%S")         
        h.src = '--'
        h.dst = '--'
        h.text = 'Connection to the HAMGO module not possible\nHAMGO nodule offline or check Setup please' 
        h.path = ' '
        GLib.idle_add(self.history.InsertHistoryCall, h)
        GLib.idle_add(self.log.InsertLogCall,  h)
      
      #time.sleep(0.5)  
    print('online terminated')  


  #-------------------------------------------------
  def update_winTitle(self):
    self.win.set_title(self.winTitle + time.strftime("%a, %d %b %Y %H:%M:%S"))    


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
  