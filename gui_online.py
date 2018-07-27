
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

class Online:

  def __init__(self):

    #--------------------------------------------------------------------------
    # --- online_ ----
    self.scrolledwindow = Gtk.ScrolledWindow()
    self.scrolledwindow.set_hexpand(True)
    self.scrolledwindow.set_vexpand(True)

    # create a liststore with one string column to use as the model
    self.liststore = Gtk.ListStore(str,str,str,str,str,str,str, float,str,str) 

    self.liststore.insert(0,['ONLINE', ' ', ' ', ' ' ,' ', ' ', ' ', time.time()+10, '#ffffff', '#000000'])
    #online_liststore.append(['OE5AAA', 'Hugo', '4020 Linz', 'JN78DH','18.06.00','44.143.97.20','1.5.4',12345])

    # sort by time (= LH) 
    self.liststore.set_sort_column_id(7, Gtk.SortType.DESCENDING)

    # create the TreeView using liststore
    # https://python-gtk-3-tutorial.readthedocs.io/en/latest/treeview.html
    #
    treeview = Gtk.TreeView(self.liststore)
    self.scrolledwindow.add(treeview)
    #online_treeview.drag_source_unset()

    # create the TreeViewColumns to display the data    
    tvcall = Gtk.TreeViewColumn('Call')
    tvname = Gtk.TreeViewColumn('Name')
    tvinfo = Gtk.TreeViewColumn('Info')
    tvLOC = Gtk.TreeViewColumn('LOC')
    tvLH = Gtk.TreeViewColumn('LH')
    tvIP = Gtk.TreeViewColumn('IP')
    tvversion = Gtk.TreeViewColumn('Version')

    # add columns to treeview
    treeview.append_column(tvcall)
    treeview.append_column(tvname)
    treeview.append_column(tvinfo)
    treeview.append_column(tvLOC)
    treeview.append_column(tvLH)
    treeview.append_column(tvIP)
    treeview.append_column(tvversion)

    # set the call text bold
    cell1 = Gtk.CellRendererText()
    cell1.props.weight_set = True
    cell1.props.weight = Pango.Weight.BOLD

    cell2 = Gtk.CellRendererText()
    #online_cell.set_property('cell-background', 'green') #white') #green')

    tvcall.pack_start(   cell1, True); tvcall.set_attributes(   cell1, text=0)
    tvname.pack_start(   cell2, True); tvname.set_attributes(   cell2, text=1)
    tvinfo.pack_start(   cell2, True); tvinfo.set_attributes(   cell2, text=2)
    tvLOC.pack_start(    cell2, True); tvLOC.set_attributes(    cell2, text=3)
    tvLH.pack_start(     cell2, True); tvLH.set_attributes(     cell2, text=4)
    tvIP.pack_start(     cell2, True); tvIP.set_attributes(     cell2, text=5)
  
    tvversion.pack_start(cell2, True); tvversion.set_attributes(cell2, text=6)
    # 7 time for sort
    # 8 background
    # 9 foreground

    tvcall.add_attribute(cell1,  "background", 8)
    tvcall.add_attribute(cell1,  "foreground", 9)

    tvname.add_attribute(cell2,  "background", 8)
    tvname.add_attribute(cell2,  "foreground", 9)

    # make treeview searchable
    #online_treeview.set_search_column(0)

    # Allow sorting on the column
    #online_tvcolumn.set_sort_column_id(0)

    # Allow drag and drop reordering of rows
    #online_treeview.set_reorderable(True)

    #online_window.add(online_treeview)


  def UpdateOnlineCall(self, call):

      #self.liststore.append([setup_config_data.call, 'Hugo', '1234 Ort', 'JN00AA','18.06.00','44.143.97.20','1.5.4',12345])

      found = False
      b = self.liststore.get_iter_first()      
      # skip online info line IF NOT NONE  
      self.liststore.set_value(b,7,time.time()+300)
      b = self.liststore.iter_next(b) 
      
      while b is not None:
        
        # delete 'OFFLINE' row
        if (self.liststore.get_value(b,0)=='OFFLINE'):
          self.liststore.remove(b)

        old = (self.liststore.get_value(b,7) < (time.time()-80))        
        if old:   
          self.liststore.set_value(b,8,'#f55e5e') # background: red  
          self.liststore.set_value(b,9,'#000000') # foregrounf: black           
        else:
          self.liststore.set_value(b,8,'#98f887') # foreground: green
          self.liststore.set_value(b,9,'#000000') # foreground: black 
          
        if self.liststore.get_value(b,0) == call.call:
          #print('online: update user: '+str(call.call))
          found = True   

          if old:
            self.liststore.set_value(b,8,'#98f887') # reactivate call -> green
            self.liststore.set_value(b,9,'#000000') # foreground: black

          self.liststore.set_value(b,1,str(call.name))
          self.liststore.set_value(b,2,str(call.info))
          self.liststore.set_value(b,3,str(call.locator))
          self.liststore.set_value(b,4,str(call.lh))
          self.liststore.set_value(b,5,str(call.ip))
          self.liststore.set_value(b,6,str(call.version))
          self.liststore.set_value(b,7,time.time())
          
        b = self.liststore.iter_next(b) 
      # end while

      if found == False:
        #print('online: insert user: '+str(call.call))
        self.liststore.append([call.call, call.name, call.info, call.locator ,str(call.lh), call.ip, call.version, time.time(),'#98f887', '#000000'])
      
      # Insert 'OFFLINE' row, if needed
      b = self.liststore.get_iter_first()   
      self.liststore.set_value(b,7,time.time()+300)
      b = self.liststore.iter_next(b)      
      while b is not None:
        if self.liststore.get_value(b,8) == '#f55e5e': # red
          self.liststore.insert_before(b,['OFFLINE', '', '', '','','','',self.liststore.get_value(b,7)+1, '#ffffff','#000000']) # whilte        
          break
        b = self.liststore.iter_next(b) 


  #-------------------------------------------------
  def SetOfflineCall(self):
    b = self.liststore.get_iter_first()      
    # skip online info line IF NOT NONE  
    self.liststore.set_value(b,7,time.time()+300)
    b = self.liststore.iter_next(b) 
    while b is not None:
      self.liststore.set_value(b,8,'#f55e5e')
      b = self.liststore.iter_next(b) 
    pass