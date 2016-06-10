DESTDIR =
BINDIR = /usr/bin
THUDIR = /etc/skel/.config/Thunar

help:
	@echo "Usage: as root"
	@echo "make install  : installs application"
	@echo "make uninstall: uninstalls application"

install:
	# nettoyage des actions thunar
	if [ -e $(DESTDIR)$(THUDIR)/uca.xml ]; then rm /etc/skel/.config/Thunar/uca.xml* ; fi
	# mise en place des dossiers
	install -d -m 755 -o root -g root $(DESTDIR)$(BINDIR)
	install -d -m 755 -o root -g root $(DESTDIR)$(THUDIR)
	# copie des scripts
	install -m 755 -o root -g root scripts/* $(DESTDIR)$(BINDIR)
	# copie des configs thunar
	install -m 644 -o root -g root uca/* $(DESTDIR)$(THUDIR)
	chmod 644 $(DESTDIR)$(THUDIR)/uca*

uninstall:
	rm $(DESTDIR)$(BINDIR)/convert2*
	rm $(DESTDIR)$(BINDIR)/imagemod-hl
	rm $(DESTDIR)$(BINDIR)/pixup
	rm $(DESTDIR)$(BINDIR)/share_with_btshare
	rm $(DESTDIR)$(BINDIR)/upload_sur_VideoBin
	rm $(DESTDIR)$(THUDIR)/uca.xml*

