#!/usr/bin/python3
# -*- coding:Utf-8 -*- 


"""
HandyMenu :     menu principal de la distribution
                HandyLinux <https://handylinux.org>

Auteurs :       Xavier Cartron <thuban@yeuxdelibad.net>
licence :       GNU General Public Licence v3
Description :   Handymenu from scratch
Dépendances :   python3-gi

"""

version = "4.0"
auteur = "thuban"
licence = "GPLv3"
homepage = "https://handylinux.org"

import os
import sys
from gi.repository import Gtk, Gdk, GObject
from gi.repository.GdkPixbuf import Pixbuf, InterpType
from gi.repository.Gio import content_type_get_icon
from textwrap import fill
import threading
import gettext
from math import ceil
from hm_utils import *

gettext.bindtextdomain('handymenu', '/usr/share/locale')
gettext.textdomain('handymenu')
_ = gettext.gettext

os.chdir(os.getenv('HOME'))

class Handymenu():
    def close_application(self, widget, event, data=None):
        # tests nécessaires pour que seul clic-gauche et Entrée soient valables
        if event.type == Gdk.EventType.BUTTON_RELEASE and \
                event.state & Gdk.ModifierType.BUTTON1_MASK:
                Gtk.main_quit()
        elif event.type == Gdk.EventType.KEY_PRESS: 
            if event.keyval == Gdk.KEY_Return:
                Gtk.main_quit()

    def configure(self, data=None):
        open_cmd(configcmd)
        Gtk.main_quit()

    def about(self, wid=None, data=None):
        # fenêtre à propos.
        m = Gtk.MessageDialog()
        m.set_markup(_('<b>Handymenu</b>\n\n\
version : {0}\n\
author : {1}\n\
licence : {2}\n\
homepage : <a href="{3}" title="HandyMenu homepage">{3}</a>').format(version, auteur, licence, homepage))


        import base64
        imgsrc="""iVBORw0KGgoAAAANSUhEUgAAABYAAAAZCAQAAACf6xZlAAAABGdBTUEAALGPC/xhBQAAACBjSFJN
AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAHdElN
RQffDAcVCjCxQGhfAAABrklEQVQ4y4XTvWtTYRQG8F+aqI0tgqZ+pVI/im0UC9JU1C2tsRVptGCE
WkFwcHIQFP8DWxVdhG6SQSj+A4IIbg4qRQuCg46CiEXaiEO7KDrk5vamucFnOuc+zz3veZ/znoRm
DOqWsOCr/6DbRXvBERM6Wws3KzoayRNGjErESfNGtQXxeaUg6jDsUKNwQNkW0OOWWVXLHpnSAXqV
7KgJdyvZB9LumdaHEWckFTx2JSg3ZNxGJoM0Y05fU3OTZoJogzJFkPLEzthrn3UziIr1K11TsRgr
fq7L/lrYFpg05FVLSx+6HhXnvYmQWfddiuTL9eGkgmktREbzwoBVB0yH3xZtVa1X3qYaEjk5pJ2I
1F7StdbGkkxIfPIZq95GxNv9WGvjo0HvAmLFmBs+eNog/hm4h4SK1sh4EPX5r3mFluLbZqPWUXHV
rljpuO++1JOp8LA5uSbpZXfUTS6TUdIP2s24G77elFMqYanjLtiUCIbS76Vf2KPsoD+SfnvtmRX0
Omy+8eWcdE6yqY1OhfWbUkPa6YYdbDNsLH4Ha8gq6QHHTGhvJOP+y8vivW/riX9jckqMmv+hKgAA
ACV0RVh0ZGF0ZTpjcmVhdGUAMjAxNS0xMi0wN1QyMjoxMDo0OCswMTowMJJ/5BMAAAAldEVYdGRh
dGU6bW9kaWZ5ADIwMTUtMTItMDdUMjI6MTA6NDgrMDE6MDDjIlyvAAAAAElFTkSuQmCC"""

        g = base64.b64decode(imgsrc)
        imgpath = "/tmp/.hmbtn.png"
        with open(imgpath, "wb") as t:
            t.write(g)
        image = Gtk.Image.new_from_file(imgpath)
        image.show()
        btn = Gtk.Button.new_with_mnemonic("_I click here because I love handylinux")
        btn.set_image(image)
        btn.set_image_position(Gtk.PositionType.TOP)
        btn.connect("button_release_event", lambda x,y: m.destroy())
        btn.connect("key_press_event", lambda x,y: m.destroy())
        btn.show()

        btnbox = m.get_action_area()
        btnbox.add(btn)

        ret = m.run()
        os.remove(imgpath)
        m.destroy()
    
    def add_recent(self,app):
        """add a recent application
        appname, icon, cmd= app['name'], app['icon'], app['cmd']
        """
        for s in self.config:
            if s['id'] == 'recent': # on prend la bonne section
                # check if app is not already in recents
                if app not in s['apps']:
                    s['apps'].insert(0,app)
                # on vire les vieux éléments
                if len(s['apps']) > max:
                    s['apps'].pop()
        save_config(self.config)

    def exec_app(self, widget, event, data):
        exe = False
        if event.type == Gdk.EventType.BUTTON_RELEASE and \
                event.state & Gdk.ModifierType.BUTTON1_MASK:
                exe = True
        elif event.type == Gdk.EventType.KEY_PRESS: 
            if event.keyval == Gdk.KEY_Return:
                exe = True
        if exe:
            appname, icon, cmd= data['name'], data['icon'], data['cmd']
            open_cmd("{} &".format(cmd.strip()))
            self.add_recent(data)
            if self.closeafterrun:
                Gtk.main_quit()

    def change_bg_on_focus(self,widget,b):
        widget.modify_bg(Gtk.StateFlags.NORMAL, self.selected_bg_color)
        widget.modify_bg(Gtk.StateFlags.PRELIGHT, self.selected_bg_color)
        
    def change_bg_on_focus_leave(self,widget,b):
        widget.modify_bg(Gtk.StateFlags.NORMAL, None)
        widget.modify_bg(Gtk.StateFlags.PRELIGHT, None)

    def create_tabs(self):
        modlist = load_modules()
        index = modlist[0] -1
        for m in modlist[1]:
            if m == "_recent_files_":
                recentfiles = get_recently_used(max)
                if recentfiles:
                    self.config.insert(index,recentfiles)
            elif m == "_most_ffox_view_":
                ffox_most = get_most_ffox_viewed(max)
                if ffox_most:
                    self.config.insert(index,ffox_most)

        for s in self.config:
            self.add_button(s)

    def add_button(self,s):
        r = 2 # 2 lignes par défaut
        # onglet coloré

        n = len(s['apps']) # number of apps to show
        if n > 0:

            r = ceil(n/3)
            if r > 2:
                r -= 1
            c = ceil(n/r)
            if c > 2:
                c -= 1

            page = Gtk.Table(rows=r, columns=c, homogeneous=True)
            page.grab_focus()
            page.show()

            cur = [0,0]
            for a in s['apps']:
                appname, icon, cmd, generic = a['name'], a['icon'], a['cmd'], a['generic']
                # image utilisée dans le bouton
                image = Gtk.Image()
                image.show()
                if icon.split('.')[-1] in ['png', 'jpg', 'jpeg', 'gif']:
                    pixbuf = Pixbuf.new_from_file(icon)
                    scaled_buf = pixbuf.scale_simple(iconsize,iconsize,InterpType.BILINEAR)
                    image.set_from_pixbuf(scaled_buf)
                elif icon.endswith('.ico'):
                    if os.path.isfile(icon):
                        pixbuf = Pixbuf.new_from_file(icon)
                        scaled_buf = pixbuf.scale_simple(iconsize,iconsize,InterpType.BILINEAR)
                        image.set_from_pixbuf(scaled_buf)
                    else:
                        image.set_from_icon_name("applications-internet", Gtk.IconSize.DIALOG)
                    image.set_pixel_size(iconsize)
                elif len(icon.split('/')) == 2: # mimetype?
                    icon = content_type_get_icon(icon)
                    image.set_from_gicon(icon, Gtk.IconSize.DIALOG)
                    image.set_pixel_size(iconsize)
                else:
                    image.set_from_icon_name(icon, Gtk.IconSize.DIALOG)
                    image.set_pixel_size(iconsize)
                # nom de l'appli
                appname = fill(appname, button_width)
                bapp = Gtk.Button.new_with_mnemonic('_{}'.format(appname))
                bapp.show()
                bapp.set_border_width(1)
                bapp.set_image(image)
                # l'image est au dessus du texte
                bapp.set_image_position(Gtk.PositionType.TOP)
                # apparence du bouton
                bapp.set_relief(Gtk.ReliefStyle.NONE)
                bapp.set_alignment(0.5, 0.5)
                #blab.props.wrap = True
                #blab.props.width_chars = 20
                # lancement au clic ou avec entrée
                bapp.connect("button_release_event", self.exec_app, a)
                bapp.connect("key_press_event", self.exec_app, a)
                bapp.set_tooltip_text(generic)

                page.attach(bapp, cur[0], cur[0]+1, cur[1], cur[1]+1,\
                    xoptions=Gtk.AttachOptions.EXPAND|Gtk.AttachOptions.FILL,\
                    yoptions=Gtk.AttachOptions.EXPAND|Gtk.AttachOptions.FILL,\
                    xpadding=1, ypadding=1)
                if cur[0] < c:
                    cur[0] +=1
                elif cur[0] == c:
                    cur[0] = 0
                    cur[1] += 1

            #self.onglets.add_titled( page, s['name'], s['name'])
            GObject.idle_add(self.onglets.add_titled, page, s['name'], s['name'])
        else:
            desc = Gtk.Label(_("This menu is still empty"))
            desc.show()
            GObject.idle_add(self.onglets.add_titled, desc, _("This menu is still empty"), _("This menu is still empty"))
                

    def close_after(self, widget):
        self.closeafterrun = widget.get_active()
        if not self.closeafterrun: #on enregistre de ne pas fermer
            with open(noclose,'w') as n:
                n.write('Thuban veut un câlin :P')
        elif os.path.isfile(noclose): #on ferme la prochiane fois
            os.remove(noclose)
            
    def make_menu(self):
        """build the menu"""
        # Conteneur principal
        mainbox = Gtk.EventBox()
        
        # pour utiliser la couleur de fond du thème GTK
        mainbox.modify_bg(Gtk.StateFlags.NORMAL, self.bg_color) 
        self.window.add(mainbox)

        vbox = Gtk.VBox(False, 2)
        vbox.set_border_width(15)
        mainbox.add(vbox)

        # Logo
        image = Gtk.Image()
        image.set_from_file(handymenuicon)
        logo = Gtk.EventBox()
        logo.add(image)
        logo.connect_object("button_release_event", self.about, None)
        logo.set_tooltip_text(_("About"))

        # Titre
        self.title = Gtk.Label()
        self.title.set_markup('<span size="32000">HandyMenu  </span>')
        self.title.set_justify(Gtk.Justification.CENTER)
        titlebox = Gtk.EventBox()
        titlebox.add(self.title)
        titlebox.connect_object("button_press_event", self.move_win, None)
        titlebox.set_tooltip_text("handylinux.org")

        # boutons
        # bouton pour fermer
        closebtn = Gtk.Button()
        croix = Gtk.Image()
        croix.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        closebtn.set_image(croix)
                
        closebtn.set_relief(Gtk.ReliefStyle.NONE)
        closebtn.connect("button_release_event", self.close_application)
        closebtn.connect("key_press_event", self.close_application)
        closebtn.set_tooltip_text(_("Close"))

        # configuration 
        qbtn = Gtk.Button()
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_PREFERENCES, Gtk.IconSize.MENU)
        qbtn.set_image(image)
        qbtn.set_relief(Gtk.ReliefStyle.NONE)
        qbtn.connect_object("clicked", self.configure, None)
        qbtn.set_tooltip_text(_("Configure"))

        # fermer ou pas
        closeafterbtn = Gtk.CheckButton()
        closeafterbtn.connect("toggled", self.close_after)
        closeafterbtn.set_active(self.closeafterrun)
        closeafterbtn.set_tooltip_text(_("Close after execution"))

        # boite à boutons 
        btnbox = Gtk.VBox(False,0)
        btnbox.pack_start(closebtn, True, True, 0)
        btnbox.pack_start(qbtn, True, True, 0)
        btnbox.pack_start(closeafterbtn, True, True, 0)

        # Boite d'en haut
        topbox = Gtk.HBox(False, 0)
        topbox.pack_start(logo, False, False, 0)
        topbox.pack_start(titlebox, True, True, 0)
        topbox.pack_start(btnbox, False, False, 0)

        vbox.pack_start(topbox, True, True, 0)

        # onglets
        self.onglets =  Gtk.Stack()  
        self.onglets.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.onglets.set_transition_duration(750)
        
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_tooltip_text(_("Toggle between categories"))
        stack_switcher.set_stack(self.onglets)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(self.onglets, True, True, 0)

        # Catégories
        thread = threading.Thread(target=self.create_tabs) 
        thread.daemon = True
        thread.start()

        self.window.show_all()

    def move_win(self, widget, event):
        """move window with a simple click"""
        self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)

    def change_message(self):
        """just change the message on top of the window, just
        for fun
        """
        msg = random_msg()
        self.title.set_markup('<span size="30000">{}</span>'.format(msg))
        # toutes les 10 secs
        self.timer = GObject.timeout_add (10000, self.change_message)

    def get_theme_colors(self):
        style_context = self.window.get_style_context()
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

    def start(self):
        Gtk.main()

    def __init__(self):
        if os.path.isfile(noclose):
            self.closeafterrun = False
        else:
            self.closeafterrun = True
            
        try:
            self.config = load_config()
        except Exception as err:
            print(err)
            set_default_config()
            self.config = load_config()


        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.connect("delete_event", lambda x,y: Gtk.main_quit())

        self.window.set_title(menuname)
        self.window.set_border_width(1) # pour avoir une bordure noire
        self.window.set_icon_from_file(handymenuicon)

        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_resizable(False)
        self.window.set_decorated(False)
        self.window.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("black"))

        self.get_theme_colors()
        
        self.make_menu()

        self.do_access(self.window)

        # pour des messages défilants aléatoires après 30s
        self.timer = GObject.timeout_add (30000, self.change_message)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
