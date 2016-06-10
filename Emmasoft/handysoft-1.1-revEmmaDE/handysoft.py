#!/usr/bin/python
# -*- coding:Utf-8 -*- 


"""

Auteur :      thuban <thuban@yeuxdelibad.net>  
licence :     GNU General Public Licence v3

Description :

    Remplacement de la logithèque debian pour handylinux

Dépendances : 
    python3-apt
    python3-gi
"""

import sys
import apt
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf
#import concurrent.futures
import threading
from time import sleep
import os

from handysoft_utils import *
from soft_install import *

import gettext
gettext.bindtextdomain(appname, '/usr/share/locale')
gettext.textdomain(appname)
_ = gettext.gettext


class DialogPackage(Gtk.Dialog):
    '''permet d'afficher une fenêtre avec des informations détaillées sur un paquet'''

    def change_bg_on_focus(self,widget,b):
        widget.modify_bg(Gtk.StateFlags.NORMAL, self.selected_bg_color)
        widget.modify_bg(Gtk.StateFlags.PRELIGHT, self.selected_bg_color)
        
    def change_bg_on_focus_leave(self,widget,b):
        widget.modify_bg(Gtk.StateFlags.NORMAL, None)
        widget.modify_bg(Gtk.StateFlags.PRELIGHT, None)

    def get_theme_colors(self):
        style_context = self.get_style_context()
        bg_color = style_context.lookup_color('bg_color')
        selected_bg_color = style_context.lookup_color('selected_bg_color')

        if bg_color[0]:
            self.bg_color = bg_color[1].to_color()
        else:
            self.bg_color = Gdk.color_parse("#eeeeee")
        if selected_bg_color[0]:
            self.selected_bg_color = selected_bg_color[1].to_color()
        else:
            self.selected_bg_color = Gdk.color_parse("#41B1FF")

    def change_focus_colors(self,i): # change colors of the widget i
        i.connect("focus_in_event", self.change_bg_on_focus)
        i.connect("enter_notify_event", self.change_bg_on_focus)
        i.connect("focus_out_event", self.change_bg_on_focus_leave)
        i.connect("leave_notify_event", self.change_bg_on_focus_leave)

    def do_access(self, widget):
        self.get_theme_colors()
        for i in widget:
            if type(i) == Gtk.Button: 
                self.change_focus_colors(i)
            elif type(i) == Gtk.StackSwitcher:
                self.change_focus_colors(i)
            elif type(i) == Gtk.HBox:
                self.do_access(i)
            elif type(i) == Gtk.VBox:
                self.do_access(i)
            elif type(i) == Gtk.Stack:
                self.do_access(i)
            elif type(i) == Gtk.Alignment:
                self.do_access(i)
            elif type(i) == Gtk.ScrolledWindow:
                self.do_access(i)

    def __init__(self, parent, pkg, cache):
        Gtk.Dialog.__init__(self, _("Package informations"), parent, 0) # on définit le titre
        self.set_border_width(10)
        self.set_default_size(300, 600)

        p = cache[pkg] # retrouve le paquet à partir du nom
        c = p.candidate # nécessaire pour avoir des infos ensuite

        self.infobox = Gtk.VBox() # ce qui va contenir toutes les infos

        name = Gtk.Label()
        name.set_markup('<b>{}</b>'.format(p.shortname))
        name.set_justify(Gtk.Justification.CENTER)
        self.infobox.pack_start(name, False, False, 15)
        
        desc, homepage = "", ""
        if c: # parfois, on n'arrive pas à avoir la version candidate
            import textwrap
            desc = textwrap.fill(c.description, 80)
            description = Gtk.Label(desc)
            self.infobox.pack_start(description, False, False, 10)

            homepage = c.homepage
            if len(homepage) > 0 :  # il n'y a pas toujours d'url pour un paquet
                url = Gtk.LinkButton(homepage, homepage)
                self.infobox.pack_start(url, False, False, 1)

        self.spinner = Gtk.Spinner() # affiche un sablier le temps que l'image soit trouvée
        self.dlimagelbl = Gtk.Label() # message indiquant qu'on télécharge l'image
        self.infobox.pack_start(self.spinner, True, True, 0)
        self.infobox.pack_start(self.dlimagelbl, True, True, 0)

        # recherche de l'image en arrière-plan
        thread = threading.Thread(target=self.addshot, args=(p.name,))
        thread.daemon = True
        thread.start()
        
        # boutons de la fenêtre
        self.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
        if p.is_installed:
            self.add_buttons(_("Remove this package"), Gtk.ResponseType.OK)
            status = Gtk.Label(_("This package is installed"))
            self.infobox.pack_start(status, False, False, 15)
        else:
            self.add_buttons(_("Install this package"), Gtk.ResponseType.OK)
            status = Gtk.Label(_("This package is not installed"))
            self.infobox.pack_start(status, False, False, 15)

        # on met tout dans une scrollwin pour avoir des barres de défilement
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(width, height)
        scroll.add(self.infobox)
        
        # on récupère la zone de stockage du dialogue
        box = self.get_content_area()
        box.add(scroll)

        self.do_access(self)
        self.show_all()

    def addshot(self, name):
        GObject.idle_add(self.spinner.start) # fait tourner!
        GObject.idle_add(self.dlimagelbl.set_text, _("Downloading screenshot...")) 
        shot = dl_shot(name, thumb=False) # récupère le screenshot
        if shot:
            image = Gtk.Image.new_from_file(shot)
            if shot == dummythb:
                ebox = Gtk.EventBox()
                ebox.add(image)
                ebox.connect("button-release-event", lambda x,y: self.upload_shot(name, y) )
                ebox.set_tooltip_text(_("Right click to add a screenshot"))
                GObject.idle_add(self.infobox.pack_start, ebox, True, True, 1)
            else:
                GObject.idle_add(self.infobox.pack_start, image, True, True, 1)
            GObject.idle_add(self.show_all)
        GObject.idle_add(self.spinner.stop)
        GObject.idle_add(self.dlimagelbl.set_text, "") 

    def upload_shot(self, name, event):
        # clic droit ok 
        if event.type == Gdk.EventType.BUTTON_RELEASE and \
                event.state & Gdk.ModifierType.BUTTON3_MASK:
            m = Gtk.MessageDialog(parent=self)
            m.set_markup(_('To add a screenshot for {}, click here : ').format(name))
            m.add_buttons(_("Click here to upload a screenshot"), Gtk.ResponseType.OK)
            m.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
            ret = m.run()
            if ret == Gtk.ResponseType.CLOSE:
                m.destroy()
            elif ret == Gtk.ResponseType.OK:
                import webbrowser
                scroturl = "https://screenshots.debian.net/upload"
                webbrowser.open(scroturl)
                m.destroy()


class Logitheque(Gtk.Window):

    def __init__(self, tosearch):
        self.cacheready = False # permet de savoir si le cache apt pourra être utilisé
        self.fullsch = True # pour recherche dans les descriptions si True
        self.logibuild = False # pour garder trace si la logithèque est construite ou pas
        self.issearching = False # pour ne pas faire 2 recherches en même temps

        Gtk.Window.__init__(self, title=appname)
        self.set_default_size(250, -1)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            
        # Icône de la fenêtre
        if os.path.isfile(handysofticon):
            self.set_icon_from_file(handysofticon)

        stack = Gtk.Stack()  # passage de la recherche à la logithèque
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        # partie recherche
        self.search = Gtk.Entry()  # barre de recherche
        self.search.set_text(_("Search package"))
        self.search.set_tooltip_text(_("Enter your research here (regexp are allowed)"))
        self.search.connect("activate", lambda x: self.search_package(self.search.get_text())) # entrée valide
        
        # bouton pour lancer la recherche
        searchbtn = Gtk.Button.new_from_icon_name("find", Gtk.IconSize.BUTTON)
        searchbtn.set_tooltip_text(_("Click to start searching"))
        searchbtn.connect("button_release_event", lambda x,y: self.search_package(self.search.get_text()))
        searchbtn.connect("activate", lambda x: self.search_package(self.search.get_text()))

        # recherche dans les descriptions ou pas
        fullschbtn = Gtk.CheckButton()
        fullschbtn.connect("toggled", self.toggle_fullsch)
        fullschbtn.set_active(self.fullsch)
        fullschbtn.set_tooltip_text(_("Search also in description"))
        
        fullschbtnlbl = Gtk.Label(_("Search in description"))

        self.iamsearching = Gtk.Label() # indicateur d'activité

        # ce qui contient toute la partie recherche
        self.searchbox = Gtk.VBox()

        self.topbox = Gtk.HBox()  # barre de recherche et indicateur à côté
        self.topbox.pack_start(self.search, True, True, 1)
        self.topbox.pack_start(searchbtn, False, False, 0)
        self.topbox.pack_start(fullschbtn, False, False, 0)
        self.topbox.pack_start(fullschbtnlbl, False, False, 1)

        # la liste des paquets trouvés
        self.tree = Gtk.TreeView()
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.add(self.tree)

        # on met dans la boîte à recherche
        self.searchbox.pack_start(self.topbox, False, False, 5) # elle est en haut
        self.searchbox.pack_start(self.iamsearching, False, False, 5) 
        self.searchbox.pack_start(self.scroll, True, True, 0)

        self.surprise = Gtk.HBox()
        self.searchbox.pack_start(self.surprise, False, True, 10)

        # partie logithèque
        self.logibox = Gtk.VBox()

        # pages
        stack.add_titled(self.searchbox, _("Search packages"), _("Search"))
        stack.add_titled(self.logibox, _("Softwares"), _("Softwares"))

        # boutons
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_tooltip_text(_("Toggle between packages search or packages list"))
        stack_switcher.connect("button_release_event", self.build_logitheque)
        stack_switcher.connect("key_press_event", self.build_logitheque)
        stack_switcher.set_stack(stack)

        # bouton pour voir le àpropos
        aboutbtn = Gtk.Button.new_from_icon_name("help-about", Gtk.IconSize.BUTTON)
        aboutbtn.set_tooltip_text(_("About"))
        aboutbtn.connect("button_release_event", lambda x,y: self.about())
        aboutbtn.connect("activate", lambda x: self.about())

        # conteneur de boutons
        btncontainer = Gtk.HBox()
        btncontainer.pack_start(stack_switcher, False, False, 0)
        btncontainer.pack_start(aboutbtn, True, False, 10)
        align = Gtk.Alignment.new(1, 0, 0.5, 0.5) # pour centrer les boutons
        align.add(btncontainer)

        # boîte principale
        mainbox = Gtk.VBox()
        mainbox.pack_start(stack, True, True, 0)
        mainbox.pack_start(align, False, False, 10)

        self.add(mainbox) # on met la boîte principale dans la fenêtre

        # open cache in bg
        opencache = threading.Thread(target=self.open_cache)
        opencache.daemon = True
        opencache.start()
        
        # chargement de la liste des screenshots

        openavailthb = threading.Thread(target=self.open_avail_thb)
        openavailthb.daemon = True
        openavailthb.start()

        self.do_access(self)
        self.show_all() # on montre tout
        self.scroll.hide()  # sauf la liste des paquets
        self.surprise.hide()  # sauf la surprise

        if tosearch:
            self.search.set_text(tosearch)
            self.search_package(tosearch)

    def toggle_fullsch(self, widget): # pour changer la recherche complete ou pas
        self.fullsch = widget.get_active()

    def build_logitheque(self, widget, event):
        if event.type == Gdk.EventType.KEY_PRESS: 
            if not event.keyval == Gdk.KEY_Return:
                return()
        if not self.logibuild:
            self.resize(width,height)
            self.prepare_logitheque()

            '''
            thread = threading.Thread(target=self.prepare_logitheque)
            thread.daemon = True
            thread.start()
            '''

    def open_cache(self):
        # ouvre le cache apt
        GObject.idle_add(self.iamsearching.set_text, _("Opening cache")) # indicateur d'activité

        self.cache = apt.Cache() 
        self.cache.open(None)
        # liste filtrée pour les recherches suivantes
        self.cachefiltered = [p for p in self.cache if trie_paquet(p.shortname, p.section)]

        self.cacheready = True
        GObject.idle_add(self.iamsearching.set_text, "") # indicateur d'activité

    def open_avail_thb(self):
        # valeur par défaut
        from data import defaultthblist
        self.availthb = defaultthblist
        # récupération de screenshots disponibles
        self.availthb = get_avail_thb()

    def cache_ready(self):
        # permet d'attendre que le cache soit prêt
        while not self.cacheready:
            print('cache not ready yet')
            sleep(0.25)

    def reload_logitheque(self):
        # on supprime tout ce que la logithèque contient comme widget
        for w in self.logibox:
            w.destroy()
        self.prepare_logitheque()
        
    def prepare_logitheque(self):
        # remplit la logithèque de paquets
        self.cache_ready() # on attend que le cache soit prêt
        # récupération de la liste de paquets à traiter
        pkg_list = get_pkg_list(self.cachefiltered)

        # le tableau
        onglets = Gtk.Notebook() 
        onglets.set_tab_pos(Gtk.PositionType.TOP)
        onglets.set_scrollable(True)
        onglets.popup_enable()
        
        GObject.idle_add(self.logibox.pack_start, onglets, True, True, 0)
        
        # il faut montrer les éléments un par un
        GObject.idle_add(self.logibox.show)
        GObject.idle_add(onglets.show)

        for c in categories:
            # ce qui sera dans cette page du tableau
            box = Gtk.VBox()
            box.show()

            # titre de la catégorie
            #label = Gtk.Label()
            #label.show()
            #label.set_markup("<span size='x-large'><b>{}</b></span>".format(c['label']))
            #box.pack_start(label, False, False, 10)

            if c['section'] == 'expert': # page spéciale pour synaptic
                label = Gtk.Label()
                label.set_markup(_('''
{} lets you install common applications easily\n\n
For a full list of available packages in Debian and Handylinux repositories, 
you must use the Synaptic Package Manager.
                ''').format(appname))
                label.show()

                btn = Gtk.Button(_("I'm an expert, open synaptic"))
                btn.connect("activate", lambda x: synaptic())
                btn.set_image_position(Gtk.PositionType.TOP)
                btn.show()
                btn.connect("button_release_event", lambda x,y: synaptic())

                icon = Gtk.Image.new_from_icon_name(c['icon'],Gtk.IconSize.DIALOG)
                btn.set_image(icon)
                box.pack_start(label, True, True, 0)
                box.pack_start(btn, False, False, 0)

            else:
                scroll = Gtk.ScrolledWindow()
                scroll.show()
                scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

                store = Gtk.ListStore(str, str, str) # lignes de la liste de paquets
                tree = Gtk.TreeView(store)
                tree.set_activate_on_single_click(True)
                tree.set_rules_hint( True )
                tree.connect("row_activated", self.show_pkg, store, 1) 
                tree.show()

                # colonne indiquant si le paquet est installé
                renderer_inst = Gtk.CellRendererPixbuf()
                renderer_inst.set_property("stock-size", 5)
                column_inst = Gtk.TreeViewColumn(_("Installed"), renderer_inst, icon_name=0)
                tree.append_column(column_inst)

                # colonne nom du paquet
                renderer_text = Gtk.CellRendererText()
                renderer_text.set_property("weight", 11000 )
                renderer_text.set_property("wrap-width", 85 )
                column_text = Gtk.TreeViewColumn(_("Package name"), renderer_text, text=1)
                column_text.set_sort_column_id(0) # on peut trier en cliquant sur l'en-tête
                tree.append_column(column_text)

                # colonne description
                renderer_desc = Gtk.CellRendererText()
                renderer_desc.set_property("wrap-width", 400 )
                column_desc = Gtk.TreeViewColumn(_("Description"), renderer_desc, text=2)
                tree.append_column(column_desc)

                task = self.fill_logitheque(store, pkg_list[c['section']])
                GObject.idle_add(next, task) # 
                scroll.add(tree)
                box.pack_start(scroll, True, True, False)

            # on met la liste dans l'onglet
            obox = Gtk.VBox() # conteneur pour titre de l'onglet
            GObject.idle_add(obox.show)

            ongletlabel = Gtk.Label(c['label']) # titre de l'onglet
            ongletlabel.set_tooltip_text(c['label'])
            ongletlabel.set_width_chars(onglet_width) # pour avoir des onglets uniformes
            GObject.idle_add(ongletlabel.show)

            o = Gtk.Image.new_from_icon_name(c['icon'],Gtk.IconSize.DND) # icone de l'onglet

            o.set_tooltip_text(c['label'])
            GObject.idle_add(o.show)

            GObject.idle_add(obox.pack_start, o, True, True, 0)
            GObject.idle_add(obox.pack_start, ongletlabel, True, True, 0)
            onglets.append_page(box, obox) # on rajoute une page dans le tableau
            GObject.idle_add(onglets.grab_focus) # pour la gestion au clavier facilitée
        
        self.logibuild = True # on indique que la logithèque est prête

    def fill_logitheque(self, store, pkg_list, screenshot=False, desc_perso=False):
        '''add packages from pkg_list to store'''
        for pkg in pkg_list:
            if desc_perso:
                name = pkg['name']
                desc = pkg['desc']
            else:
                name = pkg
                desc = ""
            try:
                p = self.cache[name]
            except Exception as e:
                print(e)
                continue

            candidate = p.candidate
            if candidate and not desc_perso:
                #description = candidate.description
                description = candidate.summary
                if len(description) > 0:
                    desc = description

            if p.is_installed:
                is_installed = "stock_yes"
                #is_installed = _("Already installed ✓")
            else:
                #is_installed = _("Not installed ✗")
                is_installed = "stock_no"

            if screenshot:
                pixbuf = None
                if p.shortname in self.availthb:
                    shot = dl_shot(name, thumb=True)
                    if shot:
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file(shot)
                    else:
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file(get_dummy())
                store.append([is_installed, name, desc, pixbuf])
            else:
                store.append([is_installed, name, desc])

            yield(True)

        yield(False)


    def search_package(self, s):
        if self.issearching:
            print("Only one research at a time")
            return(False)
        else:
            self.issearching = True

        self.resize(width, height)
        
        self.cache_ready() # on attend que le cache soit prêt
        self.iamsearching.set_text( _("Searching in packages...")) # indicateur d'activité

        s = s.strip() # récupération de la recherche
        for i in self.surprise:
            i.destroy()
        if s == "kamehameha":
            gimg = Gtk.Image.new_from_file(getimage('goku'))
            gimg.show() # on montre qu'on va chercher
            self.surprise.pack_start(gimg, True, True, 0)
            self.surprise.show()

        elif s == "dyp":
            gimg = Gtk.Image.new_from_file(getimage('dyp'))
            gimg.show() # on montre qu'on va chercher
            self.surprise.pack_start(gimg, True, True, 0)
            self.surprise.show()

        elif s == "arpinux":
            gimg = Gtk.Image.new_from_file(getimage('arpinux'))
            gimg.show() # on montre qu'on va chercher
            self.surprise.pack_start(gimg, True, True, 0)
            self.surprise.show()

        elif s == "thuban":
            self.x = 65
            self.y = 19
            self.laby = dolaby(self.x,self.y)
            self.pos = (0,0)

            def drawbravo():
                for i in self.surprise:
                    i.destroy()
                gimg = Gtk.Label()
                gimg.set_markup("<span size='xx-large'>BRAVO!</span>")
                gimg.show() # on montre qu'on va chercher

                self.surprise.pack_start(gimg, True, True, 0)
                self.surprise.show()

                GObject.timeout_add(3000,self.surprise.hide)

            def drawlaby():
                for i in self.surprise:
                    i.destroy()
                text = labytotext(self.laby, self.pos)
                text = text.replace('.', ' ')
                text = text.replace('#', "<span background='#333333'> </span>")
                text = text.replace('→', "<span background='#41B1FF'>→</span>")
                text = text.replace('@', "<span background='#FAA500'>@</span>")

                gimg = Gtk.Label()
                gimg.set_markup("<span font-family='monospace'>{}</span>".format(text))
                gimg.show() # on montre qu'on va chercher

                f = Gtk.Frame() # bordure au laby
                f.add(gimg)
                f.show()

                exitmsg = Gtk.Label("Find exit")
                exitmsg.show()

                self.surprise.pack_start(exitmsg, True, False, 0)
                self.surprise.pack_start(f, True, False, 0)
                self.surprise.show()

            def moveme(widget, event):
                cx = self.pos[0]
                cy = self.pos[1]
                if event.type == Gdk.EventType.KEY_PRESS: 
                    if event.keyval == Gdk.KEY_Right and cx < self.x -1:
                        if canigo(self.laby, (cx+1, cy)):
                            self.pos = (cx+1, cy)
                            if self.pos == (self.x-1, self.y-1):
                                drawbravo()
                            else:
                                drawlaby()
                    elif event.keyval == Gdk.KEY_Left and cx > 0:
                        if canigo(self.laby, (cx-1, cy)):
                            self.pos = (cx-1, cy)
                            if self.pos == (self.x-1, self.y-1):
                                drawbravo()
                            else:
                                drawlaby()
                    elif event.keyval == Gdk.KEY_Up and cy > 0:
                        if canigo(self.laby, (cx, cy-1)):
                            self.pos = (cx, cy-1)
                            if self.pos == (self.x-1, self.y-1):
                                drawbravo()
                            else:
                                drawlaby()
                    elif event.keyval == Gdk.KEY_Down and cy < self.y -1:
                        if canigo(self.laby, (cx, cy+1)):
                            self.pos = (cx, cy+1)
                            if self.pos == (self.x-1, self.y-1):
                                drawbravo()
                            else:
                                drawlaby()

            drawlaby()
            self.connect("key_press_event", lambda x,y: moveme(x,y))

        thread = threading.Thread(target=self.show_results, args=(s,))
        thread.daemon = True
        thread.start()

    def show_results(self, s):
        GObject.idle_add(self.scroll.remove, self.tree) # on nettoie la liste
        self.store = Gtk.ListStore(str, str, str) # lignes de la liste de paquets
        self.tree = Gtk.TreeView(self.store)
        self.tree.set_activate_on_single_click(True)
        self.tree.set_rules_hint( True )
        self.tree.connect("row_activated", self.show_pkg, self.store, 1) # au double clic, on montre des infos sur le paquet
        self.tree.connect("button-release-event", self.upload_shot, self.store) # ajout de screenshot si manquant?
        GObject.idle_add(self.tree.show)

        # définition de chaque colonne
        # colonne indiquant si le paquet est installé
        renderer_inst = Gtk.CellRendererPixbuf()
        renderer_inst.set_property("stock-size", 5)
        column_inst = Gtk.TreeViewColumn(_("Installed"), renderer_inst, icon_name=0)
        self.tree.append_column(column_inst)
        
        # colonne nom du paquet
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("weight", 11000 )
        column_text = Gtk.TreeViewColumn(_("Package name"), renderer_text, text=1)
        column_text.set_sort_column_id(1) # on peut trier en cliquant sur l'en-tête
        self.tree.append_column(column_text)

        # colonne description
        renderer_desc = Gtk.CellRendererText()
        column_desc = Gtk.TreeViewColumn(_("Description"), renderer_desc, text=2)
        self.tree.append_column(column_desc)
        
        GObject.idle_add(self.scroll.add,self.tree)
        GObject.idle_add(self.scroll.show)  # on montre les résultats
        sch_results = cache_search(self.cachefiltered, s, description=self.fullsch)
        #with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        #    for p in sch_results:
        #        executor.submit(self.addresults, p)
        for p in sch_results:
            GObject.idle_add(self.addresults,p)

        GObject.idle_add(self.iamsearching.set_text, "") # indicateur d'activité
        self.issearching = False # on laisse prêt pour une autre recherche

    def addresults(self, package):
        name = package.name
        append = self.store.append # + rapide ensuite

        try:
            candidate = package.candidate
            desc = candidate.summary
        except:
            desc = ""

        if package.is_installed:
            is_installed = "stock_yes"
        else:
            is_installed = "stock_no"
        append([is_installed, name, desc])

    def show_pkg(self, widget, row, col, store, idx):
        pkg=store[row][:][idx]

        m = DialogPackage(self,pkg,self.cache)

        ret = m.run()
        GObject.idle_add(m.hide)
        GObject.idle_add(m.destroy)

        if ret == Gtk.ResponseType.OK:
            if self.cache[pkg].is_installed:
                print('uninstall {}'.format(pkg))
                GObject.idle_add(self.hide)
                while Gtk.events_pending():
                    Gtk.main_iteration()
                remove_pkg(pkg)
                GObject.idle_add(self.show_all)
            else:
                print('install {}'.format(pkg))
                GObject.idle_add(self.hide)
                while Gtk.events_pending():
                    Gtk.main_iteration()
                install_pkg(pkg)
                GObject.idle_add(self.show_all)
            # reload the cache
            GObject.idle_add(self.open_cache)
            GObject.idle_add(self.reload_logitheque)
            GObject.idle_add(self.scroll.hide)

    def upload_shot(self, widget, event, store):
        # clic droit ok 
        if event.type == Gdk.EventType.BUTTON_RELEASE and \
                event.state & Gdk.ModifierType.BUTTON3_MASK:
            model, path = widget.get_selection().get_selected_rows()
            idx = path[0].get_indices()[0]
            pkg =  store[idx][:][1]
            #pixbuf = store[idx][:][0]
            #dummy = GdkPixbuf.Pixbuf.new_from_file(get_dummy())
            #if dummy.get_pixels() != pixbuf.get_pixels():
            if pkg not in self.availthb:
                m = Gtk.MessageDialog(parent=self)
                m.set_markup(_('To add a screenshot for {}, click here : ').format(pkg))
                m.add_buttons(_("Click here to upload a screenshot"), Gtk.ResponseType.OK)
                m.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
                ret = m.run()
                if ret == Gtk.ResponseType.CLOSE:
                    m.destroy()
                elif ret == Gtk.ResponseType.OK:
                    import webbrowser
                    scroturl = "https://screenshots.debian.net/upload"
                    webbrowser.open(scroturl)
                    m.destroy()

    def change_bg_on_focus(self,widget,b):
        widget.modify_bg(Gtk.StateFlags.NORMAL, self.selected_bg_color)
        widget.modify_bg(Gtk.StateFlags.PRELIGHT, self.selected_bg_color)
        
    def change_bg_on_focus_leave(self,widget,b):
        widget.modify_bg(Gtk.StateFlags.NORMAL, None)
        widget.modify_bg(Gtk.StateFlags.PRELIGHT, None)

    def get_theme_colors(self):
        style_context = self.get_style_context()
        bg_color = style_context.lookup_color('bg_color')
        selected_bg_color = style_context.lookup_color('selected_bg_color')

        if bg_color[0]:
            self.bg_color = bg_color[1].to_color()
        else:
            self.bg_color = Gdk.color_parse("#eeeeee")
        if selected_bg_color[0]:
            self.selected_bg_color = selected_bg_color[1].to_color()
        else:
            self.selected_bg_color = Gdk.color_parse("#41B1FF")

    def change_focus_colors(self,i): # change colors of the widget i
        i.connect("focus_in_event", self.change_bg_on_focus)
        i.connect("enter_notify_event", self.change_bg_on_focus)
        i.connect("focus_out_event", self.change_bg_on_focus_leave)
        i.connect("leave_notify_event", self.change_bg_on_focus_leave)

    def do_access(self, widget):
        self.get_theme_colors()
        for i in widget:
            if type(i) == Gtk.Button: 
                self.change_focus_colors(i)
            elif type(i) == Gtk.StackSwitcher:
                self.change_focus_colors(i)
            elif type(i) == Gtk.HBox:
                self.do_access(i)
            elif type(i) == Gtk.VBox:
                self.do_access(i)
            elif type(i) == Gtk.Stack:
                self.do_access(i)
            elif type(i) == Gtk.Alignment:
                self.do_access(i)
            elif type(i) == Gtk.ScrolledWindow:
                self.do_access(i)
            elif type(i) == Gtk.EventBox:
                self.do_access(i)
            elif type(i) == Gtk.Notebook:
                self.do_access(i)
            elif type(i) == Gtk.Table:
                self.do_access(i)

    def about(self, wid=None, data=None):
        # fenêtre à propos.
        m = Gtk.MessageDialog()
        m.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        m.set_markup(_('<b>{0}</b>\n\n\
From {2} for handylinux community with love.\n\
version : {1}\n\
licence : {3}\n\
homepage : <a href="{4}" title="handysoft homepage">{4}</a>').format(appname, version, auteur, licence, homepage))
        ret = m.run()
        m.destroy()

def gui(tosearch = False):
    GObject.threads_init()
    win = Logitheque(tosearch)
    win.connect("delete-event", Gtk.main_quit)
    Gtk.main()
     

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(imagecache):
        os.makedirs(imagecache)
    if len(sys.argv) == 2:
        gui(sys.argv[1])
    else:
        gui()
    return 0

if __name__ == '__main__':
	main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

