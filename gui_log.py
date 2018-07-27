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

import time

class Log():

  def __init__(self):

    #--------------------------------------------------------------------------
    # --- Log ----
    self.tab = Gtk.Box()
    self.tab.set_border_width(10)

    grid = Gtk.Grid()
    grid.set_column_spacing(10) 
    grid.set_row_spacing(10)

    frame = Gtk.Frame()
    frame.set_label(" Log ")

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    # create a liststore with one string column to use as the model
    self.liststore = Gtk.ListStore(str,str,str,str,str,str, int, str, str)

    # sort by time (= LH) 
    self.liststore.set_sort_column_id(5, Gtk.SortType.ASCENDING)

    # create the TreeView using liststore
    treeview = Gtk.TreeView(self.liststore)
    #treeview.connect('size-allocate', self.treeview_changed)

    # create the TreeViewColumns to display the data        
    tvtime = Gtk.TreeViewColumn('Time')
    tvtyp  = Gtk.TreeViewColumn('Type')
    tvsrc  = Gtk.TreeViewColumn('Src')
    tvdst  = Gtk.TreeViewColumn('Dst')
    tvtext = Gtk.TreeViewColumn('Text')
    tvpath = Gtk.TreeViewColumn('Path')

    # add a row with text and a stock item - color strings fort he background
    #log_liststore.append(['12.07.2018 00:37:10', 'BC', 'OE5RNL', 'ALL','Das ist der Text',';OE5XLL',time.time()])

    # add columns to treeview
    treeview.append_column(tvtime)
    treeview.append_column(tvtyp)
    treeview.append_column(tvsrc)
    treeview.append_column(tvdst)
    treeview.append_column(tvtext)
    treeview.append_column(tvpath)

    cell = Gtk.CellRendererText()
    #log_cell.set_property('cell-background', 'white') #green')

    tvtime.pack_start(cell, True);   tvtime.set_attributes(cell, text=0) 
    tvtyp.pack_start(cell,  True);   tvtyp.set_attributes(cell,  text=1)
    tvsrc.pack_start(cell,  True);   tvsrc.set_attributes(cell,  text=2)
    tvdst.pack_start(cell,  True);   tvdst.set_attributes(cell,  text=3)
    tvtext.pack_start(cell, True);   tvtext.set_attributes(cell, text=4)
    tvpath.pack_start(cell, True);   tvpath.set_attributes(cell, text=5)
    # 6 time
    # 7 background-color

    tvtime.add_attribute(cell, "background", 7)
    tvtime.add_attribute(cell, "foreground", 8)


    # # make treeview searchable
    # log_treeview.set_search_column(0)

    # Allow sorting on the column
    #log_tvcolumn.set_sort_column_id(0)

    # Allow drag and drop reordering of rows
    treeview.set_reorderable(True)

    # set gui elemets
    self.tab.add(grid)
    grid.attach(Gtk.Label('Search'), 0, 0, 1, 1)
    grid.attach(frame, 0, 1, 1, 1)

    frame.add(scrolledwindow)
    scrolledwindow.add(treeview)


  #-------------------------------------------------
  def InsertLogCall(self, call): 
    #print('InsertLogCall: '+str(call.src))
    self.liststore.insert(0,[time.strftime("%a, %d %b %Y %H:%M:%S"), str(call.htype), str(call.src), str(call.dst), str(call.text), str(call.path),time.time(),'#ffffff', '#000000' ])
