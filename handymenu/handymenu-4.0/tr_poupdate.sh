#!/bin/bash
# update translation script
# handymenu -- https://handylinux.org
echo ""
echo "générer le .pot"
echo ""
pygettext -o locale/handymenu.pot handymenu.py handymenu-configuration.py hm_utils.py hm-config-transition.py
cd locale
echo ""
echo "mise à jour des fichiers de traduction"
echo ""
msgmerge --update de/LC_MESSAGES/handymenu.po handymenu.pot
msgmerge --update en/LC_MESSAGES/handymenu.po handymenu.pot
msgmerge --update eo/LC_MESSAGES/handymenu.po handymenu.pot
msgmerge --update es/LC_MESSAGES/handymenu.po handymenu.pot
msgmerge --update fr/LC_MESSAGES/handymenu.po handymenu.pot
msgmerge --update nl/LC_MESSAGES/handymenu.po handymenu.pot
msgmerge --update ru/LC_MESSAGES/handymenu.po handymenu.pot
echo ""
echo "suppression des .mo obsolètes"
echo ""
find . -name "handymenu.mo" -exec rm {} \;
echo ""
echo "édition des fichiers : @toi de jouer. reviens et lance le script de génération des .mo"
echo -n "[Enter] pour quitter"
read anykey
exit 0
