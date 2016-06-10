# handylinux-doc-fr makefile arnault perret <arpinux@member.fsf.org> Sat  5 Sep 13:06:05 CEST 2015

DESTDIR =
DOCDIR = /usr/share/handylinux/HandyLinux_doc

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(DOCDIR)
	install -m 644 -o root -g root handylinux-manuel_installation.pdf $(DESTDIR)$(DOCDIR)
	install -m 644 -o root -g root handylinux-manuel_utilisateur.pdf $(DESTDIR)$(DOCDIR)

uninstall:
	rm $(DESTDIR)$(DOCDIR)/handylinux-manuel_installation.pdf
	rm $(DESTDIR)$(DOCDIR)/handylinux-manuel_utilisateur.pdf
