# handylinux-doc-en makefile arnault perret <arpinux@member.fsf.org> Sat  5 Sep 13:06:05 CEST 2015

DESTDIR =
DOCDIR = /usr/share/handylinux/HandyLinux_doc

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(DOCDIR)
	cp -R documentation\ HandyLinux\ \(en\) $(DESTDIR)$(DOCDIR)
	chmod -R 644 $(DESTDIR)${DOCDIR}/*

uninstall:
	rm -rf $(DESTDIR)$(DOCDIR)/documentation\ HandyLinux\ \(en\)
