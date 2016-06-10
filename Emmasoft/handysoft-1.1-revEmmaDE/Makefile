DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
APTDIR = /etc/apt/apt.conf.d
ICONDIR = /usr/share/pixmaps
SOFTDIR = /usr/share/handysoft
LANGDIR = /usr/share/locale
MANDIR = /usr/share/man/man1
STARTDIR = /etc/xdg/autostart

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APTDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(SOFTDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(LANGDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(STARTDIR)
	install -m 755 -o root -g root handysoft $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root handy-update-notifier $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root handy-update-checker $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root handy-upgrade-manager $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root networkcheck $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root *.py $(DESTDIR)$(SOFTDIR)
	install -m 644 -o root -g root handysoft.desktop $(DESTDIR)$(APPDIR)
	install -m 644 -o root -g root handy-update-checker.desktop $(DESTDIR)$(APPDIR)
	install -m 644 -o root -g root handy-update-notifier.desktop $(DESTDIR)$(STARTDIR)
	install -m 644 -o root -g root icons/*.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root mans/*.1 $(DESTDIR)$(MANDIR)
	cp -a locale/* ${DESTDIR}${LANGDIR}/
	find ${DESTDIR}${LANGDIR} -name "handysoft.po*" -exec rm {} \;
	chown -R root:root ${DESTDIR}${LANGDIR}
	install -m 644 -o root -g root aptd/00recommends $(DESTDIR)$(APTDIR)
	install -m 644 -o root -g root aptd/00trustcdrom $(DESTDIR)$(APTDIR)
	install -m 644 -o root -g root aptd/02periodic $(DESTDIR)$(APTDIR)
	install -m 644 -o root -g root aptd/99synaptic $(DESTDIR)$(APTDIR)

uninstall:
	rm -rf $(DESTDIR)$(SOFTDIR)
	rm $(DESTDIR)$(BINDIR)/handysoft
	rm $(DESTDIR)$(BINDIR)/networkcheck
	rm $(DESTDIR)$(BINDIR)/handy-update-checker
	rm $(DESTDIR)$(BINDIR)/handy-update-notifier
	rm $(DESTDIR)$(APPDIR)/handysoft.desktop
	rm $(DESTDIR)$(APPSDIR)/handy-update-checker.desktop
	rm $(DESTDIR)$(STARTDIR)/handy-update-notifier.desktop
	rm $(DESTDIR)$(ICONDIR)/handysoft.png
	rm $(DESTDIR)$(ICONDIR)/handy-update-checker.png
	rm $(DESTDIR)$(MANDIR)/handysoft.1
	rm $(DESTDIR)$(MANDIR)/handy-update-checker.1
	rm $(DESTDIR)$(MANDIR)/handy-update-notifier.1
	rm $(DESTDIR)$(MANDIR)/handy-upgrade-manager.1
	find ${DESTDIR}${LANGDIR} -name "handysoft*" -exec rm {} \;

