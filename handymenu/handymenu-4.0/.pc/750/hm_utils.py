#!/usr/bin/python3
# -*- coding:Utf-8 -*- 
# utils for handymenu

import os
import pickle
import gettext
from urllib.parse import unquote_plus
import subprocess
#import mimetypes

# options for handymenu
menuname = "HandyMenu"
configdir=os.path.expanduser('~/.handymenu')
configfile=os.path.join(configdir,'handymenu.conf')
noclose=os.path.join(configdir,'handymenu-noclose.conf')
makeaccessfile=os.path.join(configdir,'handymenu-access.conf')
modulesfile=os.path.join(configdir,'handymenu-modules.conf')
hmdir="/usr/share/handymenu"
configcmd="python3 {} &".format(os.path.join(hmdir,"handymenu-configuration.py")) 
handy_icons=os.path.join(hmdir,"icons")
handymenuicon=os.path.join(handy_icons,"handymenu_icon.png")

onglet_width = 11 
maxonglets = 7
max = 8     # maximum entry in recents
iconsize = 64
button_width = 22
win_max_width = 660
version = "4.1"
auteur = "thuban"
licence = "GPLv3"
homepage = "https://handylinux.org"

gettext.bindtextdomain('handymenu', '/usr/share/locale')
gettext.textdomain('handymenu')
_ = gettext.gettext

def set_default_config():
    print("reset configuration")
    if not os.path.isdir(configdir):
        os.mkdir(configdir)
    with open(configfile, 'wb') as pkl:
        pickle.dump(hm_default_sections, pkl, pickle.HIGHEST_PROTOCOL)

def load_config():
    with open(configfile, 'rb') as pkl:
        try:
            config = pickle.load(pkl)
        except: #ancienne configuration ou config erronée?
            set_default_config()
            config = load_config()
        return(config)

def save_config(conf):
    # remove modules firts
    modlist = load_modules()
    for modid in modlist[1]:
        for s in conf:
            if s['id'] == modid:
                conf.remove(s)
    with open(configfile, 'wb') as pkl:
        pickle.dump(conf, pkl, pickle.HIGHEST_PROTOCOL)

def add_section(config, section):
    config.append(section)
    save_config(config)
    
def move_section(config, section, index):
    """move section of +1 or -1
    index = +1  or -1
    """
    toreload=False
    for s in config:
        if s == section:
            idx = config.index(s)
            if index == -1 : # on recule l'application
                if idx > 0 :
                    config[idx], config[idx-1] = config[idx-1], config[idx]
            elif index == 1 : # on avance l'application
                if idx < len(config) - 1:
                    config[idx], config[idx+1] = config[idx+1], config[idx]
            save_config(config)
            toreload=True
            break
    return(toreload)

def add_app(config, section, app):
    for s in config:
        if s == section:
            s['apps'].append(app)
            save_config(config)

def del_app(config, section, app):
    for s in config:
        if s == section:
            s['apps'].remove(app)
            save_config(config)

def mod_app(config, section, app, new):
    for s in config:
        if s == section:
            for a in s['apps']:
                if a == app:
                    a['name'] = new
                    save_config(config)

def mod_app_icon(config, section, app, newicon):
    for s in config:
        if s == section:
            for a in s['apps']:
                if a == app:
                    a['icon'] = newicon
                    save_config(config)

def move_app(config, section, app, index):
    """move app of +1 or -1
    index = +1  or -1
    """
    for s in config:
        if s == section:
            for a in s['apps']:
                if a == app:
                    idx = s['apps'].index(a)

                    if index == -1 : # on recule l'application
                        if idx > 0 :
                            s['apps'][idx -1], s['apps'][idx] = s['apps'][idx], s['apps'][idx-1]
                    elif index == 1 : # on avance l'application
                        if idx < len(s['apps']) - 1:
                            s['apps'][idx], s['apps'][idx+1] = s['apps'][idx+1], s['apps'][idx]
                    save_config(config)
                    break

def open_cmd(cmd):
    try:
        if cmd.startswith("xdg-open"): 
            # cas du module récents et des raccourcis fichiers
            c = [ "xdg-open", "".join(cmd.split(' ', 1)[1:]) ]
        else:
            c = [ w for w in cmd.split(' ') ]
        subprocess.Popen(c)
        return True
    except :
        print("Execution failed")
        return False

def save_modules(moduleslist):
    # a modulelist is [index [module1, module2]]
    with open(modulesfile, 'wb') as pkl:
        pickle.dump(moduleslist, pkl, pickle.HIGHEST_PROTOCOL)

def add_module(module):
    modlist = load_modules()
    if module not in modlist:
        modlist[1].append(module)
    save_modules(modlist)

def del_module(module):
    modlist = load_modules()
    while module in modlist[1]:
        modlist[1].remove(module)
    save_modules(modlist)

def load_modules():
    if os.path.isfile(modulesfile): 
        with open(modulesfile, 'rb') as pkl:
            return(pickle.load(pkl))
    else:
        return([0,[]])

def set_modules_position(pos):
    modlist = load_modules()
    modlist[0] = pos
    save_modules(modlist)

def get_recently_used(max):
    """return recently used files
    only a number of max
    """
    f = os.path.expanduser("~/.local/share/recently-used.xbel")
    if not os.path.isfile(f):
        return(False)

    recents = {}
    recents['id'] = "_recent_files_"
    recents['name'] = _("Recent files")
    recents['apps'] = []
    n = 0
    with open(f, 'r') as x:
        xbel = x.readlines()
        xbel.reverse()

    name, generic, icon, cmd = False, False, False, False
    for line in xbel:
        line = line.strip()
        if line.startswith("<bookmark href"):
            path = line.split('"')[1]
            path = unquote_plus(path).replace('file://','',1)
            if os.path.isfile(path):
                name = os.path.basename(path)
                generic = name 
                cmd = 'xdg-open {}'.format(path)
                #mimetype = mimetypes.guess_type(path)[0]
                #if mimetype:
                #    icon = mimetype.replace('/','-')
                #else:
                #    icon = "document-open-recent"
                
        elif line.startswith("<mime:mime-type"):
            #icon = line.split('"')[1].replace('/','-')
            icon = line.split('"')[1]
           

        if len(recents['apps']) < max and name and generic and icon and cmd:
            if path.lower().endswith(".jpeg") or path.lower().endswith(".jpg") \
                    or path.lower().endswith(".png") or path.lower().endswith(".gif"):
                icon = path
            app = {'name' : name, 'generic' : generic, 'icon' : icon, 'cmd':cmd}
            recents['apps'].append(app)
            name, generic, icon, cmd = False, False, False, False
        if len(recents['apps']) >= max:
            break

    return(recents)

"""
def get_most_ffox_viewed(max):
    import sqlite3 as sqlite
    import shutil
    import tempfile

    ffoxdirlist = os.listdir(os.path.expanduser('~/.mozilla/firefox'))
    ffsqlite = False
    for i in ffoxdirlist:
        if i.endswith(".default"):
            ffsqlite = os.path.join(os.path.expanduser('~/.mozilla/firefox'),i,"places.sqlite")
    if not ffsqlite:
        return(False)

    tf = tempfile.NamedTemporaryFile('r', suffix='.sqlite')
    shutil.copyfile(ffsqlite, tf.name)

    conn = sqlite.connect(tf.name)
    c2 = conn.cursor()
    c2.execute("SELECT url,title,favicon_id FROM moz_places ORDER BY visit_count DESC LIMIT ?",(max,))

    most_view = {}
    most_view['id'] = "_most_ffox_view_"
    most_view['name'] = _("Most visited")
    most_view['apps'] = []
    n = 0
    for u in c2.fetchall():
        if not u[0] or not u[1]: # pour les cas où y a rien
            continue
        #c2.execute("SELECT data FROM moz_favicons WHERE id=?",(u[2],))
        #favicon = c2.fetchone()
        #if favicon:
        #    with open('/tmp/hm-favicon-{}.ico'.format(u[2]), 'wb') as fav:
        #        fav.write(favicon[0])
        #    icon = "/tmp/hm-favicon-{}.ico".format(u[2])
        #else:
        #    icon = 'text-html'
        icon = 'text-html'
        n += 1
        name = os.path.basename(u[1])
        generic = name 
        cmd = "xdg-open {}".format(u[0])
        app = {'name' : name, 'generic' : generic, 'icon' : icon, 'cmd':cmd}
        most_view['apps'].append(app)
        if n == max:
            break
    conn.close()
    tf.close()
    return(most_view)
"""

imglist = ["""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
DYsAAAAASUVORK5CYII="""]


#app = {'name' : "Description l'application",\
#        'generic' : "Nom générique de l'application",\
#        'icon' : "icône de l'application",\
#        'cmd' : "commande"}
#applist = [app1, app2, app3, ...]
#section = {'name': 'Recent', 'apps' : applist , id : ''}
#sections = [section1, section2,...]
hm_default_sections = \
[\
    {'name' : _("Latest"),\
    'id': "recent",\
    'apps': [\
        {'name' : _("Web browser"),\
        'generic': _("Surf the web"),\
        'icon' : "iceweasel",\
        'cmd' : "iceweasel"\
        },\
        {'name' : _("Personal folder"),\
        'generic': _("Browse my personal directory"),\
        'icon' : "/usr/share/handymenu/icons/file_home.png",\
        'cmd' : "exo-open --launch FileManager {}".format(os.path.expanduser("~"))\
        },\
        {'name' : _("Framasoft"),\
        'generic': _("Acces to free (as in freedom) Framasoft services"),\
        'icon' : "/usr/share/handymenu/icons/internet_framasoft.png",\
        'cmd' : "iceweasel http://www.framasoft.net/#topPgCloud"\
        },\
        {'name' : _("HandyLinux Help Center"),\
        'generic': _("Open HandyLinux Help Tool"),\
        'icon' : "/usr/share/handymenu/icons/handymenu_icon.png",\
        'cmd' : "ausecours"\
        },\
        {'name' : _("Applications list"),\
        'generic': _("Access to all installed applications"),\
        'icon' : "edit-find",\
        'cmd' : "xfce4-appfinder"\
        },\
        {'name' : _("Office suite"),\
        'generic': _("Full LibreOffice suite"),\
        'icon' : "libreoffice-main",\
        'cmd' : "libreoffice"\
        },\
    ]\
    },\

    {'name' : _("Internet"),\
    'id': 0,\
    'apps': [\
        {'name' : _("Surf the Web"),\
        'generic': _("Browse the internet"),\
        'icon' : "iceweasel",\
        'cmd' : "iceweasel"\
        },\
        {'name' : _("Read or write emails"),\
        'generic': _("Consult or edit emails"),\
        'icon' : "icedove",\
        'cmd' : "icedove"\
        },\
        {'name' : _("Communicate with skype"),\
        'generic': _("Communicate freely with the NSA"),\
        'icon' : "skype",\
        'cmd' : "skype"\
        },\
        {'name' : _("Framasoft Services"),\
        'generic': _("Acces to free (as in freedom) Framasoft services"),\
        'icon' : "/usr/share/handymenu/icons/internet_framasoft.png",\
        'cmd' : "iceweasel http://www.framasoft.net/#topPgCloud"\
        },\
        {'name' : _("P2P torrent client"),\
        'generic': _("Share datas with P2P"),\
        'icon' : "transmission",\
        'cmd' : "transmission-gtk"\
        },\
        {'name' : _("Internet help"),\
        'generic': _("Get some help about internet applications"),\
        'icon' : "/usr/share/handymenu/icons/help.png",\
        'cmd' : "iceweasel https://handylinux.org/wiki/doku.php/fr/internet"\
        },\
    ]\
    },\

    {'name' : _("Files"),\
    'id': 1,\
    'apps': [\
        {'name' : _("My Pictures"),\
        'generic': _("Browse my images folder"),\
        'icon' : "/usr/share/handymenu/icons/file_pictures.png",\
        'cmd' : "exo-open --launch FileManager {}".format(\
        subprocess.check_output(["xdg-user-dir", "PICTURES"]).decode('utf-8').strip())\
        },\
        {'name' : _("My Documents"),\
        'generic': _("Browse my documents"),\
        'icon' : "/usr/share/handymenu/icons/file_documents.png",\
        'cmd' : "exo-open --launch FileManager {}".format(\
        subprocess.check_output(["xdg-user-dir", "DOCUMENTS"]).decode('utf-8').strip())\
        },\
        {'name' : _("My Music"),\
        'generic': _("Browse my music folder"),\
        'icon' : "/usr/share/handymenu/icons/file_music.png",\
        'cmd' : "exo-open --launch FileManager {}".format(\
        subprocess.check_output(["xdg-user-dir", "MUSIC"]).decode('utf-8').strip())\
        },\
        {'name' : _("My Videos"),\
        'generic': _("Browse my videos"),\
        'icon' : "/usr/share/handymenu/icons/file_videos.png",\
        'cmd' : "exo-open --launch FileManager {}".format(\
        subprocess.check_output(["xdg-user-dir", "VIDEOS"]).decode('utf-8').strip())\
        },\
        {'name' : _("Downloads"),\
        'generic': _("Check my downloaded files"),\
        'icon' : "/usr/share/handymenu/icons/file_download.png",\
        'cmd' : "exo-open --launch FileManager {}".format(\
        subprocess.check_output(["xdg-user-dir", "DOWNLOAD"]).decode('utf-8').strip())\
        },\
        {'name' : _("Personal folder"),\
        'generic': _("Browse my personal directory"),\
        'icon' : "/usr/share/handymenu/icons/file_home.png",\
        'cmd' : "exo-open --launch FileManager {}".format(os.path.expanduser("~"))\
        },\
        {'name' : _("Check the trash"),\
        'generic': _("Check and empty trash"),\
        'icon' : "/usr/share/handymenu/icons/file_trash.png",\
        'cmd' : "exo-open --launch FileManager trash:///"\
        },\
        {'name' : _("Files help"),\
        'generic': _("Get some help about file management"),\
        'icon' : "/usr/share/handymenu/icons/help.png",\
        'cmd' : "iceweasel https://handylinux.org/wiki/doku.php/fr/fichiers"\
        },\
    ]\
    },\

    {'name' : _("Office"),\
    'id': 4,\
    'apps': [\
        {'name' : _("Text editor"),\
        'generic': _("Consult or edit text files"),\
        'icon' : "accessories-text-editor",\
        'cmd' : "mousepad"\
        },\
        {'name' : _("Take notes"),\
        'generic': _("Minimalist reminder"),\
        'icon' : "xfce4-notes-plugin",\
        'cmd' : "xfce4-notes"\
        },\
        {'name' : _("Calculator"),\
        'generic': _("Perform mathematical calculations"),\
        'icon' : "gnome-calculator",\
        'cmd' : "gnome-calculator"\
        },\
        {'name' : _("Office suite"),\
        'generic': _("Full LibreOffice suite"),\
        'icon' : "libreoffice-main",\
        'cmd' : "libreoffice"\
        },\
        {'name' : _("Scan documents"),\
        'generic': _("Simply scan a document"),\
        'icon' : "scanner",\
        'cmd' : "simple-scan"\
        },\
        {'name' : _("Office help"),\
        'generic': _("Get some help about office applications"),\
        'icon' : "/usr/share/handymenu/icons/help.png",\
        'cmd' : "iceweasel https://handylinux.org/wiki/doku.php/fr/office"\
        },\
    ]\
    },\

    {'name' : _("Multimedia"),\
    'id': 3,\
    'apps': [\
        {'name' : _("Multimedia player"),\
        'generic': _("Watch video, DVD ou play music"),\
        'icon' : "vlc",\
        'cmd' : "vlc"\
        },\
        {'name' : _("Images viewer"),\
        'generic': _("Watch your favorite pictures and photos"),\
        'icon' : "ristretto",\
        'cmd' : "ristretto"\
        },\
        {'name' : _("Music player"),\
        'generic': _("Play music, playlist or radio"),\
        'icon' : "clementine",\
        'cmd' : "clementine"\
        },\
        {'name' : _("CD/DVD burner"),\
        'generic': _("Backup datas on CD ou DVD"),\
        'icon' : "media-cdrom",\
        'cmd' : "xfburn"\
        },\
        {'name' : _("Volume control"),\
        'generic': _("Adjust computer sound level"),\
        'icon' : "xfce4-mixer",\
        'cmd' : "xfce4-mixer"\
        },\
        {'name' : _("Multimedia help"),\
        'generic': _("Get some help about multimedia applications"),\
        'icon' : "/usr/share/handymenu/icons/help.png",\
        'cmd' : "iceweasel https://handylinux.org/wiki/doku.php/fr/media"\
        },\
    ]\
    },\

    {'name' : _("Games"),\
    'id': 5,\
    'apps': [\
        {'name' : _("Play sudoku"),\
        'generic': _("Numbers puzzle"),\
        'icon' : "gnome-sudoku",\
        'cmd' : "gnome-sudoku"\
        },\
        {'name' : _("Play bricks"),\
        'generic': _("Play a Tetris clone"),\
        'icon' : "ltris",\
        'cmd' : "ltris"\
        },\
        {'name' : _("Play cards"),\
        'generic': _("Play cards"),\
        'icon' : "gnome-aisleriot",\
        'cmd' : "sol"\
        },\
        {'name' : _("Brain training"),\
        'generic': _("GBrainy games suite"),\
        'icon' : "gbrainy",\
        'cmd' : "gbrainy"\
        },\
        {'name' : _("Board game"),\
        'generic': _("Play Mahjong"),\
        'icon' : "gnome-mahjongg",\
        'cmd' : "gnome-mahjongg"\
        },\
        {'name' : _("Play with bubbles"),\
        'generic': _("Align colored bubbles"),\
        'icon' : "flobopuyo",\
        'cmd' : "flobopuyo"\
        },\
    ]\
    },\

    {'name' : _("Adventurers"),\
    'id': 6,\
    'apps': [\
        {'name' : _("Open a terminal"),\
        'generic': _("Get access to the command line"),\
        'icon' : "utilities-terminal",\
        'cmd' : "exo-open --launch TerminalEmulator"\
        },\
        {'name' : _("Software Library"),\
        'generic': _("Software management"),\
        'icon' : "handysoft",\
        'cmd' : "handysoft"\
        },\
        {'name' : _("Applications list"),\
        'generic': _("Access to all installed applications"),\
        'icon' : "edit-find",\
        'cmd' : "xfce4-appfinder"\
        },\
        {'name' : _("Network configuration"),\
        'generic': _("Configure your network connection"),\
        'icon' : "gnome-nettool",\
        'cmd' : "nm-connection-editor"\
        },\
        {'name' : _("Printer configuration"),\
        'generic': _("Add and configure a printer"),\
        'icon' : "printer",\
        'cmd' : "system-config-printer"\
        },\
        {'name' : _("Detailed configuration"),\
        'generic': _("Configure each part of HandyLinux"),\
        'icon' : "preferences-system",\
        'cmd' : "xfce4-settings-manager"\
        },\
    ]\
}\
]


