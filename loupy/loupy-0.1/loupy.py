#!/usr/bin/python
# -*- coding:Utf-8 -*- 
"""

Auteur :      thuban (thuban@yeuxdelibad.net)  
licence :     GNU General Public Licence v3

Description : loupe d'écran

Dépendances : python-gtk

"""

import pygtk
pygtk.require('2.0')
import gtk
import time
import sys

import gettext
gettext.bindtextdomain('loupy', '/usr/share/locale')
gettext.textdomain('loupy')
_ = gettext.gettext

# taille de la loupe : 
width = 210
height = 100

class Loupe():
    def start(self):
        gtk.main()

    def quit(widget = None, event = None, data = None):
        gtk.main_quit()
        sys.exit(0)

    def move_win(self):
        y = self.y - height * self.zoom /2
        x = self.x - width * self.zoom /2

        if x < 0:
            x = 0
        elif x > self.sz[0] - width*self.zoom:
            x = self.sz[0] - width * self.zoom
        if y < 0 :
            y = 0
        elif y > self.sz[1] - height*self.zoom:
            y = self.sz[1] - height * self.zoom

        x = int(x)
        y = int(y)
        self.window.move(x, y)

    def cursor_move(self, widget = None, event = None):
        if self.follow_mouse: 
            self.x, self.y, mods = self.root.get_pointer()
            self.loupe()
    
    def scrot(self):
        destpb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,width,height)
        fromx = self.x - width/2
        if fromx < 0:
            fromx = 0
        elif fromx > self.sz[0] - width:
            fromx = self.sz[0] - width

        fromy = self.y - height/2
        if fromy < 0 :
            fromy = 0
        elif fromy > self.sz[1] - height:
            fromy = self.sz[1] - height

        self.pb.copy_area(fromx, fromy, width, height, destpb, 0, 0)
        scaled_buf = destpb.scale_simple(int(width*self.zoom), int(height*self.zoom),gtk.gdk.INTERP_BILINEAR)
        self.im.set_from_pixbuf(scaled_buf)

    def focus_lost(self, widget = None, event = None):
        if not self.ignorefocuslost and self.follow_mouse:
            self.x, self.y, mods = self.root.get_pointer()
            self.move_win()

    def scroll(self, widget = None, event = None):
        self.ignorefocuslost = False
        if (self.zoom + 0.5) * width < self.sz[0] and\
            (self.zoom + 0.5) * height < self.sz[1] and\
            event.direction == gtk.gdk.SCROLL_UP:
                self.zoom += 0.5
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            if self.zoom > 2:
                self.zoom -= 0.5 
        self.loupe()

    def reload(self):
        self.window.hide_all()
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,self.sz[0],self.sz[1])
        self.pb = pb.get_from_drawable(self.root,self.root.get_colormap(),0,0,0,0,self.sz[0],self.sz[1])
        self.window.show_all()

    def keypress(self, widget = None, event = None):
        self.ignorefocuslost = True
        if event.keyval == gtk.gdk.keyval_from_name('Escape'):
            self.quit()
        elif event.keyval == gtk.gdk.keyval_from_name('r'):
            self.reload()
        elif event.keyval == gtk.gdk.keyval_from_name('Up'):
            self.y -= 5
            self.loupe()
        elif event.keyval == gtk.gdk.keyval_from_name('Down'):
            self.y += 5
            self.loupe()
        elif event.keyval == gtk.gdk.keyval_from_name('Left'):
            self.x -= 5
            self.loupe()
        elif event.keyval == gtk.gdk.keyval_from_name('Right'):
            self.x += 5
            self.loupe()
        elif event.keyval == gtk.gdk.keyval_from_name('minus')\
                or event.keyval == gtk.gdk.keyval_from_name('KP_Subtract'):
            if self.zoom > 2:
                self.zoom -= 0.5
                self.loupe()
        elif event.keyval == gtk.gdk.keyval_from_name('plus') \
                or event.keyval == gtk.gdk.keyval_from_name('KP_Add'):
            self.zoom += 0.5
            self.loupe()

    def clic(self, widget, event):
        if event.button == 1:
            self.cachecache()
        elif event.button == 3:
            if self.follow_mouse == True:
                self.follow_mouse = False
            else:
                self.reload()
                self.follow_mouse = True

    def trayclic(self, widget, event):
        if event.button == 1:
            self.cachecache()
        elif event.button == 3:
            self.menu()

    def cachecache(self):
        if self.isvisible:
            self.window.iconify()
            self.isvisible = False
        else:
            pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,self.sz[0],self.sz[1])
            self.pb = pb.get_from_drawable(self.root,self.root.get_colormap(),0,0,0,0,self.sz[0],self.sz[1])
            self.window.deiconify()
            self.isvisible = True

    def menu(self):
        m = gtk.MessageDialog(type=gtk.MESSAGE_INFO,\
                    buttons = gtk.BUTTONS_OK)
        m.set_markup(_("""<big>Loupy</big> : a simple passive magnifier.
powered by python, dev by Thuban
------
Usage :
- Left-click hide the magnifier (but still available from the systray icon).
- Right-click anchors the magnifier. Another right-click releases it.
- Mouse wheel, or press + and - keys to zoom in and out.
- Refresh the magnifier with the r key.
- You can use keyboard arrows to move the magnifier.
- Press Escape to stop the magnifier."""))
        ret = m.run()
        if ret == gtk.RESPONSE_DELETE_EVENT or ret == gtk.RESPONSE_OK:
            m.destroy()

    def loupe(self):
        self.scrot()
        self.move_win()

    def __init__(self):

        # fenêtre root
        self.root = gtk.gdk.get_default_root_window()
        self.sz = self.root.get_size()
        self.x, self.y, mods = self.root.get_pointer()
        self.zoom = 2
        self.ignorefocuslost = False
        self.isvisible = True
        self.follow_mouse = True

        # fenêtre principale
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(False)
        self.window.set_decorated(False)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_keep_above(True)
        self.window.move(self.x, self.y)
        self.window.set_border_width(1) # pour avoir une bordure noire
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.window.add_events(gtk.gdk.KEY_PRESS_MASK |\
                gtk.gdk.POINTER_MOTION_MASK | \
                gtk.gdk.BUTTON_PRESS_MASK |\
                gtk.gdk.SCROLL_MASK | \
                gtk.gdk.LEAVE_NOTIFY)

        self.window.connect("delete_event", self.quit)
        self.window.connect("motion-notify-event", self.cursor_move)
        self.window.connect("key-press-event", self.keypress)
        self.window.connect("scroll-event", self.scroll)
        self.window.connect("leave-notify-event", self.focus_lost)

        # image zoomée
        self.im = gtk.Image()
        evbox = gtk.EventBox()
        evbox.connect("button_release_event", self.clic)
        evbox.add(self.im)
        self.window.add(evbox)

        # icone dans le tray
        trayicon = gtk.status_icon_new_from_stock(gtk.STOCK_ZOOM_IN)
        trayicon.set_visible(True)
        trayicon.connect("button-press-event", self.trayclic)

        self.window.show_all()

        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,self.sz[0],self.sz[1])
        self.pb = pb.get_from_drawable(self.root,self.root.get_colormap(),0,0,0,0,self.sz[0],self.sz[1])
        self.loupe()


def main():
    prog = Loupe()
    prog.start()
    return 0        

if __name__ == "__main__":
    main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

