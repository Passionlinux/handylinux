#!/usr/bin/python3
# -*- coding:Utf-8 -*- 


"""
Description :
    Configuration du handymenu
"""

import sys
import os
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf
import gettext
import locale

from hm_utils import *

gettext.bindtextdomain('handymenu', '/usr/share/locale')
gettext.textdomain('handymenu')
_ = gettext.gettext

def get_info_desktop(desktopfile):
    """return infos from a .desktop file"""
    name, cmd, icon, generic= "", "", "", ""
    nameloc = False
    geneloc = False
    lang = locale.setlocale(locale.LC_ALL, "")[0:2]
    with open(desktopfile,'r') as d:
        df = d.readlines()
        for l in df:
            if generic == "" or geneloc == False:
                if l.startswith('GenericName[{0}]='.format(lang)):
                    generic = l.replace('GenericName[{0}]='.format(lang),'').strip()
                    geneloc = True
                elif l.startswith('GenericName='.format(lang)):
                    generic = l.replace('GenericName='.format(lang),'').strip()
            if name == "" or nameloc == False:
                if l.startswith('Name[{0}]='.format(lang)):
                    name = l.replace('Name[{0}]='.format(lang),'').strip()
                    nameloc = True
                elif l.startswith('Name='):
                    name = l.replace('Name=', '').strip()
            if cmd == "":
                if l.startswith('Exec='):
                    cmd = l.replace('Exec=', '').strip()
                    cmd = cmd.split('%')[0].strip()
                    # handle wine shortcuts
                    if cmd.startswith('env WINEPREFIX'):
                        cmd = cmd.replace('\\\\','\\')
            if icon == "":
                if l.startswith('Icon='):
                    icon = os.path.splitext(l.replace('Icon=', '').strip())[0]
    return(name, cmd, icon, generic)

class ViewHMConfig(Gtk.Dialog):

    def __init__(self, parent, config):
        Gtk.Dialog.__init__(self, _("Handymenu Configuration"), parent, 0) 
        self.set_border_width(10)
        self.set_default_size(450, 300)
        
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        
        configuration = ""
        for s in config:
            configuration += str(s['name']) + "\n"
            for app in s['apps']:
                configuration += "      {}\n".format(str(app))
        
        self.textbuffer.set_text(configuration)
        scrolledwindow.add(self.textview)
        
        # on récupère la zone de stockage du dialogue
        box = self.get_content_area()
        box.add(scrolledwindow)

        self.show_all()

class HandymenuConfig():
    def view_config(self):
        m = ViewHMConfig(self.window, self.config)
        ret = m.run()
        GObject.idle_add(m.hide)
        GObject.idle_add(m.destroy)
    
    def close_application(self, widget, event, data=None):
        open_cmd("handymenu --force &")
        Gtk.main_quit()
        return False

    def appfinder(self, widget=None, event=None):
        open_cmd('xfce4-appfinder &')

    def restart(self, widget=None, event=None):
        page = self.section_list.get_current_page()
        self.config = load_config()
        self.make_menu(initialize = False)
        if page > len(self.config):
            page = 0
        self.section_list.set_current_page(page)

    def back_to_default(self, widget):
        set_default_config()
        self.restart()

    def add_new_section(self, widget):
        name = widget.get_text().strip()
        if len(name) != 0:
            newsec =  {'name' : name, 'id': "", 'apps': [] }
            add_section(self.config, newsec)
            self.restart()

    def del_section(self, section):
        self.config.remove(section)
        save_config(self.config)
        self.restart()
    
    def move_sec(self, section, index):
        reload = move_section(self.config, section, index)
        self.section_list.set_current_page(self.config.index(section))          
        if reload:
            self.restart()

    def add_item_to_section(self, name, cmd, icon, generic, section):
        app = {'name' : name, 'icon' : icon, 'cmd' : cmd, 'generic' : generic}
        add_app(self.config, section, app)
        self.restart()

    def del_item_from_section(self, section, app):
        del_app(self.config, section, app)
        self.restart()

    def mod_app_name(self, widget, event, dialog, section, app):
        newname = widget.get_text().strip()
        if len(newname) != 0:
            mod_app(self.config, section, app, newname)
            self.restart()
        dialog.destroy()

    def mod_app_icon_dialog(self, widget, event, dialog, section, app):
        chooser = Gtk.FileChooserDialog(title=_("Choose an icon"))
        chooser.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        chooser.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        chooser.set_current_folder(os.getcwd())
        filter = Gtk.FileFilter()
        filter.set_name(_("Images"))
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        chooser.add_filter(filter)

        response = chooser.run()

        if response == Gtk.ResponseType.CANCEL:
            print(_('Closed, no files selected'))
            chooser.destroy()
        elif response == Gtk.ResponseType.OK:
            i = chooser.get_filename()
            chooser.destroy()
            mod_app_icon(self.config, section, app, i)
            self.restart()

        dialog.destroy()

    def move_app_up(self, widget, dialog, section, app):
            move_app(self.config, section, app, -1)
            dialog.destroy() 
            self.restart()

    def move_app_down(self, widget, dialog, section, app):
            move_app(self.config, section, app, 1)
            dialog.destroy() 
            self.restart()


    def handle_drop(self, data, section):
        '''handle drag n drop to add to configuration'''
        if data.startswith('file://'):
            f = data.replace("file://", "").strip()
            if os.path.isdir(f): # parse directories
                name = os.path.basename(f)
                cmd = 'exo-open --launch FileManager "{}"'.format(f)
                icon = "folder"
                self.add_item_to_section(name, cmd, icon, None, section)
            elif os.path.isfile(f): # is it file?
                if data.endswith('.desktop'): # une applicatino
                    name, cmd, icon, generic = get_info_desktop(f)
                    self.add_item_to_section(name, cmd, icon, generic, section)
                else:
                    name = os.path.basename(f) # un fichier
                    cmd = 'exo-open "{}"'.format(f)
                    #raccourci pour fichier sans icone
                    self.add_item_to_section(name, cmd, "empty", None, section) 
        elif data.startswith("http://") or \
                data.startswith("https://") or \
                data.startswith("ftp://"):  # cas d'une url
            name = data.split('/')[2]
            cmd = "exo-open --launch WebBrowser {}".format(data)
            self.add_item_to_section(name, cmd, "text-html", "Lien vers une url", section) 


    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time, section):
        if data.get_data_type().name() == "text/uri-list":
            uris = data.get_uris()
            for u in uris:
                self.handle_drop(u, section)
            drag_context.finish(True, False, time)
        return(True)

    def on_drag_motion(self, widgt, context, c, y, time):
        Gdk.drag_status(context, Gdk.DragAction.COPY, time)
        return True

    def on_drag_drop(self, widget, context, x, y, time):
        widget.drag_get_data(context, context.list_targets()[-1], time)
        return(True)
    
    def del_appli(self, widget, dialog, section, app):
        self.del_item_from_section(section, app)
        dialog.destroy() # delete parent

    def edit_appli(self, widget, event, section, app):
        d = Gtk.Dialog(title=_("Edit the launcher"))
        # Edition du nom de l'appli
        entry = Gtk.Entry()
        entry.connect("activate", self.mod_app_name, entry, d, section, app) # entrée valide
        entry.show()

        namebtn = Gtk.Button(label = _("Change"))
        namebtn.connect_object("clicked", self.mod_app_name, entry, None, d, section, app )
        namebtn.show()

        # on met ça dans une boîte
        box = Gtk.HBox(False,2)
        box.pack_start(entry, True, True, 3)
        box.pack_start(namebtn, False, False, 0)
        box.show()
        
        # et le tout dans un étiquette
        nameframe = Gtk.Frame(label = _("Change the label"))
        nameframe.add(box)
        nameframe.show()

        # Changement de l'icône
        iconbtn = Gtk.Button(label = _("Change icon"))
        iconbtn.connect_object("clicked", self.mod_app_icon_dialog, entry, None, d, section, app )
        iconbtn.show()

        # on met ça dans une boîte
        
        # et le tout dans un étiquette
        iconframe = Gtk.Frame(label = _("Change the application icon"))
        iconframe.add(iconbtn)
        iconframe.show()

        # déplacement de l'application
        upbtn = Gtk.Button(label=_("Move up"))
        downbtn = Gtk.Button(label=_("Move down"))

        upi = Gtk.Image()
        upi.set_from_stock(Gtk.STOCK_GO_UP, Gtk.IconSize.MENU)
        upbtn.set_image(upi)
        downi = Gtk.Image()
        downi.set_from_stock(Gtk.STOCK_GO_DOWN, Gtk.IconSize.MENU)
        downbtn.set_image(downi)

        upbtn.connect_object("clicked", self.move_app_up, None, d, section, app)
        downbtn.connect_object("clicked", self.move_app_down, None, d, section, app)

        upbtn.show()
        downbtn.show()
	
        # on met ça dans une boîte
        box = Gtk.HBox(False,2)
        box.pack_start(upbtn, True, True, 3)
        box.pack_start(downbtn, False, False, 0)
        box.show()
        
        # et le tout dans un étiquette
        moveframe = Gtk.Frame(label = _("Move this app"))
        moveframe.add(box)
        moveframe.show()

        # Nécessaire pour la suppression
        delbtn = Gtk.Button(label = _("Delete"), stock=Gtk.STOCK_DELETE)
        delbtn.connect("clicked", self.del_appli, d, section, app)
        delbtn.show()
        delframe = Gtk.Frame(label = _("Delete this launcher"))
        delframe.add(delbtn)
        delframe.show()

        # ajout des objets au dialogue
        d.vbox.pack_start(nameframe, True, True, 0)
        d.vbox.pack_start(iconframe, True, True, 0)
        d.vbox.pack_start(moveframe, True, True, 0)
        d.vbox.pack_start(delframe, True, True, 0)
        d.run()


    def make_entrylist(self):
        self.section_list = Gtk.Notebook()
        self.section_list.set_tab_pos(Gtk.PositionType.LEFT)   
        self.section_list.set_scrollable(True)

        for s in self.config:
            label = Gtk.Label(s['name'])
            applist = Gtk.VBox()

            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            scrolled_window.set_size_request(620,-1)
            self.section_list.append_page(scrolled_window, label)

            # pour ajouter des applications
            scrolled_window.drag_dest_set(0, [], 0)
            scrolled_window.drag_dest_add_text_targets()
            scrolled_window.drag_dest_add_uri_targets()
            scrolled_window.connect("drag-data-received", self.on_drag_data_received, s)
            scrolled_window.connect("drag-drop", self.on_drag_drop)
            scrolled_window.connect('drag-motion', self.on_drag_motion)

            # boutons de config
            hb = Gtk.HBox(False, 10)

            delbtn = Gtk.Button(label = _("Delete this section"))
            delbtn.connect_object("clicked", self.del_section, s)

            addbtn = Gtk.Button(label=_("Search for applications"))
            addbtn.connect("button_press_event", self.appfinder)
            
            hb.pack_start(addbtn, True, True, 0)
            hb.pack_start(delbtn, True, True, 0)
            
            if self.config.index(s) > 0:
                upbtn = Gtk.Button(label = _("Move section up"))
                upbtn.connect_object("clicked", self.move_sec, s, -1)
                hb.pack_start(upbtn, True, True, 0)
            if self.config.index(s) < len(self.config)-1:
                downbtn = Gtk.Button(label = _("Move section down"))
                downbtn.connect_object("clicked", self.move_sec, s, +1)
                hb.pack_start(downbtn, True, True, 0)

            applist.pack_start(hb, False,False, 10)
            
            dragdrophelp = Gtk.Label(_("To add an application, Drag and drop it below"))
            applist.pack_start(dragdrophelp, False,False, 2)

            for a in s['apps']:
                appname, icon, cmd= a['name'], a['icon'], a['cmd']
                image = Gtk.Image()
                if icon.endswith('.png') or icon.endswith('.jpg'):
                    image.set_from_file(icon)
                else:
                    image.set_from_icon_name(icon, iconsize)
                    image.set_from_icon_name(icon, Gtk.IconSize.DIALOG)
                    image.set_pixel_size(iconsize)
                # nom de l'appli
                bapp = Gtk.Button(label=appname)
                bapp.set_image(image)
                #l'image est au dessus du texte
                bapp.set_image_position(Gtk.PositionType.TOP)
                # apparence du bouton
                bapp.set_relief(Gtk.ReliefStyle.NONE)
                bapp.connect("button_release_event", self.edit_appli, s, a)
                applist.pack_start(bapp, True, True, 0)


            scrolled_window.add_with_viewport(applist)

        # ajout de la possibilité d'ajouter des sections
        addbox = Gtk.VBox()
        instruction = Gtk.Label(_("Name of the new section: "))
        entry = Gtk.Entry()
        entry.connect("activate", self.add_new_section) # entrée valide
        addbox.pack_start(instruction, False, True, 3)
        addbox.pack_start(entry, False, False, 20)

        addbtn = Gtk.Button(label = _("More"), stock=Gtk.STOCK_ADD)
        addbtn.connect_object("clicked", self.add_new_section, entry )
        addbox.pack_start(addbtn, False, False, 10)

        addlabel = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(handy_icons,"add_section.png"))
        scaled_buf = pixbuf.scale_simple(24,24,GdkPixbuf.InterpType.BILINEAR)
        addlabel.set_from_pixbuf(scaled_buf)
        addlabel.set_tooltip_text(_("Add a section"))
        self.section_list.append_page(addbox, addlabel)

        self.mainbox.pack_start(self.section_list, True, True, 0)

    def module_toggle(self, widget, module):
        if widget.get_active():
            add_module(module)
        else:
            del_module(module)
    
    def make_menu(self, initialize = True):
        """build the menu"""
        if initialize :
            self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
            self.window.connect("delete_event", self.close_application)

            self.window.set_title("Handymenu configuration")
            self.window.set_border_width(0)
        else:
            self.window.remove(self.mainbox)

        # Conteneur principal
        self.mainbox = Gtk.VBox(False, 10)
        self.mainbox.set_border_width(10)

        # configuration principale
        self.make_entrylist()

        # coches pour modules
        modulesbox = Gtk.HBox(False, 5)
        modulesframe = Gtk.Frame(label = _("Modules"))
        modulesframe.add(modulesbox)
        self.mainbox.pack_start(modulesframe, False, False, 0)

        # module recent_files
        recents_files_check = Gtk.CheckButton(_("Show recent files"))
        recents_files_check.set_tooltip_text(_("Show recent files"))
        if "_recent_files_" in load_modules()[1]:
            recents_files_check.set_active(True)
        recents_files_check.connect("toggled", self.module_toggle, "_recent_files_")
        modulesbox.pack_start(recents_files_check, False, False,0)

        # module firefox most viewed
        most_ffox_check = Gtk.CheckButton(_("Most visited"))
        most_ffox_check.set_tooltip_text(_("Show most visited uri"))
        if "_most_ffox_view_" in load_modules()[1]:
            most_ffox_check.set_active(True)
        most_ffox_check.connect("toggled", self.module_toggle, "_most_ffox_view_")
        modulesbox.pack_start(most_ffox_check, False, False,0)

        # position des modules
        self.modules_position = Gtk.SpinButton()
        #adjustment = Gtk.Adjustment(0, start, max, step, 10, 0)
        adjustment = Gtk.Adjustment(0, 1, len(self.config)+1, 1, 10, 0)
        self.modules_position.set_adjustment(adjustment)
        self.modules_position.set_numeric(True)
        self.modules_position.set_value(load_modules()[0])
        self.modules_position.set_tooltip_text(_("Position of modules in menu"))
        self.modules_position.connect("value-changed", \
                lambda x: set_modules_position(self.modules_position.get_value_as_int()))
        modulesbox.pack_start(self.modules_position, False, False,1)

        # conteneur pour les boutons
        btnbox = Gtk.HBox(True, 2)
        self.mainbox.pack_start(btnbox, False, False, 0)

        defaultbtn = Gtk.Button(label = _("Reset"))
        resetimg = Gtk.Image()
        resetimg.set_from_stock(Gtk.STOCK_REDO, Gtk.IconSize.BUTTON)
        defaultbtn.set_image(resetimg)
        defaultbtn.connect_object("clicked", self.back_to_default, self.window )
        btnbox.pack_start(defaultbtn, False, False,0)
        
        viewbtn = Gtk.Button(label = _("View config"))
        viewbtn.connect("clicked", lambda x: self.view_config())
        btnbox.pack_start(viewbtn, False, False, 0)

        savebtn = Gtk.Button(label = _("Quit"), stock=Gtk.STOCK_CLOSE)
        savebtn.connect_object("clicked", self.close_application, self.window, None )
        btnbox.pack_start(savebtn, False, False, 0)

        self.window.add(self.mainbox)
        self.window.set_default_size(620, 560)
        self.window.show_all()

    def __init__(self):
        self.config = load_config()
        self.make_menu()

def main():
    menu = HandymenuConfig()
    Gtk.main()
    return 0        

if __name__ == "__main__":
    main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
