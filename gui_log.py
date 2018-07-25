#---------------------------------------------------------------------------------------------------------------
#  filename: log.py
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

#--------------------------------------------------------------------------
# --- Log ----
log_tab = Gtk.Box()
log_tab.set_border_width(10)

log_grid = Gtk.Grid()
log_grid.set_column_spacing(10) 
log_grid.set_row_spacing(10)

log_frame = Gtk.Frame()
log_frame.set_label(" Log ")

log_scrolledwindow = Gtk.ScrolledWindow()
log_scrolledwindow.set_hexpand(True)
log_scrolledwindow.set_vexpand(True)

# create a liststore with one string column to use as the model
log_liststore = Gtk.ListStore(str,str,str,str,str,str, int, str, str)

# sort by time (= LH) 
log_liststore.set_sort_column_id(5, Gtk.SortType.ASCENDING)

# create the TreeView using liststore
log_treeview = Gtk.TreeView(log_liststore)
#treeview.connect('size-allocate', self.treeview_changed)

# create the TreeViewColumns to display the data        
log_tvtime = Gtk.TreeViewColumn('Time')
log_tvtyp  = Gtk.TreeViewColumn('Type')
log_tvsrc  = Gtk.TreeViewColumn('Src')
log_tvdst  = Gtk.TreeViewColumn('Dst')
log_tvtext = Gtk.TreeViewColumn('Text')
log_tvpath = Gtk.TreeViewColumn('Path')

# add a row with text and a stock item - color strings fort he background
#log_liststore.append(['12.07.2018 00:37:10', 'BC', 'OE5RNL', 'ALL','Das ist der Text',';OE5XLL',time.time()])

# add columns to treeview
log_treeview.append_column(log_tvtime)
log_treeview.append_column(log_tvtyp)
log_treeview.append_column(log_tvsrc)
log_treeview.append_column(log_tvdst)
log_treeview.append_column(log_tvtext)
log_treeview.append_column(log_tvpath)

log_cell = Gtk.CellRendererText()
#log_cell.set_property('cell-background', 'white') #green')

log_tvtime.pack_start(log_cell, True);   log_tvtime.set_attributes(log_cell, text=0) 
log_tvtyp.pack_start(log_cell,  True);   log_tvtyp.set_attributes(log_cell,  text=1)
log_tvsrc.pack_start(log_cell,  True);   log_tvsrc.set_attributes(log_cell,  text=2)
log_tvdst.pack_start(log_cell,  True);   log_tvdst.set_attributes(log_cell,  text=3)
log_tvtext.pack_start(log_cell, True);   log_tvtext.set_attributes(log_cell, text=4)
log_tvpath.pack_start(log_cell, True);   log_tvpath.set_attributes(log_cell, text=5)
# 6 time
# 7 background-color

log_tvtime.add_attribute(log_cell, "background", 7)
log_tvtime.add_attribute(log_cell, "foreground", 8)


# # make treeview searchable
# log_treeview.set_search_column(0)

# Allow sorting on the column
#log_tvcolumn.set_sort_column_id(0)

# Allow drag and drop reordering of rows
log_treeview.set_reorderable(True)

# set gui elemets
log_tab.add(log_grid)
log_grid.attach(Gtk.Label('Search'), 0, 0, 1, 1)
log_grid.attach(log_frame, 0, 1, 1, 1)

log_frame.add(log_scrolledwindow)
log_scrolledwindow.add(log_treeview)

