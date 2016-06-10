# loupy makefile arnault perret <arpinux@member.fsf.org> Sun  9 Aug 23:50:13 CEST 2015

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps
MANDIR = /usr/share/man/man1
LOUPYDIR = /usr/share/loupy
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
	install -d -m 755 -o root -g root $(DESTDIR)$(LOUPYDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(LANGDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	# copie des fichiers
	install -m 755 -o root -g root loupy $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root loupy.1 $(DESTDIR)$(MANDIR)
	install -m 755 -o root -g root loupy.py $(DESTDIR)$(LOUPYDIR)
	install -m 644 -o root -g root loupy_icon.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root loupy.desktop $(DESTDIR)$(APPDIR)
	# mise en place des traductions
	cp -a locale/* ${DESTDIR}${LANGDIR}/
	chown -R root:root ${DESTDIR}${LANGDIR}
	# nettoyage des traductions
	find ${DESTDIR}${LANGDIR} -name "loupy.po*" -exec rm {} \;

uninstall:
	rm -rf $(DESTDIR)$(LOUPYDIR)
	rm $(DESTDIR)$(BINDIR)/loupy
	rm $(DESTDIR)$(APPDIR)/loupy.desktop
	rm $(DESTDIR)$(MANDIR)/loupy.1
	find ${DESTDIR}${LANGDIR} -name "loupy*" -exec rm {} \;

