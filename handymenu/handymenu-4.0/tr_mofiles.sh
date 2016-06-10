#!/bin/bash
# création de .mo
# handymenu -- https://handylinux.org
echo ""
echo "suppression des anciens fichiers *.po"
echo ""
find locale -name "handymenu.po~" -exec rm {} \;
echo ""
echo "génération des .mo"
echo ""
cd locale/de/LC_MESSAGES && msgfmt handymenu.po -o handymenu.mo
cd ../../en/LC_MESSAGES && msgfmt handymenu.po -o handymenu.mo
cd ../../eo/LC_MESSAGES && msgfmt handymenu.po -o handymenu.mo
cd ../../es/LC_MESSAGES && msgfmt handymenu.po -o handymenu.mo
cd ../../fr/LC_MESSAGES && msgfmt handymenu.po -o handymenu.mo
cd ../../nl/LC_MESSAGES && msgfmt handymenu.po -o handymenu.mo
cd ../../ru/LC_MESSAGES && msgfmt handymenu.po -o handymenu.mo
echo ""
echo -n ".mo générés, [Enter] pous quitter."
read anykey
exit 0
