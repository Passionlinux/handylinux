#!/bin/bash
# création de .mo
# à exécuter après 'poupdate'
echo ""
echo "suppression des anciens fichiers *.po"
echo ""
find locale -name "handysoft.po~" -exec rm {} \;
echo ""
echo "génération des .mo"
echo ""
cd locale/de/LC_MESSAGES && msgfmt handysoft.po -o handysoft.mo
cd ../../en/LC_MESSAGES && msgfmt handysoft.po -o handysoft.mo
cd ../../eo/LC_MESSAGES && msgfmt handysoft.po -o handysoft.mo
cd ../../es/LC_MESSAGES && msgfmt handysoft.po -o handysoft.mo
cd ../../fr/LC_MESSAGES && msgfmt handysoft.po -o handysoft.mo
cd ../../nl/LC_MESSAGES && msgfmt handysoft.po -o handysoft.mo
cd ../../ru/LC_MESSAGES && msgfmt handysoft.po -o handysoft.mo
echo ""
echo -n ".mo générés, [Enter] pous quitter."
read anykey
exit 0
