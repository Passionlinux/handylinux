#!/usr/bin/env python
# -*- coding:Utf-8 -*- 


"""
Auteur :      thuban (thuban@yeuxdelibad.net)  
licence :     GNU General Public Licence v3

Description : Permet de copier rapidement des morceaux de text prédéfinis
Dépendances : python-gtk2
"""

import os
import pygtk
pygtk.require('2.0')
import gtk
import ConfigParser

name = "copcoll"
config = os.path.expanduser("~/.copcoll")
w,h = 240, 300 # largeur et hauteur

class Copcoll():
    def close_application(self, widget, event, data=None):
        gtk.main_quit()

    def set_clipboard(self, button, txt):
        self.clipboard.set_text(txt)
        return

    def add_to_config(self, titlewgt, txtwgt, section, dialog):
        title = titlewgt.get_text().strip()
        buf = txtwgt.get_buffer()
        start, end = buf.get_bounds()
        txt = buf.get_text(start,end)
        if txt != "" and title != "":
            self.conf.set(section, title, txt)

            dialog.destroy()
            self.reload()

    def delete_option(self, button, section, option):
        self.conf.remove_option(section,option)
        self.reload()

    def add_new_section(self, widget):
        name = widget.get_text().strip()
        if len(name) != 0:
            self.conf.add_section(name)
            self.reload()

    def reload(self):
        with open(config, 'wb') as configfile:
            self.conf.write(configfile)
        self.window.destroy()
        self.build_win()
        self.window.show_all()

    def add_new(self, widget, section):
        d = gtk.Dialog(title="Ajouter un raccourci")
        d.set_default_size(400, 200)

        titlelbl = gtk.Label("Titre")
        titlelbl.show()
        raclbl = gtk.Label("Nouveau texte")
        raclbl.set_size_request(150,-1)
        raclbl.show()

        titleentry = gtk.Entry()
        titleentry.show()
        racentry = gtk.TextView()
        racentry.set_size_request(150,-1)
        racentry.show()

        # on met ça dans une boîte
        box = gtk.HBox(False,2)
        box.pack_start(titlelbl, True, True, 3)
        box.pack_start(raclbl, True, True, 3)
        box.show()
        d.vbox.pack_start(box)

        box = gtk.HBox(False,2)
        box.pack_start(titleentry, True, True, 3)
        box.pack_start(racentry, True, True, 3)
        box.show()
        d.vbox.pack_start(box)
        
        addbtn = gtk.Button(label = "Ajouter")
        addbtn.connect_object("clicked", self.add_to_config, titleentry, racentry, section, d)
        addbtn.show()
        # ajout des objets au dialogue
        d.vbox.pack_start(addbtn)
        d.run()

    def show_sentences(self):
        self.section_list = gtk.Notebook()
        self.section_list.set_tab_pos(gtk.POS_LEFT)   
        self.section_list.set_scrollable(True)

        for s in self.conf.sections():
            bigbox = gtk.VBox(True,3)
            scrolled_window = gtk.ScrolledWindow()
            scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
            scrolled_window.add_with_viewport(bigbox)
            scrolled_window.set_size_request(w,-1)

            self.section_list.append_page(scrolled_window, gtk.Label(s))
            for o in self.conf.options(s):
                box = gtk.HBox(False,0)

                l = gtk.Label(o)
                box.pack_start(l, True, True, 10)
                
                bbox = gtk.HBox(True, 0)
                copy = gtk.Button()
                image = gtk.Image()
                image.set_from_stock(gtk.STOCK_COPY, gtk.ICON_SIZE_MENU)
                copy.set_image(image)
                copy.connect('clicked', self.set_clipboard, self.conf.get(s,o))

                delbtn = gtk.Button()
                image = gtk.Image()
                image.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU)
                delbtn.set_image(image)

                delbtn.connect('clicked', self.delete_option, s, o)
                bbox.pack_start(copy, False, False, 0)
                bbox.pack_start(delbtn, False, False, 0)

                box.pack_start(bbox, False, False, 0)

                bigbox.pack_start(box, False, False, 0)

            addbtn = gtk.Button(stock=gtk.STOCK_ADD)
            addbtn.connect("clicked", self.add_new, s)
            bigbox.pack_start(addbtn, False, False, 5)

        # pour ajouter des sections
        addbox = gtk.VBox()
        instruction = gtk.Label("Nom de la nouvelle catégorie: ")
        entry = gtk.Entry()
        entry.connect("activate", self.add_new_section) # entrée valide
        addbox.pack_start(instruction, False, True, 3)
        addbox.pack_start(entry, False, False, 20)

        addbtn = gtk.Button(stock=gtk.STOCK_ADD)
        addbtn.connect_object("clicked", self.add_new_section, entry )
        addbox.pack_start(addbtn, False, False, 10)


        addlabel = gtk.Image()
        addlabel.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_MENU)
        bulledesc = gtk.Tooltips()
        bulledesc.set_tip(addlabel, "Ajouter une catégorie")
        self.section_list.append_page(addbox, addlabel)

        self.mainbox.pack_start(self.section_list)

    def build_win(self):
        self.conf= ConfigParser.SafeConfigParser()
        if os.path.isfile(config):
            self.conf.read(config)
        else:
            self.conf.add_section('phrases')

        self.mainbox = gtk.VBox(True,0)
        self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)

        self.show_sentences()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.close_application)
        self.window.set_title(name)
        self.window.set_default_size(w,h)
        self.window.add(self.mainbox)

    def trayclic(self, widget):
        if self.window.get_skip_taskbar_hint():
            self.window.deiconify()
            self.window.set_skip_taskbar_hint(False)
        else:
            self.window.iconify()
            self.window.set_skip_taskbar_hint(True)

    def __init__(self):
        trayicon = gtk.status_icon_new_from_stock(gtk.STOCK_EDIT)
        trayicon.set_visible(True)
        trayicon.connect("activate", self.trayclic)
        self.build_win()
        self.window.show_all()

def main():
    copcoll = Copcoll()
    gtk.main()

    return 0

if __name__ == '__main__':
	main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

