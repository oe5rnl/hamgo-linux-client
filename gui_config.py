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

setup_tab = Gtk.Box()
setup_tab.set_border_width(10)

setup_grid = Gtk.Grid()
setup_grid.set_column_spacing(10) 
setup_grid.set_row_spacing(10)
setup_tab.add(setup_grid)

app_config = Config()
setup_config_data = app_config.getConfigData()
#self.app_server_connector.setConfig_data(setup_config_data)
print('config loaded')  

setup_call = Gtk.Entry()
setup_call.set_text(setup_config_data.call)

setup_name = Gtk.Entry()
setup_name.set_text(setup_config_data.name)

setup_qth = Gtk.Entry()
setup_qth.set_text(setup_config_data.qth)

setup_locator = Gtk.Entry()
setup_locator.set_text(setup_config_data.locator)

setup_rig1 = Gtk.Entry()
setup_rig1.set_text(setup_config_data.rig1)

setup_rig2 = Gtk.Entry()
setup_rig2.set_text(setup_config_data.rig2)

setup_rig3 = Gtk.Entry()
setup_rig3.set_text(setup_config_data.rig3)

setup_server = Gtk.Entry()
setup_server.set_text(setup_config_data.server)

setup_port = Gtk.Entry()
setup_port.set_text(setup_config_data.port)

setup_ip = Gtk.Entry()
setup_ip.set_text(setup_config_data.ip)

setup_log = Gtk.Entry()
setup_log.set_text(setup_config_data.log)

# ComboBox for Audio Devices
setup_audio_ls = Gtk.ListStore(str)
setup_audio_cbx   = Gtk.ComboBox()
setup_audio_cbx.set_model(setup_audio_ls)

setup_audio_cell = Gtk.CellRendererText()
setup_audio_cbx.pack_start(setup_audio_cell, True)
setup_audio_cbx.add_attribute(setup_audio_cell, "text", 0)

# fill ComboBox with Audio devices
setup_audio_d = subprocess.check_output(['/usr/bin/aplay', '-L']).decode("utf-8").split('\n') # +++ try select !!!
setup_audio_la=''
setup_audio_lz=0
setup_audio_d.insert(0, 'default')    #  ugly !!!!
for setup_audio_lz in setup_audio_d:

  if len(setup_audio_lz)>0:
    if (setup_audio_lz[0]!=' ') and len(setup_audio_lz)>5:
      setup_audio_ls.append((setup_audio_la[:25],))
      setup_audio_la = setup_audio_lz
      setup_audio_lz += setup_audio_lz
    else:
      if setup_audio_lz==2:
        setup_audio_la += setup_audio_lz

# select ComboBox entry from config
setup_audio_iter = setup_audio_ls.get_iter_first()      #+++
while setup_audio_ls is not None:
  if (setup_audio_ls.get_value(setup_audio_iter,0)==setup_config_data.audio):  #'default'
    break
  setup_audio_iter = setup_audio_ls.iter_next(setup_audio_iter) 
setup_audio_cbx.set_active_iter(setup_audio_iter) 


setup_lcall=Gtk.Label('Call'); setup_lcall.set_alignment(0, 0.5) 
setup_grid.attach(setup_lcall,0,0,1,1)
setup_grid.attach(setup_call,1,0,1,1)

setup_lname=Gtk.Label('Name'); setup_lname.set_alignment(0, 0.5)
setup_grid.attach(setup_lname,0,1,1,1)
setup_grid.attach(setup_name,1,1,1,1)

setup_lqth=Gtk.Label('QTH'); setup_lqth.set_alignment(0, 0.5)
setup_grid.attach(setup_lqth,0,2,1,1)
setup_grid.attach(setup_qth,1,2,1,1)

setup_llocator=Gtk.Label('Home Locator'); setup_llocator.set_alignment(0, 0.5)
setup_grid.attach(setup_llocator,0,3,1,1)
setup_grid.attach(setup_locator,1,3,1,1)

setup_lrig1=Gtk.Label('RIG1'); setup_lrig1.set_alignment(0, 0.5)
setup_grid.attach(setup_lrig1,0,4,1,1)
setup_grid.attach(setup_rig1,1,4,1,1)

setup_lrig2=Gtk.Label('RIG2'); setup_lrig2.set_alignment(0, 0.5)
setup_grid.attach(setup_lrig2,0,5,1,1)
setup_grid.attach(setup_rig2,1,5,1,1)

setup_lrig3=Gtk.Label('RIG3'); setup_lrig3.set_alignment(0, 0.5)
setup_grid.attach(setup_lrig3,0,6,1,1)
setup_grid.attach(setup_rig3,1,6,1,1)

setup_lserver=Gtk.Label('Server'); setup_lserver.set_alignment(0, 0.5)
setup_grid.attach(setup_lserver,2,0,1,1)
setup_grid.attach(setup_server,3,0,1,1)

setup_lport=Gtk.Label('Port'); setup_lport.set_alignment(0, 0.5)
setup_grid.attach(setup_lport,2,1,1,1)
setup_grid.attach(setup_port,3,1,1,1)

setup_lip=Gtk.Label('Eigene IP'); setup_lip.set_alignment(0, 0.5)
setup_grid.attach(setup_lip,2,2,1,1)
setup_grid.attach(setup_ip,3,2,1,1)

setup_llog_pah=Gtk.Label('Log Path'); setup_llog_pah.set_alignment(0, 0.5) #+++
setup_grid.attach(setup_llog_pah,2,3,1,1)
setup_grid.attach(setup_log,3,3,1,1)

setup_laudio=Gtk.Label('Audio'); setup_laudio.set_alignment(0, 0.5) #+++
setup_grid.attach(setup_laudio,2,4,1,1)
setup_grid.attach(setup_audio_cbx,3,4,1,1)

setup_btn_audio_test=Gtk.Button('Audio Test')
setup_grid.attach(setup_btn_audio_test,4,4,1,1)

setup_save = Gtk.Button('save SETUP')
setup_grid.attach(setup_save, 0, 8, 2, 1)


