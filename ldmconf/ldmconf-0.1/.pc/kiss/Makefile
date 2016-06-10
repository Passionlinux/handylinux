# ldmconf makefile thuban <thuban@yeuxdelibad.net> Mon 18 Jan 15:53:22 CET 2016

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
MANDIR = /usr/share/man/man1
DATADIR = /usr/share/ldmconf

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(DATADIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -m 755 -o root -g root ldmconf $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root ldmconf.1 $(DESTDIR)$(MANDIR)
	install -m 755 -o root -g root *.py $(DESTDIR)$(DATADIR)
	install -m 644 -o root -g root *.gif $(DESTDIR)$(DATADIR)
	install -m 644 -o root -g root ldmconf.desktop $(DESTDIR)$(APPDIR)

uninstall:
	rm -rf $(DESTDIR)$(DATADIR)
	rm $(DESTDIR)$(BINDIR)/ldmconf
	rm $(DESTDIR)$(APPDIR)/ldmconf.desktop
	rm $(DESTDIR)$(MANDIR)/ldmconf.1

