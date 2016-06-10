#!/usr/bin/python
# -*-coding:utf-8-*

import pygtk
pygtk.require("2.0")
import gtk
import os

class Handy2Debian():

	def on_button1_clicked(self, widget):
		gtk.main_quit()

	def on_button2_clicked(self, widget):
		os.system("xfce4-terminal -e /usr/share/handy2debian/move2debian &")
		gtk.main_quit()

	def __init__(self):

		window = gtk.Window()
		window.set_title("Handy2Debian")
		window.connect("destroy", self.on_button1_clicked)
		window.set_default_size(300, 200)
		
		vBox = gtk.VBox()
		label = gtk.Label()
		label.set_text("\n                         Handy2Debian  \n" +
						"\n    A little tool to move to Debian \"classic\"   \n" +
						"    and delete HandyLinux configurations.   \n" +
                        "\n    !! Warning !!   \n" +
                        "    This script will reset to default value:   \n" +
                        "    - your panel,   \n" +
                        "    - your terminal,   \n" +
                        "    - your icon theme,   \n" +
                        "    - your Thunar file manager.   \n" +
                        "    - your GTK theme (windows look),   \n" +
                        "    - your desktop (launchers, wallpaper),   \n" +
                        "    - your session connection manager SLIM/LightDM,   \n" +
                        "    - your computer startup screen GRUB.   \n" +
                        "\n    This action can't be undone.    \n" +
						"\n    Do you want to move to Debian \"classic\" ?   \n" +
						"    your password will be asked.    \n" +
                        "    ")
		vBox.pack_start(label, False, False, 10)

		hBox = gtk.HBox()
		bouton1 = gtk.ToggleButton(label = "i keep HandyLinux")
		bouton1.connect("clicked", self.on_button1_clicked)
		bouton2 = gtk.ToggleButton(label = "i move to Debian")
		bouton2.connect("clicked", self.on_button2_clicked)
		hBox.add(bouton1)
		hBox.add(bouton2)

		vBox.pack_end(hBox,  False, False, 4)
		window.add(vBox)
		window.show_all()
		gtk.main()

if __name__ == '__main__':
	Handy2Debian()
