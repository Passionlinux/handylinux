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

from handymenu import *

def main():
    menu = Handymenu()
    menu.start()
    return 0        

if __name__ == "__main__":    
    main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
