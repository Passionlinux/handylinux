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
		label.set_text("\n                             Handy2Debian  \n" +
						"\n    Un outil simple pour passer à Debian \"classic\"   \n" +
						"    et effacer la configuration HandyLinux.   \n" +
                        "\n    !! Attention !!   \n" +
                        "    Ce script va rétablir les valeurs par défaut pour :   \n" +
                        "    - votre panel,   \n" +
                        "    - votre terminal,   \n" +
                        "    - votre thème d'icônes,   \n" +
                        "    - votre thème GTK (les fenêtres),   \n" +
                        "    - votre écran de démarrage GRUB,   \n" +
                        "    - votre gestionnaire de connexion SLIM/LightDM,   \n" +
                        "    - votre bureau (lanceurs, fond d'écran),   \n" +
                        "    - votre gestionnaire de fichiers Thunar.   \n" +
                        "\n    Cette action est définitive.    \n" +
						"\n    Désirez-vous passer à Debian \"classic\" ?   \n" +
						"    votre mot de passe vous sera demandé.    \n" +
                        "    ")
		vBox.pack_start(label, False, False, 10)

		hBox = gtk.HBox()
		bouton1 = gtk.ToggleButton(label = "je garde HandyLinux")
		bouton1.connect("clicked", self.on_button1_clicked)
		bouton2 = gtk.ToggleButton(label = "je passe à Debian")
		bouton2.connect("clicked", self.on_button2_clicked)
		hBox.add(bouton1)
		hBox.add(bouton2)

		vBox.pack_end(hBox,  False, False, 4)
		window.add(vBox)
		window.show_all()
		gtk.main()

if __name__ == '__main__':
	Handy2Debian()
