#!/usr/bin/env python
# -*- coding:Utf-8 -*- 

import urllib.request
import os
import re
import base64
import time
from data import *

appname = "handysoft"
version = "1.1"
auteur = "thuban"
licence = "GPLv3"
homepage = "https://handylinux.org/wiki/doku.php/fr/packages#handysoft"

import gettext
gettext.bindtextdomain(appname, '/usr/share/locale')
gettext.textdomain(appname)
_ = gettext.gettext

handysofticon = "/usr/share/pixmaps/handysoft.png" 
termcmd = "/usr/bin/x-terminal-emulator -e"

imagecache = os.path.expanduser("~/.local/share/handysoft/cache/")
dummythb = os.path.join(imagecache,"dummythb.png")
thblistfile = os.path.join(imagecache,"thblist.pkl")
month = 60*60*24*30 #secondes dans un mois

iconsize = 32
onglet_width = 10
width, height = 600, 450 

categories = [ \
    {'section': 'hlfav', 'icon':'/usr/share/pixmaps/handymenu_icon.png', 'label':_('Suggested') },\
    {'section': 'games', 'icon':'applications-games', 'label':_('Games') },\
    {'section': 'educ', 'icon':'applications-science', 'label':_('Education') },\
    {'section': 'multimedia', 'icon':'applications-multimedia', 'label':_('Multimedia') },\
    {'section': 'internet', 'icon':'applications-internet', 'label':_('Internet') },\
    {'section': 'office', 'icon':'applications-office', 'label':_('Office') },\
    {'section': 'graphics', 'icon':'applications-graphics', 'label':_('Graphics') },\
    {'section': 'misc', 'icon':'applications-utilities', 'label':_('Tools and others') },\
    {'section': 'expert', 'icon':'applications-system', 'label':_('Expert') }
    ]

# catégories RàB
dontcare = ['debug', 'gnustep', 'haskell', 'ruby', \
            'gnu-r', 'ocaml', 'libdevel', 'python', 'interpreters', \
            'doc', 'tasks', 'introspection', 'java', 'tex', \
            'kernel', 'php', 'shells', 'news', 'libs', 'zope',\
            'httpd', 'hamradio', 'devel', 'oldlibs', 'database', \
            'lisp', 'perl', 'cli-mono', 'vcs', 'comm', 'metapackages']


def getcateg(section):
    '''classe les paquets selon les catégories suivantes : 
    games,
    educ,
    multimedia,
    internet,
    office,
    graphics
    misc : divers
    '''
    office = ['text', 'editors', 'fonts']
    educ = ['science', 'math', 'education', 'electronics']
    multimedia = ['sound', 'video']
    internet = ['web', 'mail', 'net']

    if section =='games':
        return(section)
    elif section in educ:
        return('educ')
    elif section in multimedia:
        return('multimedia')
    elif section in internet:
        return('internet')
    elif section in office:
        return('office')
    elif section == 'graphics':
        return('graphics')
    else:
        return("misc")

def get_pkg_list(cache):
    sections = {'games':[], 'educ':[], 'multimedia':[], 'internet':[],\
            'office':[], 'graphics':[], 'misc':[]}

    for p in cache:
        sections[getcateg(p.section)].append(p.name)

    return(sections)

def trie_paquet(shortname, section):
    if section in dontcare:
        return(False)
    elif not keeppkg(shortname):
        return(False)
    #if p.is_installed: # on ne liste pas les paqets déjà installés
    #    continue

    return(True)

def keeppkg(pkg):
    ends = ['-data', '-common', '-examples', '-core', \
    '-mysql', '-postgres', '-sqlite', \
    '-cli', '-dev']
    #begins = ['lib']

    #for i in begins:
    #    if pkg.startswith(i):
    #        return(False)
    for i in ends:
        if pkg.endswith(i):
            return(False)
    return(True)

def dl_shot_hl(package, thumb=True):
    if thumb:
        url = "http://artwork.handylinux.org/pkgs/thb/{}".format(package)
    else:
        url = "http://artwork.handylinux.org/pkgs/{}".format(package)
    try:
        response = urllib.request.urlopen(url) 
    except:
        response = False

    return(response)

def dl_shot(package, thumb=True):
    """ download package screenshot"""
    if thumb:
        imgpath = os.path.join(imagecache,"{}-thb.png".format(package)) 
    else:
        imgpath = os.path.join(imagecache,"{}.png".format(package)) 

    if os.path.isfile(imgpath):
        return(imgpath)

    else:
        response = dl_shot_hl(package, thumb)
        if not response:
            try:
                if thumb:
                    url = "http://screenshots.debian.net/thumbnail/{}".format(package)
                else:
                    url = "http://screenshots.debian.net/screenshot/{}".format(package)
                response = urllib.request.urlopen(url) 
            except:
                # pas de screenshot disponible
                return(get_dummy())

        with open(imgpath, "wb") as fp:
            data = response.read() # a `bytes` object
            fp.write(data)
            return(fp.name)

def get_dummy():
    '''return the dummy thumbnail'''
    if not os.path.isfile(dummythb):
        with open(dummythb, "wb") as dummy:
            img = base64.b64decode(dummythbb64)
            dummy.write(img)
    return(dummythb)


def get_avail_thb():
    '''récupère la liste des paquets possédant un aperçu
    et l'enregistre si besoin
    '''
    recup = False
    if not os.path.isfile(thblistfile) : # si le fichier n'existe pas
        recup = True
    elif time.time() - os.path.getmtime(thblistfile) > month : # fichier + vieux qu'un mois
        print("vieille liste de screenshots, on recharge")
        recup = True

    if recup:
        thbs = []
        try:
            import json
            url = 'https://screenshots.debian.net/packages/pkglist'
            with urllib.request.urlopen(url) as resp:
                j = json.loads(resp.read().decode('utf-8'))
            # thb dispos avec hl:
            url = 'http://artwork.handylinux.org/pkgs/thb/hlfavs.list'
            with urllib.request.urlopen(url) as resp:
                hlthblist = [n.decode('utf-8').strip() for n in resp.readlines()]
            # liste des thb disponibles
            thbs = [p.get('name') for p in j['packages']] + hlthblist

            # on sauve cette liste
            import pickle
            with open(thblistfile, 'wb') as pkl:
                pickle.dump(thbs, pkl, pickle.HIGHEST_PROTOCOL)
        except:
            pass

        return(thbs)

    else:
        # on retourne le fichier listant les paquets dispos
        import pickle
        with open(thblistfile, 'rb') as pkl:
            return(pickle.load(pkl))

def getimage(name):
    import tempfile
    g = base64.b64decode(imagesdic[name])
    t = tempfile.NamedTemporaryFile(delete=False)
    t.write(g)
    return(t.name)

def synaptic():
    import subprocess
    subprocess.Popen("gksudo synaptic", shell=True)
    from gi.repository import Gtk
    Gtk.main_quit()

def update_checker():
    import subprocess
    subprocess.Popen("handy-update-checker", shell=True)

def cache_search(cache, sch, description=False):
    """search for a package matching 'sch' in cache"""
    sch = sch.lower()
    exp = re.compile(sch)
    if description:
        try:
            res = [p for p in cache if exp.search(p.name.lower()) != None \
                    or exp.search(p.candidate.description.lower()) != None]
        except AttributeError : # le paquet n'a pas de description
            res = [p for p in cache if exp.search(p.name.lower()) != None ]
    else:
        res = [p for p in cache if exp.search(p.name.lower()) != None ]

    # On met au début les paquets qui commences comme la recherche.
    # tri par partinence très basique...
    res_sorted = []
    first = False
    for p in res:
        if p.name.lower() == sch:
            first = res.pop(res.index(p))
        elif p.name.lower().startswith(sch):
            res.insert(0,res.pop(res.index(p)))
    if first:
        res.insert(0,first)

    return(res)
'''
    for p in cache:
        #if not trie_paquet(p.shortname, p.section):
        #    continue
        found = exp.search(p.name.lower())
        if found != None:
            res.append(p)
        elif description:
            c = p.candidate
            if c:
                found = exp.search(c.description.lower())
                if found != None:
                    res.append(p)
'''

def install_pkg(pkg):
    import subprocess
    installer = os.path.join(os.path.dirname(os.path.realpath(__file__)),"soft_install.py")
    aptcmd = "apt-get install -y {}".format(pkg)
    msg = _("Installing a new package : ")
    subprocess.call('gksudo -m "{3} {1}" "python3 {0} -m {3} {1} -c {2}"'.format(\
        installer, pkg, aptcmd, msg), shell=True)

def remove_pkg(pkg):
    import subprocess
    installer = os.path.join(os.path.dirname(os.path.realpath(__file__)),"soft_install.py")
    aptcmd = "apt-get purge -y {}".format(pkg)
    msg = _("Removing a package : ")
    subprocess.call('gksudo -m "{3} {1}" "python3 {0} -m {3} {1} -c {2}"'.format(\
        installer, pkg, aptcmd, msg), shell=True)


def dolaby(x,y):
    laby = Laby(0, 0, x, y, (0,0), (x-1,y-1))            #création du labyrinthe
    laby.construire()

    # remplissage des murs
    i = 0
    line = ''
    labyrinth = laby._get_laby()
    labyrinth[-1].car = "→"

    carlist = []
    row = []
    i = 0
    for c in laby._get_laby():
        # une ligne par liste intermédiaire
        row.append(c.car)
        i +=1
        if i == x:
            carlist.append(row)
            row = []
            i = 0
    return(carlist)

def canigo(laby, newpos):
    if laby[newpos[1]][newpos[0]] != '#':
        return(True)
    else:
        return(False)
 
def labytotext(laby, pos):
    text=""
    for line in laby:
        text += "".join(line)
        text += "\n"

    linelength = len(laby[0])
    tmptxt = list(text)

    playerpos = pos[0] + ( pos[1] * (linelength +1))
    if tmptxt[playerpos] != "#":
        tmptxt[playerpos] = "@"

    text = "".join(tmptxt)
    text = text[:-1] # enlève le dernier retour chariot
    return(text)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

