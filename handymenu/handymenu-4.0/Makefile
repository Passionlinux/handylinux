# handymenu makefile arnault perret <arpinux@member.fsf.org> Sat 13 Jun 17:13:32 CEST 2015

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps
MANDIR = /usr/share/man/man1
MENUDIR = /usr/share/handymenu
LANGDIR = /usr/share/locale
ICSDIR = /usr/share/handymenu/icons

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
	install -d -m 755 -o root -g root $(DESTDIR)$(ICSDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -m 755 -o root -g root handymenu $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root handymenu.1 $(DESTDIR)$(MANDIR)
	install -m 755 -o root -g root *.py $(DESTDIR)$(MENUDIR)
	install -m 644 -o root -g root icons/*.png $(DESTDIR)$(ICSDIR)
	install -m 644 -o root -g root handymenu_icon.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handymenu_v1_icon.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handymenu.desktop $(DESTDIR)$(APPDIR)
	cp -a locale/* ${DESTDIR}${LANGDIR}/
	find ${DESTDIR}${LANGDIR} -name "handymenu.po*" -exec rm {} \;
	chown -R root:root ${DESTDIR}${LANGDIR}

uninstall:
	rm -rf $(DESTDIR)$(MENUDIR)
	rm $(DESTDIR)$(BINDIR)/handymenu
	rm $(DESTDIR)$(APPDIR)/handymenu.desktop
	rm $(DESTDIR)$(MANDIR)/handymenu.1
	find ${DESTDIR}${LANGDIR} -name "handymenu*" -exec rm {} \;

