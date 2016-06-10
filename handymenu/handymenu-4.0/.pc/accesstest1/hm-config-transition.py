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
            name = line.replace("name :::", "").strip()
            cursection['name'] = name
        elif line.startswith("id :::"):
            i = line.replace("id :::", "").strip()
            if i != "recent":
                i = int(i)
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

