# redshift-config makefile arnault perret <arpinux@member.fsf.org>

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
MANDIR = /usr/share/man/man1
REDDIR = /usr/share/redshift-config
LANGDIR = /usr/share/redshift-config/lang

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(REDDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(LANGDIR)
	install -m 755 -o root -g root redshift-config $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root redshift-config.1 $(DESTDIR)$(MANDIR)
	install -m 644 -o root -g root redshift-config.desktop $(DESTDIR)$(APPDIR)
	cp -a lang/* ${DESTDIR}${LANGDIR}/
	chown -R root:root ${DESTDIR}${LANGDIR}

uninstall:
	rm $(DESTDIR)$(BINDIR)/redshift-config
	rm $(DESTDIR)$(APPDIR)/redshift-config.desktop
	rm $(DESTDIR)$(MANDIR)/redshift-config.1
	rm -rf $(DESTDIR)$(REDDIR)

