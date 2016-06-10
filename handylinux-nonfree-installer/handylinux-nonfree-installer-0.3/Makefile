DESTDIR =
BINDIR = /usr/bin
NONFREEDIR = /usr/share/handylinux-nonfree

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(NONFREEDIR)
	install -m 755 -o root -g root teamviewer-installer-launcher $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root teamviewer-installer $(DESTDIR)$(NONFREEDIR)

uninstall:
	rm $(DESTDIR)$(BINDIR)/teamviewer-installer-launcher
	rm -R -f $(DESTDIR)$(NONFREEDIR)

