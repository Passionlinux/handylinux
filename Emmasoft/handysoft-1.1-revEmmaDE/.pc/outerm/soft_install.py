#!/usr/bin/python3
# -*- coding:Utf-8 -*- 

"""

Auteur :      thuban 
licence :     GNU General Public Licence

Description : installateur pour handysoft
"""

from gi.repository import Gtk,GObject,Vte,GLib
import sys
import os

from handysoft_utils import *
import gettext
gettext.bindtextdomain(appname, '/usr/share/locale')
gettext.textdomain(appname)
_ = gettext.gettext

class Package_master():
    def __init__(self,message, cmd):
        cmd = "{} && exit 0 || exit 1\n".format(cmd)
        self.window = Gtk.Window(title=message)
        self.window.set_border_width(10)
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.set_icon_name("package")
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_default_size(400, -1)

        self.box = Gtk.VBox(spacing=2) #conteneur principal
        self.window.add(self.box)
        
        self.titlelabel = Gtk.Label()
        self.titlelabel.set_text("{}".format(message))
        self.box.pack_start(self.titlelabel, True, True, 2)

        # barre de progression
        self.progressbar = Gtk.ProgressBar()
        GObject.timeout_add(250,self.pulsate)

        self.box.pack_start(self.progressbar, True, True, 2)

        # le VTE
        self.terminal     = Vte.Terminal()
        self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/bash" ],
            ["PS1=\n"],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            None,
            )
        self.terminal.connect("child-exited", self.end)
        self.terminal.set_size_request(500,250)

        #terminal.connect("child-exited", Gtk.main_quit)
        self.terminal.set_size_request(500,250)

        buttonbox = Gtk.HBox()
        copybtn = Gtk.Button(stock = Gtk.STOCK_COPY)
        copybtn.connect("key_press_event", lambda x,y:self.copyterminal())
        copybtn.connect("button_release_event", lambda x,y:self.copyterminal())
        buttonbox.pack_start(copybtn, True, True, 5)

        hiddenbox = Gtk.VBox()
        hiddenbox.pack_start(self.terminal,True, True, 0)
        hiddenbox.pack_start(buttonbox,True, False, 5)

        expander = Gtk.Expander(label="Details")
        expander.set_resize_toplevel(True)
        expander.add(hiddenbox)
        self.box.pack_start(expander, True, True, 2)
        
        self.window.show_all()

        self.terminal.feed_child(cmd, len(cmd))
        self.terminal.set_property("input-enabled", False)

    def pulsate(self):
        self.progressbar.pulse()
        GObject.timeout_add(250, self.pulsate)

    def copyterminal(self):
        self.terminal.select_all()
        self.terminal.copy_clipboard()

    def end(self, term, exitstatus):
        self.progressbar.hide()
        if exitstatus == 0:
            self.titlelabel.set_markup(_("<span size='large'>☺ All changes applied with success</span>"))
        else:
            self.titlelabel.set_markup(_("<span size='large'>☹ An Error Occurred!</span>"))

        closebtn = Gtk.Button(stock = Gtk.STOCK_GO_BACK)
        closebtn.connect("button_release_event", lambda x,y: Gtk.main_quit())
        closebtn.connect("key_press_event", lambda x,y: Gtk.main_quit())
        self.box.pack_start(closebtn, True, True, 5)
        self.window.show_all()

def main():
    #print("usage : {} -m <message> -c <command>".format(sys.argv[0]))
    message = " ".join( sys.argv[sys.argv.index('-m')+1 : sys.argv.index('-c')])
    cmd = " ".join(sys.argv[(sys.argv.index('-c') +1):])

    if os.geteuid() != 0:
        import subprocess
        print("You need to have root privileges to run this script.")
        subprocess.call('gksudo "{} -m {} -c {}"'.format(os.path.realpath(__file__), message, cmd), shell=True)

    elif os.geteuid() == 0:
        win = Package_master(message, cmd)
        Gtk.main()

    
if __name__ == '__main__':
    main()
