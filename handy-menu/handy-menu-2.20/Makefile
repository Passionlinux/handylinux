# handy-menu makefile arnault perret <arpinux@member.fsf.org> Mon May 5 20:21:52 CET 2014

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps
MANDIR = /usr/share/man/man1
MENUDIR = /usr/share/handy-menu
LANGDIR = /usr/share/handy-menu/lang
THMDIR = /usr/share/handy-menu/themes
BANDIR = /usr/share/handy-menu/themes/banniere
ICSDIR = /usr/share/handy-menu/themes/icons
FZDIR = /usr/share/handy-menu/themes/icons/Faenza_icons
HLDIR = /usr/share/handy-menu/themes/icons/HandyLinux
HLNDIR = /usr/share/handy-menu/themes/icons/HandyLinux-nitrux
HLCDIR = /usr/share/handy-menu/themes/icons/HandyLinux_nocolor
JBKDIR = /usr/share/handy-menu/themes/icons/Jamba_Blues_icons

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MENUDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(LANGDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(THMDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(BANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICSDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICSDIR)/Faenza_icons
	install -d -m 755 -o root -g root $(DESTDIR)$(ICSDIR)/HandyLinux
	install -d -m 755 -o root -g root $(DESTDIR)$(ICSDIR)/HandyLinux-nitrux
	install -d -m 755 -o root -g root $(DESTDIR)$(ICSDIR)/HandyLinux_nocolor
	install -d -m 755 -o root -g root $(DESTDIR)$(ICSDIR)/Jamba_Blues_icons
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -m 755 -o root -g root handymenu $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root handymenu.1 $(DESTDIR)$(MANDIR)
	install -m 755 -o root -g root handymenu.py $(DESTDIR)$(MENUDIR)
	install -m 644 -o root -g root handymenu.glade $(DESTDIR)$(MENUDIR)
	install -m 644 -o root -g root handymenu_icon.png $(DESTDIR)$(MENUDIR)
	install -m 644 -o root -g root themes/banniere/*.png $(DESTDIR)$(THMDIR)/banniere
	install -m 644 -o root -g root themes/icons/Faenza_icons/*.png $(DESTDIR)$(FZDIR)
	install -m 644 -o root -g root themes/icons/HandyLinux/*.png $(DESTDIR)$(HLDIR)
	install -m 644 -o root -g root themes/icons/HandyLinux-nitrux/*.png $(DESTDIR)$(HLNDIR)
	install -m 644 -o root -g root themes/icons/HandyLinux_nocolor/*.png $(DESTDIR)$(HLCDIR)
	install -m 644 -o root -g root themes/icons/Jamba_Blues_icons/*.png $(DESTDIR)$(JBKDIR)
	install -m 644 -o root -g root handymenu_icon.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handymenu_v1_icon.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handymenu.desktop $(DESTDIR)$(APPDIR)
	cp -a lang/* ${DESTDIR}${LANGDIR}/
	chown -R root:root ${DESTDIR}${LANGDIR}

uninstall:
	rm -rf $(DESTDIR)$(MENUDIR)
	rm $(DESTDIR)$(BINDIR)/handymenu
	rm $(DESTDIR)$(APPDIR)/handymenu.desktop
	rm $(DESTDIR)$(MANDIR)/handymenu.1

