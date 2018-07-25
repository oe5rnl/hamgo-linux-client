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

from gui_config import setup_config_data

#-------------------------------------------------------------------------
# --- broadcast ---

bc_grid = Gtk.Grid()
bc_grid.set_column_spacing(10) 
bc_grid.set_row_spacing(10)

bc_content = Gtk.Box()
bc_content.set_border_width(10)        
bc_content.add(bc_grid)

bc_scrolledwindow = Gtk.ScrolledWindow()
bc_scrolledwindow.set_hexpand(True)
bc_scrolledwindow.set_vexpand(True)

# start-textview
bc_txt_buf = Gtk.TextBuffer()
bc_txt_buf.set_text("Text")
bc_textview = Gtk.TextView(buffer=bc_txt_buf)
bc_textview.set_wrap_mode(Gtk.WrapMode.WORD)
bc_scrolledwindow.add(bc_textview)
# end-textview
  
bc_send = Gtk.Button('send Broadcast')        

bc_grid.attach(bc_scrolledwindow, 0, 0, 1, 1)
#bc_grid.attach(bc_entry_txt, 0, 0, 1, 1)
bc_grid.attach(Gtk.Label(""), 0, 1, 2, 1)
bc_grid.attach(bc_send, 0, 2, 2, 1)
      


#--------------------------------------------------------------------------
# CQ

cq_grid = Gtk.Grid()
cq_grid.set_column_spacing(10) 
cq_grid.set_row_spacing(10)

cq_content = Gtk.Box()
cq_content.set_border_width(10)        
cq_content.add(cq_grid)

cq_scrolledwindow = Gtk.ScrolledWindow()
cq_scrolledwindow.set_hexpand(True)
cq_scrolledwindow.set_vexpand(True)

# start-textview
cq_txt_buf = Gtk.TextBuffer()
cq_txt_buf.set_text("CQ Text")
cq_textview = Gtk.TextView(buffer=cq_txt_buf)
cq_textview.set_wrap_mode(Gtk.WrapMode.WORD)
cq_scrolledwindow.add(cq_textview)
# end-textview
  
cq_send = Gtk.Button('send CQ')        

#cq_sendRefresh = Gtk.Button('Refresh')        
#cq_sendRefresh.connect("clicked", cq_on_sendRefresh_clicked) #--- unten

cq_grid.attach(cq_scrolledwindow, 0, 0, 1, 1)
#cq_grid.attach(self.cq_entry_txt, 0, 0, 1, 1)
cq_grid.attach(Gtk.Label(""), 0, 1, 2, 1)
cq_grid.attach(cq_send, 0, 2, 2, 1)
#cq_grid.attach(cq_sendRefresh, 3, 2, 2, 1)
    


#--------------------------------------------------------------------------
# group call

def gc_cbx_changed(e):
  #'gc_cbx_changed')
  #setup_config_data.gc = #+++
  pass

gc_grid = Gtk.Grid()
gc_grid.set_column_spacing(10) 
gc_grid.set_row_spacing(10)

gc_content = Gtk.Box()
gc_content.set_border_width(10)        
gc_content.add(gc_grid)

gc_scrolledwindow = Gtk.ScrolledWindow()
gc_scrolledwindow.set_hexpand(True)
gc_scrolledwindow.set_vexpand(True)

# ComboBox for GC 
gc_liststore = Gtk.ListStore(str)
gc_group_combo  = Gtk.ComboBox()
gc_group_combo.set_model(gc_liststore)

gc_group_combo.connect("changed", gc_cbx_changed)

gc_group_cell = Gtk.CellRendererText()
gc_group_combo.pack_start(gc_group_cell, True)
gc_group_combo.add_attribute(gc_group_cell, "text", 0)

gc_liststore.append(("'OE5RNL fake !'",))
gc_liststore.append(("OE1",))
gc_liststore.append(("OE2",))             
gc_liststore.append(("OE3",))             
gc_liststore.append(("OE4",))             
gc_liststore.append(("OE5",))             
gc_liststore.append(("OE6",))             
gc_liststore.append(("OE7",))             
gc_liststore.append(("OE8",))             
gc_liststore.append(("OE9",))             
gc_liststore.append(("DVINTERN",))             

# select ComboBox entry from config
gc_iter = gc_liststore.get_iter_first()      #+++
while gc_liststore is not None:
  if (gc_liststore.get_value(gc_iter,0)==setup_config_data.gc):  #'default'
    break
  gc_iter = gc_liststore.iter_next(gc_iter) 
gc_group_combo.set_active_iter(gc_iter) 

# Message text
gc_txt_buf = Gtk.TextBuffer()
gc_txt_buf.set_text("GC Text")
gc_textview = Gtk.TextView(buffer=gc_txt_buf)
gc_textview.set_wrap_mode(Gtk.WrapMode.WORD)
gc_scrolledwindow.add(gc_textview)

gc_send = Gtk.Button('send Group Call')        

gc_grid.attach(gc_group_combo, 0, 0, 1, 1) 
gc_grid.attach(gc_scrolledwindow, 0, 1, 1, 1)
gc_grid.attach(Gtk.Label(""), 0, 2, 2, 1)
gc_grid.attach(gc_send, 0, 3, 2, 1)


#--------------------------------------------------------------------------
# --- Em

em_grid = Gtk.Grid()
em_grid.set_column_spacing(10) 
em_grid.set_row_spacing(10)

em_content = Gtk.Box()
em_content.set_border_width(10)        
em_content.add(em_grid)

em_scrolledwindow = Gtk.ScrolledWindow()
em_scrolledwindow.set_hexpand(True)
em_scrolledwindow.set_vexpand(True)

# start-textview
em_txt_buf = Gtk.TextBuffer()
em_txt_buf.set_text("EM Text")
em_textview = Gtk.TextView(buffer=em_txt_buf)
em_textview.set_wrap_mode(Gtk.WrapMode.WORD)
em_scrolledwindow.add(em_textview)
# end-textview
  
em_send = Gtk.Button('send Emergency message')        
#em_sendEmergency.connect("clicked", em_on_sendEmergency_clicked) #---

em_grid.attach(em_scrolledwindow, 0, 0, 1, 1)
#em_grid.attach(em_entry_txt, 0, 0, 1, 1)
em_grid.attach(Gtk.Label(""), 0, 1, 2, 1)
em_grid.attach(em_send, 0, 2, 2, 1)

