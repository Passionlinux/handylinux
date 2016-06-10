# mpartage makefile arnault perret <arpinux@member.fsf.org>

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/icons
MANDIR = /usr/share/man/man1
PARTDIR = /usr/share/m_partage
LANGDIR = /usr/share/m_partage/lang

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(PARTDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(LANGDIR)
	install -m 755 -o root -g root m_partage $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root m_partage.1 $(DESTDIR)$(MANDIR)
	install -m 644 -o root -g root m_partage.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root m_partage.desktop $(DESTDIR)$(APPDIR)
	cp -a lang/* ${DESTDIR}${LANGDIR}/
	chown -R root:root ${DESTDIR}${LANGDIR}

uninstall:
	rm $(DESTDIR)$(BINDIR)/m_partage
	rm $(DESTDIR)$(APPDIR)/m_partage.desktop
	rm $(DESTDIR)$(ICONDIR)/m_partage.png
	rm $(DESTDIR)$(MANDIR)/m_partage.1
	rm -rf $(DESTDIR)$(PARTDIR)

