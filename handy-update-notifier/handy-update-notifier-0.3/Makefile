# handy-update-notifier makefile arnault perret <arpinux@member.fsf.org>

DESTDIR =
BINDIR = /usr/bin
APTDIR = /etc/apt/apt.conf.d
APPSDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps
MANDIR = /usr/share/man/man1

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APTDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPSDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -m 755 -o root -g root handy-update-notifier $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root handy-update-checker $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root handy-upgrade-manager $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root handy-update-checker.desktop $(DESTDIR)$(APPSDIR)
	install -m 644 -o root -g root handy-update-checker.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root 00recommends $(DESTDIR)$(APTDIR)
	install -m 644 -o root -g root 00trustcdrom $(DESTDIR)$(APTDIR)
	install -m 644 -o root -g root 02periodic $(DESTDIR)$(APTDIR)
	install -m 644 -o root -g root 99synaptic $(DESTDIR)$(APTDIR)
	install -m 644 -o root -g root *.1 $(DESTDIR)$(MANDIR)

uninstall:
	rm $(DESTDIR)$(BINDIR)/handy-udate-notifier
	rm $(DESTDIR)$(BINDIR)/handy-udate-checker
	rm $(DESTDIR)$(BINDIR)/handy-upgrade-manager
	rm $(DESTDIR)$(APPSDIR)/handy-update-checker.desktop
	rm $(DESTDIR)$(ICONDIR)/handy-update-checker.png
	rm $(DESTDIR)$(MANDIR)/handy-update-notifier.1
	rm $(DESTDIR)$(MANDIR)/handy-update-checker.1
	rm $(DESTDIR)$(MANDIR)/handy-upgrade-manager.1

