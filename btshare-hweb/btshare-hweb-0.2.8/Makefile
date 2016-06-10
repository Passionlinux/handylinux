# btshare-web makefile arnault perret <arpinux@member.fsf.org> Fri May  1 19:15:21 CEST 2015

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/icons
MANDIR = /usr/share/man/man1
BTDIR = /usr/share/btshare

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(BTDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -m 755 -o root -g root btshare-web $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root btshare-web.1 $(DESTDIR)$(MANDIR)
	install -m 644 -o root -g root btshare-web.desktop $(DESTDIR)$(APPDIR)
	install -m 644 -o root -g root btshare.png $(DESTDIR)$(ICONDIR)
	cp -a btshare/* $(DESTDIR)$(BTDIR)
	chown -R root:root ${DESTDIR}${BTDIR}
	install -m 644 -o root -g root AUTHORS $(DESTDIR)$(BTDIR)
	install -m 644 -o root -g root README.md $(DESTDIR)$(BTDIR)

uninstall:
	rm -rf $(DESTDIR)$(BTDIR)
	rm $(DESTDIR)$(BINDIR)/btshare-web
	rm $(DESTDIR)$(APPDIR)/btshare-web.desktop
	rm $(DESTDIR)$(MANDIR)/btshare-web.1
	rm $(DESTDIR)$(ICONDIR)/btshare.png

