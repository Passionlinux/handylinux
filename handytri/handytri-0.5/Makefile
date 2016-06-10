# handytri makefile arnault perret <arpinux@member.fsf.org>

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/icons
MANDIR = /usr/share/man/man1

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -m 755 -o root -g root handytri $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root handytri.1 $(DESTDIR)$(MANDIR)
	install -m 644 -o root -g root handytri.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handytri.desktop $(DESTDIR)$(APPDIR)

uninstall:
	rm $(DESTDIR)$(BINDIR)/handytri
	rm $(DESTDIR)$(APPDIR)/handytri.desktop
	rm $(DESTDIR)$(MANDIR)/handytri.1
	rm ${DESTDIR}${ICONDIR}/handytri.png

