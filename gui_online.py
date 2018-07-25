
#---------------------------------------------------------------------------------------------------------------
#  filename: online.py
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

import time

#--------------------------------------------------------------------------
# --- online_ ----
online_scrolledwindow = Gtk.ScrolledWindow()
online_scrolledwindow.set_hexpand(True)
online_scrolledwindow.set_vexpand(True)

# create a liststore with one string column to use as the model
online_liststore = Gtk.ListStore(str,str,str,str,str,str,str, float,str,str) 

online_liststore.insert(0,['ONLINE', ' ', ' ', ' ' ,' ', ' ', ' ', time.time()+10, '#ffffff', '#000000'])
#online_liststore.append(['OE5AAA', 'Hugo', '4020 Linz', 'JN78DH','18.06.00','44.143.97.20','1.5.4',12345])

# sort by time (= LH) 
online_liststore.set_sort_column_id(7, Gtk.SortType.DESCENDING)

# create the TreeView using liststore
# https://python-gtk-3-tutorial.readthedocs.io/en/latest/treeview.html
#
online_treeview = Gtk.TreeView(online_liststore)
online_scrolledwindow.add(online_treeview)
#online_treeview.drag_source_unset()

# create the TreeViewColumns to display the data    
online_tvcall = Gtk.TreeViewColumn('Call')
online_tvname = Gtk.TreeViewColumn('Name')
online_tvinfo = Gtk.TreeViewColumn('Info')
online_tvLOC = Gtk.TreeViewColumn('LOC')
online_tvLH = Gtk.TreeViewColumn('LH')
online_tvIP = Gtk.TreeViewColumn('IP')
online_tvversion = Gtk.TreeViewColumn('Version')

# add columns to treeview
online_treeview.append_column(online_tvcall)
online_treeview.append_column(online_tvname)
online_treeview.append_column(online_tvinfo)
online_treeview.append_column(online_tvLOC)
online_treeview.append_column(online_tvLH)
online_treeview.append_column(online_tvIP)
online_treeview.append_column(online_tvversion)

# set the call text bold
online_cell1 = Gtk.CellRendererText()
online_cell1.props.weight_set = True
online_cell1.props.weight = Pango.Weight.BOLD

online_cell2 = Gtk.CellRendererText()
#online_cell.set_property('cell-background', 'green') #white') #green')

online_tvcall.pack_start(   online_cell1, True); online_tvcall.set_attributes(   online_cell1, text=0)
online_tvname.pack_start(   online_cell2, True); online_tvname.set_attributes(   online_cell2, text=1)
online_tvinfo.pack_start(   online_cell2, True); online_tvinfo.set_attributes(   online_cell2, text=2)
online_tvLOC.pack_start(    online_cell2, True); online_tvLOC.set_attributes(    online_cell2, text=3)
online_tvLH.pack_start(     online_cell2, True); online_tvLH.set_attributes(     online_cell2, text=4)
online_tvIP.pack_start(     online_cell2, True); online_tvIP.set_attributes(     online_cell2, text=5)
online_tvversion.pack_start(online_cell2, True); online_tvversion.set_attributes(online_cell2, text=6)
# 7 time for sort
# 8 background
# 9 foreground

online_tvcall.add_attribute(online_cell1,  "background", 8)
online_tvcall.add_attribute(online_cell1,  "foreground", 9)

online_tvname.add_attribute(online_cell2,  "background", 8)
online_tvname.add_attribute(online_cell2,  "foreground", 9)

# make treeview searchable
#online_treeview.set_search_column(0)

# Allow sorting on the column
#online_tvcolumn.set_sort_column_id(0)

# Allow drag and drop reordering of rows
#online_treeview.set_reorderable(True)

#online_window.add(online_treeview)

