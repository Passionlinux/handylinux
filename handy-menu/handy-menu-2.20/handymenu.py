#!/usr/bin/python
# -*-coding:utf-8-*

#####################################
# handy linux main menu             #
# by manon <http://shovel-crew.org> #
#     <3 manon 13 09 2014 <3        #
#####################################

import pygtk
pygtk.require("2.0")
import gtk
import os
import threading, gobject
import ConfigParser
import locale
import shutil
from os import chdir
from PIL import Image

EMPLACEMENT_ICONS = "/usr/share/handy-menu/themes/icons/"
EMPLACEMENT_BANNIERES = "/usr/share/handy-menu/themes/banniere/"
FICHIER_CONF_PERSO = os.getenv('HOME') + "/.handymenu.conf"
FICHIER_GLADE = "/usr/share/handy-menu/handymenu.glade"

LANG = locale.setlocale(locale.LC_ALL, "")[0:2]

chdir(os.getenv('HOME'))

if os.path.isdir("/usr/share/handy-menu/lang/" + LANG) == True:
	FICHIER_CONF = "/usr/share/handy-menu/lang/" + LANG + "/handymenu.conf"

else:
	FICHIER_CONF = "/usr/share/handy-menu/lang/en/handymenu.conf"
	print "Translation Missing"

if os.path.isfile(FICHIER_CONF_PERSO) != True:
	shutil.copyfile(FICHIER_CONF, FICHIER_CONF_PERSO)

config = ConfigParser.RawConfigParser()
config.read(FICHIER_CONF_PERSO)

options, dossier = {}, {}

gobject.threads_init()

########################################################################
# main window
########################################################################
class HandyMenu():

	def __init__(self):
		
		self.interface = gtk.Builder()
		self.interface.add_from_file(FICHIER_GLADE)
		self.interface.connect_signals(self)
		self.dossierXDG(self)
		self.load_config(self)

	def load_config(self, widget):
		# charge la configuration definie dans le fichier de configuration
		for bouton in config.sections():
			if bouton == 'non_glade_theme' or bouton == 'non_glade_config':
				pass
			if config.has_option(bouton, 'bouton_label') == True:
				self.interface.get_object(bouton).set_label(config.get(bouton, 'bouton_label'))
			if config.has_option(bouton, 'bouton_tooltip_text') == True:
				self.interface.get_object(bouton).set_tooltip_text(config.get(bouton, 'bouton_tooltip_text'))
			if (config.has_option(bouton, 'active') == True) and config.get(bouton, 'active') == 'False':
				self.interface.get_object(bouton).set_active(False)
			if config.get('non_glade_theme', 'check1_active') == 'True':
				self.interface.get_object('handy-menu').set_resizable(True)
			#if config.get('non_glade_theme', 'check2_active') == 'True':
			#	self.interface.get_object('handy-menu').set_position('mouse')
			if config.has_option(bouton, 'image') == True:
				image = config.get(bouton, 'id')
				self.interface.get_object(image).set_from_file(config.get(bouton, 'image'))

	def dossierXDG(self, widget):
		# recupere l'emplacement nom des dossiers
		confXDG = open(os.getenv('HOME')+"/.config/user-dirs.dirs", 'r')
		info = [info for info in confXDG if info.startswith('XDG')]
		for emplacement in info:
			dossier[emplacement.split('=')[0]] = emplacement.replace('\"', '').split('=')[1]
		confXDG.close()

	def on_mainWindow_destroy(self, widget, event):
		gtk.main_quit()

########################################################################
# files tab
########################################################################	
	def on_mes_images_clicked(self, widget):
		os.system("exo-open --launch FileManager " + dossier['XDG_PICTURES_DIR'])
		self.quitter(self)

	def on_mes_documents_clicked(self, widget):
		os.system("exo-open --launch FileManager " + dossier['XDG_DOCUMENTS_DIR'])
		self.quitter(self)

	def on_mes_telechargements_clicked(self, widget):
		os.system("exo-open --launch FileManager " + dossier['XDG_DOWNLOAD_DIR'])
		self.quitter(self)

	def on_dossier_personnel_clicked(self, widget):
		os.system("exo-open --launch FileManager $HOME &")
		self.quitter(self)

	def on_ma_musique_clicked(self, widget):
		os.system("exo-open --launch FileManager " + dossier['XDG_MUSIC_DIR'])
		self.quitter(self)

	def on_vider_corbeille_clicked(self, widget):
		os.system("exo-open --launch FileManager trash:/// &")
		self.quitter(self)

	def on_mes_videos_clicked(self, widget):
		os.system("exo-open --launch FileManager " + dossier['XDG_VIDEOS_DIR'])
		self.quitter(self)

	def on_aide_fichiers_clicked(self, widget):
		os.system("x-www-browser http://wiki.handylinux.org/doku.php/fr/fichiers &")
		self.quitter(self)

########################################################################
# web tab
########################################################################
	def on_webbrowser_event(self, widget, event):
		self.on_action_event(self, event, config.get('web', 'cmd'), 'web')
						
	def on_icedove_envent(self, widget, event):
		self.on_action_event(self, event, config.get('icedove', 'cmd'), 'icedove')

	def on_skype_event(self, widget, event):
		self.on_action_event(self, event, config.get('skype', 'cmd'), 'skype')

	def on_transmission_envent(self, widget, event):
		self.on_action_event(self, event, config.get('transmission', 'cmd'), 'transmission')

	def on_facebook_event(self, widget, event):
		self.on_action_event(self, event, config.get('facebook', 'cmd'), 'facebook')
		
	def on_aide_internet_envent(self, widget, event):
		self.on_action_event(self, event, config.get('aide_internet', 'cmd'), 'aide_internet')

########################################################################
# media tab
########################################################################
	def on_vlc_envent(self, widget, event):
		self.on_action_event(self, event, config.get('vlc', 'cmd'), 'vlc')

	def on_ristretto_envent(self, widget, event):
		self.on_action_event(self, event, config.get('ristretto', 'cmd'), 'ristretto')

	def on_quodlibet_envent(self, widget, event):
		self.on_action_event(self, event, config.get('quodlibet', 'cmd'), 'quodlibet')

	def on_xfburn_envent(self, widget, event):
		self.on_action_event(self, event, config.get('xfburn', 'cmd'), 'xfburn')

	def on_mixer_envent(self, widget, event):
		self.on_action_event(self, event, config.get('mixer', 'cmd'), 'mixer')
		
	def on_aide_media_envent(self, widget, event):
		self.on_action_event(self, event, config.get('aide_media', 'cmd'), 'aide_media')

########################################################################
# office tab
########################################################################
	def on_mousepad_envent(self, widget, event):
		self.on_action_event(self, event, config.get('mousepad', 'cmd'), 'mousepad')

	def on_xpad_envent(self, widget, event):
		self.on_action_event(self, event, config.get('xpad', 'cmd'), 'xpad')

	def on_libreoffice_envent(self, widget, event):
		self.on_action_event(self, event, config.get('libreoffice', 'cmd'), 'libreoffice')

	def on_xcalc_envent(self, widget, event):
		self.on_action_event(self, event, config.get('xcalc', 'cmd'), 'xcalc')

	def on_xsane_envent(self, widget, event):
		self.on_action_event(self, event, config.get('xsane', 'cmd'), 'xsane')

	def on_aide_office_envent(self, widget, event):
		self.on_action_event(self, event, config.get('aide_office', 'cmd'), 'aide_office')

########################################################################
# game tab
########################################################################
	def on_sudoku_envent(self, widget, event):
		self.on_action_event(self, event, config.get('sudoku', 'cmd'), 'sudoku')

	def on_cards_envent(self, widget, event):
		self.on_action_event(self, event, config.get('cards', 'cmd'), 'cards')

	def on_boards_envent(self, widget, event):
		self.on_action_event(self, event, config.get('boards', 'cmd'), 'boards')

	def on_gbrainy_envent(self, widget, event):
		self.on_action_event(self, event, config.get('gbrainy', 'cmd'), 'gbrainy')

########################################################################
# dev tab
########################################################################
	def on_terminal_envent(self, widget, event):
		self.on_action_event(self, event, config.get('terminal', 'cmd'), 'terminal')

	def on_synaptic_envent(self, widget, event):
		self.on_action_event(self, event, config.get('synaptic', 'cmd'), 'synaptic')

	def on_appslist_envent(self, widget, event):
		self.on_action_event(self, event, config.get('appslist', 'cmd'), 'appslist')

	def on_network_envent(self, widget, event):
		self.on_action_event(self, event, config.get('network', 'cmd'), 'network')

	def on_dev_print_envent(self, widge, event):
		self.on_action_event(self, event, config.get('dev_prin', 'cmd'), 'dev_prin')

	def on_dev_config_envent(self, widget, event):
		self.on_action_event(self, event, config.get('devconfig', 'cmd'), 'devconfig')

########################################################################
# action
########################################################################
	def on_preferences_clicked(self, widget):
		ConfHandyMenu(self, self.interface).start()

	def on_aide_clicked(self, widget):
		os.system("x-www-browser http://wiki.handylinux.org &")
		self.quitter(self)

	def on_check_clicked(self, widget):
		if widget.get_active():
			config.set('checkbutton1', 'active', 'True')
		else:
			config.set('checkbutton1', 'active', 'False')

		with open(FICHIER_CONF_PERSO, 'wb') as configfile:
			config.write(configfile)
			
	def on_action_event(self, widget, event, commande, id_config):
		if str(event.type).split(' ')[1] == 'GDK_BUTTON_PRESS':	
			if event.button == 1 :
				os.system(commande)
				self.quitter(self)
			elif event.button == 3:
				AppliHandyMenu(self, self.interface, id_config).start()
				
		elif str(event.type).split(' ')[1] == 'GDK_KEY_PRESS':
			key = str(event).split('=')[1][0:-1]
			if key  in ['space', 'Return']:#  
				os.system(commande)
				self.quitter(self)

	def quitter(self, widget):
		if config.get('checkbutton1', 'active') == "True":
			gtk.main_quit()

########################################################################
# config
########################################################################
class ConfHandyMenu(threading.Thread):

	def __init__ (self, widget, interface):
		threading.Thread.__init__ (self, target=self)
		self.interface = interface 

	def Quitter(self, widget):
		self.maFenetre.destroy()

	def liste_bannieres_dispo(self, liste_banniere):
		# forme la liste deroulante par rapport aux bannieres dispo
		bannieres_dispo= [nom for nom  in os.listdir(EMPLACEMENT_BANNIERES)]
		for banniere in bannieres_dispo:
			self.liste_banniere.append_text(banniere)

	def banniere_choix(self, liste_banniere):
		# fonction appelée au choix de la banniere dans la liste deroulante
		choix = self.liste_banniere.get_active_text() #recuperation du choix
		# Changement dans l'interface
		self.interface.get_object('handymenu_banner').set_from_file(EMPLACEMENT_BANNIERES + choix)
		# Ecriture dans le fichier config
		config.set('aide', 'image', EMPLACEMENT_BANNIERES + choix)
		self.write_config(self)

	def liste_icones_dispo(self, liste_icones):
		icones_dispo = [nom for nom  in os.listdir(EMPLACEMENT_ICONS)]
		for icone in icones_dispo:
			liste_icones.append_text(icone)

	def icones_choix(self, liste_icones):
		config_base = ConfigParser.RawConfigParser()
		config_base.read(FICHIER_CONF)
		choix = liste_icones.get_active_text()
		icones = [icone for icone in config.sections() if config.has_option(icone, 'image') == True]
		for icone in icones:
			if os.path.basename(config.get(icone, 'image')) != os.path.basename(config_base.get(icone, 'image')):
				pass
			else:
				config.set(icone, 'image', EMPLACEMENT_ICONS + choix + '/' + os.path.basename(config.get(icone, 'image')))
				self.write_config(self)
				self.interface.get_object(config.get(icone, 'id')).set_from_file(config.get(icone, 'image'))

	def on_redimensionnement(self, widget):
		# active ou desactive le redimensionnement
		if widget.get_active():
			config.set('non_glade_theme', 'check1_active', 'True')
			self.interface.get_object('handy-menu').set_resizable(True)
		else:
			config.set('non_glade_theme', 'check1_active', 'False')
			self.interface.get_object('handy-menu').set_resizable(False)

		self.write_config(self)

	#def position_ouverture(self, widget):
		# active ou desactive l'ouverture du menu au niveau du lanceur
	#	if widget.get_active():
	#		config.set('non_glade_theme', 'check2_active', 'True')
	#	else:
	#		config.set('non_glade_theme', 'check2_active', 'False')
	#	self.write_config(self)	

	def write_config(self, widget):
		with open(FICHIER_CONF_PERSO, 'wb') as configfile:
			config.write(configfile)

	def run(self):
		self.maFenetre = gtk.Window()
		self.maFenetre.set_title(config.get('non_glade_theme', 'title'))
		self.maFenetre.connect("destroy", self.Quitter)
		self.maFenetre.set_icon_from_file('/usr/share/pixmaps/handymenu_icon.png')
		self.maFenetre.set_modal(True)
		separateur = gtk.HSeparator()
		separateur.set_size_request(150, 10)

		separateur2 = gtk.HSeparator()
		separateur2.set_size_request(150, 10)

		separateur3 = gtk.HSeparator()
		separateur3.set_size_request(150, 10)

		fram1 = gtk.AspectFrame(label=config.get('non_glade_theme', 'title'), xalign=0.5, yalign=0.4, ratio=1.0, obey_child=True)
		fram1.set_shadow_type(gtk.SHADOW_OUT)

		boutonvBox = gtk.VBox()
		checkOption1 = gtk.CheckButton(config.get('non_glade_theme', 'check1'))
		if config.get('non_glade_theme', 'check1_active') == 'True':
			checkOption1.set_active(True)
	#	checkOption2 = gtk.CheckButton(config.get('non_glade_theme', 'check2'))
	#	if config.get('non_glade_theme', 'check2_active') == 'True':
	#		checkOption2.set_active(True)

		checkOption1.connect("clicked", self.on_redimensionnement)
	#	checkOption2.connect("clicked", self.position_ouverture)

		boutonvBox.add(checkOption1)
	#	boutonvBox.add(checkOption2)
		fram1.add(boutonvBox)

		fram2 = gtk.Frame(config.get('non_glade_theme', 'fram2'))
		fram2.set_shadow_type(gtk.SHADOW_OUT)
		listevbox = gtk.VBox()

		self.liste_banniere = gtk.combo_box_new_text()
		self.liste_banniere.append_text(config.get('non_glade_theme', 'list1'))
		self.liste_banniere.set_wrap_width(0)
		self.liste_banniere.set_active(0)
		self.liste_bannieres_dispo(self.liste_banniere)
		self.liste_banniere.connect('changed', self.banniere_choix)

		liste_icones = gtk.combo_box_new_text()
		liste_icones.append_text(config.get('non_glade_theme', 'list2'))
		liste_icones.set_active(0)
		self.liste_icones_dispo(liste_icones)
		liste_icones.connect('changed', self.icones_choix)

		listevbox.add(self.liste_banniere)
		listevbox.add(liste_icones)
		fram2.add(listevbox)

		boutonQuitter = gtk.ToggleButton(label = config.get('non_glade_theme', 'quit'))
		boutonQuitter.connect("clicked" ,self.Quitter)

		mainvbox = gtk.VBox()
		mainvbox.add(separateur)
		mainvbox.add(fram1)
		mainvbox.add(separateur2)
		mainvbox.add(fram2)
		mainvbox.add(separateur3)
		mainvbox.add(boutonQuitter)

		self.maFenetre.add(mainvbox)
		self.maFenetre.show_all()
		gtk.main()

class AppliHandyMenu(threading.Thread):

	def __init__ (self, widget, interface, id_bouton):
		threading.Thread.__init__ (self, target=self)
		self.interface = interface 
		self.bouton_id = id_bouton	
		self.image = config.get(id_bouton, 'image')
		self.id = config.get(id_bouton, 'id')

	def Quitter(self, widget):
		self.maFenetre.destroy()

	def motion_cb(self, wid, context, x, y, time):
		# selection du widget envoi du signal copie
		context.drag_status(gtk.gdk.ACTION_COPY, time)
		return True

	def drop_cb(self, wid, context, x, y, time):
		wid.drag_get_data(context, context.targets[-1], time)
		return True

	def got_data_cb(self, wid, context, x, y, data, info, time):
		# Recuperation de l'emplacement du fichier depose
		emplacement = data.get_uris()[0].split('file://')[1]
		# changement de l'Encodage de l'emplacement ( coder en hex apres le glisser deposer )
		emplacement = self.m_decode(emplacement)#Encode utf8

		# Verification si le fichier est bien un .desktop
		if os.path.splitext(emplacement)[1] == '.desktop':
			#appelle fonction de configuration
			self.conf_desktop(self, emplacement)
		else:
			# le fichier n est pas un .desktop
			self.label.set_text("\n" + os.path.basename(emplacement) + "\n\n"+ config.get('non_glade_config', 'labelError') + "\n\n")

	def conf_desktop(self, widget, emplacement):
		# Lecture du fichier .desktop 
		config_desktop = ConfigParser.RawConfigParser()
		config_desktop.read(emplacement)

		#recuperation de la commande et de l'image dans le fichier .desktop
		newCommande = config_desktop.get('Desktop Entry', 'Exec')
		iconDesktop = config_desktop.get('Desktop Entry', 'Icon')

		#Analyse la config gtk pour récuperer l'emplacement de l'image
		icon_theme = gtk.icon_theme_get_default()
		if iconDesktop.replace('.png', '') not in icon_theme.list_icons():
			icon = iconDesktop
		else:
			icon = icon_theme.lookup_icon(iconDesktop.replace('.png', ''), 0, 0).get_filename()

		# Teste exitence dossier .icons, si faux on le creer
		if os.path.isdir(os.getenv('HOME') + '/.handymenu_icons/') == False:
			os.mkdir(os.getenv('HOME') + '/.handymenu_icons/')

		#Copie de l'icone dans le dossier $Home/.icons
		newIcon = os.getenv('HOME') + '/.handymenu_icons/' + os.path.basename(icon)
		if os.path.isfile(newIcon) == True:
			os.remove(newIcon)
		shutil.copyfile(icon, newIcon)

		#Test si l'icon est au format .svg and .xpm
		newIcon_png = newIcon
		if '.svg' in newIcon:
			newIcon_png = newIcon.replace('.svg', '.png')
		if '.xpm' in newIcon:
			newIcon_png = newIcon.replace('.xpm', '.png')
		if '.svg' in newIcon or '.xpm' in newIcon:
			# si icone format svg , reformatage en png et redimensionnement avec imagemagick/convert pour une meilleure qualité
			os.system('convert' + ' ' + '-density' + ' ' + '1200' + ' ' + '-resize' + ' ' + '75x75' + ' ' + newIcon + ' ' + newIcon_png)
			os.remove(newIcon)

		# Redimensionnement de l'icone
		im = Image.open(newIcon_png)
		out = im.resize((75,75))
		out.save(newIcon_png)

		# Changement dans le fichier de configuration
		if '%' in newCommande :
			newCommande = newCommande.split('%')[0]
		config.set(self.bouton_id, 'cmd', newCommande + ' &')
		config.set(self.bouton_id, 'image', os.path.splitext(newIcon)[0] + '.png')
		self.write_config(self)

		# Changement dans l'interface ( label + icone)
		self.label.set_text("\n\n" + newCommande + "\n\n")
		self.interface.get_object(self.id).set_from_file(os.path.splitext(newIcon)[0] + '.png')
		self.image.set_from_file(config.get(self.bouton_id, 'image'))

	def write_config(self, widget):
		with open(FICHIER_CONF_PERSO, 'wb') as configfile:
			config.write(configfile)

	def m_decode(self, emplacement):
		liste = []
		searchCode = emplacement.split('%')
		searchCode.remove(searchCode[0])

		for index, element in enumerate(searchCode):
			if len(element) == 2 and element != searchCode[-1]:
				liste.append( element + searchCode[index + 1][:2])

		emplacement = emplacement.replace('%', '')
		for element in liste:
			if element in emplacement:
				emplacement = emplacement.replace(element, element.decode('hex'))

		return emplacement

	def validation(self, widget, text_bouton, tooltip_bouton):
		new_text_bouton = text_bouton.get_text()#recup new text
		new_tooltip_bouton = tooltip_bouton.get_text()
		#modif interface
		self.interface.get_object(self.bouton_id).set_label(new_text_bouton)
		self.interface.get_object(self.bouton_id).set_tooltip_text(new_tooltip_bouton)
		#modif config
		config.set(self.bouton_id, 'bouton_label', new_text_bouton)
		config.set(self.bouton_id, 'bouton_tooltip_text', new_tooltip_bouton)
		#modif fichier config
		self.write_config(self)

	def reinitialise(self, widget):
		# Lecture du fichier de configuration de base 
		configBase = ConfigParser.RawConfigParser()
		configBase.read(FICHIER_CONF)

		# Reinitialise les valeur du bouton d'origine dans le fichier configuration perso. Commande, image , label, tooltip
		config.set(self.bouton_id, 'cmd', configBase.get(self.bouton_id, 'cmd'))
		config.set(self.bouton_id, 'image', configBase.get(self.bouton_id, 'image'))
		config.set(self.bouton_id, 'bouton_label', configBase.get(self.bouton_id, 'bouton_label'))
		config.set(self.bouton_id, 'bouton_tooltip_text', configBase.get(self.bouton_id, 'bouton_label'))
		self.write_config(self)

		# Reinitialise l'interface 
		self.label.set_text("\n\n" + config.get('non_glade_config', 'label1') + "\n\n")
		self.interface.get_object(self.id).set_from_file(configBase.get(self.bouton_id, 'image'))
		self.interface.get_object(self.bouton_id).set_label(configBase.get(self.bouton_id, 'bouton_label'))
		self.interface.get_object(self.bouton_id).set_tooltip_text(configBase.get(self.bouton_id, 'bouton_tooltip_text'))
		self.image.set_from_file(configBase.get(self.bouton_id, 'image'))
		self.text_bouton.set_text(self.interface.get_object(self.bouton_id).get_label())
		self.tooltip_bouton.set_text(self.interface.get_object(self.bouton_id).get_tooltip_text())

	def applications(self, widget):
		os.system("xfce4-appfinder &")

	def run(self):

		self.maFenetre = gtk.Window()
		self.maFenetre.set_title(config.get('non_glade_config', 'title'))
		self.maFenetre.connect("destroy", self.Quitter)
		self.maFenetre.set_size_request(450, 530)
		#self.maFenetre.set_size_request(450, 490)
		self.maFenetre.set_icon_from_file('/usr/share/pixmaps/handymenu_icon.png')
		self.maFenetre.set_modal(True)

		separateur = gtk.HSeparator()
		separateur.set_size_request(150, 10)

		separateur2 = gtk.HSeparator()
		separateur2.set_size_request(150, 10)

		separateur3 = gtk.HSeparator()
		separateur3.set_size_request(150, 21)

		separateur4 = gtk.HSeparator()
		separateur4.set_size_request(150, 10)

		fram1 = gtk.Frame(label=config.get('non_glade_config', 'fram1'))
		fram1.set_shadow_type(gtk.SHADOW_OUT)

		vBox = gtk.VBox()

		self.image = gtk.Image()
		self.image.set_from_file(config.get(self.bouton_id, 'image'))

		vBox.add(self.image)

		self.label = gtk.Label("\n\n" + config.get('non_glade_config', 'label1') + "\n\n")
		self.label.drag_dest_set(0, [], 0)
		self.label.connect('drag_motion', self.motion_cb)
		self.label.connect('drag_drop', self.drop_cb)
		self.label.connect('drag_data_received', self.got_data_cb)
		vBox.add(self.label)
		self.listLabel = gtk.Button(config.get('non_glade_config', 'button4'))
		self.listLabel.connect("clicked", self.applications)
		vBox.add(self.listLabel)
		fram1.add(vBox)

		fram2 = gtk.Frame(label=config.get('non_glade_config', 'fram2'))
		fram2.set_shadow_type(gtk.SHADOW_OUT)

		vBox2 = gtk.VBox()
		info_text = gtk.Label(config.get('non_glade_config', 'info1'))
		self.text_bouton = gtk.Entry()
		self.text_bouton.set_text(self.interface.get_object(self.bouton_id).get_label())
		self.text_bouton.connect("activate", self.validation, self.text_bouton)

		info_tooltip = gtk.Label(config.get('non_glade_config', 'info2'))
		self.tooltip_bouton = gtk.Entry()
		self.tooltip_bouton.set_text(self.interface.get_object(self.bouton_id).get_tooltip_text())
		self.tooltip_bouton.connect("activate", self.validation, self.text_bouton)

		bouton_valider = gtk.Button(config.get('non_glade_config', 'button1'))
		bouton_valider.connect("clicked", self.validation, self.text_bouton, self.tooltip_bouton)

		vBox2.pack_start(info_text, False, False, 6)
		vBox2.add(self.text_bouton)
		vBox2.pack_start(info_tooltip, False, False, 6)
		vBox2.add(self.tooltip_bouton)
		vBox2.pack_end(bouton_valider, False, False, 10)

		fram2.add(vBox2)

		boutonRefresh = gtk.ToggleButton(label = config.get('non_glade_config', 'button3'))
		boutonRefresh.connect('clicked', self.reinitialise)

		boutonQuitter = gtk.ToggleButton(label = config.get('non_glade_config', 'button2'))
		boutonQuitter.connect("clicked" ,self.Quitter)

		mainvbox = gtk.VBox()
		mainvbox.add(separateur)
		mainvbox.add(fram1)
		#mainvbox.add(separateur4)
		mainvbox.add(fram2)
		mainvbox.add(separateur3)
		mainvbox.add(boutonRefresh)
		mainvbox.pack_end(boutonQuitter, False, False, 10)

		self.maFenetre.add(mainvbox)
		self.maFenetre.show_all()

########################################################################
if __name__ == "__main__":

	HandyMenu()
	gtk.main()
