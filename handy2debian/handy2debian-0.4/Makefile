# handy2debian makefile arnault perret <arpinux@member.fsf.org>

DESTDIR =
BINDIR = /usr/bin
APPDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps
MANDIR = /usr/share/man/man1
DEFDEBDIR = /usr/share/handy2debian
SKELDIR = /usr/share/handy2debian/skel

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(APPDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(MANDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(DEFDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(DEFDEBDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(SKELDIR)
	install -m 755 -o root -g root handy2debian $(DESTDIR)$(BINDIR)
	install -m 755 -o root -g root move2debian $(DESTDIR)$(DEFDEBDIR)
	install -m 644 -o root -g root handy2debian.1 $(DESTDIR)$(MANDIR)
	install -m 755 -o root -g root confirm2debian-en.py $(DESTDIR)$(DEFDEBDIR)
	install -m 755 -o root -g root confirm2debian-fr.py $(DESTDIR)$(DEFDEBDIR)
	install -m 644 -o root -g root grub $(DESTDIR)$(DEFDEBDIR)
	install -m 644 -o root -g root issue $(DESTDIR)$(DEFDEBDIR)
	install -m 644 -o root -g root issue.net $(DESTDIR)$(DEFDEBDIR)
	install -m 644 -o root -g root slim.conf $(DESTDIR)$(DEFDEBDIR)
	install -m 644 -o root -g root lightdm.conf $(DESTDIR)$(DEFDEBDIR)
	install -m 644 -o root -g root lightdm-gtk-greeter.conf $(DESTDIR)$(DEFDEBDIR)
	install -m 644 -o root -g root .bashrc $(DESTDIR)$(SKELDIR)
	install -m 644 -o root -g root .bash_logout $(DESTDIR)$(SKELDIR)
	install -m 644 -o root -g root .profile $(DESTDIR)$(SKELDIR)
	install -m 644 -o root -g root handy2debian_icon.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root handy2debian.desktop $(DESTDIR)$(APPDIR)

uninstall:
	rm -rf $(DESTDIR)$(DEFDEBDIR)
	rm $(DESTDIR)$(BINDIR)/handy2debian
	rm $(DESTDIR)$(APPDIR)/handy2debian.desktop
	rm $(DESTDIR)$(ICONDIR)/handy2debian_icon.png
	rm $(DESTDIR)$(MANDIR)/handy2debian.1

