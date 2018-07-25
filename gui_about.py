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

import os, sys


    
#--------------------------------------------------------------------------
# --- About ----
about_tab = Gtk.Box()
about_tab.set_border_width(10)

about_grid = Gtk.Grid()
about_grid.set_column_spacing(10)
about_grid.set_row_spacing(10)
about_tab.add(about_grid)

about_img = Gtk.Image.new_from_file(os.path.dirname(os.path.abspath(sys.argv[0]))+'/Raute_klein.jpg')
about_img.set_alignment(0, 0.5)
about_grid.attach(about_img,0,0,1,1)

about_l1 = Gtk.Label(' '.rjust(50)+'HAM Messanger (Linux v0.0.1)')
about_l1.set_alignment(0, 0.5)
about_grid.attach(about_l1,0,0,1,1)

about_l2 = Gtk.Label('HAM Messenger')
about_l2.set_alignment(0, 0.5)
about_grid.attach(about_l2,0,1,1,1)

about_l3 = Gtk.Label('A information-and communication-tool for HAMNET')
about_l3.set_alignment(0, 0.5)
about_grid.attach(about_l3,0,3,1,1)

about_l4 = Gtk.Label('The HAMMessanger is designed to work on a store&forward basis.')
about_l4.set_alignment(0, 0.5)
about_grid.attach(about_l4,0,4,1,1)

about_l5 = Gtk.Label('The Store&Forward-Protocol designed by Alex OE1VQS & Kurt OE1KBC')
about_l5.set_alignment(0, 0.5)
about_grid.attach(about_l5,0,5,1,1)

about_l6 = Gtk.Label('The linux client was written by OE5RNL and OE5NVL based on OE1KBCs Windows .NET Client')
about_l6.set_alignment(0, 0.5)
about_grid.attach(about_l6,0,7,1,1)

about_l6a = Gtk.Label('Thanks Kurt !')
about_l6a.set_alignment(0, 0.5)
about_grid.attach(about_l6a,0,8,1,1)

about_l7 = Gtk.LinkButton("http://wiki.oevsv.at/index.php", "Digitaler Backbone")
#about_l7 = Gtk.Label('Documentation wiki.oevsv.at/index.php?Kategorie:Digitaler Backbone')
#about_l7.set_alignment(0, 0.5)
about_grid.attach(about_l7,0,10,1,1)

about_l8 = Gtk.LinkButton("http://news.ampr.at", "news.ampr.at")
about_grid.attach(about_l8,0,11,1,1)

about_l9 = Gtk.Label("GNU GENERAL PUBLIC LICENSE V3")
about_l9.set_alignment(0, 0.5)
about_grid.attach(about_l9,0,12,1,1)


                       



