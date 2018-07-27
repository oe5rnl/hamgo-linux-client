#---------------------------------------------------------------------------------------------------------------
#  filename: debug_info.py
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

import os, sys, platform

import com

#--------------------------------------------------------------------------
# Debug Info
class Debug_info():

  def __init__(self):

    self.tab = Gtk.Box()
    self.tab.set_border_width(10)

    grid = Gtk.Grid()
    grid.set_column_spacing(10)
    grid.set_row_spacing(10)
    self.tab.add(grid)

    gtk    = os.popen("dpkg -l libgtk2.0-0 libgtk-3-0").readlines()
    self.osname = os.popen("/bin/cat /etc/os-release | /bin/grep PRETTY_NAME=").readlines()[0].split('=')[1]

    info_text =  'Aplication Name: HAM Messanger ('+com.version+')\n' \
            'Aplication executable name: '+str(os.path.dirname(os.path.abspath(sys.argv[0])))+'\n\n' \
            'OS-Name='+self.osname+'\n' \
            'Platform: System= '+str(platform.system())+'  Release='+str(platform.release())+'  Version='+str(platform.version())+'\n' \
            'Platform-machine= '+str(platform.machine())+'\n' \
            'Platform-platform='+str(platform.platform())+'\n' \
            'Python Version: '+sys.version.split('\n')[0]+' '+sys.version.split('\n')[1]+'\n' \
            '\nGtk Version:\n   '+str(gtk[6])+'   '+str(gtk[7])+' ' \
            '  gi.version_info '+str(gi.version_info)

    info_lbl = Gtk.Label(info_text)
    info_lbl.set_selectable(True)
    info_lbl.set_alignment(0, 0.5)
    grid.attach(info_lbl,0,0,1,1)


  def linux_distribution(self):
    try:
      return platform.linux_distribution()
    except:
      return "N/A"


