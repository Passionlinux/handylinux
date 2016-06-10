#!/usr/bin/env python
# -*-coding:utf-8-*-

import pygtk
pygtk.require("2.0")
import gtk, os
import subprocess as sub

class Theme:

	def __init__(self,font="",termFont="",xfceTheme="",xfwmTheme="",cursorName="",cursorSize="",wall=""):
		self.xfceFont = font
		self.xfwmFont = font
		self.termFont = termFont
		self.xfceTheme = xfceTheme
		self.xfwmTheme = xfwmTheme
		self.cursorName = cursorName
		self.cursorSize = cursorSize
		self.wall = wall

	def apply(self,widget):
		os.system('xfconf-query -s "' + self.xfceFont + '" -c xfwm4 -p /general/title_font')
		os.system('xfconf-query -s "' + self.xfwmFont + '" -c xsettings -p /Gtk/FontName')
		os.system('xfconf-query -s "' + self.xfceTheme + '" -c xsettings -p /Net/ThemeName')
		os.system('xfconf-query -s "' + self.xfwmTheme + '" -c xfwm4 -p /general/theme')
		os.system('xfconf-query -s "' + self.cursorName + '" -c xsettings -p /Gtk/CursorThemeName')
		os.system('xfconf-query -s "' + self.cursorSize + '" -c xsettings -p /Gtk/CursorThemeSize')
		os.system('xfconf-query -s "' + self.wall + '" -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path')
		if os.system('grep --quiet "FontName" ~/.config/Terminal/terminalrc') == 0:
			if self.termFont == "":
				os.system('sed -i "s/FontName.*//g" ~/.config/Terminal/terminalrc')
			else:
				os.system('sed -i "s/FontName.*/FontName=' + self.termFont + '/g" ~/.config/Terminal/terminalrc')
		elif self.termFont != "":
			os.system('echo "FontName=' + self.termFont + '" >> ~/.config/Terminal/terminalrc')

	def getCurrent(self):
		self.xfceFont = sub.check_output(['xfconf-query','-c','xfwm4','-p','/general/title_font']).rstrip('\n')
		self.xfwmFont = sub.check_output(['xfconf-query','-c','xsettings','-p','/Gtk/FontName']).rstrip('\n')
		self.xfceTheme = sub.check_output(['xfconf-query','-c','xsettings','-p','/Net/ThemeName']).rstrip('\n')
		self.xfwmTheme = sub.check_output(['xfconf-query','-c','xfwm4','-p','/general/theme']).rstrip('\n')
		self.cursorName = sub.check_output(['xfconf-query','-c','xsettings','-p','/Gtk/CursorThemeName']).rstrip('\n')
		self.cursorSize = sub.check_output(['xfconf-query','-c','xsettings','-p','/Gtk/CursorThemeSize']).rstrip('\n')
		self.wall = sub.check_output(['xfconf-query','-c','xfce4-desktop','-p','/backdrop/screen0/monitor0/image-path']).rstrip('\n')
		if os.system('grep --quiet "FontName" ~/.config/Terminal/terminalrc') == 0:
			self.termFont = sub.check_output(['grep "FontName" ~/.config/Terminal/terminalrc'], shell=True).rstrip('\n').split('=')[1]

class Main:
	def Quitter(self, widget):
		gtk.main_quit()

	def __init__(self):
		smallLightTheme = Theme("Droid Sans Bold 10", "Monospace 10", "HandyLinuxClear", "HandyLinuxClear", "Adwaita", "22", "/usr/share/xfce4/backdrops/handy_flat_clear_by_Starsheep.png")
		normalLightTheme = Theme("Droid Sans Bold 12", "Monospace 12", "HandyLinuxClear", "HandyLinuxClear", "Adwaita", "22", "/usr/share/xfce4/backdrops/handy_flat_clear_by_Starsheep.png")
		largeLightTheme = Theme("Droid Sans Bold 18", "Monospace 18", "HandyLinuxClear", "HandyLinuxClearBigButton", "Adwaita", "48", "/usr/share/xfce4/backdrops/handy_flat_clear_by_Starsheep.png")
		smallDarkTheme = Theme("Droid Sans Bold 10", "Monospace 10", "HandyLinuxDark", "HandyLinuxDark", "DMZ-White", "22", "/usr/share/xfce4/backdrops/handy_flat_darkblack_by_Starsheep.png")
		normalDarkTheme = Theme("Droid Sans Bold 12", "Monospace 12", "HandyLinuxDark", "HandyLinuxDark", "DMZ-White", "22", "/usr/share/xfce4/backdrops/handy_flat_darkblack_by_Starsheep.png")
		largeDarkTheme = Theme("Droid Sans Bold 18", "Monospace 18", "HandyLinuxDark", "HandyLinuxDarkBigButton", "DMZ-White", "48", "/usr/share/xfce4/backdrops/handy_flat_darkblack_by_Starsheep.png")

		currentTheme = Theme()
		currentTheme.getCurrent()

		window = gtk.Window()
		window.set_title("HandyTheme")
		window.connect("destroy", self.Quitter)
		window.set_default_size(450, 250)

		table = gtk.Table(3,3,False)

		boutonSmallLight =  gtk.Button()
		imgSmallLight = gtk.Image()
		imgSmallLight.set_from_file("icons/smallLight.png")
		boutonSmallLight.set_image(imgSmallLight)
		boutonSmallLight.connect("clicked", smallLightTheme.apply)

		boutonNormalLight =  gtk.Button()
		imgNormalLight = gtk.Image()
		imgNormalLight.set_from_file("icons/normalLight.png")
		boutonNormalLight.set_image(imgNormalLight)
		boutonNormalLight.connect("clicked", normalLightTheme.apply)

		boutonLargeLight =  gtk.Button()
		imgLargeLight = gtk.Image()
		imgLargeLight.set_from_file("icons/largeLight.png")
		boutonLargeLight.set_image(imgLargeLight)
		boutonLargeLight.connect("clicked", largeLightTheme.apply)

		boutonSmallDark =  gtk.Button()
		imgSmallDark = gtk.Image()
		imgSmallDark.set_from_file("icons/smallDark.png")
		boutonSmallDark.set_image(imgSmallDark)
		boutonSmallDark.connect("clicked", smallDarkTheme.apply)

		boutonNormalDark =  gtk.Button()
		imgNormalDark = gtk.Image()
		imgNormalDark.set_from_file("icons/normalDark.png")
		boutonNormalDark.set_image(imgNormalDark)
		boutonNormalDark.connect("clicked", normalDarkTheme.apply)

		boutonLargeDark =  gtk.Button()
		imgLargeDark = gtk.Image()
		imgLargeDark.set_from_file("icons/largeDark.png")
		boutonLargeDark.set_image(imgLargeDark)
		boutonLargeDark.connect("clicked", largeDarkTheme.apply)

		boutonReset = gtk.Button(stock=gtk.STOCK_UNDO)
		boutonReset.connect("clicked", currentTheme.apply)

		table.attach(boutonSmallLight,0,1,0,1)
		table.attach(boutonNormalLight,1,2,0,1)
		table.attach(boutonLargeLight,2,3,0,1)

		table.attach(boutonSmallDark,0,1,1,2)
		table.attach(boutonNormalDark,1,2,1,2)
		table.attach(boutonLargeDark,2,3,1,2)

		table.attach(boutonReset,0,3,2,3)

		table.set_row_spacings(5)
		table.set_col_spacings(5)
		table.set_row_spacing(1,10)

		window.add(table)
		window.show_all()

if __name__ == "__main__":
	Main()
	gtk.main()
