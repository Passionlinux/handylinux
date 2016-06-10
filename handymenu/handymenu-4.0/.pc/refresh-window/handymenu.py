#!/usr/bin/python3
# -*- coding:Utf-8 -*- 


"""
HandyMenu :     menu principal de la distribution
                HandyLinux <https://handylinux.org>

Auteurs :       Xavier Cartron <thuban@yeuxdelibad.net>
licence :       GNU General Public Licence v3
Description :   Handymenu from scratch
Dépendances :   python3-gi xdg-user-dirs xdg-utils

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
from concurrent.futures import ThreadPoolExecutor
import gettext
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
            GObject.idle_add(self.window.hide)
            res = open_cmd("{}".format(cmd.strip()))
            if res:
                self.add_recent(data)
                if self.closeafterrun:
                    Gtk.main_quit()
            else:
                m = Gtk.MessageDialog(parent=self.window, buttons=Gtk.ButtonsType.OK)
                m.set_markup(_('<b>Error at launching {}</b>\n\nIs it installed?').format(cmd))
                m.run()
                m.destroy()
            
            self.window.show_all()
                
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
                    
        with ThreadPoolExecutor(max_workers=4) as executor:
            for page, label in executor.map(self.add_button, self.config):
                self.onglets.append_page(page, label)

        if len(self.config) > maxonglets: # dyp il aime pas :P
            self.onglets.set_scrollable(True)# dyp y veut pas :P
            self.window.set_size_request(win_max_width, -1) # pour éviter que la fenêtre soit trop large


    def add_button(self,s):
        # Description du bouton
        label = Gtk.Label()
        label.set_markup_with_mnemonic("_{}".format(s['name']))
        label.set_width_chars(onglet_width) # pour avoir des onglets uniformes

        if len(s['apps']) > 0:
            page = Gtk.FlowBox()
            page.set_valign(Gtk.Align.START)
            page.set_max_children_per_line(4)
            page.set_selection_mode(Gtk.SelectionMode.NONE)

            for a in s['apps']:
                appname, icon, cmd, generic = a['name'], a['icon'], a['cmd'], a['generic']
                    
                # image utilisée dans le bouton
                image = Gtk.Image()
                filename, ext = os.path.splitext(icon)
                if ext.lower() in ['.png', '.jpg', '.jpeg', '.gif'] :
                    try:
                        if os.path.isfile(icon):
                            pixbuf = Pixbuf.new_from_file(icon)
                            scaled_buf = pixbuf.scale_simple(iconsize,iconsize,InterpType.BILINEAR)
                            image.set_from_pixbuf(scaled_buf)
                        else:
                            image.set_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
                    except:
                        image.set_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
                        
                elif ext == ".ico":
                    if os.path.isfile(icon):
                        pixbuf = Pixbuf.new_from_file(icon)
                        scaled_buf = pixbuf.scale_simple(iconsize,iconsize,InterpType.BILINEAR)
                        image.set_from_pixbuf(scaled_buf)
                    else:
                        image.set_from_icon_name("applications-internet", Gtk.IconSize.DIALOG)
                    
                elif len(icon.split('/')) == 2: # mimetype?
                    icon = content_type_get_icon(icon)
                    image.set_from_gicon(icon, Gtk.IconSize.DIALOG)
                    
                else:
                    image.set_from_icon_name(icon, Gtk.IconSize.DIALOG)
                
                image.set_pixel_size(iconsize)
                    
                # nom de l'appli
                appname = fill(appname, button_width)
                bapp = Gtk.Button.new_with_mnemonic('_{}'.format(appname))
                bapp.set_border_width(1)
                bapp.set_image(image)
                # l'image est au dessus du texte
                bapp.set_image_position(Gtk.PositionType.TOP)
                # apparence du bouton
                bapp.set_relief(Gtk.ReliefStyle.NONE)
                # lancement au clic ou avec entrée
                bapp.connect("button_release_event", self.exec_app, a)
                bapp.connect("key_press_event", self.exec_app, a)
                bapp.set_tooltip_text(generic)
                page.add(bapp)

        else:
            page = Gtk.Label(_("This menu is still empty"))
            label = Gtk.Label(_("This menu is still empty"))
            
        return(page, label)
                

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
        self.onglets = Gtk.Notebook()
        self.onglets.set_tab_pos(Gtk.PositionType.TOP)
        self.onglets.set_show_border(False)
        
        vbox.pack_start(self.onglets, True, True, 0)
        
        # Catégories
        self.create_tabs() 
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
        self.bg_color = Gdk.color_parse("#eeeeee")
        self.selected_bg_color = Gdk.color_parse("#41B1FF")
        
        try: # no error even if old gtk3
            if bg_color[0]:
                self.bg_color = bg_color[1].to_color()
            if selected_bg_color[0]:
                self.selected_bg_color = selected_bg_color[1].to_color()
        except:
            bg_color = Gdk.color_parse("#eeeeee")
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
            elif type(i) == Gtk.HBox:
                self.do_access(i)
            elif type(i) == Gtk.VBox:
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
            try: #HL-1.9
                if type(i) == Gtk.FlowBox:
                    self.do_access(i)
                elif type(i) == Gtk.FlowBoxChild:
                    self.change_focus_colors(i)
            except:
                pass
                

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
        self.onglets.grab_focus() # pour la gestion au clavier facilitée

        self.do_access(self.window)

        # pour des messages défilants aléatoires après 30s
        self.timer = GObject.timeout_add (30000, self.change_message)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
