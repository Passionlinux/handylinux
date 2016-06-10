#!/usr/bin/python
# -*- coding:Utf-8 -*- 


"""

Auteur :      thuban <thuban@yeuxdelibad.net>  
licence :     GNU General Public Licence v3

Description : Conversion de la configuration du menu v3 au menu v4
    (passage de python2 à python3)
"""

import sys
import pickle
import os
import gettext

gettext.bindtextdomain('handymenu', '/usr/share/locale')
gettext.textdomain('handymenu')
_ = gettext.gettext

configfile=os.path.expanduser('~/.handymenu.conf')
configdir=os.path.expanduser('~/.handymenu')
newconfigfile=os.path.join(configdir,'handymenu.conf')
tmpfile='/tmp/handymenuconfigconversion'


def config2txt():
    print("Saving handymenu3 configuration")
    with open(configfile, 'rb') as pkl:
        config = pickle.load(pkl)

    txtconfig = ""

    for section in config:
        for key, value in section.iteritems():
            txtconfig += str(key) + " ::: "
            if key == "apps":
                appstring = ""
                for item in value:
                    appstring += '{'
                    app = ""
                    for titre, texte in item.iteritems():
                        app += '"{}":"{}",'.format(titre,texte)
                    #remove last ,
                    app = app.rsplit(',', 1)[0]
                    appstring += app + '}!!'

                appstring = appstring.rsplit('!!', 1)[0]
                txtconfig += appstring + "\n"
            else:
                txtconfig += str(value) + "\n"

        txtconfig += "---endsection---" + "\n"

    with open(tmpfile, 'w') as t:
        t.write(txtconfig)


def txt2config():
    import subprocess
    newfileapplist = [\
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
    ]

    newrecentsapplist = [\
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
 
    print("Converting to handymenu4 configuration")
    if not os.path.isdir(configdir):
        os.mkdir(configdir)

    with open(tmpfile, 'r') as t:
        config = t.readlines()

    newconfig = []
    cursection = {}
    for line in config:
        line = line.strip()
        if line.startswith("apps :::"):
            applist = []
            applistofdic = line.replace("apps :::", "").strip()
            for d in applistofdic.split('!!'):
                applist.append(eval(d))

            cursection['apps'] = applist
        elif line.startswith("name :::"):
            if "name ::: Fichiers" in line:
                # set new syntax
                cursection['apps'] = newfileapplist

            name = line.replace("name :::", "").strip()
            cursection['name'] = name
        elif line.startswith("id :::"):
            i = line.replace("id :::", "").strip()
            if i != "recent":
                i = int(i)
            else:
                cursection['apps'] = newrecentsapplist
            cursection['id'] = i
        elif line.strip() == "---endsection---" :
            newconfig.append(cursection)
            cursection = {}

    with open(newconfigfile, 'wb') as pkl:
        pickle.dump(newconfig, pkl, pickle.HIGHEST_PROTOCOL)


def main():
    if len(sys.argv) != 2:
        print("usage:")
        print("python hm-config-transition.py 1")
        print("python3 hm-config-transition.py 2")
    else:
        if sys.argv[1] == "1":
            config2txt()
        elif sys.argv[1] == "2":
            txt2config()

    return 0

if __name__ == '__main__':
	main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
