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

import time

#--------------------------------------------------------------------------
# --- History ----

class History():

  def __init__(self):

    def treeview_changed(widget, event, data=None):
        #print('treeview_changed')
        adj = scrolledwindow.get_vadjustment()
        adj.set_value( 1 )


    self.frame = Gtk.Frame()
    self.frame.set_label(" History ")

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    # create a liststore with one string column to use as the model
    self.liststore = Gtk.ListStore(str,str,str,str,str, int,str,str)

    # sort by time (= LH) 
    self.liststore.set_sort_column_id(5, Gtk.SortType.DESCENDING)

    # create the TreeView using liststore
    treeview = Gtk.TreeView(self.liststore)
    treeview.connect('size-allocate', treeview_changed) #---

    scrolledwindow.add(treeview)

    # create the TreeViewColumns to display the data        
    tvtyp  = Gtk.TreeViewColumn('Typ')
    tvtime = Gtk.TreeViewColumn('Time')
    tvsrc  = Gtk.TreeViewColumn('Src')
    tvdst  = Gtk.TreeViewColumn('Dst')
    tvtext = Gtk.TreeViewColumn('Text')

    # add a row with text and a stock item - color strings forthe background
    #self.liststore.append([' ', '19.06.2018', 'src', 'dst','Das ist der Text'])

    # add columns to treeview
    treeview.append_column(tvtyp)
    treeview.append_column(tvtime)
    treeview.append_column(tvsrc)
    treeview.append_column(tvdst)
    treeview.append_column(tvtext)

    cell = Gtk.CellRendererText()
    #history_cell.set_property('cell-background', 'white') #green') #---

    tvtyp.pack_start(cell, True);    tvtyp.set_attributes(cell,  text=0)
    tvtime.pack_start(cell, True);   tvtime.set_attributes(cell, text=1)
    tvsrc.pack_start(cell,  True);   tvsrc.set_attributes(cell,  text=2)
    tvdst.pack_start(cell,  True);   tvdst.set_attributes(cell,  text=3)
    tvtext.pack_start(cell, True);   tvtext.set_attributes(cell, text=4)
    # 5 time for sort
    # 6 backgroundColor
    # 7 foregroundColor

    tvtyp.add_attribute(cell, "background", 6)
    tvtyp.add_attribute(cell, "foreground", 7)


    # make treeview searchable
    treeview.set_search_column(0)

    # Allow sorting on the column
    #self.tvcolumn.set_sort_column_id(0)

    # Allow drag and drop reordering of rows
    treeview.set_reorderable(True)

    #self.window.add(self.treeview)

    self.frame.add(scrolledwindow)


  #-------------------------------------------------
  def InsertHistoryCall(self,hist): 
    if   hist.dst == 'ALL':
      backgroundColor = '#ffffff' # white
      foregroundColor = '#0000ff' # blue
    elif hist.dst == 'CQ':
      backgroundColor = '#faf86a' # yellow
      foregroundColor = '#000000' # black      
    elif hist.dst == 'EM':
      backgroundColor = '#ff0000' # red
      foregroundColor  = '#ffffff'       
    elif hist.payloadType == 4:   #GC
      backgroundColor = '#00ff00' # green
      foregroundColor = '#000000' # green       
    else:
      backgroundColor = '#ffffff'
      foregroundColor  = '#000000'        

    self.liststore.insert(0,[str(hist.htype), str(hist.time), str(hist.src), str(hist.dst), str(hist.text), time.time(), backgroundColor, foregroundColor]) 

