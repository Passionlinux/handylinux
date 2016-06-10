# Cyclope makefile arnault perret <arpinux@member.fsf.org> Sun 19 Jul 15:34:13 CEST 2015

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps
MANDIR = /usr/share/man/man1
LANGDIR = /usr/share/locale

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	# mise en place des dossiers
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(LANGDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	# copie des fichiers
	install -m 755 -o root -g root cyclope $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root cyclope.1 $(DESTDIR)$(MANDIR)
	install -m 644 -o root -g root cyclope_icon.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root cyclope.desktop $(DESTDIR)$(APPDIR)
	# mise en place des traductions
	cp -a locale/* ${DESTDIR}${LANGDIR}/
	chown -R root:root ${DESTDIR}${LANGDIR}
	# nettoyage des traductions
	find ${DESTDIR}${LANGDIR} -name "cyclope.po*" -exec rm {} \;

uninstall:
	rm $(DESTDIR)$(BINDIR)/cyclope
	rm $(DESTDIR)$(APPDIR)/cyclope.desktop
	rm $(DESTDIR)$(MANDIR)/cyclope.1
	find ${DESTDIR}${LANGDIR} -name "cyclope*" -exec rm {} \;

