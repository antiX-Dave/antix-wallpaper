#!/usr/bin/env python
# Dependencies: feh, rox (pinboard), login_background.sh, gtk, pygtk,
# xset-root, desktop_tool, python os mod, python re mod, python sys mod
# File Name: wallpaper.py
# Version: 2.1
# Purpose: allows the user to select a meathod for setting the wallpaper, 
#          as well as a wallpaper / color / default folder based on their
#          choice of options. Requires window manager session codename to
#          be recorded in $DESKTOP_CODE. 
# Authors: Dave

# Copyright (C) antiXCommunity http://antix.freeforums.org
# License: gplv2
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
################################################################################
#################################################################
import pygtk, gtk
pygtk.require('2.0')
import os
import re
import sys
from desktop_tool import DesktopToolWidget
from desktop_tool import get_icon as get_icon

#Set variables
class Var: 
    def write(self, variable, item):
        if variable == "SAVED":
            WRITE_FILE = Var.CONF_USER_FILE_WALLPAPERS+".tmp"
            READ_FILE = Var.CONF_USER_FILE_WALLPAPERS
            CONF_VARIABLE = Var.DESKTOP_CODE
        else:
            WRITE_FILE = Var.CONF_USER_FILE+".tmp"
            READ_FILE = Var.CONF_USER_FILE
            CONF_VARIABLE = variable
        
        text = file((WRITE_FILE), "w")
        text.write("")
        text.close()
        text = file((WRITE_FILE), "a")
        for line in open(READ_FILE, "r").xreadlines():
            if "#" not in line:
                if re.search(r'^%s=' % (CONF_VARIABLE), line):
                    text.write (CONF_VARIABLE+"="+item+"\n") 
                else:
                    text.write (line) 
            else:
                text.write (line) 
        text.close()        
        os.system("mv %s %s" % ((WRITE_FILE), (READ_FILE)))
                        
    def read(self):        
        var = Var
        var.USER_HOME = os.environ['HOME']
        var.DISPLAY = os.environ['DISPLAY']
        with open(var.USER_HOME+"/.antix-session/desktop-code"+var.DISPLAY, "r") as f:
            var.DESKTOP_CODE = f.readline()
            var.DESKTOP_CODE = re.sub(r'\n', '', var.DESKTOP_CODE)
        var.DESKTOP = re.sub(r'.*-', '', var.DESKTOP_CODE)
        if re.search(r'rox|space', var.DESKTOP_CODE):
			var.ICON_MANAGER = True
        else:
			var.ICON_MANAGER = False
        var.CONF_USER_DIR = var.USER_HOME+"/.antix-session/"
        var.CONF_USER_FILE = var.CONF_USER_DIR+"wallpaper.conf"
        var.CONF_USER_FILE_WALLPAPERS = var.CONF_USER_DIR+"wallpaper-list.conf"
        var.CONF_SYSTEM_FILE = "/usr/share/antix-settings/wallpaper/wallpaper.conf"
        var.CONF_SYSTEM_FILE_WALLPAPERS = "/usr/share/antix-settings/wallpaper/wallpaper-list.conf"
        
        if not os.path.exists(var.CONF_USER_DIR):
            os.system("mkdir %s" % (var.CONF_USER_DIR))
            os.system("cp %s %s" % ((var.CONF_SYSTEM_FILE),(var.CONF_USER_DIR)))
            os.system("cp %s %s" % ((var.CONF_SYSTEM_FILE_WALLPAPERS),(var.CONF_USER_DIR)))
        else:
            if not os.path.isfile(var.CONF_USER_FILE):
                os.system("cp %s %s" % ((var.CONF_SYSTEM_FILE),(var.CONF_USER_DIR)))
                os.system("cp %s %s" % ((var.CONF_SYSTEM_FILE_WALLPAPERS),(var.CONF_USER_DIR)))
            
        for line in open(var.CONF_USER_FILE, "r").xreadlines():
            if "#" not in line:
                if re.search(r'^.*=', line):
                    pieces = line.split('=')
                    var.VARIABLE=(pieces[0])
                    var.VARIABLE = re.sub(r'\n', '', var.VARIABLE)
                    OBJECT=(pieces[1])
                    OBJECT = re.sub(r'\n', '', OBJECT)
                    setattr(var, var.VARIABLE, OBJECT)
        
        FOUND="0"            
        print var.DESKTOP_CODE
        for line in open(var.CONF_USER_FILE_WALLPAPERS, "r").xreadlines():
            if "#" not in line:
                if re.search(r'^%s=' % (var.DESKTOP_CODE), line):
                    pieces = line.split('=')
                    OBJECT = (pieces[1])
                    OBJECT = re.sub(r'\n', '', OBJECT)
                    var.SAVED = OBJECT
                    FOUND = "1"
		
        if FOUND == "0":
            text = file((var.CONF_USER_FILE_WALLPAPERS), "a")
            text.write (var.DESKTOP_CODE+"="+var.DEFAULT+"\n") 
            text.close
            var.SAVED = var.DEFAULT

        var.IMAGE = var.SAVED
        var.CURRENTCOLOR = var.COLOR

class Error:
    def __init__(self, error):
        cmdstring = "yad --image=\"error\"\
        --title=\"user-management error\"\
        --text=\"user-management has run into an error,\
        \nplease rerun and correct the following error!\
        \n\n%s\n\"\
        --button=\"gtk-ok:0\"" % (error)
        os.system(cmdstring) 

class Build_Picture:
    def build_color(self):
        Build_Picture.image = gtk.VBox()
        Build_Picture.draw = gtk.DrawingArea()
        Build_Picture.color = Build_Picture.draw.get_colormap().alloc_color('#'+Var.CURRENTCOLOR)
        Build_Picture.draw.set_size_request(300, 200)
        Build_Picture.draw.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        Build_Picture.draw.modify_bg(gtk.STATE_NORMAL, Build_Picture.color)
        Build_Picture.image.pack_start(Build_Picture.draw)
        Build_Picture.label = gtk.Label("Note: you cannot change the color with rox desktop")
        Build_Picture.image.pack_start(Build_Picture.label)
        Build_Picture.label.show()
        Build_Picture.draw.show()
        MainWindow.imagebox.pack_start(Build_Picture.image)
        Build_Picture.image.show()
          
    def build_image(self, image):
        Build_Picture.pix = gtk.gdk.pixbuf_new_from_file_at_scale(image,300,200,True)
        #Build_Picture.pix = Build_Picture.pix.scale_simple(300, 200, gtk.gdk.INTERP_BILINEAR)
        Build_Picture.image = gtk.image_new_from_pixbuf(Build_Picture.pix)
        MainWindow.imagebox.pack_start(Build_Picture.image)
        Build_Picture.image.show()
       
class Picture_Select:
        
    def update_preview(self, dialog, preview):
        filename = dialog.get_preview_filename()
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 200,200)
            preview.set_from_pixbuf(pixbuf)
            have_preview = True
        except:
            have_preview = False
        dialog.set_preview_widget_active(have_preview)
        return
        
    def __init__(self,widget):
        dialog = gtk.FileChooserDialog("Open...", None, gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_current_folder(os.path.expanduser(Var.FOLDER))
        dialog.set_default_response(gtk.RESPONSE_OK)
        pixbuf = get_icon("wallpaper", 48)
        dialog.set_icon(pixbuf)
        
        filter = gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_mime_type("image/tiff")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.jpeg")
        filter.add_pattern("*.tiff")
        filter.add_pattern("*.tif")
        dialog.add_filter(filter)
  
        previewImage = gtk.Image()
        dialog.set_preview_widget(previewImage)
        dialog.set_use_preview_label(False)
        dialog.connect("update-preview", self.update_preview, previewImage)
  
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
          Var.IMAGE = dialog.get_filename()
          MainWindow.imagebox.remove(Build_Picture.image)
          Build_Picture().build_image(Var.IMAGE)
          
        elif response == gtk.RESPONSE_CANCEL:
  		  print "No file selected"  
        dialog.destroy()
      
class Folder_Select:
    def __init__(self,widget):
        dialog = gtk.FileChooserDialog("Open...", None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        pixbuf = get_icon("wallpaper", 48)
        dialog.set_icon(pixbuf)
        dialog.set_current_folder(os.path.expanduser(Var.FOLDER))
        dialog.set_default_response(gtk.RESPONSE_OK)
        
        filter = gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
          Var.FOLDER = dialog.get_filename()
          Var().write('FOLDER', Var.FOLDER)
        elif response == gtk.RESPONSE_CANCEL:
  		  print "No file selected"  
        dialog.destroy()
       
class ColorSelect:
    def color_changed_cb(self, widget):
        Var.CURRENTCOLOR = self.colorseldlg.colorsel.get_current_color()
        Var.CURRENTCOLOR = Var.CURRENTCOLOR.to_string()
        Var.CURRENTCOLOR = re.sub(r'#', '', Var.CURRENTCOLOR)
        MainWindow.imagebox.remove(Build_Picture.image)
        Build_Picture().build_color()

    def __init__(self, widget):
        self.color = Build_Picture.image.get_colormap().alloc_color('#'+Var.CURRENTCOLOR)
        self.colorseldlg = gtk.ColorSelectionDialog("Select background color")
        pixbuf = get_icon("wallpaper", 48)
        self.colorseldlg.set_icon(pixbuf)
        colorsel = self.colorseldlg.colorsel
        colorsel.set_previous_color(self.color)
        colorsel.set_current_color(self.color)
        colorsel.set_has_palette(True)
        colorsel.connect("color_changed", self.color_changed_cb)
        response = self.colorseldlg.run()

        if response -- gtk.RESPONSE_OK:
            self.color = colorsel.get_current_color()
            write_color = self.color.to_string()
            write_color = re.sub(r'#', '', write_color)
        else:
            MainWindow.image.modify_bg(gtk.STATE_NORMAL, self.color)

        self.colorseldlg.destroy()

class Help:
    def __init__(self, widget):
        text = open((Var.HELPFILE), "r")
        HELPTEXT = text.read()
        text.close
        help = gtk.Dialog()
        help.set_position(gtk.WIN_POS_CENTER)
        help.set_size_request(350, 350)
        help.set_resizable(False)
        help.set_title("antiX Wallpaper - help")
        pixbuf = get_icon("wallpaper", 48)
        help.set_icon(pixbuf)
  
        helptext = gtk.TextBuffer()
        helptext.set_text(HELPTEXT)
  
        view = gtk.TextView();
        view.set_buffer(helptext)
        view.set_editable(False)
        setting =view.get_buffer()
        view.set_wrap_mode(gtk.WRAP_WORD)
        view.show()
  
        textsw = gtk.ScrolledWindow()
        textsw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        textsw.add(view)
        textsw.set_size_request(350,300)
        textsw.show()
  
        help.vbox.pack_start(textsw, True, True, 0)
        help.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        
        help.run()
        help.destroy()
        
class About:
    def __init__(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("antiX Wallpaper")
        pixbuf = get_icon("wallpaper", 48)
        about.set_icon(pixbuf)
        about.set_version("2.1.0")
        about.set_copyright("(c)the antiX community")
        about.set_comments("This is an antiX application for setting the wallpaper on the preinstalled window managers")
        about.set_website("http://antix.freeforums.org")
        pixbuf = get_icon("wallpaper", 48)
        about.set_logo(pixbuf)
        about.run()
        about.destroy()

class MainWindow:
    def set(self, widget):
        def Static():
            Var().write('TYPE', 'static')
            Var().write('STYLE', style)
            Var().write('SAVED', Var.IMAGE)
            os.system("login_background.sh &")
          
        def No_Wallpaper():
            Var().write('TYPE', 'color')
            Var().write('COLOR', Var.CURRENTCOLOR)
            os.system("login_background.sh &")
          
        def Random_Wallpaper():
            Var().write('TYPE', 'random')
            Var().write('STYLE', style)
            os.system("login_background.sh &")
          
        def Random_Wallpaper_Timed():
            Var().write('TYPE', 'random-time')
            Var().write('STYLE', style)
            os.system("login_background.sh &")
        
        model = self.combo2.get_model()
        index = self.combo2.get_active()
        style = model[index][0]
        model = self.combo.get_model()
        index = self.combo.get_active()
        SELECT = model[index][0]
        options = {"Static" : Static, "No Wallpaper" : No_Wallpaper, "Random Wallpaper" : Random_Wallpaper, "Random Wallpaper Timed" : Random_Wallpaper_Timed}
        options[SELECT]()
    
    def combochange (self, widget):
        def Static():
            self.colorbutton.hide()
            self.folderbutton.hide()
            self.picturebutton.show()
            if Var.ICON_MANAGER != True:
                self.combo2.show()
            else:
		        self.combo2.hide()
            MainWindow.imagebox.remove(Build_Picture.image)
            Build_Picture().build_image(Var.IMAGE)
            
        def No_Wallpaper():
            self.picturebutton.hide()
            self.folderbutton.hide()
            self.combo2.hide()
            self.colorbutton.show()
            MainWindow.imagebox.remove(Build_Picture.image)
            Build_Picture().build_color()
            
        def Random_Wallpaper():
            self.colorbutton.hide()
            self.picturebutton.hide()
            self.folderbutton.show()
            if Var.ICON_MANAGER != True:
                self.combo2.show()
            else:
		        self.combo2.hide()
            MainWindow.imagebox.remove(Build_Picture.image)
            Build_Picture().build_image(Var.DEFAULT)
            
        def Random_Wallpaper_Timed():
            self.colorbutton.hide()
            self.picturebutton.hide()
            self.folderbutton.show()
            if Var.ICON_MANAGER != True:
                self.combo2.show()
            else:
		        self.combo2.hide()
            MainWindow.imagebox.remove(Build_Picture.image)
            Build_Picture().build_image(Var.DEFAULT)
            
        model = self.combo.get_model()
        index = self.combo.get_active()
        SELECT = model[index][0]
        options = {"Static" : Static, "No Wallpaper" : No_Wallpaper, "Random Wallpaper" : Random_Wallpaper, "Random Wallpaper Timed" : Random_Wallpaper_Timed}
        options[SELECT]()
      
      
    def __init__(self):
      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
      self.window.set_position(gtk.WIN_POS_CENTER)
      pixbuf = get_icon("wallpaper", 48)
      self.window.set_icon(pixbuf)
      self.window.set_size_request(350,350)
      self.window.set_title("antiX Wallpaper")

      self.menubar = gtk.MenuBar()

      self.menu = gtk.Menu()
      self.filemenu = gtk.MenuItem("Options")
      self.filemenu.set_submenu(self.menu)
      self.filemenu.show()
      
      self.helpmenu = gtk.ImageMenuItem(gtk.STOCK_HELP)
      self.helpmenu.connect("activate", Help)
      self.helpmenu.show()
      self.menu.append(self.helpmenu)

      self.aboutmenu = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
      self.aboutmenu.connect("activate", About)
      self.aboutmenu.show()
      self.menu.append(self.aboutmenu)

      self.foldermenu = gtk.ImageMenuItem(gtk.STOCK_OPEN)
      self.foldermenu.set_label("Default Folder")
      self.foldermenu.connect("activate", Folder_Select)
      self.foldermenu.show()
      self.menu.append(self.foldermenu)

      self.imagemenu = gtk.ImageMenuItem(gtk.STOCK_OPEN)
      self.imagemenu.set_label("Open Image")
      self.imagemenu.connect("activate", Picture_Select)
      self.imagemenu.show()
      self.menu.append(self.imagemenu)

      self.colormenu = gtk.ImageMenuItem(gtk.STOCK_OPEN)
      self.colormenu.set_label("Default Color")
      self.colormenu.connect("activate", ColorSelect)
      self.colormenu.show()
      self.menu.append(self.colormenu)

      self.exit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
      self.exit.connect("activate", lambda w: gtk.main_quit())
      self.exit.show()
      self.menu.append(self.exit)
      self.menu.show()

      self.menubar.append(self.filemenu)
      self.menubar.show()

      MainWindow.imagebox = gtk.HBox()
      MainWindow.imagebox.show()
      Build_Picture().build_image(Var.IMAGE)

      self.combo = gtk.combo_box_new_text()
      self.combo.append_text("Static")
      if Var.ICON_MANAGER != True:
          self.combo.append_text("No Wallpaper")
      self.combo.append_text("Random Wallpaper")
      self.combo.append_text("Random Wallpaper Timed")
      
      self.combo.set_active(0)
      self.combo.connect("changed", self.combochange)
      self.combo.show()
      
      self.combo2 = gtk.combo_box_new_text()
      self.combo2.append_text("scale")
      self.combo2.append_text("center")
      self.combo2.append_text("fill")
      self.combo2.set_active(0)
      if Var.ICON_MANAGER != True:
          self.combo2.show()
      else:
		  self.combo2.hide()

      self.folderbutton = gtk.Button()
      icon_button = DesktopToolWidget('Select Folder', 'document-open-folder', 30, gtk.ORIENTATION_HORIZONTAL, wrap = 7)
      self.folderbutton.add(icon_button)
      self.folderbutton.connect("clicked", Folder_Select)
      self.folderbutton.set_size_request(100,50)
      self.folderbutton.hide()

      self.picturebutton = gtk.Button()
      icon_button = DesktopToolWidget("Select Picture", 'insert-image', 30, gtk.ORIENTATION_HORIZONTAL, wrap = 7)
      self.picturebutton.add(icon_button)
      self.picturebutton.connect("clicked", Picture_Select)
      self.picturebutton.set_size_request(100,50)
      self.picturebutton.show()

      self.colorbutton = gtk.Button()
      icon_button = DesktopToolWidget('Select Color', 'color-picker', 30, gtk.ORIENTATION_HORIZONTAL, wrap = 7)
      self.colorbutton.add(icon_button)
      self.colorbutton.connect("clicked", ColorSelect)
      self.colorbutton.set_size_request(100,50)
      self.colorbutton.hide()
      
      self.closebutton = gtk.Button()
      icon_button = DesktopToolWidget('Close', 'dialog-close', 30, gtk.ORIENTATION_HORIZONTAL, wrap = 7)
      self.closebutton.add(icon_button)
      self.closebutton.connect("clicked", lambda w: gtk.main_quit())
      self.closebutton.set_size_request(100,50)
      self.closebutton.show()
      
      self.okbutton = gtk.Button()
      icon_button = DesktopToolWidget('Apply', 'dialog-ok-apply', 30, gtk.ORIENTATION_HORIZONTAL, wrap = 7)
      self.okbutton.add(icon_button)
      self.okbutton.connect("clicked", self.set)
      self.okbutton.set_size_request(100,50)
      self.okbutton.show()
      
      self.buttonbox = gtk.HButtonBox()
      self.buttonbox.pack_start(self.folderbutton)
      self.buttonbox.pack_start(self.colorbutton)
      self.buttonbox.pack_start(self.picturebutton)
      self.buttonbox.pack_start(self.closebutton)
      self.buttonbox.pack_start(self.okbutton)
      self.buttonbox.show()

      self.topbox = gtk.VBox()
      self.topbox.pack_start(self.menubar)
      self.topbox.pack_start(self.imagebox)
      self.topbox.pack_start(self.combo)
      self.topbox.pack_start(self.combo2)
      self.topbox.show()
      
      self.mainbox = gtk.VBox()
      self.mainbox.pack_start(self.topbox)
      self.mainbox.pack_start(self.buttonbox)
      self.mainbox.show()
      
      self.window.show()
      self.window.add(self.mainbox)
      self.window.connect("destroy", lambda w: gtk.main_quit())
      
    def main(self):
      gtk.main()
      
Var().read()
if __name__ == "__main__":
 base = MainWindow()
 base.main()
