# handylinux-links makefile arnault perret <arpinux@member.fsf.org> Mon 15 Jun 00:58:04 CEST 2015

DESTDIR =
APPDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps

help:
	@echo "Usage: as root"
	@echo "make install  : installs links"
	@echo "make uninstall: uninstalls links"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root social_launchers/*.desktop $(DESTDIR)$(APPDIR)
	install -m 644 -o root -g root social_launchers_icons/*.png $(DESTDIR)$(ICONDIR)

uninstall:
	rm $(DESTDIR)$(APPDIR)/handysocial*
	rm $(DESTDIR)$(APPDIR)/handydoc*
	rm $(DESTDIR)$(APPDIR)/handyfun*
	rm $(DESTDIR)$(APPDIR)/handyfree*

