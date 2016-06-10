#!/bin/bash
# update translation script
mkdir -p locale/de/LC_MESSAGES/
mkdir -p locale/en/LC_MESSAGES/
mkdir -p locale/eo/LC_MESSAGES/
mkdir -p locale/es/LC_MESSAGES/
mkdir -p locale/fr/LC_MESSAGES/
mkdir -p locale/it/LC_MESSAGES/
mkdir -p locale/nl/LC_MESSAGES/
mkdir -p locale/pt/LC_MESSAGES/
mkdir -p locale/ru/LC_MESSAGES/
echo ""
echo "générer le .pot"
echo ""
pygettext -o locale/handysoft.pot handysoft.py handysoft_utils.py images.py hlfavs.py soft_install.py
cd locale
echo ""
echo "mise à jour des fichiers de traduction"
echo ""
msgmerge --update de/LC_MESSAGES/handysoft.po handysoft.pot
msgmerge --update en/LC_MESSAGES/handysoft.po handysoft.pot
msgmerge --update eo/LC_MESSAGES/handysoft.po handysoft.pot
msgmerge --update es/LC_MESSAGES/handysoft.po handysoft.pot
msgmerge --update fr/LC_MESSAGES/handysoft.po handysoft.pot
msgmerge --update it/LC_MESSAGES/handysoft.po handysoft.pot
msgmerge --update nl/LC_MESSAGES/handysoft.po handysoft.pot
msgmerge --update pt/LC_MESSAGES/handysoft.po handysoft.pot
msgmerge --update ru/LC_MESSAGES/handysoft.po handysoft.pot
echo ""
echo "suppression des .mo obsolètes"
echo ""
find . -name "handysoft.mo" -exec rm {} \;
echo ""
echo "édition des fichiers : @toi de jouer. reviens et lance le script de génération des .mo"
echo -n "[Enter] pour quitter"
read anykey
exit 0
