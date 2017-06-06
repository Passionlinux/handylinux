DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps
ETCDIR = /etc
HLDIR = /usr/share/handylinux

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	#mise en place des dossiers
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ETCDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(HLDIR)
	#version handylinux
	install -m 644 -o root -g root handylinux_version $(DESTDIR)$(ETCDIR)
	#mise en place du guide
	cp -a guide/* $(DESTDIR)$(HLDIR)
	chown root:root $(DESTDIR)$(HLDIR)
	#mise en place des icons
	install -m 644 -o root -g root handylinux.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handyhelp.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handyinfo.png $(DESTDIR)$(ICONDIR)
	#mise en place des scripts
	install -m 755 -o root -g root myhandylinux $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root info4forum $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root ausecours $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root pastemyterm $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root networkcheck $(DESTDIR)$(BINDIR)
	#mise en place des lanceurs
	install -m 644 -o root -g root myhandylinux.desktop $(DESTDIR)$(APPDIR)
	install -m 644 -o root -g root info4forum.desktop $(DESTDIR)$(APPDIR)
	install -m 644 -o root -g root ausecours.desktop $(DESTDIR)$(APPDIR)
	#mise en place de iceweasel2firefox au cas ou
	install -m 755 -o root -g root iceweasel2firefox $(DESTDIR)$(HLDIR)
	install -m 755 -o root -g root iceweasel2firefox-launcher $(DESTDIR)$(HLDIR)
	install -m 644 -o root -g root iceweasel2firefox.desktop $(DESTDIR)$(HLDIR)
	#mise en place du sources.list via lescahiersdudebutant.fr
	install -m 644 -o root -g root handylinux.list $(DESTDIR)$(HLDIR)


uninstall:
	#suppression des icons
	rm $(DESTDIR)$(ICONDIR)/handylinux.png
	rm $(DESTDIR)$(ICONDIR)/handyhelp.png
	rm $(DESTDIR)$(ICONDIR)/handyinfo.png
	#suppression des scripts
	rm $(DESTDIR)$(BINDIR)/myhandylinux
	rm $(DESTDIR)$(BINDIR)/info4forum
	rm $(DESTDIR)$(BINDIR)/ausecours
	rm $(DESTDIR)$(BINDIR)/pastemyterm
	rm $(DESTDIR)$(BINDIR)/networkcheck
	#suppression des lanceurs
	rm $(DESTDIR)$(APPDIR)/myhandylinux.desktop
	rm $(DESTDIR)$(APPDIR)/info4forum.desktop
	rm $(DESTDIR)$(APPDIR)/ausecours.desktop
	#suppression du dossier HandyLinux
	rm -Rf $(DESTDIR)$(HLDIR)
