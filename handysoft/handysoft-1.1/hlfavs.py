#!/usr/bin/env python
# -*- coding:Utf-8 -*- 

appname = "handysoft"

import gettext
gettext.bindtextdomain(appname, '/usr/share/locale')
gettext.textdomain(appname)
_ = gettext.gettext

hlfavs = [\
    {"name": "asunder", "desc" : _("Graphical audio CD ripper and encoder") },\
    {"name": "atril","desc" : _("Simple multi-page document viewer") },\
    {"name": "audacity","desc" : _("Cross-platform multi-track audio editor") },\
    {"name": "avidemux","desc" : _("Free video editor") },\
    {"name": "calibre","desc" : _("E-book converter and library management") },\
    {"name": "catfish","desc" : _("File searching tool, configurable via the command line") },\
    {"name": "cheese","desc" : _("Tool to take pictures and videos from your webcam") },\
    {"name": "clementine","desc" : _("Modern music player and library organizer") },\
    {"name": "conky","desc" : _("Highly configurable system monitor") },\
    {"name": "cyclope","desc" : _("Minimalist images viewer") },\
    {"name": "darktable","desc" : _("Virtual lighttable and darkroom for photographers") },\
    {"name": "dtrx","desc" : _("Intelligently extract multiple archive types") },\
    {"name": "evince","desc" : _("Simple multi-page document viewer") },\
    {"name": "file-roller","desc" : _("Archive manager for GNOME") },\
    {"name": "filezilla","desc" : _("Full-featured graphical FTP/FTPS/SFTP client") },\
    {"name": "geany","desc" : _("Small and lightweight integrated development environment") },\
    {"name": "gimp","desc" : _("The GNU Image Manipulation Program") },\
    {"name": "gparted","desc" : _("GNOME partition editor") },\
    {"name": "gthumb","desc" : _("Image viewer and browser") },\
    {"name": "handbrake","desc" : _("Versatile DVD ripper and video transcoder") },\
    {"name": "icedove","desc" : _("Mail/news client with RSS and integrated spam filter support") },\
    {"name": "iceweasel","desc" : _("Web browser based on Firefox") },\
    {"name": "inkscape","desc" : _("Vector-based drawing program") },\
    {"name": "loupy","desc" : _("Simple passive magnifier") },\
    {"name": "oggconvert","desc" : _("Convert media files to free formats") },\
    {"name": "openshot","desc" : _("Create and edit videos and movies") },\
    {"name": "pcmanfm","desc" : _("Extremely fast and lightweight file manager") },\
    {"name": "phatch","desc" : _("Simple to use Photo Batch Processor") },\
    {"name": "quodlibet","desc" : _("Audio library manager and player for GTK3") },\
    {"name": "radiotray","desc" : _("Online radio streaming player") },\
    {"name": "ranger","desc" : _("File manager with an ncurses frontend written in Python") },\
    {"name": "ristretto","desc" : _("Lightweight picture-viewer for the Xfce desktop environment") },\
    {"name": "shotwell","desc" : _("Digital photo organizer") },\
    {"name": "thunar","desc" : _("File Manager for Xfce") },\
    {"name": "transmission","desc" : _("Lightweight BitTorrent client") },\
    {"name": "vim","desc" : _("Vi IMproved - enhanced vi editor") },\
    {"name": "vlc","desc" : _("Multimedia player and streamer") },\
    {"name": "winff","desc" : _("Graphical video and audio batch converter") },\
    {"name": "xarchiver","desc" : _("GTK+ frontend for most used compression formats") },\
    {"name": "xcfa","desc" : _("X Convert File Audio") },\
 ]
