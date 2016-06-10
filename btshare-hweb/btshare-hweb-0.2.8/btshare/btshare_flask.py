#!/usr/bin/env python
# -*- coding:Utf-8 -*- 
# Fichier: btshare_flask.py
# Cree le 30 avril 2015 09:33:10

import os
import time
import json
import socket

from flask import *
from werkzeug import secure_filename


def get_open_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        port = s.getsockname()[1]
        s.close()
        return port

def convb(nbbyte):
    """convert a number of bytes to a good unit
    return a string
    """
    l = len(str(nbbyte))
    if l < 4:
        return("{0:.2f} B".format(nbbyte))
    elif l < 7:
        return("{0:.2f} kB".format(nbbyte/1000))
    elif l < 10:
        return("{0:.2f} MB".format(nbbyte/1000000))
    else:
        return("{0:.2f} GB".format(nbbyte/1000000000))

def shutdown_server():
    """stop flask cleanly"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

class App:
    def __init__(self, torrent_session):
        self.app = Flask(__name__)

        self.shareinfos = self.dlinfos = self.sessinfos = ""
        self.retour = self.curpage = ""
        self.lastupdate = time.time()
        self.port = get_open_port()

        self.session = torrent_session

        @self.app.route('/')
        def index():
            self.curpage = "/"
            if self.session.sharedir == "":
                return redirect("/selectdir")

            self.updateup()
            return render_template('index.html',\
                    sharedir = self.session.sharedir, \
                    shareinfos = self.shareinfos, \
                    sessinfos = self.sessinfos, \
                    retour = self.retour)
            
        @self.app.route('/up')
        def up():
            return redirect("/")

        @self.app.route('/down')
        def down():
            self.curpage = "/down"
            if self.session.sharedir == "":
                return redirect("/selectdir")

            self.updatedl()
            return render_template('down.html',\
                    sharedir = self.session.sharedir, \
                    dlinfos = self.dlinfos, \
                    sessinfos = self.sessinfos, \
                    retour = self.retour)

        @self.app.route('/selectdir')
        def selectdir():
            return render_template('seldir.html', retour=self.retour)

        @self.app.route('/_getupinfos')
        def getupinfos():
            self.updateup()
            return jsonify(sessinfos=self.sessinfos,\
                    shareinfos=self.shareinfos,\
                    dlinfos=self.dlinfos)

        @self.app.route('/_getdlinfos')
        def getdlinfos():
            self.updatedl()
            return jsonify(sessinfos=self.sessinfos,\
                    dlinfos=self.dlinfos)

        @self.app.route('/chgdir' ,methods=['POST'])
        def chgdir():
            if request.method == 'POST':
                nd = request.form['filename']
                if os.path.isdir(nd):
                    self.session.sharedir = nd
                    self.retour = ""
                else:
                    self.retour = """{0} n'existe pas.
                    Exemple : /home/moi/partage""".format(nd)

            return redirect(self.curpage)

        @self.app.route('/_newtorrent' ,methods=['POST'])
        def newtorrent():
            if request.method == 'POST':
                torrentfile = request.files['torrentfile']
                filename = secure_filename(torrentfile.filename)
                if filename:
                    if filename.endswith(".torrent"):
                        #ajout du torrent
                        dest = os.path.join(self.session.torrentdir,filename)
                        torrentfile.save(dest)
                        self.session.addtorrent(dest)
                        self.retour = ""
                    else:
                        self.retour = """seulement les fichiers terminant par
                        .torrent sont acceptés"""
            return redirect(self.curpage)

        @self.app.route('/_newmagnet' ,methods=['POST'])
        def newmagnet():
            if request.method == 'POST':
                magneturi = str(request.form['magnetlink'])
                if magneturi.find("magnet:") == 0:
                    print(magneturi)
                    self.retour = ""
                    self.session.addmagnet(magneturi)
                else:
                    self.retour = "Le lien magnet semble invalide"
            return redirect(self.curpage)

        @self.app.route('/shutdown')
        def quitter():
            shutdown_server()
            return 'Server shutting down...'

        @self.app.route('/helpme')
        def aide():
            return render_template('help.html')

        @self.app.route('/_delete' ,methods=['POST'])
        def delete():
            if request.method == 'POST':
                todelete = float(request.form['todelete'])
                for i in self.session.torlist:
                    if i.num == todelete:
                        self.session.deltorrent(i)

            return redirect(self.curpage)

    def run(self):
        self.app.run(port = self.port)

    def update(self):
        newtime = time.time()
        if newtime - self.lastupdate > 1:
            self.lastupdate = newtime
            self.session.inspect()
            self.session.gettorinfo()

    def updatedl(self):
        self.updatesessinfos()
        self.dlinfos = ""
        for si in self.session.torlistinfos:
            if not si['finished']:
                self.dlinfos += """
<div class='torrentdl' style='background-size: {4:.1f}% 100%;'>\
    <div class='torname'>{0}\
        <form action='/_delete' method='post'>\
            <input type='hidden' name='todelete' value='{5}'>\
            <input type='submit' value='Supprimer'>\
        </form>\
    </div>\
    <div class='infos'>Réception : {1}/s -\
        Envoi : {2}/s -\
        Pairs : {3} - \
            {4:.1f}%\
    </div>\
</div>""".format(   si['name'],\
                    convb(si['down']),\
                    convb(si['up']),\
                    si['num_peers'],\
                    si['progress'],\
                    si['num'])

    def updatesessinfos(self):
        self.update()
        nup = ndown = 0
        for si in self.session.torlistinfos:
            if si['finished']:
                nup +=1
            else:
                ndown +=1

        self.sessinfos = "{0} Envoi(s) : {1}/s - {2} Réception(s) : {3}/s - Total : {4}".format(\
            nup,\
            convb(self.session.ses.status().upload_rate) , \
            ndown,\
            convb(self.session.ses.status().download_rate) , \
            convb(self.session.ses.status().total_upload))

    def updateup(self):
        self.updatesessinfos()
        self.shareinfos = ""
        for si in self.session.torlistinfos:
            if si['finished']:
                self.shareinfos += """
<div class='torrent'>\
    <div class='torname'>{0}\
        <form action='/_delete' method='post'>\
            <input type='hidden' name='todelete' value='{4}'>\
            <input type='submit' value='Supprimer'>\
        </form>\
    </div>\
    <div class='infos'>Envoi : {1}/s -\
        Pairs : {2}\
    </div>\
    <div>Magnet à \
        <span class='btn'>\
            <a onClick='copyToClipboard(\"{3}\");'>Copier</a>\
        </span>:\
        <span class='magnet'>{3}</span> \
    </div>\
</div>""".format( si['name'],\
                convb(si['up']),\
                si['num_peers'],\
                si['magnet'],\
                si['num'])

