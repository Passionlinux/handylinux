# BTshare : quickly

##Dependencies : 
python3-libtorrent 
python3-tk or python3-flask

## Usage
run 

    python3 btshare.py /directory/to/share

or

    python3 btshare-web.py /directory/to/share

#BTshare : pour partager ses documents simplement
[BTshare](http://yeuxdelibad.net/Programmation/BTshare.html) est un
petit outil écrit en python pour faciliter le partage de documents. Il
s'appuie sur le protocole BitTorrent pour réaliser cette tâche.

##Pourquoi?
Les solutions déjà existantes pour envoyer des fichiers ne me
convenaient tout simplement pas. En effet, 

- Déposer ses documents sur un service d'hébergement (mega, dl.free...)
  est long, et une fois le fichier déposé, il ne vous appartient plus
  vraiment. Il est alors quelque part sur un disque dur dans le
  monde...
- Héberger un serveur ftp ou http chez soi, c'est chouette. Cependant, c'est peu accessible, ça suppose d'ouvrir des ports, et surtout, l'upload reste très lent.
- Utiliser un script qui simplifie cette procédure, solution utilisée entre autres par les programmes [droopy](http://stackp.online.fr/?p=28) ou [m_partage](http://shovel-crew.org/?static12/m-partage-source), ne retire pas le défaut de la limite d'upload.

Avec BTshare, la vitesse de chargement est toujours limitée, mais, ce
défaut est diminué à partir du moment ou vous partagez le même fichier
avec plusieurs personnes, chacun devenant alors un pair.

De plus, s'appuyant sur bittorrent, les flux sont entièrement cryptés
(rc4) par défaut.

##Ça ressemble à quoi?
Voici quelques captures d'écran.

Version tk : 

![interface tk](http://yeuxdelibad.net/Images/btshare.png)

Version web:

![choix de dossier](http://yeuxdelibad.net/Images/btshare-web-start.png)
![Aperçu de BTshare](http://yeuxdelibad.net/Images/btshare-web.png)

Se voulant le plus simple possible, vous choisissez au démarrage un
dossier à partager. Tous les documents/dossiers placés dedans sont alors
partagés. Il ne vous reste plus qu'à envoyer le lien magnet à vos
correspondants pour qu'ils récupèrent votre fichier.

Une interface est accessible dans le navigateur, et permet par ailleurs
de rajouter des documents à télécharger. Bien sûr, on peut s'en servir
comme d'un client bittorrent, mais ce n'est pas l'objectif principal,
donc ne vous attendez pas à de multiples fonctionnalités.

##Le mot de la fin
N'hésitez pas à contribuer, le dépôt git est là pour ça.
