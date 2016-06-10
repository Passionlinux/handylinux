#!/usr/bin/env python3
# -*- coding:Utf-8 -*- 
# Fichier: btshare.py
# Cree le 27 mars 2015 16:37:22


"""

Auteur :      thuban (thuban@yeuxdelibad.net)  
licence :     GNU General Public Licence 3

Description :
    btshare : permet de partager de gros fichiers via bittorrent

TODO : 
    - Ajout de boutons pour ajouter/supprimer des torrents
    - Ajout d'un menu de configuration?
    Plus d'informations sur les partages

"""
import sys
import os
import webbrowser
import threading
import socket

# local imports
from btshare_session import *
from btshare_flask import *

configdir="~/.btshare"

def lock(process_name):
    """only one instance"""
    global lock_socket   # Without this our lock gets garbage collected
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + process_name)
        with open(os.path.join(\
                os.path.expanduser(configdir),\
                "btshare.pid"),"w") as p:
            p.write(str(os.getpid()))
    except socket.error:
        print("BTshare est déjà en cours d'exécution")
        sys.exit(0)

def help():
    print("usage : {0} <directory with files to share>".format(sys.argv[0]))
    print("once running:")
    print("     {0} /path/to/torrent_file_to_add".format(sys.argv[0]))
    print("or")
    print("     {0} magnet:?xt=urn:btih:268ba89e2f[...]&dn=name".format(sys.argv[0]))
    sys.exit(0)


def main():
    if len(sys.argv) > 2:
        help()
    elif len(sys.argv) == 2:
        a = os.path.expanduser(sys.argv[1])
    else:
        a = ""
    confdir = os.path.expanduser(configdir)
    torrentdir = os.path.join(confdir,"torrents")
    new = os.path.join(confdir,"new")
    newmagnet = os.path.join(new,"newmagnet")

    if not os.path.isdir(confdir):
        os.makedirs(confdir)
    if not os.path.isdir(torrentdir):
        os.makedirs(torrentdir)
    if not os.path.isdir(new):
        os.makedirs(new)

    if os.path.isdir(a):
        share = a
    elif a.endswith(".torrent"):
        print("copy {0} to {1}".format(a,new))
        copy(a,new)
        share = ""
    elif a.find("magnet:") == 0:
        print("add {0} to BTshare".format(a))
        with open(newmagnet, "w") as m:
            m.write(a)
        share = ""
    else:
        share = ""


    lock("BTshare")

    ses = LTSession(share, confdir)
    ses.run()

    btshare = App(ses)

    flask_thread = threading.Thread(target=btshare.run)
    flask_thread.start()
    webbrowser.open("http://localhost:{0}".format(btshare.port))


    return 0

if __name__ == '__main__':
	main()

