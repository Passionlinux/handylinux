DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps
SOFTDIR = /usr/share/handysoft
LANGDIR = /usr/share/locale
MANDIR = /usr/share/man/man1

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(SOFTDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(LANGDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -m 755 -o root -g root handysoft $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root *.py $(DESTDIR)$(SOFTDIR)
	install -m 644 -o root -g root handysoft.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handysoft.desktop $(DESTDIR)$(APPDIR)
	install -m 644 -o root -g root handysoft.1 $(DESTDIR)$(MANDIR)
	cp -a locale/* ${DESTDIR}${LANGDIR}/
	find ${DESTDIR}${LANGDIR} -name "handysoft.po*" -exec rm {} \;
	chown -R root:root ${DESTDIR}${LANGDIR}

uninstall:
	rm -rf $(DESTDIR)$(SOFTDIR)
	rm $(DESTDIR)$(BINDIR)/handysoft
	rm $(DESTDIR)$(APPDIR)/handysoft.desktop
	rm $(DESTDIR)$(MANDIR)/handysoft.1
	find ${DESTDIR}${LANGDIR} -name "handysoft*" -exec rm {} \;

