#---------------------------------------------------------------------------------------------------------------
#  filename: history.py
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
# --- History ----

def history_treeview_changed(widget, event, data=None):
    #print('treeview_changed')
    adj = history_scrolledwindow.get_vadjustment()
    adj.set_value( 1 )


history_frame = Gtk.Frame()
history_frame.set_label(" History ")

history_scrolledwindow = Gtk.ScrolledWindow()
history_scrolledwindow.set_hexpand(True)
history_scrolledwindow.set_vexpand(True)

# create a liststore with one string column to use as the model
history_liststore = Gtk.ListStore(str,str,str,str,str, int,str,str)

# sort by time (= LH) 
history_liststore.set_sort_column_id(5, Gtk.SortType.DESCENDING)

# create the TreeView using liststore
history_treeview = Gtk.TreeView(history_liststore)
history_treeview.connect('size-allocate', history_treeview_changed) #---

history_scrolledwindow.add(history_treeview)

# create the TreeViewColumns to display the data        
history_tvtyp  = Gtk.TreeViewColumn('Typ')
history_tvtime = Gtk.TreeViewColumn('Time')
history_tvsrc  = Gtk.TreeViewColumn('Src')
history_tvdst  = Gtk.TreeViewColumn('Dst')
history_tvtext = Gtk.TreeViewColumn('Text')

# add a row with text and a stock item - color strings forthe background
#self.liststore.append([' ', '19.06.2018', 'src', 'dst','Das ist der Text'])

# add columns to treeview
history_treeview.append_column(history_tvtyp)
history_treeview.append_column(history_tvtime)
history_treeview.append_column(history_tvsrc)
history_treeview.append_column(history_tvdst)
history_treeview.append_column(history_tvtext)

history_cell = Gtk.CellRendererText()
#history_cell.set_property('cell-background', 'white') #green') #---

history_tvtyp.pack_start(history_cell, True);    history_tvtyp.set_attributes(history_cell,  text=0)
history_tvtime.pack_start(history_cell, True);   history_tvtime.set_attributes(history_cell, text=1)
history_tvsrc.pack_start(history_cell,  True);   history_tvsrc.set_attributes(history_cell,  text=2)
history_tvdst.pack_start(history_cell,  True);   history_tvdst.set_attributes(history_cell,  text=3)
history_tvtext.pack_start(history_cell, True);   history_tvtext.set_attributes(history_cell, text=4)
# 5 time for sort
# 6 backgroundColor
# 7 foregroundColor

history_tvtyp.add_attribute(history_cell, "background", 6)
history_tvtyp.add_attribute(history_cell, "foreground", 7)


# make treeview searchable
history_treeview.set_search_column(0)

# Allow sorting on the column
#self.tvcolumn.set_sort_column_id(0)

# Allow drag and drop reordering of rows
history_treeview.set_reorderable(True)

#self.window.add(self.treeview)

history_frame.add(history_scrolledwindow)
