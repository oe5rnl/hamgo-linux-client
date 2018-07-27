#---------------------------------------------------------------------------------------------------------------
#  filename: about.py
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

import os, sys, com

class About():

  def __init__(self):
    
    #--------------------------------------------------------------------------
    # --- About ----
    self.tab = Gtk.Box()
    self.tab.set_border_width(10)

    grid = Gtk.Grid()
    grid.set_column_spacing(10)
    grid.set_row_spacing(10)
    self.tab.add(grid)

    img = Gtk.Image.new_from_file(os.path.dirname(os.path.abspath(sys.argv[0]))+'/Raute_klein.jpg')
    img.set_alignment(0, 0.5)
    grid.attach(img,0,0,1,1)

    l1 = Gtk.Label(' '.rjust(50)+'HAM Messanger (Linux'+com.version+')')
    l1.set_alignment(0, 0.5)
    grid.attach(l1,0,0,1,1)

    l2 = Gtk.Label('HAM Messenger')
    l2.set_alignment(0, 0.5)
    grid.attach(l2,0,1,1,1)

    l3 = Gtk.Label('A information-and communication-tool for HAMNET')
    l3.set_alignment(0, 0.5)
    grid.attach(l3,0,3,1,1)

    l4 = Gtk.Label('The HAMMessanger is designed to work on a store&forward basis.')
    l4.set_alignment(0, 0.5)
    grid.attach(l4,0,4,1,1)

    l5 = Gtk.Label('The Store&Forward-Protocol designed by Alex OE1VQS & Kurt OE1KBC')
    l5.set_alignment(0, 0.5)
    grid.attach(l5,0,5,1,1)

    l6 = Gtk.Label('The linux client was written by OE5RNL and OE5NVL based on OE1KBCs Windows .NET Client')
    l6.set_alignment(0, 0.5)
    grid.attach(l6,0,7,1,1)

    l6a = Gtk.Label('Thanks Kurt !')
    l6a.set_alignment(0, 0.5)
    grid.attach(l6a,0,8,1,1)

    l7 = Gtk.LinkButton("http://wiki.oevsv.at/index.php", "Digitaler Backbone")
    #l7 = Gtk.Label('Documentation wiki.oevsv.at/index.php?Kategorie:Digitaler Backbone')
    #l7.set_alignment(0, 0.5)
    grid.attach(l7,0,10,1,1)

    l8 = Gtk.LinkButton("http://news.ampr.at", "news.ampr.at")
    grid.attach(l8,0,11,1,1)

    l9 = Gtk.Label("GNU GENERAL PUBLIC LICENSE V3")
    l9.set_alignment(0, 0.5)
    grid.attach(l9,0,12,1,1)


                       



