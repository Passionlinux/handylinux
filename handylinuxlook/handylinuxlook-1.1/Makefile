# handylinuxlook makefile arnault perret <arpinux@member.fsf.org> Mon Feb 23 01:02:26 CET 2015

DESTDIR =
BINDIR = /usr/bin
THMDIR = /usr/share/themes
WALLDIR = /usr/share/xfce4/backdrops
DOCDIR = /usr/share/doc/handylinuxlook
HDTMDIR = /usr/share/handytheme
SLIMDIR = /usr/share/slim/themes
LDMDIR = /usr/share/images/desktop-base
APPSDIR = /usr/share/applications
ICONDIR = /usr/share/pixmaps

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	install -d -m 755 -o root -g root $(DESTDIR)$(APPSDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(THMDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(WALLDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(DOCDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(HDTMDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(SLIMDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(LDMDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(ICONDIR)
	install -m 755 -o root -g root handytheme $(DESTDIR)$(BINDIR)
	install -m 644 -o root -g root handytheme.desktop $(DESTDIR)$(APPSDIR)
	install -m 644 -o root -g root handytheme.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root pixmaps/*.png $(DESTDIR)$(ICONDIR)
	install -m 644 -o root -g root walls/*.png $(DESTDIR)$(WALLDIR)
	install -m 644 -o root -g root walls/*.jpg $(DESTDIR)$(WALLDIR)
	install -m 644 -o root -g root README $(DESTDIR)$(DOCDIR)
	install -m 644 -o root -g root lightdm/handylinux2-lightdm.png $(DESTDIR)$(LDMDIR)
	cp -R themes/* $(DESTDIR)$(THMDIR)/
	cp -R HandyTheme/* $(DESTDIR)$(HDTMDIR)/
	cp -R slim/* $(DESTDIR)$(SLIMDIR)/

uninstall:
	rm -rf $(DESTDIR)$(THMDIR)/HandyLinuxClear
	rm -rf $(DESTDIR)$(THMDIR)/HandyLinuxDark
	rm -rf $(DESTDIR)$(LDMDIR)/handylinux2-lightdm.png
	rm -rf $(DESTDIR)$(HDTMDIR)
	rm -rf $(DESTDIR)$(DOCDIR)
	rm -rf $(DESTDIR)$(SLIMDIR)/handylinux
	rm -rf $(DESTDIR)$(SLIMDIR)/handylinux-1
	rm $(DESTDIR)$(BINDIR)/handytheme
	rm $(DESTDIR)$(APPSDIR)/handytheme.desktop

