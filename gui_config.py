#---------------------------------------------------------------------------------------------------------------
#  filename: config.py
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

import configparser, os, sys, subprocess


#  START: Config Classes
#--------------------------------------------------
class Config_data:
  
  #--------------------------------------------------
  def __init__(self):
      self.call    = 'your call'
      self.name    = 'your name'
      self.qth     = 'your qth'
      self.locator = 'your locator'
      self.rig1    = 'your rig1'
      self.rig2    = 'your rig2'
      self.rig3    = 'your rig3'
      self.server  = 'hamgo server ip'
      self.ip      = 'server ip'
      self.port    = '9124'
      self.log     = 'log path'
      self.audio   = 'default'
      self.gc      = 'OE1'


#--------------------------------------------------
class Config():
     
    #--------------------------------------------------
    def __init__(self):
      
      self.config_data = Config_data()
      self.read_ini(self.config_data)     
      pass

    def getConfigData(self):
      return self.config_data

    #--------------------------------------------------
    def read_ini(self,config_data):

        if os.path.isfile(os.path.dirname(os.path.abspath(sys.argv[0]))+'/application.ini'):
            config = configparser.ConfigParser()
            config.read(os.path.dirname(os.path.abspath(sys.argv[0]))+'/application.ini')
            config_data.call    = config['HAMGO-CLIENT']['call']
            config_data.name    = config['HAMGO-CLIENT']['name']
            config_data.qth     = config['HAMGO-CLIENT']['qth']
            config_data.locator = config['HAMGO-CLIENT']['locator']
            config_data.rig1    = config['HAMGO-CLIENT']['rig1']
            config_data.rig2    = config['HAMGO-CLIENT']['rig2']
            config_data.rig3    = config['HAMGO-CLIENT']['rig3']
            config_data.server  = config['HAMGO-CLIENT']['server']
            config_data.ip      = config['HAMGO-CLIENT']['ip']
            config_data.port    = config['HAMGO-CLIENT']['port']
            config_data.log     = config['HAMGO-CLIENT']['log']
            config_data.audio   = config['HAMGO-CLIENT']['audio']
            config_data.gc      = config['HAMGO-CLIENT']['gc']
            

    #--------------------------------------------------
    def save_ini(self,config_data):

        config = configparser.ConfigParser()
        appini = os.path.dirname(os.path.abspath(sys.argv[0]))+'/application.ini'
        config.read(appini)

        config['HAMGO-CLIENT']['call'] = config_data.call
        config['HAMGO-CLIENT']['name'] = config_data.name
        config['HAMGO-CLIENT']['qth'] = config_data.qth
        config['HAMGO-CLIENT']['locator'] = config_data.locator
        config['HAMGO-CLIENT']['rig1'] = config_data.rig1
        config['HAMGO-CLIENT']['rig2'] = config_data.rig2
        config['HAMGO-CLIENT']['rig3'] = config_data.rig3
        config['HAMGO-CLIENT']['server'] = config_data.server
        config['HAMGO-CLIENT']['ip'] = config_data.ip
        config['HAMGO-CLIENT']['port'] = config_data.port
        config['HAMGO-CLIENT']['log'] = config_data.log
        config['HAMGO-CLIENT']['audio'] = config_data.audio
        config['HAMGO-CLIENT']['gc'] = config_data.gc    
        
        with open(appini, 'w') as configfile:    # save
          config.write(configfile)
          print('config-saved')
        
#--------------------------------------------------
#  ENDE: Config Classes



#--------------------------------------------------------------------------
# --- Setup ----
#--------------------------------------------------

class Setup():

  def __init__(self):

    self.gc = None
    self.sc = None
    self.mh = None

    self.tab = Gtk.Box()
    self.tab.set_border_width(10)

    grid = Gtk.Grid()
    grid.set_column_spacing(10) 
    grid.set_row_spacing(10)
    self.tab.add(grid)

    self.app_config = Config()
    #self.config_data = self.app_config.getConfigData() #???
    #self.app_server_connector.setConfig_data(setup_config_data)
    print('config loaded')  

    self.call = Gtk.Entry()
    self.call.set_text(self.app_config.config_data.call)

    self.name = Gtk.Entry()
    self.name.set_text(self.app_config.config_data.name)

    self.qth = Gtk.Entry()
    self.qth.set_text(self.app_config.config_data.qth)

    self.locator = Gtk.Entry()
    self.locator.set_text(self.app_config.config_data.locator)

    self.rig1 = Gtk.Entry()
    self.rig1.set_text(self.app_config.config_data.rig1)

    self.rig2 = Gtk.Entry()
    self.rig2.set_text(self.app_config.config_data.rig2)

    self.rig3 = Gtk.Entry()
    self.rig3.set_text(self.app_config.config_data.rig3)

    self.server = Gtk.Entry()
    self.server.set_text(self.app_config.config_data.server)

    self.port = Gtk.Entry()
    self.port.set_text(self.app_config.config_data.port)

    self.ip = Gtk.Entry()
    self.ip.set_text(self.app_config.config_data.ip)

    self.log = Gtk.Entry()
    self.log.set_text(self.app_config.config_data.log)

    # ComboBox for Audio Devices
    self.audio_ls = Gtk.ListStore(str)
    self.audio_cbx   = Gtk.ComboBox()
    self.audio_cbx.set_model(self.audio_ls)

    audio_cell = Gtk.CellRendererText()
    self.audio_cbx.pack_start(audio_cell, True)
    self.audio_cbx.add_attribute(audio_cell, "text", 0)

    # fill ComboBox with Audio devices
    audio_d = subprocess.check_output(['/usr/bin/aplay', '-L']).decode("utf-8").split('\n') # +++ try select !!!
    audio_la=''
    audio_lz=0
    audio_d.insert(0, 'default')    #  ugly !!!!
    for audio_lz in audio_d:

      if len(audio_lz)>0:
        if (audio_lz[0]!=' ') and len(audio_lz)>5:
          self.audio_ls.append((audio_la[:25],))
          audio_la = audio_lz
          audio_lz += audio_lz
        else:
          if audio_lz==2:
            audio_la += audio_lz

    # select ComboBox entry from config
    audio_iter = self.audio_ls.get_iter_first()      #+++
    while self.audio_ls is not None:
      if (self.audio_ls.get_value(audio_iter,0)==self.app_config.config_data.audio):  #'default'
        break
      audio_iter = self.audio_ls.iter_next(audio_iter) 
    self.audio_cbx.set_active_iter(audio_iter) 


    lcall=Gtk.Label('Call'); lcall.set_alignment(0, 0.5) 
    grid.attach(lcall,0,0,1,1)
    grid.attach(self.call,1,0,1,1)

    lname=Gtk.Label('Name'); lname.set_alignment(0, 0.5)
    grid.attach(lname,0,1,1,1)
    grid.attach(self.name,1,1,1,1)

    lqth=Gtk.Label('QTH'); lqth.set_alignment(0, 0.5)
    grid.attach(lqth,0,2,1,1)
    grid.attach(self.qth,1,2,1,1)

    llocator=Gtk.Label('Home Locator'); llocator.set_alignment(0, 0.5)
    grid.attach(llocator,0,3,1,1)
    grid.attach(self.locator,1,3,1,1)

    lrig1=Gtk.Label('RIG1'); lrig1.set_alignment(0, 0.5)
    grid.attach(lrig1,0,4,1,1)
    grid.attach(self.rig1,1,4,1,1)

    lrig2=Gtk.Label('RIG2'); lrig2.set_alignment(0, 0.5)
    grid.attach(lrig2,0,5,1,1)
    grid.attach(self.rig2,1,5,1,1)

    lrig3=Gtk.Label('RIG3'); lrig3.set_alignment(0, 0.5)
    grid.attach(lrig3,0,6,1,1)
    grid.attach(self.rig3,1,6,1,1)

    lserver=Gtk.Label('Server'); lserver.set_alignment(0, 0.5)
    grid.attach(lserver,2,0,1,1)
    grid.attach(self.server,3,0,1,1)

    lport=Gtk.Label('Port'); lport.set_alignment(0, 0.5)
    grid.attach(lport,2,1,1,1)
    grid.attach(self.port,3,1,1,1)

    lip=Gtk.Label('Eigene IP'); lip.set_alignment(0, 0.5)
    grid.attach(lip,2,2,1,1)
    grid.attach(self.ip,3,2,1,1)

    llog_pah=Gtk.Label('Log Path'); llog_pah.set_alignment(0, 0.5) #+++
    grid.attach(llog_pah,2,3,1,1)
    grid.attach(self.log,3,3,1,1)

    laudio=Gtk.Label('Audio'); laudio.set_alignment(0, 0.5) #+++
    grid.attach(laudio,2,4,1,1)
    grid.attach(self.audio_cbx,3,4,1,1)

    btn_audio_test=Gtk.Button('Audio Test')
    grid.attach(btn_audio_test,4,4,1,1)

    save = Gtk.Button('save SETUP')
    grid.attach(save, 0, 8, 2, 1)

    save.connect("clicked", self.on_save_config_clicked)
    btn_audio_test.connect("clicked", self.on_audio_test_clicked)


  def on_save_config_clicked(self,button):

    server_tmp = self.app_config.config_data.server
    port_tmp   = self.app_config.config_data.port

    # config_data = Config_data
    self.app_config.config_data.call    = self.call.get_text()
    self.app_config.config_data.name    = self.name.get_text()
    self.app_config.config_data.qth     = self.qth.get_text()
    self.app_config.config_data.locator = self.locator.get_text()
    self.app_config.config_data.rig1    = self.rig1.get_text()
    self.app_config.config_data.rig2    = self.rig2.get_text()
    self.app_config.config_data.rig3    = self.rig3.get_text()
    self.app_config.config_data.server  = self.server.get_text()
    self.app_config.config_data.port    = self.port.get_text()
    self.app_config.config_data.ip      = self.ip.get_text()
    self.app_config.config_data.log     = self.log.get_text()
    self.app_config.config_data.audio   = self.audio_ls.get_value(self.audio_cbx.get_active_iter(),0)
    
    self.app_config.config_data.gc      = self.gc.gc_liststore.get_value(self.gc.gc_group_combo.get_active_iter(),0) # ??????

    self.app_config.save_ini(self.app_config.config_data) 

    self.sc.setConfig_data(self.app_config.config_data)

    if ((server_tmp  != self.server.get_text()) or (port_tmp != self.port.get_text()) ):
      self.sc.reconnect(True)

    self.mh.setText(self.app_config.config_data.call+'  '+self.app_config.config_data.name+'  '+self.app_config.config_data.qth+'  '+self.app_config.config_data.locator)
    
  #---- setup_btn_audio_test ----------------------------------  
  def on_audio_test_clicked(self,w):
    #print('button: Audio test')
    a = str(os.path.dirname(os.path.abspath(sys.argv[0])))+'/buzzer_x.wav'
    subprocess.Popen(["/usr/bin/aplay", '-D'+self.app_config.config_data.audio, a])

  #-----------------------
  def set_GcGroup(self, group):
    self.gc = group

  def set_Reconnect(self, sc):
    self.sc = sc

  def set_mainHeader(self, mh):
    self.mh = mh
