# liveUSBcreator makefile arnault perret <arpinux@member.fsf.org>

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
	install -m 755 -o root -g root liveUSBcreator $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root liveUSBcreator.1 $(DESTDIR)$(MANDIR)
	install -m 644 -o root -g root liveUSBcreator.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root liveUSBcreator.desktop $(DESTDIR)$(APPDIR)

uninstall:
	rm $(DESTDIR)$(BINDIR)/liveUSBcreator
	rm $(DESTDIR)$(APPDIR)/liveUSBcreator.desktop
	rm $(DESTDIR)$(MANDIR)/liveUSBcreator.1
	rm ${DESTDIR}${ICONDIR}/liveUSBcreator.png

