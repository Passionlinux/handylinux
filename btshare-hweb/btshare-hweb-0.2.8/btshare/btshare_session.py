#!/usr/bin/env python3
# -*- coding:Utf-8 -*- 
# Fichier: btshare_session.py
# Cree le 29 avril 2015 21:23:42

import os
import time
import base64
import binascii
import pickle
import random
import libtorrent as lt

def mktorrent(f,o):
    """create a torrent from file f (or directory) to o.torrent"""
    print("Let's create : {}".format(o))
    fs = lt.file_storage()
    lt.add_files(fs, f)
    t = lt.create_torrent(fs)
    t.set_creator('btshare.py - libtorrent {0}'.format(lt.version))
    t.set_comment("Smile!")
    t.add_node("dht.transmissionbt.com", 6881)
    t.add_node("router.bittorrent.com", 6881)
    t.add_node("127.0.0.1", 6881)
    lt.set_piece_hashes(t, os.path.dirname(f))
    torrent = t.generate()    
    with open(o, "wb") as torrentfile:
        torrentfile.write(lt.bencode(torrent))

def mkmagnet(t):
    """get magnet from t (t is a torrent file) """
    info = lt.torrent_info(t)
    b32m = (lt.make_magnet_uri(info))
    mhash, dn = b32m.split('btih:')[1].split('&')
    mhex = binascii.hexlify(base64.b32decode(mhash)).decode('ascii')
    mgt = "magnet:?xt=urn:btih:{0}&{1}".format(mhex,dn)

    # I don't like this way, but the other give a wrong magnet link
    #mgt = os.popen("transmission-show -m {0}".format(t)).read()
    return(mgt)

def magnet(t):
    """give magnet from torrent t"""
    with open(t, 'rb') as tf:
        metadata = lt.bdecode(tf.read())
        hashcontents = lt.bencode(metadata[b'info'])
        digest = hashlib.sha1(hashcontents).digest()
        b32hash = base64.b32encode(digest)
        return(b32hash)



class Ptge:
    """objet qui contient des informations sur un partage"""
    def __init__(self, torrent_file= False,\
            torrent_name= False,\
            magnet= False,\
            filedir= False):
        self.num = random.random()
        self.tf = torrent_file
        self.tn = torrent_name
        self.mgt = magnet
        self.filedir = filedir

class LTSession:
    """session de partage"""
    def __init__(self, sharedir, configdir):
        self.sharedir = sharedir
        # default locations
        self.configdir = os.path.expanduser(configdir)
        self.torrentdir = os.path.join(self.configdir,"torrents")
        self.pkl = os.path.join(self.configdir,"btshare.pkl")
        self.new = os.path.join(self.configdir,"new")
        self.newmagnet = os.path.join(self.new,"newmagnet")

        self.ses = lt.session()

        pe = self.ses.get_pe_settings()
        pe.out_enc_policy = lt.enc_policy.forced
        pe.in_enc_policy = lt.enc_policy.forced
        pe.allowed_enc_level = lt.enc_level.rc4
        pe.prefer_rc4 = True
        self.ses.set_pe_settings(pe)

        self.ses.listen_on(6881, 6891)
        #self.ses.listen_on(49152, 65535)
        self.ses.start_dht()
        self.ses.add_dht_router("router.bittorrent.com", 6881)
        self.ses.add_dht_router("dht.transmissionbt.com", 6881)
        self.ses.start_upnp()

        self.torlist = [] # (Ptge1, Ptge2, Ptge3)
        self.hdic = {}    # {'Ptge1' : handle, 'Ptge2' : handle }
        self.torlistinfos = []

    def anynew(self):
        """check if there is new torrents or magnet in self.new directory"""
        # fichiers torrents
        l = os.listdir(self.new)
        for f in l:
            if f.endswith(".torrent"):
                print("New torrent to add : {0}".format(f))
                nt = os.path.join(self.new,f)
                print(nt)
                self.addtorrent(nt)
                os.remove(nt)

        # magnets links
        if os.path.isfile(self.newmagnet):
            with open(self.newmagnet, "r") as m:
                ml = m.readlines()
            for line in ml:
                if line.find("magnet:") == 0:
                    print("New magnet to add : {0}".format(line))
                    self.addmagnet(line.strip())
            with open(self.newmagnet, "w") as m: pass

    def inspect(self):
        """check what file to share"""
        l = os.listdir(self.sharedir)
        tuplist = os.listdir(self.torrentdir)
        namelist = []
        for t in self.torlist:
            namelist.append(t.tn)

        # Nouveaux partages
        # par ajout de fichier
        for i in l:
            if i not in namelist: 
                size = os.path.getsize(os.path.join(self.sharedir,i))
                time.sleep(.2)
                newsize = os.path.getsize(os.path.join(self.sharedir,i))
                while size != newsize:
                    print("{} doit être en cours de copie, on patiente".format(i))
                    size = os.path.getsize(os.path.join(self.sharedir,i))
                    time.sleep(1)
                    newsize = os.path.getsize(os.path.join(self.sharedir,i))
                mktorrent(os.path.join(self.sharedir,i),\
                        os.path.join(self.torrentdir,"{}.torrent".format(i)))
                self.addtorrent(os.path.join(self.torrentdir,"{}.torrent".format(i)))

        # par ajout externe de torrent
        self.anynew()

        # Retrait de partage
        for t in self.torlist:
            state = self.hdic[t.num].status().state
            if (t.tn not in l) and (state == lt.torrent_status.seeding):
                print("to delete : {}".format(t.tn))
                self.deltorrent(t)


    def addPtge(self, ptge, handle):
        """add share to session"""
        if ptge not in self.torlist:
            self.torlist.append(ptge)

        self.hdic[ptge.num] = handle 
        self.savesession()

    def addtorrent(self, t):
        """add t (t is a torrent file)"""
        with open(t, 'rb') as tf:
            e = lt.bdecode(tf.read())
            tinfo = lt.torrent_info(e)

            h = self.ses.add_torrent({'ti': tinfo,\
                    'save_path': self.sharedir,\
                    'storage_mode': lt.storage_mode_t.storage_mode_allocate,\
                    'paused': False}) 
            try:
                mgt = mkmagnet(t)
            except:
                mgt = False
            p = Ptge(t, h.name(), mgt, self.sharedir)
            self.addPtge(p,h)

    def addmagnet(self, m):
        """add m (m is a magnet uri)"""

        params = { 'save_path': self.sharedir}
        h = lt.add_magnet_uri(self.ses, m, params)

        p = Ptge(False, h.name(), m, self.sharedir)
        self.addPtge(p,h)
 
    def deltorrent(self, ptge):
        """remove torrent from seed list."""
        self.ses.remove_torrent(self.hdic[ptge.num], 1)
        self.hdic.pop(ptge.num)
        if os.path.isfile(ptge.tf):
            os.remove(ptge.tf)
        self.torlist.remove(ptge)
        self.savesession()

    def savesession(self):
        with open(self.pkl, "wb") as pkl:
            pickle.dump(self.torlist, pkl, pickle.HIGHEST_PROTOCOL)

    def loadsession(self):
        print('loading previous shares...')
        if os.path.isfile(self.pkl):
            with open(self.pkl, "rb") as pkl:
                try: 
                    toload = pickle.load(pkl)
                except EOFError: 
                    toload= []
                for i in toload:
                    if i.filedir == self.sharedir:
                        if i.tf:
                            self.addtorrent(i.tf)
                        elif i.mgt:
                            self.addmagnet(i.mgt)
    
    def run(self):
        self.loadsession()

    def gettorinfo(self):
        self.torlistinfos = []
        for seed in self.torlist:
            tmp={}
            tmp['num'] = seed.num
            h = self.hdic[seed.num]
            s = h.status()
            tmp['has_metadata'] = h.has_metadata()
            tmp['name'] = seed.tn
            tmp['up'] = s.upload_rate
            tmp['totup'] = s.total_upload
            tmp['num_peers'] = s.num_peers
            tmp['down'] = s.download_rate
            tmp['progress'] = s.progress * 100
            tmp['finished'] = s.is_finished
            #tmp['fsize'] = os.path.getsize(seed[1])
            tmp['magnet'] = seed.mgt
            self.torlistinfos.append(tmp)


