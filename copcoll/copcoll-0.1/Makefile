# makefile thuban <thuban@yeuxdelibad.net>

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -m 755 -o root -g root copcoll $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root copcoll.desktop $(DESTDIR)$(APPDIR)

uninstall:
	rm $(DESTDIR)$(BINDIR)/copcoll
	rm $(DESTDIR)$(APPDIR)/copcoll.desktop
