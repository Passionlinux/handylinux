#!/usr/bin/python3
# -*- coding:Utf-8 -*- 
# utils for handymenu

import os
import pickle
import gettext
from random import randint
from urllib.parse import unquote_plus
import subprocess
#import mimetypes

# options for handymenu
menuname = "HandyMenu"
configfile=os.path.expanduser('~/.handymenu4.conf')
noclose=os.path.expanduser('~/.handymenu-noclose.conf')
modulesfile=os.path.expanduser('~/.handymenu-modules.conf')
hmdir="/usr/share/handymenu"
configcmd="python3 {} &".format(os.path.join(hmdir,"handymenu-configuration.py")) 
handy_icons=os.path.join(hmdir,"icons")
handymenuicon=os.path.join(handy_icons,"handymenu_icon.png")

onglet_width = 11 
maxonglets = 7
max = 8     # maximum entry in recents
iconsize = 64
button_width = 22
win_max_width = 780

gettext.bindtextdomain('handymenu', '/usr/share/locale')
gettext.textdomain('handymenu')
_ = gettext.gettext

messages = [_("HandyLinux Rocks!"),\
        _("Come say hi to our forum"),\
        "Handylinux",\
        _("Computers for everyone"),\
        _("My debian is handy"),\
        _("All you need is handy"),\
        _("Beware, bunnies everywhere"),\
        "☺"
        ]


def set_default_config():
    print("reset configuration")
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

def random_msg():
    """return a random message"""
    return(messages[randint(0,len(messages)-1)])

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
                cmd = "xdg-open {}".format(path)
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

def get_most_ffox_viewed(max):
    """return a list of most viewed pages in firefox"""
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
        c2.execute("SELECT data FROM moz_favicons WHERE id=?",(u[2],))
        favicon = c2.fetchone()
        if favicon:
            with open('/tmp/hm-favicon-{}.ico'.format(u[2]), 'wb') as fav:
                fav.write(favicon[0])
            icon = "/tmp/hm-favicon-{}.ico".format(u[2])
        else:
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


