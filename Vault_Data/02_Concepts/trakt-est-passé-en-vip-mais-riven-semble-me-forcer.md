---
id: "202608301750"
title: "trakt est passé en vip mais riven semble me forcer a utiliser leur api une alternative"
type: "concept"
origin: ["gemini_takeout"]
semantic_topic: "Data_Engineering"
tags: ["data_engineering", "takeout_coldstart"]
created_at: "2026-08-30"
updated_at: "2026-10-19"
total_time_invested_min: 70931
summary_1_line: "trakt est passé en vip mais riven semble me forcer a utiliser leur api une alternative ?"
---

# trakt est passé en vip mais riven semble me forcer a utiliser leur api une alternative

- **Problématique / Instruction :** trakt est passé en vip mais riven semble me forcer a utiliser leur api une alternative ?

  - *Conclusion retenue :* Le blocage de la création d'applications et de jetons API gratuits par Trakt (devenu réservé aux comptes VIP) pose en effet problème dans les configurations Riven. Plusieurs alternatives permettent de contourner Trakt, soit en restant sur Riven, soit...

- **Problématique / Instruction :** en gros mon probleme c'est que je veux pouvoir passer par plex sur ps5 pour ajouteru du contenu sauf que lorsque j'ajoute un contenu a la watchlist ça semble declencher une requete sur trakt

  - *Conclusion retenue :* Ce comportement vient du fait que Riven utilise par défaut Trakt comme résolveur d'identifiants (mapping entre ID Plex, TMDb, IMDb et TVDb) pour chaque élément détecté, même si la source de déclenchement est la Watchlist Plex. Pour utiliser la Watchl...

- **Problématique / Instruction :** trakt est a enabled false et pourtant ...

  - *Conclusion retenue :* C'est un problème connu dans l'architecture interne de Riven : même avec trakt.enabled: false , certaines branches du code (notamment les résolveurs d'ID et le parseur de métadonnées backend) appellent toujours l'API Trakt en dur avec le client_id pu...

- **Problématique / Instruction :** riven 0.23.6

  - *Conclusion retenue :* En version 0.23.6 , le comportement s'explique techniquement par le fonctionnement interne du worker TraktIndexer : Dans Riven, le paramètre trakt.enabled: false désactive uniquement Trakt comme source de contenu (les listes / watchlists Trakt). En r...

- **Problématique / Instruction :** alolon-s on pour jellyseer

  - *Conclusion retenue :* Voici le guide pas à pas pour déployer Jellyseerr, le synchroniser avec ta Watchlist Plex (sur PS5) et le relier à Riven. 1. Déploiement Docker de Jellyseerr Ajoute ce bloc à ton docker-compose.yml (ou lance-le directement via Container Manager sur t...

- **Problématique / Instruction :** tous les content auf mdblist sont sur false

  - *Conclusion retenue :* Le fait que plex_watchlist et jellyfin continuent de tourner en boucle malgré les modifications dans l'interface s'explique par deux choses : Le scheduler en mémoire : Riven charge les tâches de fond au démarrage. Si tu désactives une source dans l'U...

- **Problématique / Instruction :** c'est sur wsl du coup je mets l'ip wsl ?

  - *Conclusion retenue :* Non, l'IP interne de WSL change souvent et peut poser des problèmes de routage entre conteneurs Docker. Voici les meilleures options selon ta façon de faire tourner Docker : Cas 1 : Les deux conteneurs tournent sous Docker (le plus simple) S'ils sont...

- **Problématique / Instruction :** quand je fait test ça me dit failed to send webhook

  - *Conclusion retenue :* Trois causes principales expliquent cet échec d'envoi du webhook depuis Jellyseerr vers Riven : 1. La route exacte du Webhook Riven Selon les versions de Riven, le chemin d'écoute du webhook Jellyseerr/Overseerr varie : http://<IP_OU_HÔTE>:3000/api/v...

- **Problématique / Instruction :** comment je vois le nom du contenuer

  - *Conclusion retenue :* Dans ton terminal WSL (ou PowerShell avec Docker Desktop), lance la commande : docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Networks}}" Le nom exact de chaque conteneur apparaîtra dans la colonne NAMES . Si les deux conteneurs partag...

- **Problématique / Instruction :** toujours fail

  - *Conclusion retenue :* Le bouton Test de Jellyseerr envoie un payload générique de test qui ne contient pas d'ID de média (pas de champ media ), ce que le validateur d'API de Riven rejette souvent avec une erreur 400/422, provoquant l'affichage « failed to send webhook » d...

- **Problématique / Instruction :** ok la j'ai eu un 200

  - *Conclusion retenue :* La passerelle fonctionne. Le flux complet est désormais opérationnel sans dépendre de Trakt : Tu ajoutes un média à ta Watchlist Plex depuis la PS5. Jellyseerr récupère la Watchlist lors de sa synchronisation planifiée (ou manuelle via Jobs & Cache )...

- **Problématique / Instruction :** j'ai lancer manuellement la tach plex watchlist sync et rien sur le slogs de riven

  - *Conclusion retenue :* Si le job Plex Watchlist Sync s'exécute dans Jellyseerr sans rien envoyer à Riven, c'est généralement pour l'une des 3 raisons suivantes : 1. L'élément est déjà considéré comme possédé / demandé Dans Jellyseerr, va dans l'onglet Requests (Demandes) o...

- **Problématique / Instruction :** on va tenter seerrbridge

  - *Conclusion retenue :* Attention sur un point clé : le projet SeerrBridge officiel (Woahai321) nécessite également un Client ID Trakt pour son moteur de résolution interne. Pour te débarrasser définitivement de Trakt tout en conservant Jellyseerr (et l'ajout depuis ta PS5)...

- **Problématique / Instruction :** bah je suis on 0.23.6 dfe raven je crois c'est la latest release

  - *Conclusion retenue :* Effectivement, la version 0.23.6 est la dernière release taguée stable de Riven, et le correctif retirant les appels Trakt en dur n'a pas encore fait l'objet d'une nouvelle version numérotée. Deux solutions concrètes pour débloquer la situation : Sol...

- **Problématique / Instruction :** fail to resolve nightly

  - *Conclusion retenue :* Le tag nightly n'existe pas sous ce nom dans le registre Docker de Riven. Le projet publie ses builds de développement sur GitHub Container Registry ( ghcr.io ) ou sous le tag beta / main . Option 1 : Tester les tags de développement récents Modifie ...

- **Problématique / Instruction :** ok t'sais quoi on va repartir de zero parce que la ...

  - *Conclusion retenue :* C'est la meilleure décision : Riven a accumulé trop de frictions (dépendance à Trakt codée en dur, instabilités FUSE et conflits de migrations PostgreSQL). Le moyen le plus propre et fiable d'avoir Plex (PS5) $\rightarrow$ Téléchargement instantané R...

- **Problématique / Instruction :** b

  - *Conclusion retenue :* On nettoie d'abord l'ancien environnement, puis on déploie un docker-compose.yml complet et propre. 1. Nettoyage complet de l'ancienne stack Dans ton terminal WSL : cd ~/debrid-stack docker compose down -v cd ~ rm -rf debrid-stack mkdir debrid-stack ...

- **Problématique / Instruction :** on est d'accord qu'avec cette stack je vais pouvoir ajouter du contenu sur la ps5 automatiquement

  - *Conclusion retenue :* Oui, exactement. C'est le fonctionnement natif de cette stack : Sur ta PS5 : Tu ajoutes un film ou une série à ta Watchlist Plex . Jellyseerr récupère automatiquement cet ajout lors de sa synchronisation périodique avec ton compte Plex. Jellyseerr tr...

- **Problématique / Instruction :** ok tous les ocnteneurs sont up

  - *Conclusion retenue :* On configure la chaîne dans l'ordre logique. Étape 1 : Configurer RDT-Client avec Real-Debrid Ouvre http://localhost:6500 dans ton navigateur. Crée ton compte administrateur initial. Va dans Settings $\rightarrow$ Provider : Provider : Sélectionne Re...

- **Problématique / Instruction :** ah mais attends je veux pas que ça dl sur mon pc

  - *Conclusion retenue :* Dans ce cas, il faut faire du streaming direct (Zero Storage / Symlinks / Montage virtuel) et non du téléchargement physique via RDT-Client. Avec le streaming direct : Aucun fichier n'est téléchargé sur ton disque dur. Real-Debrid héberge le fichier ...

- **Problématique / Instruction :** k faut que je rm rf ce que j'ai fait ud coup

  - *Conclusion retenue :* Oui, fais un reset complet pour repartir propre. Dans ton terminal WSL : cd ~/debrid-stack docker compose down -v cd ~ rm -rf debrid-stack mkdir debrid-stack && cd debrid-stack mkdir -p zurg config media Dès que ton dossier est prêt, préviens-moi et ...

- **Problématique / Instruction :** ok j'ai lancer les commandes

  - *Conclusion retenue :* On configure les deux fichiers de liaison Real-Debrid, puis le compose. 1. Fichier de configuration Zurg Crée le fichier zurg/config.yml : nano zurg/config.yml Colle ce contenu en remplaçant <TON_TOKEN_REAL_DEBRID> par ta clé API Real-Debrid : zurg: ...

- **Problématique / Instruction :** j'ai pas de logs

  - *Conclusion retenue :* L'absence de logs signifie que la commande rclone mount tourne en tâche de fond sans erreur bloquante. Vérification du statut du conteneur Vérifie l'état de rclone-zurg : docker compose ps Si son statut affiche Up , le montage est actif. Test direct ...

- **Problématique / Instruction :** att jellyseer est pas config

  - *Conclusion retenue :* On configure Jellyseerr pas à pas : Étape 1 : Assistant de démarrage initial Ouvre ton navigateur sur http://localhost:5055 . Clique sur Sign In with Plex et connecte-toi avec ton compte Plex. Sélectionne ton serveur Plex dans la liste déroulante. Su...

- **Problématique / Instruction :** test fail

  - *Conclusion retenue :* Je ne peux pas utiliser Google Tasks, car les paramètres Gmail requis sont désactivés. Activez ces paramètres pour continuer....

- **Problématique / Instruction :** le test du webhook a fail

  - *Conclusion retenue :* Le bouton Test de Jellyseerr envoie un payload générique de test sans identifiant de film ou série. Comme le script cherchait un média réel, il renvoyait une erreur 404 à Jellyseerr. Voici la mise à jour pour gérer le test de notification et valider ...

- **Problématique / Instruction :** ok ça marche

  - *Conclusion retenue :* Parfait. Il ne reste plus qu'à faire le test de bout en bout : Sur ta PS5 (ou sur l'app mobile / web Plex) : ajoute un film ou une série à ta Watchlist . Sur Jellyseerr : va dans Settings $\rightarrow$ Jobs & Cache et clique sur Run Now sur Plex Watc...

- **Problématique / Instruction :** erreur 404

  - *Conclusion retenue :* L'erreur 404 provient de l'API Torrentio (soit parce que l'identifiant envoyé par Jellyseerr était au format TMDb au lieu d'IMDb tt... , soit parce que le titre exact n'a pas de flux direct avec cette clé). On va rendre le script plus robuste : Il af...

- **Problématique / Instruction :** touours 404

  - *Conclusion retenue :* Affiche la ligne de debug générée dans le terminal pour voir le payload exact reçu par le pont : docker compose logs --tail=50 jellyseerr-bridge Colle ici les lignes [DEBUG PAYLOAD] et [ERREUR] qui apparaissent....

- **Problématique / Instruction :** ok ça marche un peu mais sur les 3 films j'en ai un seul

  - *Conclusion retenue :* C'est tout à fait normal au vu des 3 films demandés dans tes logs : Toy Story 5 / Obsession (2026) / Spider-Man: Brand New Day (2026) : Ce sont des films prévus pour 2026 . Pour des œuvres non sorties ou très récentes, soit aucun torrent n'existe enc...

- **Problématique / Instruction :** mais attend en vrai c'est vraiment du bruicolage je snes que je vais passer un temps infini avec ce bridge y'apas un autre moyuen ?

  - *Conclusion retenue :* Oui, il existe des solutions industrielles et éprouvées : Option 1 : RDT-Client + Radarr / Sonarr (Le standard officiel de la communauté) C’est la méthode la plus robuste et la plus utilisée avec Plex. Fonctionnement : Tu installes Radarr (films), So...

- **Problématique / Instruction :** plex debrid n'est plus maintenu car remplacer par je sais plus quoi

  - *Conclusion retenue :* Le successeur direct et moderne de Plex_Debrid s'appelle Riven (ou DUMB / Decypharr ). C'est un projet dédié créé pour remplacer le code obsolète de Plex_Debrid : Il possède une interface Web moderne . Il se connecte en natif à ta Watchlist Plex et à...

- **Problématique / Instruction :** oui mais on reviens au probleme de trakkt

  - *Conclusion retenue :* Non, Riven ne nécessite absolument pas Trakt . L'obligation d'avoir Trakt venait de l'ancienne version de Plex_Debrid . Riven a été réécrit pour supprimer cette dépendance : Plex natif : Riven se connecte directement à l'API Plex via ton Plex Token ....

- **Problématique / Instruction :** non c'est faux recherche sur internet il reste du trakt hardcoder qui me bloque

  - *Conclusion retenue :* Tu as tout à fait raison : le backend de Riven s'appuie structurellement sur l'API de Trakt pour la normalisation de sa base de données interne de métadonnées, ce qui pose blocage si on refuse d'utiliser l'écosystème Trakt. Pour obtenir une solution ...

- **Problématique / Instruction :** on va tester decypharr et on verra

  - *Conclusion retenue :* Decypharr est une passerelle écrite en Go qui émule l'API d'un client de téléchargement (comme qBittorrent) pour les services Debrid (Real-Debrid, etc.) sans rien télécharger en local. Il s'interface parfaitement avec la stack et évite tout bricolage...

- **Problématique / Instruction :** ok je config decipharr j'ai deja mis real debrid la j'ai usenet je peux skip non

  - *Conclusion retenue :* Oui, tu peux complètement ignorer et passer (skip) la partie Usenet. Tu utilises exclusivement Real-Debrid pour le cache torrent/streaming direct via Zurg, donc Usenet ne te servira pas. Passe à l'étape suivante (configuration de la Watchlist / Scrap...

- **Problématique / Instruction :** dopwnlaod folder je mets quoi ?

  - *Conclusion retenue :* Mets /mnt (ou /mnt/movies / /mnt/shows si le champ sépare films et séries). Dans la configuration Docker qu'on a définie, ton dossier virtuel media est monté sur le chemin interne /mnt ....

- **Problématique / Instruction :** ok done

  - *Conclusion retenue :* On relie Jellyseerr à Decypharr pour que chaque ajout (Watchlist PS5 ou recherche) soit envoyé directement à Real-Debrid. 1. Récupérer la clé API Decypharr Dans Decypharr ( http://localhost:8282 ), va dans Settings $\rightarrow$ General (ou API / Sec...

- **Problématique / Instruction :** je trouve pas le chemin exact

  - *Conclusion retenue :* Dans Decypharr, il n'y a pas besoin de chercher une URL de webhook spécifique : Decypharr s'ajoute directement comme un serveur de téléchargement Radarr/Sonarr ou via l'API qBittorrent. Voici la méthode directe dans Jellyseerr ( http://localhost:5055...

- **Problématique / Instruction :** apres j'ai pas dl radarre t sonarr la

  - *Conclusion retenue :* C'est là tout le problème de Decypharr : Decypharr n'est pas un remplaçant de Radarr/Sonarr, c'est juste un client de téléchargement (comme qBittorrent, mais relié à Real-Debrid). Decypharr ne sait pas chercher des torrents tout seul : il attend que ...

- **Problématique / Instruction :** j'ai compose up mais je dois config maiotnenant non

  - *Conclusion retenue :* Oui. La configuration se fait en 4 étapes simples et directes : 1. Prowlarr ( http://localhost:9696 ) — Les Indexeurs Ouvre Prowlarr, va dans Indexers $\rightarrow$ Add Indexer . Ajoute tes trackers publics habituels (ex. 1337x , YTS , Torrent9 , Sha...

- **Problématique / Instruction :** j'ai rien dans select root folder j'ai fait test et ça a fonctionner mais rien de dispo

  - *Conclusion retenue :* C'est normal : le dossier racine ( Root Folder ) doit d'abord être déclaré à l'intérieur de Radarr et Sonarr . Tant qu'il n'y est pas créé, Jellyseerr ne reçoit aucun choix via l'API. 1. Déclarer le dossier dans Radarr Va sur Radarr ( http://localhos...

- **Problématique / Instruction :** le /movies a la racine ?

  - *Conclusion retenue :* Oui, tout à fait. Dans l'explorateur de dossiers de Radarr, choisis directement /movies tout en haut de l'arborescence (à la racine / ). C'est le point de montage interne défini dans Docker qui pointe vers ton dossier ./media/movies . Même principe d...

- **Problématique / Instruction :** il doit pointer vers le dossier movies dans debrid stack media ?

  - *Conclusion retenue :* Exactement. Dans ton fichier docker-compose.yml , Docker fait la correspondance suivante : Hôte (ta machine) : ~/debrid-stack/media/movies Conteneur Radarr : /movies Donc dans l'interface web de Radarr, sélectionner /movies pointe en réalité directem...

- **Problématique / Instruction :** ok j'ai ajouter les deux dossiers dans cahque apli mais ça apparait toujours pas sur jelly

  - *Conclusion retenue :* Jellyseerr met en cache la réponse précédente de l'API de Radarr/Sonarr tant que la page n'a pas été rechargée ou que le bouton Test n'a pas été ré-exécuté. Pour débloquer l'apparition : 1. Recharger et tester dans Jellyseerr Sur la page Jellyseerr (...

- **Problématique / Instruction :** ok c'est bon

  - *Conclusion retenue :* Tout est en place. La chaîne complète et automatisée est opérationnelle : Test de bout en bout Faire une demande : Ajoute un film ou une série à ta Watchlist Plex depuis ta PS5 (ou fais une demande directe dans Jellyseerr sur http://localhost:5055 )....

- **Problématique / Instruction :** j'ai jaouter une serie sur plex elle apparait dans decypharr et sonarr mais je la vois pas dans plex

  - *Conclusion retenue :* Si la série est bien visible dans Decypharr et Sonarr , cela signifie que la recherche et l'ajout sur Real-Debrid ont fonctionné. Si elle n'apparaît pas encore dans Plex, cela se situe à l'une de ces 3 étapes : 1. Vérifier si les fichiers sont montés...

- **Problématique / Instruction :** elle apparait pas dans real debrid

  - *Conclusion retenue :* Si le torrent n'est pas sur Real-Debrid, le blocage se situe entre Sonarr et Decypharr . 1. Vérifier les logs de Decypharr Dans ton terminal WSL, regarde ce que reçoit Decypharr : docker compose logs --tail=30 decypharr Si tu vois une erreur 401 Unau...

- **Problématique / Instruction :** jm ai mis une serie ne watchlist mais elle apparait pas dans sonaarrr

  - *Conclusion retenue :* Si une série ajoutée à ta Watchlist Plex n'arrive pas dans Sonarr , la coupure se situe entre Plex et Jellyseerr (ou Jellyseerr et Sonarr). 1. Forcer la synchronisation de la Watchlist dans Jellyseerr Plex ne pousse pas les ajouts en temps réel par w...

- **Problématique / Instruction :** si j'appuie pas sur request dans jellysseer la serie apparait pas dans osnarr

  - *Conclusion retenue :* C'est parce que l'option de demande automatique ( Auto-Request ) de la Watchlist n'est pas activée pour ton utilisateur dans Jellyseerr. Sans cela, Jellyseerr synchronise la liste à titre informatif mais attend une validation manuelle. Pour automatis...

- **Problématique / Instruction :** pas moyen que ça le fasse automatiquement ?

  - *Conclusion retenue :* Oui, tout à fait. Si la recherche automatique ne s'est pas déclenchée, c'est simplement parce que l'option Enable Automatic Search n'est pas cochée dans les paramètres du serveur au sein de Jellyseerr. Activer la recherche automatique dans Jellyseerr...

- **Problématique / Instruction :** c'etais deja fait mais ça semble pas dl

  - *Conclusion retenue :* Si Jellyseerr envoie bien la commande mais que rien ne se télécharge, le blocage vient soit des trackers dans Prowlarr , soit du profil de qualité/langue dans Sonarr . Voici les points précis à vérifier dans l'ordre : 1. Vérifier la liaison Prowlarr ...

- **Problématique / Instruction :** 2026-08-30 19:28:12.1|Debug|ProcessProvider|Found 0 processes with the name: Sonarr.Console
2026-08-30 19:28:12.1|Debug|ProcessProvider|Found 1 processes with the name: Sonarr
2026-08-30 19:28:12.1|Debug|ProcessProvider| - [153] Sonarr
2026-08-30 19:28:12.1|Info|MigrationController|*** Migrating data source=/config/logs.db;cache size=-20000;datetimekind=Utc;journal mode=Wal;pooling=True;version=3;busytimeout=100 ***
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|DatabaseEngineVersionCheck migrating
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|PerformDBOperation 
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Performing DB Operation
2026-08-30 19:28:12.1|Info|DatabaseEngineVersionCheck|SQLite 3.53.4
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0110902s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|DatabaseEngineVersionCheck migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0112221s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|VersionMigration migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|CreateTable VersionInfo
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE TABLE "VersionInfo" ("Version" INTEGER NOT NULL)
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0003364s
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|VersionMigration migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0074179s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|VersionUniqueMigration migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|CreateIndex VersionInfo (Version)
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE UNIQUE INDEX "UC_Version" ON "VersionInfo" ("Version" ASC)
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0002956s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|AlterTable VersionInfo
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 9E-07s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|CreateColumn VersionInfo AppliedOn DateTime
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|ALTER TABLE "VersionInfo" ADD COLUMN "AppliedOn" DATETIME
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0007021s
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|VersionUniqueMigration migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028511s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|VersionDescriptionMigration migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|AlterTable VersionInfo
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 1E-06s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|CreateColumn VersionInfo Description String
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|ALTER TABLE "VersionInfo" ADD COLUMN "Description" TEXT
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0004224s
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|VersionDescriptionMigration migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026965s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|1: InitialSetup migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|InitialSetup|Starting migration of Log DB to 1
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|CreateTable Logs
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE TABLE "Logs" ("Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Message" TEXT NOT NULL, "Time" DATETIME NOT NULL, "Logger" TEXT NOT NULL, "Method" TEXT, "Exception" TEXT, "ExceptionType" TEXT, "Level" TEXT NOT NULL)
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0004509s
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (1, '2026-08-30T17:28:12', 'InitialSetup')
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|1: InitialSetup migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0037341s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|2: remove_tvrage_imdb_unique_constraint migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|remove_tvrage_imdb_unique_constraint|Starting migration of Log DB to 2
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (2, '2026-08-30T17:28:12', 'remove_tvrage_imdb_unique_constraint')
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|2: remove_tvrage_imdb_unique_constraint migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027227s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|3: remove_renamed_scene_mapping_columns migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|remove_renamed_scene_mapping_columns|Starting migration of Log DB to 3
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (3, '2026-08-30T17:28:12', 'remove_renamed_scene_mapping_columns')
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|3: remove_renamed_scene_mapping_columns migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0042401s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|4: updated_history migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|updated_history|Starting migration of Log DB to 4
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (4, '2026-08-30T17:28:12', 'updated_history')
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|4: updated_history migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026859s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|5: added_eventtype_to_history migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|added_eventtype_to_history|Starting migration of Log DB to 5
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (5, '2026-08-30T17:28:12', 'added_eventtype_to_history')
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|5: added_eventtype_to_history migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028251s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|6: add_index_to_log_time migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|add_index_to_log_time|Starting migration of Log DB to 6
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|DeleteTable Logs
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|DROP TABLE "Logs"
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0002639s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|CreateTable Logs
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE TABLE "Logs" ("Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Message" TEXT NOT NULL, "Time" DATETIME NOT NULL, "Logger" TEXT NOT NULL, "Method" TEXT, "Exception" TEXT, "ExceptionType" TEXT, "Level" TEXT NOT NULL)
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0003948s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|CreateIndex Logs (Time)
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE INDEX "IX_Logs_Time" ON "Logs" ("Time" ASC)
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0001997s
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (6, '2026-08-30T17:28:12', 'add_index_to_log_time')
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|6: add_index_to_log_time migrated
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0045461s
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|7: add_renameEpisodes_to_naming migrating
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.1|Info|add_renameEpisodes_to_naming|Starting migration of Log DB to 7
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (7, '2026-08-30T17:28:12', 'add_renameEpisodes_to_naming')
2026-08-30 19:28:12.1|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.1|Info|FluentMigrator.Runner.MigrationRunner|7: add_renameEpisodes_to_naming migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0030731s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|8: remove_backlog migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|remove_backlog|Starting migration of Log DB to 8
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (8, '2026-08-30T17:28:12', 'remove_backlog')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|8: remove_backlog migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0034596s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|9: fix_rename_episodes migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|fix_rename_episodes|Starting migration of Log DB to 9
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (9, '2026-08-30T17:28:12', 'fix_rename_episodes')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|9: fix_rename_episodes migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0033935s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|10: add_monitored migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_monitored|Starting migration of Log DB to 10
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (10, '2026-08-30T17:28:12', 'add_monitored')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|10: add_monitored migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002705s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|11: remove_ignored migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|remove_ignored|Starting migration of Log DB to 11
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (11, '2026-08-30T17:28:12', 'remove_ignored')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|11: remove_ignored migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0030103s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|12: remove_custom_start_date migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|remove_custom_start_date|Starting migration of Log DB to 12
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (12, '2026-08-30T17:28:12', 'remove_custom_start_date')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|12: remove_custom_start_date migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026376s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|13: add_air_date_utc migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_air_date_utc|Starting migration of Log DB to 13
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (13, '2026-08-30T17:28:12', 'add_air_date_utc')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|13: add_air_date_utc migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024894s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|14: drop_air_date migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|drop_air_date|Starting migration of Log DB to 14
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (14, '2026-08-30T17:28:12', 'drop_air_date')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|14: drop_air_date migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027036s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|15: add_air_date_as_string migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_air_date_as_string|Starting migration of Log DB to 15
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (15, '2026-08-30T17:28:12', 'add_air_date_as_string')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|15: add_air_date_as_string migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024314s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|16: updated_imported_history_item migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|updated_imported_history_item|Starting migration of Log DB to 16
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (16, '2026-08-30T17:28:12', 'updated_imported_history_item')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|16: updated_imported_history_item migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002428s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|17: reset_scene_names migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|reset_scene_names|Starting migration of Log DB to 17
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (17, '2026-08-30T17:28:12', 'reset_scene_names')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|17: reset_scene_names migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023903s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|18: remove_duplicates migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|remove_duplicates|Starting migration of Log DB to 18
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (18, '2026-08-30T17:28:12', 'remove_duplicates')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|18: remove_duplicates migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027167s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|19: restore_unique_constraints migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|restore_unique_constraints|Starting migration of Log DB to 19
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (19, '2026-08-30T17:28:12', 'restore_unique_constraints')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|19: restore_unique_constraints migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023893s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|20: add_year_and_seasons_to_series migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_year_and_seasons_to_series|Starting migration of Log DB to 20
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (20, '2026-08-30T17:28:12', 'add_year_and_seasons_to_series')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|20: add_year_and_seasons_to_series migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025712s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|21: drop_seasons_table migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|drop_seasons_table|Starting migration of Log DB to 21
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (21, '2026-08-30T17:28:12', 'drop_seasons_table')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|21: drop_seasons_table migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002893s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|22: move_indexer_to_generic_provider migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|move_indexer_to_generic_provider|Starting migration of Log DB to 22
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (22, '2026-08-30T17:28:12', 'move_indexer_to_generic_provider')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|22: move_indexer_to_generic_provider migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024641s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|23: add_config_contract_to_indexers migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_config_contract_to_indexers|Starting migration of Log DB to 23
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (23, '2026-08-30T17:28:12', 'add_config_contract_to_indexers')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|23: add_config_contract_to_indexers migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025758s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|24: drop_tvdb_episodeid migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|drop_tvdb_episodeid|Starting migration of Log DB to 24
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (24, '2026-08-30T17:28:12', 'drop_tvdb_episodeid')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|24: drop_tvdb_episodeid migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025504s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|25: move_notification_to_generic_provider migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|move_notification_to_generic_provider|Starting migration of Log DB to 25
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (25, '2026-08-30T17:28:12', 'move_notification_to_generic_provider')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|25: move_notification_to_generic_provider migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028495s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|26: add_config_contract_to_notifications migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_config_contract_to_notifications|Starting migration of Log DB to 26
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (26, '2026-08-30T17:28:12', 'add_config_contract_to_notifications')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|26: add_config_contract_to_notifications migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029984s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|27: fix_omgwtfnzbs migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|fix_omgwtfnzbs|Starting migration of Log DB to 27
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (27, '2026-08-30T17:28:12', 'fix_omgwtfnzbs')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|27: fix_omgwtfnzbs migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029793s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|28: add_blacklist_table migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_blacklist_table|Starting migration of Log DB to 28
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (28, '2026-08-30T17:28:12', 'add_blacklist_table')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|28: add_blacklist_table migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029818s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|29: add_formats_to_naming_config migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_formats_to_naming_config|Starting migration of Log DB to 29
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (29, '2026-08-30T17:28:12', 'add_formats_to_naming_config')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|29: add_formats_to_naming_config migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0038534s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|30: add_season_folder_format_to_naming_config migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_season_folder_format_to_naming_config|Starting migration of Log DB to 30
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (30, '2026-08-30T17:28:12', 'add_season_folder_format_to_naming_config')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|30: add_season_folder_format_to_naming_config migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0037707s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|31: delete_old_naming_config_columns migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|delete_old_naming_config_columns|Starting migration of Log DB to 31
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (31, '2026-08-30T17:28:12', 'delete_old_naming_config_columns')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|31: delete_old_naming_config_columns migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0032248s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|32: set_default_release_group migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|set_default_release_group|Starting migration of Log DB to 32
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (32, '2026-08-30T17:28:12', 'set_default_release_group')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|32: set_default_release_group migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028696s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|33: add_api_key_to_pushover migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_api_key_to_pushover|Starting migration of Log DB to 33
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (33, '2026-08-30T17:28:12', 'add_api_key_to_pushover')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|33: add_api_key_to_pushover migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0030505s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|34: remove_series_contraints migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|remove_series_contraints|Starting migration of Log DB to 34
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (34, '2026-08-30T17:28:12', 'remove_series_contraints')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|34: remove_series_contraints migrated
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029742s
2026-08-30 19:28:12.2|Info|FluentMigrator.Runner.MigrationRunner|35: add_series_folder_format_to_naming_config migrating
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.2|Info|add_series_folder_format_to_naming_config|Starting migration of Log DB to 35
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (35, '2026-08-30T17:28:12', 'add_series_folder_format_to_naming_config')
2026-08-30 19:28:12.2|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|35: add_series_folder_format_to_naming_config migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025948s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|36: update_with_quality_converters migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|update_with_quality_converters|Starting migration of Log DB to 36
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (36, '2026-08-30T17:28:12', 'update_with_quality_converters')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|36: update_with_quality_converters migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026491s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|37: add_configurable_qualities migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_configurable_qualities|Starting migration of Log DB to 37
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (37, '2026-08-30T17:28:12', 'add_configurable_qualities')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|37: add_configurable_qualities migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024941s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|38: add_on_upgrade_to_notifications migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_on_upgrade_to_notifications|Starting migration of Log DB to 38
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (38, '2026-08-30T17:28:12', 'add_on_upgrade_to_notifications')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|38: add_on_upgrade_to_notifications migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0033853s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|39: add_metadata_tables migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_metadata_tables|Starting migration of Log DB to 39
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (39, '2026-08-30T17:28:12', 'add_metadata_tables')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|39: add_metadata_tables migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025354s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|40: add_metadata_to_episodes_and_series migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_metadata_to_episodes_and_series|Starting migration of Log DB to 40
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (40, '2026-08-30T17:28:12', 'add_metadata_to_episodes_and_series')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|40: add_metadata_to_episodes_and_series migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028737s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|41: fix_xbmc_season_images_metadata migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|fix_xbmc_season_images_metadata|Starting migration of Log DB to 41
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (41, '2026-08-30T17:28:12', 'fix_xbmc_season_images_metadata')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|41: fix_xbmc_season_images_metadata migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029045s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|42: add_download_clients_table migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_download_clients_table|Starting migration of Log DB to 42
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (42, '2026-08-30T17:28:12', 'add_download_clients_table')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|42: add_download_clients_table migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027403s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|43: convert_config_to_download_clients migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|convert_config_to_download_clients|Starting migration of Log DB to 43
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (43, '2026-08-30T17:28:12', 'convert_config_to_download_clients')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|43: convert_config_to_download_clients migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027978s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|44: fix_xbmc_episode_metadata migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|fix_xbmc_episode_metadata|Starting migration of Log DB to 44
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (44, '2026-08-30T17:28:12', 'fix_xbmc_episode_metadata')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|44: fix_xbmc_episode_metadata migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027651s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|45: add_indexes migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_indexes|Starting migration of Log DB to 45
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (45, '2026-08-30T17:28:12', 'add_indexes')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|45: add_indexes migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002547s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|46: fix_nzb_su_url migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|fix_nzb_su_url|Starting migration of Log DB to 46
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (46, '2026-08-30T17:28:12', 'fix_nzb_su_url')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|46: fix_nzb_su_url migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025433s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|47: add_temporary_blacklist_columns migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_temporary_blacklist_columns|Starting migration of Log DB to 47
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (47, '2026-08-30T17:28:12', 'add_temporary_blacklist_columns')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|47: add_temporary_blacklist_columns migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026105s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|48: add_title_to_scenemappings migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_title_to_scenemappings|Starting migration of Log DB to 48
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (48, '2026-08-30T17:28:12', 'add_title_to_scenemappings')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|48: add_title_to_scenemappings migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0033141s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|49: fix_dognzb_url migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|fix_dognzb_url|Starting migration of Log DB to 49
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (49, '2026-08-30T17:28:12', 'fix_dognzb_url')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|49: fix_dognzb_url migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029012s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|50: add_hash_to_metadata_files migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_hash_to_metadata_files|Starting migration of Log DB to 50
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (50, '2026-08-30T17:28:12', 'add_hash_to_metadata_files')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|50: add_hash_to_metadata_files migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026315s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|51: download_client_import migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|download_client_import|Starting migration of Log DB to 51
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (51, '2026-08-30T17:28:12', 'download_client_import')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|51: download_client_import migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0038695s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|52: add_columns_for_anime migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_columns_for_anime|Starting migration of Log DB to 52
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (52, '2026-08-30T17:28:12', 'add_columns_for_anime')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|52: add_columns_for_anime migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029508s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|53: add_series_sorttitle migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_series_sorttitle|Starting migration of Log DB to 53
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (53, '2026-08-30T17:28:12', 'add_series_sorttitle')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|53: add_series_sorttitle migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027991s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|54: rename_profiles migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|rename_profiles|Starting migration of Log DB to 54
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (54, '2026-08-30T17:28:12', 'rename_profiles')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|54: rename_profiles migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0032225s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|55: drop_old_profile_columns migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|drop_old_profile_columns|Starting migration of Log DB to 55
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (55, '2026-08-30T17:28:12', 'drop_old_profile_columns')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|55: drop_old_profile_columns migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028274s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|56: add_mediainfo_to_episodefile migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_mediainfo_to_episodefile|Starting migration of Log DB to 56
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (56, '2026-08-30T17:28:12', 'add_mediainfo_to_episodefile')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|56: add_mediainfo_to_episodefile migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0031625s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|57: convert_episode_file_path_to_relative migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|convert_episode_file_path_to_relative|Starting migration of Log DB to 57
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (57, '2026-08-30T17:28:12', 'convert_episode_file_path_to_relative')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|57: convert_episode_file_path_to_relative migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025729s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|58: drop_episode_file_path migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|drop_episode_file_path|Starting migration of Log DB to 58
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (58, '2026-08-30T17:28:12', 'drop_episode_file_path')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|58: drop_episode_file_path migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0030857s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|59: add_enable_options_to_indexers migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|add_enable_options_to_indexers|Starting migration of Log DB to 59
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (59, '2026-08-30T17:28:12', 'add_enable_options_to_indexers')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|59: add_enable_options_to_indexers migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0063339s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|60: remove_enable_from_indexers migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|remove_enable_from_indexers|Starting migration of Log DB to 60
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (60, '2026-08-30T17:28:12', 'remove_enable_from_indexers')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|60: remove_enable_from_indexers migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002559s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|61: clear_bad_scene_names migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|clear_bad_scene_names|Starting migration of Log DB to 61
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (61, '2026-08-30T17:28:12', 'clear_bad_scene_names')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|61: clear_bad_scene_names migrated
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027696s
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|62: convert_quality_models migrating
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.3|Info|convert_quality_models|Starting migration of Log DB to 62
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (62, '2026-08-30T17:28:12', 'convert_quality_models')
2026-08-30 19:28:12.3|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.3|Info|FluentMigrator.Runner.MigrationRunner|62: convert_quality_models migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025262s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|63: add_remotepathmappings migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_remotepathmappings|Starting migration of Log DB to 63
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (63, '2026-08-30T17:28:12', 'add_remotepathmappings')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|63: add_remotepathmappings migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023411s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|64: remove_method_from_logs migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|remove_method_from_logs|Starting migration of Log DB to 64
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|DeleteColumn Logs Method
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE TABLE "Logs_temp" ("Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Message" TEXT NOT NULL, "Time" DATETIME NOT NULL, "Logger" TEXT NOT NULL, "Exception" TEXT, "ExceptionType" TEXT, "Level" TEXT NOT NULL)
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "Logs_temp" ("Id", "Message", "Time", "Logger", "Exception", "ExceptionType", "Level") SELECT "Id", "Message", "Time", "Logger", "Exception", "ExceptionType", "Level" FROM "Logs"
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|DROP TABLE "Logs"
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|ALTER TABLE "Logs_temp" RENAME TO "Logs"
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE INDEX "IX_Logs_Time" ON "Logs" ("Time" ASC)
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0021728s
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (64, '2026-08-30T17:28:12', 'remove_method_from_logs')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|64: remove_method_from_logs migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0047837s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|65: make_scene_numbering_nullable migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|make_scene_numbering_nullable|Starting migration of Log DB to 65
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (65, '2026-08-30T17:28:12', 'make_scene_numbering_nullable')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|65: make_scene_numbering_nullable migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0031767s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|66: add_tags migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_tags|Starting migration of Log DB to 66
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (66, '2026-08-30T17:28:12', 'add_tags')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|66: add_tags migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027733s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|67: add_added_to_series migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_added_to_series|Starting migration of Log DB to 67
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (67, '2026-08-30T17:28:12', 'add_added_to_series')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|67: add_added_to_series migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024672s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|68: add_release_restrictions migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_release_restrictions|Starting migration of Log DB to 68
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (68, '2026-08-30T17:28:12', 'add_release_restrictions')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|68: add_release_restrictions migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028294s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|69: quality_proper migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|quality_proper|Starting migration of Log DB to 69
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (69, '2026-08-30T17:28:12', 'quality_proper')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|69: quality_proper migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0032973s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|70: delay_profile migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|delay_profile|Starting migration of Log DB to 70
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (70, '2026-08-30T17:28:12', 'delay_profile')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|70: delay_profile migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029669s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|71: unknown_quality_in_profile migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|unknown_quality_in_profile|Starting migration of Log DB to 71
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (71, '2026-08-30T17:28:12', 'unknown_quality_in_profile')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|71: unknown_quality_in_profile migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027661s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|72: history_downloadId migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|history_downloadId|Starting migration of Log DB to 72
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (72, '2026-08-30T17:28:12', 'history_downloadId')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|72: history_downloadId migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0033451s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|73: clear_ratings migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|clear_ratings|Starting migration of Log DB to 73
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (73, '2026-08-30T17:28:12', 'clear_ratings')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|73: clear_ratings migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024191s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|74: disable_eztv migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|disable_eztv|Starting migration of Log DB to 74
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (74, '2026-08-30T17:28:12', 'disable_eztv')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|74: disable_eztv migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024129s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|75: force_lib_update migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|force_lib_update|Starting migration of Log DB to 75
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (75, '2026-08-30T17:28:12', 'force_lib_update')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|75: force_lib_update migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024616s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|76: add_users_table migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_users_table|Starting migration of Log DB to 76
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (76, '2026-08-30T17:28:12', 'add_users_table')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|76: add_users_table migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027997s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|77: add_add_options_to_series migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_add_options_to_series|Starting migration of Log DB to 77
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (77, '2026-08-30T17:28:12', 'add_add_options_to_series')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|77: add_add_options_to_series migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023983s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|78: add_commands_table migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_commands_table|Starting migration of Log DB to 78
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (78, '2026-08-30T17:28:12', 'add_commands_table')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|78: add_commands_table migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023302s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|79: dedupe_tags migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|dedupe_tags|Starting migration of Log DB to 79
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (79, '2026-08-30T17:28:12', 'dedupe_tags')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|79: dedupe_tags migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025714s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|81: move_dot_prefix_to_transmission_category migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|move_dot_prefix_to_transmission_category|Starting migration of Log DB to 81
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (81, '2026-08-30T17:28:12', 'move_dot_prefix_to_transmission_category')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|81: move_dot_prefix_to_transmission_category migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029415s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|82: add_fanzub_settings migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_fanzub_settings|Starting migration of Log DB to 82
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (82, '2026-08-30T17:28:12', 'add_fanzub_settings')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|82: add_fanzub_settings migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0032471s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|83: additonal_blacklist_columns migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|additonal_blacklist_columns|Starting migration of Log DB to 83
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (83, '2026-08-30T17:28:12', 'additonal_blacklist_columns')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|83: additonal_blacklist_columns migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002665s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|84: update_quality_minmax_size migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|update_quality_minmax_size|Starting migration of Log DB to 84
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (84, '2026-08-30T17:28:12', 'update_quality_minmax_size')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|84: update_quality_minmax_size migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0038402s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|85: expand_transmission_urlbase migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|expand_transmission_urlbase|Starting migration of Log DB to 85
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (85, '2026-08-30T17:28:12', 'expand_transmission_urlbase')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|85: expand_transmission_urlbase migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027978s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|86: pushbullet_device_ids migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|pushbullet_device_ids|Starting migration of Log DB to 86
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (86, '2026-08-30T17:28:12', 'pushbullet_device_ids')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|86: pushbullet_device_ids migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025774s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|87: remove_eztv migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|remove_eztv|Starting migration of Log DB to 87
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (87, '2026-08-30T17:28:12', 'remove_eztv')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|87: remove_eztv migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027296s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|88: pushbullet_devices_channels_list migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|pushbullet_devices_channels_list|Starting migration of Log DB to 88
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (88, '2026-08-30T17:28:12', 'pushbullet_devices_channels_list')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|88: pushbullet_devices_channels_list migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.00407s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|89: add_on_rename_to_notifcations migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_on_rename_to_notifcations|Starting migration of Log DB to 89
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (89, '2026-08-30T17:28:12', 'add_on_rename_to_notifcations')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|89: add_on_rename_to_notifcations migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0033824s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|90: update_kickass_url migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|update_kickass_url|Starting migration of Log DB to 90
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (90, '2026-08-30T17:28:12', 'update_kickass_url')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|90: update_kickass_url migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0032964s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|91: added_indexerstatus migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|added_indexerstatus|Starting migration of Log DB to 91
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (91, '2026-08-30T17:28:12', 'added_indexerstatus')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|91: added_indexerstatus migrated
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027851s
2026-08-30 19:28:12.4|Info|FluentMigrator.Runner.MigrationRunner|92: add_unverifiedscenenumbering migrating
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.4|Info|add_unverifiedscenenumbering|Starting migration of Log DB to 92
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (92, '2026-08-30T17:28:12', 'add_unverifiedscenenumbering')
2026-08-30 19:28:12.4|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|92: add_unverifiedscenenumbering migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0044004s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|93: naming_config_replace_illegal_characters migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|naming_config_replace_illegal_characters|Starting migration of Log DB to 93
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (93, '2026-08-30T17:28:12', 'naming_config_replace_illegal_characters')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|93: naming_config_replace_illegal_characters migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025944s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|94: add_tvmazeid migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|add_tvmazeid|Starting migration of Log DB to 94
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (94, '2026-08-30T17:28:12', 'add_tvmazeid')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|94: add_tvmazeid migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029304s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|95: add_additional_episodes_index migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|add_additional_episodes_index|Starting migration of Log DB to 95
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (95, '2026-08-30T17:28:12', 'add_additional_episodes_index')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|95: add_additional_episodes_index migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026455s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|96: disable_kickass migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|disable_kickass|Starting migration of Log DB to 96
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (96, '2026-08-30T17:28:12', 'disable_kickass')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|96: disable_kickass migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0043288s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|97: add_reason_to_pending_releases migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|add_reason_to_pending_releases|Starting migration of Log DB to 97
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (97, '2026-08-30T17:28:12', 'add_reason_to_pending_releases')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|97: add_reason_to_pending_releases migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0044335s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|98: remove_titans_of_tv migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|remove_titans_of_tv|Starting migration of Log DB to 98
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (98, '2026-08-30T17:28:12', 'remove_titans_of_tv')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|98: remove_titans_of_tv migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025604s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|99: extra_and_subtitle_files migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|extra_and_subtitle_files|Starting migration of Log DB to 99
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (99, '2026-08-30T17:28:12', 'extra_and_subtitle_files')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|99: extra_and_subtitle_files migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0031184s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|100: add_scene_season_number migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|add_scene_season_number|Starting migration of Log DB to 100
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (100, '2026-08-30T17:28:12', 'add_scene_season_number')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|100: add_scene_season_number migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0031605s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|101: add_ultrahd_quality_in_profiles migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|add_ultrahd_quality_in_profiles|Starting migration of Log DB to 101
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (101, '2026-08-30T17:28:12', 'add_ultrahd_quality_in_profiles')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|101: add_ultrahd_quality_in_profiles migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002602s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|102: add_language_to_episodeFiles_history_and_blacklist migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|add_language_to_episodeFiles_history_and_blacklist|Starting migration of Log DB to 102
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (102, '2026-08-30T17:28:12', 'add_language_to_episodeFiles_history_and_blacklist')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|102: add_language_to_episodeFiles_history_and_blacklist migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027161s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|103: fix_metadata_file_extensions migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|fix_metadata_file_extensions|Starting migration of Log DB to 103
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (103, '2026-08-30T17:28:12', 'fix_metadata_file_extensions')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|103: fix_metadata_file_extensions migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0040629s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|104: remove_kickass migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|remove_kickass|Starting migration of Log DB to 104
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (104, '2026-08-30T17:28:12', 'remove_kickass')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|104: remove_kickass migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028275s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|105: rename_torrent_downloadstation migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|rename_torrent_downloadstation|Starting migration of Log DB to 105
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (105, '2026-08-30T17:28:12', 'rename_torrent_downloadstation')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|105: rename_torrent_downloadstation migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028768s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|106: update_btn_url migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|update_btn_url|Starting migration of Log DB to 106
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (106, '2026-08-30T17:28:12', 'update_btn_url')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|106: update_btn_url migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.003283s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|107: remove_wombles migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|remove_wombles|Starting migration of Log DB to 107
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (107, '2026-08-30T17:28:12', 'remove_wombles')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|107: remove_wombles migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0036749s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|108: fix_extra_file_extension migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|fix_extra_file_extension|Starting migration of Log DB to 108
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (108, '2026-08-30T17:28:12', 'fix_extra_file_extension')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|108: fix_extra_file_extension migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0035304s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|109: import_extra_files migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|import_extra_files|Starting migration of Log DB to 109
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (109, '2026-08-30T17:28:12', 'import_extra_files')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|109: import_extra_files migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0046057s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|110: fix_extra_files_config migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|fix_extra_files_config|Starting migration of Log DB to 110
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (110, '2026-08-30T17:28:12', 'fix_extra_files_config')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|110: fix_extra_files_config migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0085352s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|111: create_language_profiles migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|create_language_profiles|Starting migration of Log DB to 111
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (111, '2026-08-30T17:28:12', 'create_language_profiles')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|111: create_language_profiles migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025564s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|112: added_regex_to_scenemapping migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|added_regex_to_scenemapping|Starting migration of Log DB to 112
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (112, '2026-08-30T17:28:12', 'added_regex_to_scenemapping')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|112: added_regex_to_scenemapping migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0040897s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|113: consolidate_indexer_baseurl migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|consolidate_indexer_baseurl|Starting migration of Log DB to 113
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (113, '2026-08-30T17:28:12', 'consolidate_indexer_baseurl')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|113: consolidate_indexer_baseurl migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029778s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|114: rename_indexer_status_id migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|rename_indexer_status_id|Starting migration of Log DB to 114
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (114, '2026-08-30T17:28:12', 'rename_indexer_status_id')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|114: rename_indexer_status_id migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025531s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|115: add_downloadclient_status migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|add_downloadclient_status|Starting migration of Log DB to 115
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (115, '2026-08-30T17:28:12', 'add_downloadclient_status')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|115: add_downloadclient_status migrated
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0030224s
2026-08-30 19:28:12.5|Info|FluentMigrator.Runner.MigrationRunner|116: disable_nyaa migrating
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.5|Info|disable_nyaa|Starting migration of Log DB to 116
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (116, '2026-08-30T17:28:12', 'disable_nyaa')
2026-08-30 19:28:12.5|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|116: disable_nyaa migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002699s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|117: add_webrip_and_br480_qualites_in_profile migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_webrip_and_br480_qualites_in_profile|Starting migration of Log DB to 117
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (117, '2026-08-30T17:28:12', 'add_webrip_and_br480_qualites_in_profile')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|117: add_webrip_and_br480_qualites_in_profile migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026518s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|118: add_history_eventType_index migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_history_eventType_index|Starting migration of Log DB to 118
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (118, '2026-08-30T17:28:12', 'add_history_eventType_index')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|118: add_history_eventType_index migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0032159s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|119: separate_automatic_and_interactive_searches migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|separate_automatic_and_interactive_searches|Starting migration of Log DB to 119
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (119, '2026-08-30T17:28:12', 'separate_automatic_and_interactive_searches')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|119: separate_automatic_and_interactive_searches migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0039749s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|120: update_series_episodes_history_indexes migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|update_series_episodes_history_indexes|Starting migration of Log DB to 120
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (120, '2026-08-30T17:28:12', 'update_series_episodes_history_indexes')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|120: update_series_episodes_history_indexes migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023821s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|121: update_animetosho_url migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|update_animetosho_url|Starting migration of Log DB to 121
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (121, '2026-08-30T17:28:12', 'update_animetosho_url')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|121: update_animetosho_url migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027258s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|122: add_remux_qualities_in_profile migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_remux_qualities_in_profile|Starting migration of Log DB to 122
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (122, '2026-08-30T17:28:12', 'add_remux_qualities_in_profile')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|122: add_remux_qualities_in_profile migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024444s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|123: add_history_seriesId_index migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_history_seriesId_index|Starting migration of Log DB to 123
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (123, '2026-08-30T17:28:12', 'add_history_seriesId_index')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|123: add_history_seriesId_index migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025897s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|124: remove_media_browser_metadata migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|remove_media_browser_metadata|Starting migration of Log DB to 124
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (124, '2026-08-30T17:28:12', 'remove_media_browser_metadata')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|124: remove_media_browser_metadata migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023069s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|125: remove_notify_my_android_and_pushalot_notifications migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|remove_notify_my_android_and_pushalot_notifications|Starting migration of Log DB to 125
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (125, '2026-08-30T17:28:12', 'remove_notify_my_android_and_pushalot_notifications')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|125: remove_notify_my_android_and_pushalot_notifications migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026647s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|126: add_custom_filters migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_custom_filters|Starting migration of Log DB to 126
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (126, '2026-08-30T17:28:12', 'add_custom_filters')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|126: add_custom_filters migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027212s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|127: rename_restrictions_to_release_profiles migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|rename_restrictions_to_release_profiles|Starting migration of Log DB to 127
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (127, '2026-08-30T17:28:12', 'rename_restrictions_to_release_profiles')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|127: rename_restrictions_to_release_profiles migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023509s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|128: rename_quality_profiles_add_upgrade_allowed migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|rename_quality_profiles_add_upgrade_allowed|Starting migration of Log DB to 128
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (128, '2026-08-30T17:28:12', 'rename_quality_profiles_add_upgrade_allowed')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|128: rename_quality_profiles_add_upgrade_allowed migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0057362s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|129: add_relative_original_path_to_episode_file migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_relative_original_path_to_episode_file|Starting migration of Log DB to 129
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (129, '2026-08-30T17:28:12', 'add_relative_original_path_to_episode_file')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|129: add_relative_original_path_to_episode_file migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002385s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|130: episode_last_searched_time migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|episode_last_searched_time|Starting migration of Log DB to 130
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (130, '2026-08-30T17:28:12', 'episode_last_searched_time')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|130: episode_last_searched_time migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025231s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|131: download_propers_config migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|download_propers_config|Starting migration of Log DB to 131
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (131, '2026-08-30T17:28:12', 'download_propers_config')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|131: download_propers_config migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023531s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|132: add_download_client_priority migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_download_client_priority|Starting migration of Log DB to 132
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (132, '2026-08-30T17:28:12', 'add_download_client_priority')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|132: add_download_client_priority migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024786s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|134: add_specials_folder_format migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_specials_folder_format|Starting migration of Log DB to 134
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (134, '2026-08-30T17:28:12', 'add_specials_folder_format')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|134: add_specials_folder_format migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0021526s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|135: health_issue_notification migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|health_issue_notification|Starting migration of Log DB to 135
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (135, '2026-08-30T17:28:12', 'health_issue_notification')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|135: health_issue_notification migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023764s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|136: add_indexer_and_enabled_to_release_profiles migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_indexer_and_enabled_to_release_profiles|Starting migration of Log DB to 136
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (136, '2026-08-30T17:28:12', 'add_indexer_and_enabled_to_release_profiles')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|136: add_indexer_and_enabled_to_release_profiles migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0022103s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|137: add_airedbefore_to_episodes migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_airedbefore_to_episodes|Starting migration of Log DB to 137
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (137, '2026-08-30T17:28:12', 'add_airedbefore_to_episodes')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|137: add_airedbefore_to_episodes migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0039587s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|138: remove_bitmetv migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|remove_bitmetv|Starting migration of Log DB to 138
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (138, '2026-08-30T17:28:12', 'remove_bitmetv')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|138: remove_bitmetv migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024922s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|139: add_download_history migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_download_history|Starting migration of Log DB to 139
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (139, '2026-08-30T17:28:12', 'add_download_history')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|139: add_download_history migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025424s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|140: remove_chown_and_folderchmod_config_v2 migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|remove_chown_and_folderchmod_config_v2|Starting migration of Log DB to 140
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (140, '2026-08-30T17:28:12', 'remove_chown_and_folderchmod_config_v2')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|140: remove_chown_and_folderchmod_config_v2 migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024238s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|141: add_update_history migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_update_history|Starting migration of Log DB to 141
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|CreateTable UpdateHistory
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE TABLE "UpdateHistory" ("Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Date" DATETIME NOT NULL, "Version" TEXT NOT NULL, "EventType" INTEGER NOT NULL)
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0003671s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|CreateIndex UpdateHistory (Date)
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE INDEX "IX_UpdateHistory_Date" ON "UpdateHistory" ("Date" ASC)
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0001965s
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (141, '2026-08-30T17:28:12', 'add_update_history')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|141: add_update_history migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028633s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|142: import_lists migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|import_lists|Starting migration of Log DB to 142
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (142, '2026-08-30T17:28:12', 'import_lists')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|142: import_lists migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025396s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|143: add_priority_to_indexers migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|add_priority_to_indexers|Starting migration of Log DB to 143
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (143, '2026-08-30T17:28:12', 'add_priority_to_indexers')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|143: add_priority_to_indexers migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0035187s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|144: import_lists_series_type_and_season_folder migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|import_lists_series_type_and_season_folder|Starting migration of Log DB to 144
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (144, '2026-08-30T17:28:12', 'import_lists_series_type_and_season_folder')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|144: import_lists_series_type_and_season_folder migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002285s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|145: remove_growl migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|remove_growl|Starting migration of Log DB to 145
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (145, '2026-08-30T17:28:12', 'remove_growl')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|145: remove_growl migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025015s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|146: cleanup_duplicates_updatehistory migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|cleanup_duplicates_updatehistory|Starting migration of Log DB to 146
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|PerformDBOperation 
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Performing DB Operation
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0011156s
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (146, '2026-08-30T17:28:12', 'cleanup_duplicates_updatehistory')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|146: cleanup_duplicates_updatehistory migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0046117s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|147: swap_filechmod_for_folderchmod migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|swap_filechmod_for_folderchmod|Starting migration of Log DB to 147
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (147, '2026-08-30T17:28:12', 'swap_filechmod_for_folderchmod')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|147: swap_filechmod_for_folderchmod migrated
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028591s
2026-08-30 19:28:12.6|Info|FluentMigrator.Runner.MigrationRunner|148: mediainfo_channels migrating
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.6|Info|mediainfo_channels|Starting migration of Log DB to 148
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (148, '2026-08-30T17:28:12', 'mediainfo_channels')
2026-08-30 19:28:12.6|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|148: mediainfo_channels migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023335s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|149: add_on_delete_to_notifications migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_on_delete_to_notifications|Starting migration of Log DB to 149
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (149, '2026-08-30T17:28:12', 'add_on_delete_to_notifications')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|149: add_on_delete_to_notifications migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024333s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|150: add_scene_mapping_origin migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_scene_mapping_origin|Starting migration of Log DB to 150
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (150, '2026-08-30T17:28:12', 'add_scene_mapping_origin')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|150: add_scene_mapping_origin migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024139s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|151: remove_custom_filter_type migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|remove_custom_filter_type|Starting migration of Log DB to 151
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (151, '2026-08-30T17:28:12', 'remove_custom_filter_type')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|151: remove_custom_filter_type migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027067s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|152: update_btn_url_to_https migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|update_btn_url_to_https|Starting migration of Log DB to 152
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (152, '2026-08-30T17:28:12', 'update_btn_url_to_https')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|152: update_btn_url_to_https migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024218s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|153: add_on_episodefiledelete_for_upgrade migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_on_episodefiledelete_for_upgrade|Starting migration of Log DB to 153
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (153, '2026-08-30T17:28:12', 'add_on_episodefiledelete_for_upgrade')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|153: add_on_episodefiledelete_for_upgrade migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025293s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|154: add_name_release_profile migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_name_release_profile|Starting migration of Log DB to 154
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (154, '2026-08-30T17:28:12', 'add_name_release_profile')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|154: add_name_release_profile migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025591s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|155: add_arabic_and_hindi_languages migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_arabic_and_hindi_languages|Starting migration of Log DB to 155
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (155, '2026-08-30T17:28:12', 'add_arabic_and_hindi_languages')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|155: add_arabic_and_hindi_languages migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023572s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|156: add_bypass_to_delay_profile migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_bypass_to_delay_profile|Starting migration of Log DB to 156
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (156, '2026-08-30T17:28:12', 'add_bypass_to_delay_profile')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|156: add_bypass_to_delay_profile migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025897s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|157: email_multiple_addresses migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|email_multiple_addresses|Starting migration of Log DB to 157
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (157, '2026-08-30T17:28:12', 'email_multiple_addresses')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|157: email_multiple_addresses migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0054393s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|158: cdh_per_downloadclient migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|cdh_per_downloadclient|Starting migration of Log DB to 158
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (158, '2026-08-30T17:28:12', 'cdh_per_downloadclient')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|158: cdh_per_downloadclient migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0030562s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|159: add_indexer_tags migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_indexer_tags|Starting migration of Log DB to 159
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (159, '2026-08-30T17:28:12', 'add_indexer_tags')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|159: add_indexer_tags migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0023593s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|160: rename_blacklist_to_blocklist migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|rename_blacklist_to_blocklist|Starting migration of Log DB to 160
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (160, '2026-08-30T17:28:12', 'rename_blacklist_to_blocklist')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|160: rename_blacklist_to_blocklist migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002624s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|161: remove_plex_hometheatre migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|remove_plex_hometheatre|Starting migration of Log DB to 161
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (161, '2026-08-30T17:28:12', 'remove_plex_hometheatre')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|161: remove_plex_hometheatre migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026679s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|162: release_profile_to_array migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|release_profile_to_array|Starting migration of Log DB to 162
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (162, '2026-08-30T17:28:12', 'release_profile_to_array')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|162: release_profile_to_array migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0030423s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|163: mediainfo_to_ffmpeg migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|mediainfo_to_ffmpeg|Starting migration of Log DB to 163
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (163, '2026-08-30T17:28:12', 'mediainfo_to_ffmpeg')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|163: mediainfo_to_ffmpeg migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0101194s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|164: download_client_per_indexer migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|download_client_per_indexer|Starting migration of Log DB to 164
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (164, '2026-08-30T17:28:12', 'download_client_per_indexer')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|164: download_client_per_indexer migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026089s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|165: add_on_update_to_notifications migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_on_update_to_notifications|Starting migration of Log DB to 165
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (165, '2026-08-30T17:28:12', 'add_on_update_to_notifications')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|165: add_on_update_to_notifications migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002257s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|166: update_series_sort_title migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|update_series_sort_title|Starting migration of Log DB to 166
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (166, '2026-08-30T17:28:12', 'update_series_sort_title')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|166: update_series_sort_title migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026043s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|167: add_tvdbid_to_episode migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_tvdbid_to_episode|Starting migration of Log DB to 167
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (167, '2026-08-30T17:28:12', 'add_tvdbid_to_episode')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|167: add_tvdbid_to_episode migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025204s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|168: add_additional_info_to_pending_releases migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_additional_info_to_pending_releases|Starting migration of Log DB to 168
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (168, '2026-08-30T17:28:12', 'add_additional_info_to_pending_releases')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|168: add_additional_info_to_pending_releases migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0033303s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|169: add_malayalam_and_ukrainian_languages migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_malayalam_and_ukrainian_languages|Starting migration of Log DB to 169
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (169, '2026-08-30T17:28:12', 'add_malayalam_and_ukrainian_languages')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|169: add_malayalam_and_ukrainian_languages migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0034672s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|170: add_language_tags_to_subtitle_files migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_language_tags_to_subtitle_files|Starting migration of Log DB to 170
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (170, '2026-08-30T17:28:12', 'add_language_tags_to_subtitle_files')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|170: add_language_tags_to_subtitle_files migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027386s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|171: add_custom_formats migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_custom_formats|Starting migration of Log DB to 171
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (171, '2026-08-30T17:28:12', 'add_custom_formats')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|171: add_custom_formats migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.005714s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|172: add_SeasonSearchMaximumSingleEpisodeAge_to_indexers migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_SeasonSearchMaximumSingleEpisodeAge_to_indexers|Starting migration of Log DB to 172
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (172, '2026-08-30T17:28:12', 'add_SeasonSearchMaximumSingleEpisodeAge_to_indexers')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|172: add_SeasonSearchMaximumSingleEpisodeAge_to_indexers migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028714s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|173: remove_omg migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|remove_omg|Starting migration of Log DB to 173
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (173, '2026-08-30T17:28:12', 'remove_omg')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|173: remove_omg migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002647s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|174: add_salt_to_users migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|add_salt_to_users|Starting migration of Log DB to 174
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (174, '2026-08-30T17:28:12', 'add_salt_to_users')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|174: add_salt_to_users migrated
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002934s
2026-08-30 19:28:12.7|Info|FluentMigrator.Runner.MigrationRunner|175: language_profiles_to_custom_formats migrating
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.7|Info|language_profiles_to_custom_formats|Starting migration of Log DB to 175
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (175, '2026-08-30T17:28:12', 'language_profiles_to_custom_formats')
2026-08-30 19:28:12.7|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|175: language_profiles_to_custom_formats migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0034107s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|176: original_language migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|original_language|Starting migration of Log DB to 176
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (176, '2026-08-30T17:28:12', 'original_language')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|176: original_language migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0070395s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|177: add_on_manual_interaction_required_to_notifications migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_on_manual_interaction_required_to_notifications|Starting migration of Log DB to 177
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (177, '2026-08-30T17:28:12', 'add_on_manual_interaction_required_to_notifications')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|177: add_on_manual_interaction_required_to_notifications migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029029s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|178: list_sync_time migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|list_sync_time|Starting migration of Log DB to 178
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (178, '2026-08-30T17:28:12', 'list_sync_time')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|178: list_sync_time migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028039s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|179: add_auto_tagging migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_auto_tagging|Starting migration of Log DB to 179
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (179, '2026-08-30T17:28:12', 'add_auto_tagging')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|179: add_auto_tagging migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0031777s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|180: task_duration migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|task_duration|Starting migration of Log DB to 180
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (180, '2026-08-30T17:28:12', 'task_duration')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|180: task_duration migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0031746s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|181: quality_definition_preferred_size migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|quality_definition_preferred_size|Starting migration of Log DB to 181
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (181, '2026-08-30T17:28:12', 'quality_definition_preferred_size')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|181: quality_definition_preferred_size migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0032154s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|182: add_custom_format_score_bypass_to_delay_profile migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_custom_format_score_bypass_to_delay_profile|Starting migration of Log DB to 182
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (182, '2026-08-30T17:28:12', 'add_custom_format_score_bypass_to_delay_profile')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|182: add_custom_format_score_bypass_to_delay_profile migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.002866s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|183: update_images_remote_url migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|update_images_remote_url|Starting migration of Log DB to 183
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (183, '2026-08-30T17:28:12', 'update_images_remote_url')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|183: update_images_remote_url migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025436s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|184: remove_invalid_roksbox_metadata_images migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|remove_invalid_roksbox_metadata_images|Starting migration of Log DB to 184
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (184, '2026-08-30T17:28:12', 'remove_invalid_roksbox_metadata_images')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|184: remove_invalid_roksbox_metadata_images migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0034336s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|185: add_episode_runtime migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_episode_runtime|Starting migration of Log DB to 185
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (185, '2026-08-30T17:28:12', 'add_episode_runtime')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|185: add_episode_runtime migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0036808s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|186: add_result_to_commands migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_result_to_commands|Starting migration of Log DB to 186
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (186, '2026-08-30T17:28:12', 'add_result_to_commands')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|186: add_result_to_commands migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025543s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|187: add_on_series_add_to_notifications migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_on_series_add_to_notifications|Starting migration of Log DB to 187
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (187, '2026-08-30T17:28:12', 'add_on_series_add_to_notifications')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|187: add_on_series_add_to_notifications migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0034335s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|188: postgres_update_timestamp_columns_to_with_timezone migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|postgres_update_timestamp_columns_to_with_timezone|Starting migration of Log DB to 188
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|AlterTable Logs
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 2E-06s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|AlterColumn Logs Time DateTimeOffset
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE TABLE "Logs_temp" ("Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Message" TEXT NOT NULL, "Time" DATETIME NOT NULL, "Logger" TEXT NOT NULL, "Exception" TEXT, "ExceptionType" TEXT, "Level" TEXT NOT NULL)
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "Logs_temp" ("Id", "Message", "Time", "Logger", "Exception", "ExceptionType", "Level") SELECT "Id", "Message", "Time", "Logger", "Exception", "ExceptionType", "Level" FROM "Logs"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|DROP TABLE "Logs"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|ALTER TABLE "Logs_temp" RENAME TO "Logs"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE INDEX "IX_Logs_Time" ON "Logs" ("Time" ASC)
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0020885s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|AlterTable UpdateHistory
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 1.5E-06s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|AlterColumn UpdateHistory Date DateTimeOffset
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE TABLE "UpdateHistory_temp" ("Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Date" DATETIME NOT NULL, "Version" TEXT NOT NULL, "EventType" INTEGER NOT NULL)
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "UpdateHistory_temp" ("Id", "Date", "Version", "EventType") SELECT "Id", "Date", "Version", "EventType" FROM "UpdateHistory"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|DROP TABLE "UpdateHistory"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|ALTER TABLE "UpdateHistory_temp" RENAME TO "UpdateHistory"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE INDEX "IX_UpdateHistory_Date" ON "UpdateHistory" ("Date" ASC)
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0019922s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|AlterTable VersionInfo
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 1.5E-06s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|AlterColumn VersionInfo AppliedOn DateTimeOffset
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE TABLE "VersionInfo_temp" ("Version" INTEGER NOT NULL, "AppliedOn" DATETIME, "Description" TEXT)
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo_temp" ("Version", "AppliedOn", "Description") SELECT "Version", "AppliedOn", "Description" FROM "VersionInfo"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|DROP TABLE "VersionInfo"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|ALTER TABLE "VersionInfo_temp" RENAME TO "VersionInfo"
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|CREATE UNIQUE INDEX "UC_Version" ON "VersionInfo" ("Version" ASC)
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0018269s
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (188, '2026-08-30T17:28:12', 'postgres_update_timestamp_columns_to_with_timezone')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|188: postgres_update_timestamp_columns_to_with_timezone migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0050268s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|189: add_colon_replacement_to_naming_config migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_colon_replacement_to_naming_config|Starting migration of Log DB to 189
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (189, '2026-08-30T17:28:12', 'add_colon_replacement_to_naming_config')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|189: add_colon_replacement_to_naming_config migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027775s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|190: health_restored_notification migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|health_restored_notification|Starting migration of Log DB to 190
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (190, '2026-08-30T17:28:12', 'health_restored_notification')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|190: health_restored_notification migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028401s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|191: add_download_client_tags migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_download_client_tags|Starting migration of Log DB to 191
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (191, '2026-08-30T17:28:12', 'add_download_client_tags')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|191: add_download_client_tags migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0066323s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|192: import_exclusion_type migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|import_exclusion_type|Starting migration of Log DB to 192
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (192, '2026-08-30T17:28:12', 'import_exclusion_type')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|192: import_exclusion_type migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028362s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|193: add_import_list_items migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_import_list_items|Starting migration of Log DB to 193
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (193, '2026-08-30T17:28:12', 'add_import_list_items')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|193: add_import_list_items migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028256s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|194: add_notification_status migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_notification_status|Starting migration of Log DB to 194
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (194, '2026-08-30T17:28:12', 'add_notification_status')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|194: add_notification_status migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024385s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|195: parse_language_tags_from_existing_subtitle_files migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|parse_language_tags_from_existing_subtitle_files|Starting migration of Log DB to 195
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (195, '2026-08-30T17:28:12', 'parse_language_tags_from_existing_subtitle_files')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|195: parse_language_tags_from_existing_subtitle_files migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026888s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|196: add_finale_type migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|add_finale_type|Starting migration of Log DB to 196
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (196, '2026-08-30T17:28:12', 'add_finale_type')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|196: add_finale_type migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025751s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|197: list_add_missing_search migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|list_add_missing_search|Starting migration of Log DB to 197
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (197, '2026-08-30T17:28:12', 'list_add_missing_search')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|197: list_add_missing_search migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026758s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|198: parse_title_from_existing_subtitle_files migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|parse_title_from_existing_subtitle_files|Starting migration of Log DB to 198
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (198, '2026-08-30T17:28:12', 'parse_title_from_existing_subtitle_files')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|198: parse_title_from_existing_subtitle_files migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025012s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|199: series_last_aired migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|series_last_aired|Starting migration of Log DB to 199
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (199, '2026-08-30T17:28:12', 'series_last_aired')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|199: series_last_aired migrated
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029991s
2026-08-30 19:28:12.8|Info|FluentMigrator.Runner.MigrationRunner|200: AddNewItemMonitorType migrating
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.8|Info|AddNewItemMonitorType|Starting migration of Log DB to 200
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (200, '2026-08-30T17:28:12', 'AddNewItemMonitorType')
2026-08-30 19:28:12.8|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|200: AddNewItemMonitorType migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0027015s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|201: email_encryption migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|email_encryption|Starting migration of Log DB to 201
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (201, '2026-08-30T17:28:12', 'email_encryption')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|201: email_encryption migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0034736s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|202: add_indexer_flags migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_indexer_flags|Starting migration of Log DB to 202
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (202, '2026-08-30T17:28:12', 'add_indexer_flags')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|202: add_indexer_flags migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0045065s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|203: release_type migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|release_type|Starting migration of Log DB to 203
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (203, '2026-08-30T17:28:12', 'release_type')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|203: release_type migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0031172s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|204: add_add_release_hash migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_add_release_hash|Starting migration of Log DB to 204
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (204, '2026-08-30T17:28:12', 'add_add_release_hash')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|204: add_add_release_hash migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028012s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|205: rename_season_pack_spec migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|rename_season_pack_spec|Starting migration of Log DB to 205
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (205, '2026-08-30T17:28:12', 'rename_season_pack_spec')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|205: rename_season_pack_spec migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026465s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|206: add_tmdbid migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_tmdbid|Starting migration of Log DB to 206
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (206, '2026-08-30T17:28:12', 'add_tmdbid')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|206: add_tmdbid migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0032685s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|209: add_on_import_complete_to_notifications migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_on_import_complete_to_notifications|Starting migration of Log DB to 209
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (209, '2026-08-30T17:28:12', 'add_on_import_complete_to_notifications')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|209: add_on_import_complete_to_notifications migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025775s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|210: add_monitored_seasons_filter migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_monitored_seasons_filter|Starting migration of Log DB to 210
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (210, '2026-08-30T17:28:12', 'add_monitored_seasons_filter')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|210: add_monitored_seasons_filter migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026733s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|211: add_custom_colon_replacement_to_naming_config migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_custom_colon_replacement_to_naming_config|Starting migration of Log DB to 211
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (211, '2026-08-30T17:28:12', 'add_custom_colon_replacement_to_naming_config')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|211: add_custom_colon_replacement_to_naming_config migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0025967s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|212: add_minium_upgrade_format_score_to_quality_profiles migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_minium_upgrade_format_score_to_quality_profiles|Starting migration of Log DB to 212
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (212, '2026-08-30T17:28:12', 'add_minium_upgrade_format_score_to_quality_profiles')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|212: add_minium_upgrade_format_score_to_quality_profiles migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0028627s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|214: add_blurary576p_quality_in_profiles migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_blurary576p_quality_in_profiles|Starting migration of Log DB to 214
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (214, '2026-08-30T17:28:12', 'add_blurary576p_quality_in_profiles')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|214: add_blurary576p_quality_in_profiles migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0029848s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|215: add_blurary576p_quality_in_profiles_with_grouped_blurary480p migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_blurary576p_quality_in_profiles_with_grouped_blurary480p|Starting migration of Log DB to 215
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (215, '2026-08-30T17:28:12', 'add_blurary576p_quality_in_profiles_with_grouped_blurary480p')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|215: add_blurary576p_quality_in_profiles_with_grouped_blurary480p migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0024653s
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|217: add_mal_and_anilist_ids migrating
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Beginning Transaction
2026-08-30 19:28:12.9|Info|add_mal_and_anilist_ids|Starting migration of Log DB to 217
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|INSERT INTO "VersionInfo" ("Version", "AppliedOn", "Description") VALUES (217, '2026-08-30T17:28:12', 'add_mal_and_anilist_ids')
2026-08-30 19:28:12.9|Info|NzbDrone.Core.Datastore.Migration.Framework.NzbDroneSQLiteProcessor|Committing Transaction
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|217: add_mal_and_anilist_ids migrated
2026-08-30 19:28:12.9|Info|FluentMigrator.Runner.MigrationRunner|=> 0.0026366s
2026-08-30 19:28:12.9|Debug|MigrationController|Took: 00:00:00.8153367
2026-08-30 19:28:13.0|Info|Microsoft.Hosting.Lifetime|Now listening on: http://[::]:8989
2026-08-30 19:28:13.0|Info|UpdaterConfigProvider|Update mechanism BuiltIn not supported in the current configuration, changing to Docker.
2026-08-30 19:28:13.1|Debug|QualityDefinitionService|Setting up default quality config
2026-08-30 19:28:13.1|Info|QualityProfileService|Setting up default quality profiles
2026-08-30 19:28:13.2|Debug|NotificationFactory|Initializing Providers. Count 25
2026-08-30 19:28:13.2|Debug|IndexerFactory|Initializing Providers. Count 10
2026-08-30 19:28:13.2|Debug|ImportListFactory|Initializing Providers. Count 11
2026-08-30 19:28:13.2|Debug|MetadataFactory|Initializing Providers. Count 5
2026-08-30 19:28:13.2|Debug|DownloadClientFactory|Initializing Providers. Count 18
2026-08-30 19:28:13.2|Info|Microsoft.Hosting.Lifetime|Application started. Press Ctrl+C to shut down.
2026-08-30 19:28:13.2|Info|Microsoft.Hosting.Lifetime|Hosting environment: Production
2026-08-30 19:28:13.2|Info|Microsoft.Hosting.Lifetime|Content root path: /app/sonarr/bin
2026-08-30 19:28:13.4|Info|ManagedHttpDispatcher|IPv4 is available: True, IPv6 will be disabled
2026-08-30 19:28:14.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was not authenticated.
2026-08-30 19:33:13.3|Debug|ImportListSyncService|No import lists with automatic add enabled
2026-08-30 19:33:46.0|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.1|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.1|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.1|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.1|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.2|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.2|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.2|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.2|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.2|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.2|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.2|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Api|[GET] /api/v3/localization/language: 200.OK (13 ms)
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Api|[GET] /api/v3/tag: 200.OK (10 ms)
2026-08-30 19:33:46.4|Debug|Api|[GET] /api/v3/customFilter: 200.OK (11 ms)
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Api|[GET] /api/v3/language: 200.OK (9 ms)
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (16 ms)
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Api|[GET] /api/v3/config/ui: 200.OK (18 ms)
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.4|Debug|Api|[GET] /api/v3/localization: 200.OK (7 ms)
2026-08-30 19:33:46.4|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (42 ms)
2026-08-30 19:33:46.4|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.5|Debug|Api|[GET] /api/v3/series: 200.OK (50 ms)
2026-08-30 19:33:46.5|Debug|Api|[GET] /api/v3/importlist: 200.OK (43 ms)
2026-08-30 19:33:46.5|Debug|Api|[GET] /api/v3/system/status: 200.OK (42 ms)
2026-08-30 19:33:46.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:33:46.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.6|Debug|Api|[GET] /api/v3/queue/status: 200.OK (3 ms)
2026-08-30 19:33:46.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:46.6|Debug|Api|[GET] /api/v3/series: 200.OK (4 ms)
2026-08-30 19:33:46.6|Debug|Api|[GET] /api/v3/health: 200.OK (10 ms)
2026-08-30 19:33:46.6|Debug|Sonarr.Http.Authentication.NoAuthenticationHandler|AuthenticationScheme: None was successfully authenticated.
2026-08-30 19:33:46.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:33:46.6|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (36 ms)
2026-08-30 19:33:46.6|Debug|Api|[GET] /api/v3/config/host: 200.OK (36 ms)
2026-08-30 19:33:58.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:58.7|Debug|Api|[PUT] /api/v3/config/host: 202.Accepted (71 ms)
2026-08-30 19:33:58.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:33:58.8|Debug|Api|[GET] /api/v3/system/status: 200.OK (2 ms)
2026-08-30 19:34:00.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:00.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:00.6|Debug|Api|[GET] /api/v3/health: 200.OK (1 ms)
2026-08-30 19:34:00.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:00.6|Debug|Api|[GET] /api/v3/system/status: 200.OK (1 ms)
2026-08-30 19:34:00.7|Debug|Api|[GET] /api/v3/diskspace: 200.OK (38 ms)
2026-08-30 19:34:03.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:03.1|Debug|Api|[GET] /api/v3/config/host: 200.OK (1 ms)
2026-08-30 19:34:04.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:04.0|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:34:23.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:23.3|Debug|Api|[GET] /api/v3/indexer/schema: 200.OK (93 ms)
2026-08-30 19:34:23.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:24.5|Debug|Newznab|Downloading Feed http://172.20.115.225:9696/0/api?t=tvsearch&cat=5000,5010,5020,5030,5040,5045,5050,5090,5070&extended=1&apikey=(removed)&offset=0&limit=100
2026-08-30 19:34:25.5|Debug|Api|[POST] /api/v3/indexer/test: 200.OK (2236 ms)
2026-08-30 19:34:29.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:29.2|Debug|Newznab|Downloading Feed http://172.20.115.225:9696/0/api?t=tvsearch&cat=5000,5010,5020,5030,5040,5045,5050,5090,5070&extended=1&apikey=(removed)&offset=0&limit=100
2026-08-30 19:34:30.3|Debug|Api|[POST] /api/v3/indexer/test: 200.OK (1105 ms)
2026-08-30 19:34:30.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:30.3|Debug|Api|[GET] /api/v3/indexer: 200.OK (1 ms)
2026-08-30 19:34:30.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:31.4|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100
2026-08-30 19:34:32.7|Debug|Api|[POST] /api/v3/indexer: 201.Created (2447 ms)
2026-08-30 19:34:32.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:33.8|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050,5070&extended=1&apikey=(removed)&offset=0&limit=100
2026-08-30 19:34:35.2|Debug|Api|[POST] /api/v3/indexer: 201.Created (2418 ms)
2026-08-30 19:34:37.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:34:37.8|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:35:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:13.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (2 ms)
2026-08-30 19:35:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:13.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:35:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (26 ms)
2026-08-30 19:35:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (19 ms)
2026-08-30 19:35:38.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:38.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:38.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:38.4|Debug|Api|[GET] /api/v3/config/downloadclient: 200.OK (2 ms)
2026-08-30 19:35:38.4|Debug|Api|[GET] /api/v3/downloadclient: 200.OK (4 ms)
2026-08-30 19:35:38.4|Debug|Api|[GET] /api/v3/remotepathmapping: 200.OK (5 ms)
2026-08-30 19:35:39.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:39.0|Debug|Api|[GET] /api/v3/downloadclient/schema: 200.OK (23 ms)
2026-08-30 19:35:55.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:55.1|Debug|QBittorrentProxyV2|qBittorrent authentication succeeded.
2026-08-30 19:35:55.1|Debug|Api|[POST] /api/v3/downloadclient/test: 200.OK (48 ms)
2026-08-30 19:35:55.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:35:55.9|Debug|Api|[POST] /api/v3/downloadclient: 201.Created (24 ms)
2026-08-30 19:36:00.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:36:00.9|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:36:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:36:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:36:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:36:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:36:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:36:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:36:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:36:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:38:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:38:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:38:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:38:13.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:38:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:38:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:38:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:38:13.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:38:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:38:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:38:43.3|Debug|ImportListSyncService|No import lists with automatic add enabled
2026-08-30 19:38:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:38:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:39:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:39:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:39:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:39:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:39:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:39:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:39:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:39:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:41:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:41:13.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:41:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:41:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:41:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:41:13.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:41:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:41:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:42:32.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:32.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:32.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:32.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:32.3|Debug|Api|[GET] /api/v3/rootFolder: 200.OK (5 ms)
2026-08-30 19:42:32.3|Debug|Api|[GET] /api/v3/config/mediamanagement: 200.OK (28 ms)
2026-08-30 19:42:32.3|Debug|Api|[GET] /api/v3/config/naming: 200.OK (26 ms)
2026-08-30 19:42:32.4|Debug|Parser|Parsing string 'The.Series.Title's!.S01E01.1080p.WEBDL.x264-EVOLVE'
2026-08-30 19:42:32.8|Debug|Parser|Episode Parsed. The Series Title's! - S01E01 
2026-08-30 19:42:32.8|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:42:32.8|Debug|QualityParser|Trying to parse quality for 'The.Series.Title's!.S01E01.1080p.WEBDL.x264-EVOLVE'
2026-08-30 19:42:32.9|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:42:32.9|Debug|Parser|Release Group parsed: EVOLVE
2026-08-30 19:42:32.9|Debug|Parser|Parsing string 'The.Series.Title's!.S01E01-E03.1080p.WEBDL.x264-EVOLVE'
2026-08-30 19:42:32.9|Debug|Parser|Episode Parsed. The Series Title's! - S01E01-02-03 
2026-08-30 19:42:32.9|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:42:32.9|Debug|QualityParser|Trying to parse quality for 'The.Series.Title's!.S01E01-E03.1080p.WEBDL.x264-EVOLVE'
2026-08-30 19:42:32.9|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:42:32.9|Debug|Parser|Release Group parsed: EVOLVE
2026-08-30 19:42:32.9|Debug|Parser|Parsing string 'The.Series.Title's!.2013.10.30.1080p.WEBDL.x264-EVOLVE'
2026-08-30 19:42:33.1|Debug|Parser|Episode Parsed. The Series Title's - 2013-10-30 
2026-08-30 19:42:33.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:42:33.1|Debug|QualityParser|Trying to parse quality for 'The.Series.Title's!.2013.10.30.1080p.WEBDL.x264-EVOLVE'
2026-08-30 19:42:33.1|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:42:33.1|Debug|Parser|Release Group parsed: EVOLVE
2026-08-30 19:42:33.1|Debug|Parser|Parsing string '[RlsGroup] The Series Title's! - 001 [1080P]'
2026-08-30 19:42:33.2|Debug|Parser|Episode Parsed. The Series Title's! - 001 
2026-08-30 19:42:33.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:42:33.2|Debug|QualityParser|Trying to parse quality for '[RlsGroup] The Series Title's! - 001 [1080P]'
2026-08-30 19:42:33.2|Debug|Parser|Quality parsed: HDTV-1080p v1
2026-08-30 19:42:33.2|Debug|Parser|Release Group parsed: RlsGroup
2026-08-30 19:42:33.2|Debug|Parser|Parsing string '[RlsGroup] The Series Title's! - 001 - 103 [1080p]'
2026-08-30 19:42:33.2|Debug|Parser|Episode Parsed. The Series Title's! - 001 
2026-08-30 19:42:33.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:42:33.2|Debug|QualityParser|Trying to parse quality for '[RlsGroup] The Series Title's! - 001 - 103 [1080p]'
2026-08-30 19:42:33.2|Debug|Parser|Quality parsed: HDTV-1080p v1
2026-08-30 19:42:33.2|Debug|Parser|Release Group parsed: RlsGroup
2026-08-30 19:42:33.2|Debug|Api|[GET] /api/v3/config/naming/examples: 200.OK (880 ms)
2026-08-30 19:42:34.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:34.7|Debug|Api|[GET] /api/v3/filesystem?path=&allowFoldersWithoutTrailingSlashes=true&includeFiles=true: 200.OK (12 ms)
2026-08-30 19:42:36.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:36.5|Debug|Api|[GET] /api/v3/filesystem?path=%2Ftv%2F&allowFoldersWithoutTrailingSlashes=true&includeFiles=true: 200.OK (1 ms)
2026-08-30 19:42:37.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:37.6|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:42:37.6|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:42:37.6|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:42:37.6|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:42:37.6|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:42:37.6|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:42:37.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:37.6|Debug|Api|[POST] /api/v3/rootFolder: 201.Created (27 ms)
2026-08-30 19:42:37.6|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:42:37.6|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:42:37.6|Debug|Api|[GET] /api/v3/rootFolder: 200.OK (2 ms)
2026-08-30 19:42:42.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:42.6|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:42:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:42:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:42:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:42:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:42:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:43:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:43:13.3|Info|RssSyncService|Starting RSS Sync
2026-08-30 19:43:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:43:13.3|Debug|FetchAndParseRssService|Available indexers 2
2026-08-30 19:43:13.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100
2026-08-30 19:43:13.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050,5070&extended=1&apikey=(removed)&offset=0&limit=100
2026-08-30 19:43:13.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:43:13.7|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:43:15.9|Debug|FetchAndParseRssService|Found 40 reports
2026-08-30 19:43:15.9|Info|DownloadDecisionMaker|Processing 40 releases
2026-08-30 19:43:15.9|Debug|DownloadDecisionMaker|Processing release 'Average.Joe.S02e03.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:15.9|Debug|Parser|Parsing string 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:43:15.9|Debug|Parser|Episode Parsed. Average Joe - S02E03 
2026-08-30 19:43:15.9|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:15.9|Debug|QualityParser|Trying to parse quality for 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:43:15.9|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:15.9|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Average Joe
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Average.Joe.S02e03.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Trying - Season 05 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: FRQC
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Trying
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Trying - S05E08 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Trying
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Women In Blue - S02E03 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Women In Blue
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Ted Lasso
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Chicago.Fire.S14e01.Web.H264' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Chicago.Fire.S14e01.Web.H264'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Chicago Fire - S14E01 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Chicago.Fire.S14e01.Web.H264'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Chicago Fire
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Chicago.Fire.S14e01.Web.H264' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Furious.S01e07.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Furious.S01e07.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Furious - S01E07 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Furious.S01e07.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Furious
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Furious.S01e07.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Furious.S01e06.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Furious.S01e06.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Furious - S01E06 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Furious.S01e06.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Furious
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Furious.S01e06.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. The Walking Dead Dead City - S03E05 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series The Walking Dead Dead City
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. The Walking Dead Dead City - S03E04 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series The Walking Dead Dead City
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Lanterns - S01E02 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Mtlqc
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Lanterns
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Lanterns - S01E01 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Lanterns
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Gomorra.Origins.S01e02.Web.X264' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Gomorra.Origins.S01e02.Web.X264'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Gomorra Origins - S01E02 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Gomorra.Origins.S01e02.Web.X264'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Gomorra Origins
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Gomorra.Origins.S01e02.Web.X264' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Gomorra.Origins.S01e01.Web.X264' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Gomorra.Origins.S01e01.Web.X264'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Gomorra Origins - S01E01 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Gomorra.Origins.S01e01.Web.X264'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Gomorra Origins
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Gomorra.Origins.S01e01.Web.X264' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Stuart.Fails.To.Save.The.Universe.V.F.S01e06.Vostfr.Web.Ac3.5.1.H264' from 'Torrent9 (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Stuart.Fails.To.Save.The.Universe.V.F.S01e06.Vostfr.Web.Ac3.5.1.H264'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Stuart Fails To Save The Universe V F - S01E06 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Stuart.Fails.To.Save.The.Universe.V.F.S01e06.Vostfr.Web.Ac3.5.1.H264'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Stuart Fails To Save The Universe V F
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Stuart.Fails.To.Save.The.Universe.V.F.S01e06.Vostfr.Web.Ac3.5.1.H264' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Tip.Toe.S01e05.Final.Vff.Web.Eac3.5.1.H264' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Tip.Toe.S01e05.Final.Vff.Web.Eac3.5.1.H264'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Tip Toe - S01E05 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Tip.Toe.S01e05.Final.Vff.Web.Eac3.5.1.H264'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Tip Toe
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Tip.Toe.S01e05.Final.Vff.Web.Eac3.5.1.H264' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Star.Trek.Strange.New.Worlds.S04e06.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Star.Trek.Strange.New.Worlds.S04e06.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Star Trek Strange New Worlds - S04E06 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Star.Trek.Strange.New.Worlds.S04e06.Web.H264-Gl0p'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Star Trek Strange New Worlds
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Star.Trek.Strange.New.Worlds.S04e06.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'The.Shards.S01e07.Homecoming.Part.Two.Dsnp.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'The.Shards.S01e07.Homecoming.Part.Two.Dsnp.Web.H264-Byor'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. The Shards - S01E07 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'The.Shards.S01e07.Homecoming.Part.Two.Dsnp.Web.H264-Byor'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series The Shards
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'The.Shards.S01e07.Homecoming.Part.Two.Dsnp.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'The.Shards.S01e06.Homecoming.Part.One.Dsnp.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'The.Shards.S01e06.Homecoming.Part.One.Dsnp.Web.H264-Byor'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. The Shards - S01E06 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'The.Shards.S01e06.Homecoming.Part.One.Dsnp.Web.H264-Byor'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series The Shards
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'The.Shards.S01e06.Homecoming.Part.One.Dsnp.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Special Ops Lioness - S03E05 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Special Ops Lioness
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:43:16.0|Debug|Parser|Episode Parsed. Special Ops Lioness - S03E05 
2026-08-30 19:43:16.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.0|Debug|QualityParser|Trying to parse quality for 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:43:16.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.0|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.0|Debug|ParsingService|No matching series Special Ops Lioness
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Release 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.0|Debug|DownloadDecisionMaker|Processing release 'The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.0|Debug|Parser|Parsing string 'The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag'
2026-08-30 19:43:16.2|Debug|Parser|Unable to parse The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag'
2026-08-30 19:43:16.2|Debug|Parser|Unable to parse The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'WWE.SmackDown.2026.08.28.NF.VOD.1080p.WEB.h265-HEEL' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'WWE.SmackDown.2026.08.28.NF.VOD.1080p.WEB.h265-HEEL'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. WWE SmackDown - 2026-08-28 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'WWE.SmackDown.2026.08.28.NF.VOD.1080p.WEB.h265-HEEL'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: HEEL
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series WWE SmackDown
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'WWE.SmackDown.2026.08.28.NF.VOD.1080p.WEB.h265-HEEL' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Diarra.From.Detroit.S02e06.Vff.Web.Eac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Diarra.From.Detroit.S02e06.Vff.Web.Eac3.5.1.H264-Frqc'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Diarra From Detroit - S02E06 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Diarra.From.Detroit.S02e06.Vff.Web.Eac3.5.1.H264-Frqc'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Diarra From Detroit
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Diarra.From.Detroit.S02e06.Vff.Web.Eac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Average.Joe.S02e03.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Average Joe - S02E03 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Average Joe
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Average.Joe.S02e03.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Trying - Season 05 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: FRQC
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Trying
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Trying - S05E08 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Trying
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Women In Blue - S02E03 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Women In Blue
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Ted Lasso
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Chicago.Fire.S14e01.Web.H264' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Chicago.Fire.S14e01.Web.H264'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Chicago Fire - S14E01 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Chicago.Fire.S14e01.Web.H264'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Chicago Fire
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Chicago.Fire.S14e01.Web.H264' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'President.Curtis.S01e05.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'President.Curtis.S01e05.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. President Curtis - S01E05 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'President.Curtis.S01e05.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series President Curtis
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'President.Curtis.S01e05.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'President.Curtis.S01e04.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'President.Curtis.S01e04.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. President Curtis - S01E04 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'President.Curtis.S01e04.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series President Curtis
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'President.Curtis.S01e04.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Furious.S01e07.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Furious.S01e07.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Furious - S01E07 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Furious.S01e07.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Furious
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Furious.S01e07.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Furious.S01e06.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Furious.S01e06.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Furious - S01E06 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Furious.S01e06.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Furious
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Furious.S01e06.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. The Walking Dead Dead City - S03E05 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series The Walking Dead Dead City
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. The Walking Dead Dead City - S03E04 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series The Walking Dead Dead City
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Lanterns - S01E02 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Mtlqc
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Lanterns
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Lanterns - S01E01 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: French
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Lanterns
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Gomorra.Origins.S01e02.Web.X264' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Gomorra.Origins.S01e02.Web.X264'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Gomorra Origins - S01E02 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Gomorra.Origins.S01e02.Web.X264'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Gomorra Origins
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Gomorra.Origins.S01e02.Web.X264' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Processing release 'Gomorra.Origins.S01e01.Web.X264' from 'World-torrent (Prowlarr)'
2026-08-30 19:43:16.2|Debug|Parser|Parsing string 'Gomorra.Origins.S01e01.Web.X264'
2026-08-30 19:43:16.2|Debug|Parser|Episode Parsed. Gomorra Origins - S01E01 
2026-08-30 19:43:16.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:43:16.2|Debug|QualityParser|Trying to parse quality for 'Gomorra.Origins.S01e01.Web.X264'
2026-08-30 19:43:16.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:43:16.2|Debug|Parser|Release Group parsed: 
2026-08-30 19:43:16.2|Debug|ParsingService|No matching series Gomorra Origins
2026-08-30 19:43:16.2|Debug|DownloadDecisionMaker|Release 'Gomorra.Origins.S01e01.Web.X264' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:43:16.2|Info|RssSyncService|RSS Sync Completed. Reports found: 40, Reports grabbed: 0
2026-08-30 19:43:16.2|Debug|PendingReleaseService|Removing failed releases from pending
2026-08-30 19:43:16.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:43:16.2|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:43:43.3|Debug|ImportListSyncService|No import lists with automatic add enabled
2026-08-30 19:43:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:43:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:44:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:13.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:44:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:44:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:13.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:44:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:44:13.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:13.6|Debug|Api|[GET] /api/v3/config/host: 200.OK (1 ms)
2026-08-30 19:44:22.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:22.1|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:44:22.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:22.1|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:44:22.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:22.1|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:44:22.1|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:44:22.1|Debug|Api|[GET] /api/v3/rootfolder?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:44:22.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:22.1|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:44:28.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:28.1|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:44:28.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:28.1|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:44:37.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:37.6|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:44:37.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:37.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:37.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:37.6|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:44:37.6|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:44:37.6|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (3 ms)
2026-08-30 19:44:37.6|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:44:37.6|Debug|Api|[GET] /api/v3/rootfolder?apikey=(removed) 200.OK (3 ms)
2026-08-30 19:44:39.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:39.9|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:44:39.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:39.9|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:44:43.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:43.2|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:44:43.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:43.2|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:44:52.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:44:52.2|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:45:05.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:45:05.1|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:45:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:45:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:45:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:45:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:45:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:45:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:45:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:45:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:46:44.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:46:44.3|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:46:49.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:46:49.9|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:46:49.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:46:49.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:46:49.9|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:46:49.9|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:46:49.9|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:46:49.9|Debug|Api|[GET] /api/v3/rootfolder?apikey=(removed) 200.OK (11 ms)
2026-08-30 19:46:55.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:46:55.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:46:55.6|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:46:55.9|Debug|Api|[GET] /api/v3/series/lookup?apikey=(removed)&term=tvdb:383203: 200.OK (407 ms)
2026-08-30 19:46:55.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:46:56.0|Info|AddSeriesService|Adding Series [383203][Ted Lasso] Path: [/tv/Ted Lasso]
2026-08-30 19:46:56.1|Info|SceneMappingService|Updating Scene mappings
2026-08-30 19:46:56.1|Debug|XemProxy|Fetching alternate names
2026-08-30 19:46:56.1|Info|RefreshSeriesService|Updating Ted Lasso
2026-08-30 19:46:56.1|Debug|SeriesService|Tags not updated for 'Ted Lasso'
2026-08-30 19:46:56.1|Info|RefreshEpisodeService|Starting episode info refresh for: [383203][Ted Lasso]
2026-08-30 19:46:56.1|Info|RefreshEpisodeService|Finished episode refresh for series: [383203][Ted Lasso].
2026-08-30 19:46:56.1|Debug|RefreshSeriesService|Finished series refresh for Ted Lasso
2026-08-30 19:46:56.1|Debug|XemProxy|Fetching Series IDs from
2026-08-30 19:46:56.2|Debug|XemService|Scene numbering is not available for Ted Lasso [383203]
2026-08-30 19:46:56.2|Debug|SeriesService|Tags not updated for 'Ted Lasso'
2026-08-30 19:46:56.2|Info|MediaCoverService|Downloading Banner for [383203][Ted Lasso] https://artworks.thetvdb.com/banners/v4/series/383203/banners/60dfad53daf18.jpg
2026-08-30 19:46:56.2|Debug|HttpClient|Downloading [https://artworks.thetvdb.com/banners/v4/series/383203/banners/60dfad53daf18.jpg] to [/config/MediaCover/1/banner.jpg]
2026-08-30 19:46:56.2|Warn|DiskScanService|Series' root folder (/tv) is empty.
2026-08-30 19:46:56.3|Info|SeriesScannedHandler|[Ted Lasso] was recently added, performing post-add actions
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|[Ted Lasso] Setting episode monitored status.
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Unmonitoring Episodes with Files
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Monitoring Episodes without Files
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Unmonitoring all episodes in season 0
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Unmonitoring season 0 because all episodes are not monitored
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Unmonitoring all episodes in season 2
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Unmonitoring season 2 because all episodes are not monitored
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Unmonitoring all episodes in season 3
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Unmonitoring season 3 because all episodes are not monitored
2026-08-30 19:46:56.3|Debug|EpisodeMonitoredService|Unmonitoring all episodes in season 4
2026-08-30 19:46:56.4|Debug|HttpClient|Downloading Completed. took 0s
2026-08-30 19:46:56.4|Info|MediaCoverService|Downloading Poster for [383203][Ted Lasso] https://artworks.thetvdb.com/banners/v4/series/383203/posters/61010b6167190.jpg
2026-08-30 19:46:56.4|Debug|HttpClient|Downloading [https://artworks.thetvdb.com/banners/v4/series/383203/posters/61010b6167190.jpg] to [/config/MediaCover/1/poster.jpg]
2026-08-30 19:46:56.4|Debug|SeriesService|Tags not updated for 'Ted Lasso'
2026-08-30 19:46:56.5|Info|EpisodeSearchService|Performing search for 10 episodes
2026-08-30 19:46:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:46:56.5|Debug|Api|[GET] /api/v3/command: 200.OK (3 ms)
2026-08-30 19:46:56.5|Info|ReleaseSearchService|Searching indexers for [Ted Lasso : S01]. 2 active indexers
2026-08-30 19:46:56.5|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=1
2026-08-30 19:46:56.5|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=1
2026-08-30 19:46:56.5|Debug|HttpClient|Downloading Completed. took 0s
2026-08-30 19:46:56.5|Info|MediaCoverService|Downloading Fanart for [383203][Ted Lasso] https://artworks.thetvdb.com/banners/v4/series/383203/backgrounds/60d5931c1f29c.jpg
2026-08-30 19:46:56.5|Debug|HttpClient|Downloading [https://artworks.thetvdb.com/banners/v4/series/383203/backgrounds/60d5931c1f29c.jpg] to [/config/MediaCover/1/fanart.jpg]
2026-08-30 19:46:56.7|Debug|HttpClient|Downloading Completed. took 0s
2026-08-30 19:46:56.7|Info|MediaCoverService|Downloading Clearlogo for [383203][Ted Lasso] https://artworks.thetvdb.com/banners/v4/series/383203/clearlogo/611c3acf767fe.png
2026-08-30 19:46:56.7|Debug|HttpClient|Downloading [https://artworks.thetvdb.com/banners/v4/series/383203/clearlogo/611c3acf767fe.png] to [/config/MediaCover/1/clearlogo.png]
2026-08-30 19:46:56.7|Debug|HttpClient|Downloading Completed. took 0s
2026-08-30 19:46:56.7|Debug|MediaCoverService|Resizing Banner-70 for [383203][Ted Lasso]
2026-08-30 19:46:56.8|Debug|Api|[POST] /api/v3/series?apikey=(removed) 201.Created (805 ms)
2026-08-30 19:46:56.9|Debug|MediaCoverService|Resizing Banner-35 for [383203][Ted Lasso]
2026-08-30 19:46:56.9|Debug|MediaCoverService|Resizing Poster-500 for [383203][Ted Lasso]
2026-08-30 19:46:56.9|Debug|MediaCoverService|Resizing Poster-250 for [383203][Ted Lasso]
2026-08-30 19:46:56.9|Debug|MediaCoverService|Resizing Fanart-360 for [383203][Ted Lasso]
2026-08-30 19:46:57.0|Debug|MediaCoverService|Resizing Fanart-180 for [383203][Ted Lasso]
2026-08-30 19:46:57.0|Debug|CleanExtraFileService|Cleaning missing metadata files for series: Ted Lasso
2026-08-30 19:46:57.0|Info|MetadataService|Series folder does not exist, skipping metadata image creation
2026-08-30 19:46:58.9|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=1
2026-08-30 19:46:59.2|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=1
2026-08-30 19:47:01.0|Debug|ReleaseSearchService|Total of 16 reports were found for [Ted Lasso : S01] from 2 indexers
2026-08-30 19:47:01.0|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:47:01
2026-08-30 19:47:01.0|Info|DownloadDecisionMaker|Processing 16 releases
2026-08-30 19:47:01.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:47:01.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:47:01.0|Debug|Parser|Languages parsed: French
2026-08-30 19:47:01.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:47:01.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:47:01.0|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:47:01.1|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:47:01.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:47:01.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:47:01.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:47:01.1|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:47:01.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:47:01.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:47:01.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:47:01.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.1|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.1|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:47:01.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:47:01.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:47:01.1|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:47:01.1|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:47:01.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:47:01.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:47:01.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:47:01.1|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:47:01.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:47:01.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:47:01.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:47:01.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.1|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.1|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:47:01.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:47:01.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:47:01.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:47:01.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:47:01.1|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:47:01.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:47:01.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:47:01.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.1|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.1|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:47:01.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:47:01.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:47:01.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:47:01.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:47:01.1|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:47:01.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:47:01.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:47:01.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.1|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.1|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:47:01.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:47:01.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:47:01.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:47:01.2|Debug|Api|[GET] /api/v3/series: 200.OK (3 ms)
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: FW
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso 2020 - Season 03 WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|No episodes in the release are monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 3x1-12, [Permanent] Wrong season, [Permanent] One or more episodes is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - Season 02 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 02 WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|No episodes in the release are monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 2x1-12, [Permanent] Wrong season, [Permanent] One or more episodes is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - Season 01 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' accepted
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|Episode is not monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season, [Permanent] Episode is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'World-torrent (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: FW
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso 2020 - Season 03 WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|No episodes in the release are monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 3x1-12, [Permanent] Wrong season, [Permanent] One or more episodes is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - Season 02 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 02 WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|MonitoredEpisodeSpecification|No episodes in the release are monitored. Rejecting
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 2x1-12, [Permanent] Wrong season, [Permanent] One or more episodes is not monitored
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)'
2026-08-30 19:47:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:47:01.2|Debug|Parser|Episode Parsed. Ted Lasso - Season 01 
2026-08-30 19:47:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:47:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:47:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:47:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:47:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:47:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:47:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:47:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:47:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:47:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:47:01.2|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:47:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:47:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)' accepted
2026-08-30 19:47:01.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:01.2|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:47:03.6|Warn|HttpClient|HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest (124 bytes)
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

2026-08-30 19:47:03.6|Warn|ProcessDownloadDecisions|Couldn't add release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from Indexer World-torrent (Prowlarr) to download queue.

[v4.0.19.2979] NzbDrone.Core.Download.Clients.DownloadClientException: Failed to connect to qBittorrent, check your settings.
 ---> NzbDrone.Common.Http.HttpException: HTTP request failed: [400:BadRequest] [POST] at [http://decypharr:8282/api/v2/torrents/add]
   at NzbDrone.Common.Http.HttpClient.ExecuteAsync(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 119
   at NzbDrone.Common.Http.HttpClient.Execute(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 128
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

   --- End of inner exception stack trace ---
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.AddTorrentFromUrl(String torrentUrl, TorrentSeedConfiguration seedConfiguration, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 159
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrent.AddFromMagnetLink(RemoteEpisode remoteEpisode, String hash, String magnetLink) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrent.cs:line 84
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromMagnetUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String magnetUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 235
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromWebUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String torrentUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 158
   at NzbDrone.Core.Download.TorrentClientBase`1.Download(RemoteEpisode remoteEpisode, IIndexer indexer) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 124
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, IDownloadClient downloadClient) in ./Sonarr.Core/Download/DownloadService.cs:line 98
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/DownloadService.cs:line 63
   at NzbDrone.Core.Download.ProcessDownloadDecisions.ProcessDecisionInternal(DownloadDecision decision, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/ProcessDownloadDecisions.cs:line 204

2026-08-30 19:47:04.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:04.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:04.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:04.4|Debug|Api|[GET] /api/v3/queue/details?seriesId=1: 200.OK (1 ms)
2026-08-30 19:47:04.5|Debug|Api|[GET] /api/v3/episode?seriesId=1: 200.OK (11 ms)
2026-08-30 19:47:04.5|Debug|Api|[GET] /api/v3/episodeFile?seriesId=1: 200.OK (12 ms)
2026-08-30 19:47:05.0|Warn|HttpClient|HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest (124 bytes)
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

2026-08-30 19:47:05.0|Warn|ProcessDownloadDecisions|Couldn't add release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from Indexer Torrent9 (Prowlarr) to download queue.

[v4.0.19.2979] NzbDrone.Core.Download.Clients.DownloadClientException: Failed to connect to qBittorrent, check your settings.
 ---> NzbDrone.Common.Http.HttpException: HTTP request failed: [400:BadRequest] [POST] at [http://decypharr:8282/api/v2/torrents/add]
   at NzbDrone.Common.Http.HttpClient.ExecuteAsync(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 119
   at NzbDrone.Common.Http.HttpClient.Execute(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 128
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

   --- End of inner exception stack trace ---
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.AddTorrentFromUrl(String torrentUrl, TorrentSeedConfiguration seedConfiguration, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 159
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrent.AddFromMagnetLink(RemoteEpisode remoteEpisode, String hash, String magnetLink) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrent.cs:line 84
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromMagnetUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String magnetUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 235
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromWebUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String torrentUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 158
   at NzbDrone.Core.Download.TorrentClientBase`1.Download(RemoteEpisode remoteEpisode, IIndexer indexer) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 124
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, IDownloadClient downloadClient) in ./Sonarr.Core/Download/DownloadService.cs:line 98
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/DownloadService.cs:line 63
   at NzbDrone.Core.Download.ProcessDownloadDecisions.ProcessDecisionInternal(DownloadDecision decision, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/ProcessDownloadDecisions.cs:line 204

2026-08-30 19:47:05.0|Info|EpisodeSearchService|Completed search for 10 episodes. 0 reports downloaded.
2026-08-30 19:47:05.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:05.0|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:47:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:13.3|Debug|Api|[GET] /api/v3/queue/details?seriesId=1: 200.OK (1 ms)
2026-08-30 19:47:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:47:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:47:13.3|Debug|Api|[GET] /api/v3/queue/details?seriesId=1: 200.OK (0 ms)
2026-08-30 19:47:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:48:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:48:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:48:43.3|Debug|ImportListSyncService|No import lists with automatic add enabled
2026-08-30 19:48:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:48:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:48:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:48:43.3|Debug|Api|[GET] /api/v3/queue/details?seriesId=1: 200.OK (1 ms)
2026-08-30 19:48:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:48:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:48:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:48:43.3|Debug|Api|[GET] /api/v3/queue/details?seriesId=1: 200.OK (1 ms)
2026-08-30 19:48:43.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:48:43.4|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:50:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:50:13.3|Debug|Api|[GET] /api/v3/queue/details?seriesId=1: 200.OK (0 ms)
2026-08-30 19:50:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:50:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:50:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:50:13.3|Debug|Api|[GET] /api/v3/queue/details?seriesId=1: 200.OK (1 ms)
2026-08-30 19:50:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:50:13.4|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:51:21.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/localization/language: 200.OK (0 ms)
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/customFilter: 200.OK (1 ms)
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (0 ms)
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/language: 200.OK (1 ms)
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/series: 200.OK (4 ms)
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/tag: 200.OK (1 ms)
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (2 ms)
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/config/ui: 200.OK (1 ms)
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/system/status: 200.OK (1 ms)
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/importlist: 200.OK (1 ms)
2026-08-30 19:51:21.5|Debug|Api|[GET] /api/v3/localization: 200.OK (2 ms)
2026-08-30 19:51:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.6|Debug|Api|[GET] /api/v3/episode?seriesId=1: 200.OK (2 ms)
2026-08-30 19:51:21.6|Debug|Api|[GET] /api/v3/queue/details?seriesId=1: 200.OK (1 ms)
2026-08-30 19:51:21.6|Debug|Api|[GET] /api/v3/episodeFile?seriesId=1: 200.OK (2 ms)
2026-08-30 19:51:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:21.6|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:51:21.6|Debug|Api|[GET] /api/v3/queue/status: 200.OK (1 ms)
2026-08-30 19:51:21.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:23.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:23.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:23.0|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:51:23.0|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:51:24.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/localization/language: 200.OK (0 ms)
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/tag: 200.OK (0 ms)
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/customFilter: 200.OK (1 ms)
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (1 ms)
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/language: 200.OK (0 ms)
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (0 ms)
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/importlist: 200.OK (0 ms)
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/config/ui: 200.OK (0 ms)
2026-08-30 19:51:24.7|Debug|Api|[GET] /api/v3/system/status: 200.OK (0 ms)
2026-08-30 19:51:24.8|Debug|Api|[GET] /api/v3/localization: 200.OK (1 ms)
2026-08-30 19:51:24.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:24.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.8|Debug|Api|[GET] /api/v3/queue/status: 200.OK (0 ms)
2026-08-30 19:51:24.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.8|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:51:24.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:24.8|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:51:24.8|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:51:24.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:25.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:25.3|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:51:42.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/localization/language: 200.OK (0 ms)
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/tag: 200.OK (0 ms)
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/language: 200.OK (0 ms)
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/customFilter: 200.OK (1 ms)
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/importlist: 200.OK (1 ms)
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (0 ms)
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (2 ms)
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/config/ui: 200.OK (1 ms)
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/system/status: 200.OK (0 ms)
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/series: 200.OK (3 ms)
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/localization: 200.OK (1 ms)
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/queue/status: 200.OK (1 ms)
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/series: 200.OK (10 ms)
2026-08-30 19:51:42.9|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (13 ms)
2026-08-30 19:51:42.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:51:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:51:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:43.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:51:43.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:43.3|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:51:43.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:43.4|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:51:44.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:44.8|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:51:44.8|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:51:44.8|Debug|Api|[GET] /api/v3/rootFolder: 200.OK (5 ms)
2026-08-30 19:51:45.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:45.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:45.5|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:51:45.5|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:51:45.5|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:51:45.5|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:51:45.5|Debug|Api|[GET] /api/v3/rootFolder: 200.OK (3 ms)
2026-08-30 19:51:45.5|Debug|Api|[GET] /api/v3/rootFolder: 200.OK (3 ms)
2026-08-30 19:51:46.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:46.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:51:46.1|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:51:46.1|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:52:21.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:21.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/localization/language: 200.OK (0 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/language: 200.OK (0 ms)
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/importlist: 200.OK (2 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (0 ms)
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (2 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/config/ui: 200.OK (0 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/series: 200.OK (4 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/tag: 200.OK (3 ms)
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/customFilter: 200.OK (3 ms)
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/system/status: 200.OK (1 ms)
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/localization: 200.OK (2 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/queue/status: 200.OK (0 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:52:21.6|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:52:21.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:30.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:30.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/localization/language: 200.OK (0 ms)
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/tag: 200.OK (0 ms)
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/customFilter: 200.OK (0 ms)
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/language: 200.OK (0 ms)
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/importlist: 200.OK (1 ms)
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (0 ms)
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/config/ui: 200.OK (0 ms)
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/system/status: 200.OK (0 ms)
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (3 ms)
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/localization: 200.OK (1 ms)
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/series: 200.OK (4 ms)
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/queue/status: 200.OK (1 ms)
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:52:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:52:30.4|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:52:30.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:31.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/localization/language: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/language: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/tag: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/importlist: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (1 ms)
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/customFilter: 200.OK (2 ms)
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/config/ui: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/system/status: 200.OK (1 ms)
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/series: 200.OK (3 ms)
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/localization: 200.OK (2 ms)
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/queue/status: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:52:32.1|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:52:32.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:53:08.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:08.1|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:53:08.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:08.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:08.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:08.1|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:53:08.1|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:53:08.1|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:53:08.1|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:53:08.1|Debug|Api|[GET] /api/v3/rootfolder?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:53:10.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:10.5|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:53:10.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:10.5|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:53:13.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:13.3|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:53:13.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:13.4|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:53:13.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:13.4|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:53:13.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:13.4|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:53:13.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:13.4|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:53:19.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:19.6|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:53:19.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:19.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:19.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:19.6|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:53:19.6|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:53:19.6|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:53:19.6|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:53:19.6|Debug|Api|[GET] /api/v3/rootfolder?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:53:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:24.7|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (3 ms)
2026-08-30 19:53:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:24.7|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:53:35.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:35.4|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (3 ms)
2026-08-30 19:53:43.3|Debug|ImportListSyncService|No import lists with automatic add enabled
2026-08-30 19:53:43.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:43.4|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:53:56.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:53:56.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/localization/language: 200.OK (0 ms)
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/customFilter: 200.OK (0 ms)
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/tag: 200.OK (1 ms)
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/language: 200.OK (0 ms)
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/importlist: 200.OK (0 ms)
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (0 ms)
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (1 ms)
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/config/ui: 200.OK (0 ms)
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/system/status: 200.OK (1 ms)
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/localization: 200.OK (1 ms)
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/queue/status: 200.OK (1 ms)
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:53:56.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:53:56.5|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:53:56.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:54:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:00.0|Debug|Api|[POST] /api/v3/command?apikey=(removed) 201.Created (9 ms)
2026-08-30 19:54:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:00.0|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (1 ms)
2026-08-30 19:54:00.0|Debug|Api|[GET] /api/v3/queue?apikey=(removed)&includeEpisode=true: 200.OK (22 ms)
2026-08-30 19:54:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:54:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:00.0|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:54:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:54:12.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:12.4|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:54:14.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/localization/language: 200.OK (0 ms)
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/customFilter: 200.OK (1 ms)
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/tag: 200.OK (1 ms)
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/importlist: 200.OK (0 ms)
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/language: 200.OK (0 ms)
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/config/ui: 200.OK (0 ms)
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/qualityprofile: 200.OK (1 ms)
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/indexerFlag: 200.OK (1 ms)
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/system/status: 200.OK (1 ms)
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/series: 200.OK (3 ms)
2026-08-30 19:54:14.7|Debug|Api|[GET] /api/v3/localization: 200.OK (2 ms)
2026-08-30 19:54:14.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:54:14.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.8|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:54:14.8|Debug|Api|[GET] /api/v3/queue/status: 200.OK (1 ms)
2026-08-30 19:54:14.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:14.8|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:54:14.8|Debug|Api|[GET] /api/v3/series: 200.OK (2 ms)
2026-08-30 19:54:14.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: SignalR was successfully authenticated.
2026-08-30 19:54:24.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:24.7|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:54:36.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:36.8|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:54:36.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:36.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:36.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:54:36.8|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:54:36.8|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:54:36.8|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:54:36.8|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:54:36.8|Debug|Api|[GET] /api/v3/rootfolder?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:55:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:00.0|Debug|Api|[POST] /api/v3/command?apikey=(removed) 201.Created (5 ms)
2026-08-30 19:55:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:00.0|Debug|Api|[GET] /api/v3/queue?apikey=(removed)&includeEpisode=true: 200.OK (2 ms)
2026-08-30 19:55:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:00.0|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:55:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:55:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:00.0|Debug|Api|[GET] /api/v3/queue/details?all=true: 200.OK (0 ms)
2026-08-30 19:55:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:55:16.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:16.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:16.3|Debug|Api|[GET] /api/v3/series/lookup?apikey=(removed)&term=tvdb:383203: 200.OK (2 ms)
2026-08-30 19:55:16.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:16.3|Debug|SeriesService|Tags not updated for 'Ted Lasso'
2026-08-30 19:55:16.3|Debug|Api|[PUT] /api/v3/series?apikey=(removed) 202.Accepted (36 ms)
2026-08-30 19:55:16.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:16.3|Debug|Api|[POST] /api/v3/command?apikey=(removed) 201.Created (5 ms)
2026-08-30 19:55:16.3|Info|EpisodeSearchService|Performing search for 38 episodes
2026-08-30 19:55:16.3|Info|ReleaseSearchService|Searching indexers for [Ted Lasso : S02]. 2 active indexers
2026-08-30 19:55:16.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=2
2026-08-30 19:55:16.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=2
2026-08-30 19:55:16.6|Debug|Api|[GET] /api/v3/series/lookup?apikey=(removed)&term=tvdb:94571: 200.OK (309 ms)
2026-08-30 19:55:16.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:16.6|Info|AddSeriesService|Adding Series [94571][Community] Path: [/tv/Community]
2026-08-30 19:55:16.6|Info|RefreshSeriesService|Updating Community
2026-08-30 19:55:16.6|Debug|Api|[POST] /api/v3/series?apikey=(removed) 201.Created (70 ms)
2026-08-30 19:55:16.7|Debug|SeriesService|Tags not updated for 'Community'
2026-08-30 19:55:16.7|Info|RefreshEpisodeService|Starting episode info refresh for: [94571][Community]
2026-08-30 19:55:16.7|Info|RefreshEpisodeService|Finished episode refresh for series: [94571][Community].
2026-08-30 19:55:16.7|Debug|RefreshSeriesService|Finished series refresh for Community
2026-08-30 19:55:16.7|Debug|XemService|Scene numbering is not available for Community [94571]
2026-08-30 19:55:16.7|Debug|SeriesService|Tags not updated for 'Community'
2026-08-30 19:55:16.7|Info|MediaCoverService|Downloading Banner for [94571][Community] https://artworks.thetvdb.com/banners/graphical/94571-g.jpg
2026-08-30 19:55:16.7|Warn|DiskScanService|Series' root folder (/tv) is empty.
2026-08-30 19:55:16.7|Info|SeriesScannedHandler|[Community] was recently added, performing post-add actions
2026-08-30 19:55:16.7|Debug|HttpClient|Downloading [https://artworks.thetvdb.com/banners/graphical/94571-g.jpg] to [/config/MediaCover/2/banner.jpg]
2026-08-30 19:55:16.7|Debug|EpisodeMonitoredService|[Community] Setting episode monitored status.
2026-08-30 19:55:16.7|Debug|EpisodeMonitoredService|Unmonitoring Episodes with Files
2026-08-30 19:55:16.7|Debug|EpisodeMonitoredService|Monitoring Episodes without Files
2026-08-30 19:55:16.7|Debug|EpisodeMonitoredService|Unmonitoring all episodes in season 0
2026-08-30 19:55:16.7|Debug|EpisodeMonitoredService|Unmonitoring season 0 because all episodes are not monitored
2026-08-30 19:55:16.7|Warn|MediaCoverMapper|File /config/MediaCover/2/poster.jpg not found
2026-08-30 19:55:16.9|Debug|SeriesService|Tags not updated for 'Community'
2026-08-30 19:55:17.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:17.0|Debug|Api|[GET] /api/v3/command: 200.OK (1 ms)
2026-08-30 19:55:17.0|Info|EpisodeSearchService|Performing search for 110 episodes
2026-08-30 19:55:17.0|Info|ReleaseSearchService|Searching indexers for [Community : S01]. 2 active indexers
2026-08-30 19:55:17.0|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=1
2026-08-30 19:55:17.0|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=1
2026-08-30 19:55:18.8|Debug|HttpClient|Downloading Completed. took 2s
2026-08-30 19:55:18.8|Info|MediaCoverService|Downloading Poster for [94571][Community] https://artworks.thetvdb.com/banners/posters/94571-7.jpg
2026-08-30 19:55:18.8|Debug|HttpClient|Downloading [https://artworks.thetvdb.com/banners/posters/94571-7.jpg] to [/config/MediaCover/2/poster.jpg]
2026-08-30 19:55:19.0|Debug|HttpClient|Downloading Completed. took 0s
2026-08-30 19:55:19.0|Info|MediaCoverService|Downloading Fanart for [94571][Community] https://artworks.thetvdb.com/banners/fanart/original/94571-7.jpg
2026-08-30 19:55:19.0|Debug|HttpClient|Downloading [https://artworks.thetvdb.com/banners/fanart/original/94571-7.jpg] to [/config/MediaCover/2/fanart.jpg]
2026-08-30 19:55:19.1|Debug|HttpClient|Downloading Completed. took 0s
2026-08-30 19:55:19.1|Info|MediaCoverService|Downloading Clearlogo for [94571][Community] https://artworks.thetvdb.com/banners/v4/series/94571/clearlogo/611b5455cd0f2.png
2026-08-30 19:55:19.1|Debug|HttpClient|Downloading [https://artworks.thetvdb.com/banners/v4/series/94571/clearlogo/611b5455cd0f2.png] to [/config/MediaCover/2/clearlogo.png]
2026-08-30 19:55:19.2|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=2
2026-08-30 19:55:19.3|Debug|HttpClient|Downloading Completed. took 0s
2026-08-30 19:55:19.3|Debug|MediaCoverService|Resizing Banner-70 for [94571][Community]
2026-08-30 19:55:19.3|Debug|MediaCoverService|Resizing Banner-35 for [94571][Community]
2026-08-30 19:55:19.3|Debug|MediaCoverService|Resizing Poster-500 for [94571][Community]
2026-08-30 19:55:19.3|Debug|MediaCoverService|Resizing Poster-250 for [94571][Community]
2026-08-30 19:55:19.4|Debug|MediaCoverService|Resizing Fanart-360 for [94571][Community]
2026-08-30 19:55:19.4|Debug|MediaCoverService|Resizing Fanart-180 for [94571][Community]
2026-08-30 19:55:19.5|Debug|CleanExtraFileService|Cleaning missing metadata files for series: Community
2026-08-30 19:55:19.5|Info|MetadataService|Series folder does not exist, skipping metadata image creation
2026-08-30 19:55:21.0|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=2
2026-08-30 19:55:21.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:21.7|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:55:22.0|Debug|ReleaseSearchService|Total of 0 reports were found for [Community : S01] from 2 indexers
2026-08-30 19:55:22.0|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:55:22
2026-08-30 19:55:22.1|Info|DownloadDecisionMaker|No results found
2026-08-30 19:55:22.1|Info|ReleaseSearchService|Searching indexers for [Community : S02]. 2 active indexers
2026-08-30 19:55:22.1|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=2
2026-08-30 19:55:22.1|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=2
2026-08-30 19:55:23.0|Debug|ReleaseSearchService|Total of 22 reports were found for [Ted Lasso : S02] from 2 indexers
2026-08-30 19:55:23.0|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:55:23
2026-08-30 19:55:23.0|Info|DownloadDecisionMaker|Processing 22 releases
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: French
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: French
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: FW
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:23.0|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.0|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:23.0|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:55:23.0|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.0|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.0|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso 2020 - Season 03 WEBDL-1080p v1
2026-08-30 19:55:23.0|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.0|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.0|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.0|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 3x1-12, [Permanent] Wrong season
2026-08-30 19:55:23.0|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.0|Debug|Parser|Parsing string 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:23.0|Debug|Parser|Episode Parsed. Ted Lasso - Season 02 
2026-08-30 19:55:23.0|Debug|Parser|Languages parsed: French
2026-08-30 19:55:23.0|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:23.0|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:23.0|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:55:23.0|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.0|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.0|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' accepted
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - Season 01 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: French
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 01 WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 1x1-10, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: French
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: French
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: FW
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso 2020 - Season 03 WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 3x1-12, [Permanent] Wrong season
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - Season 02 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: French
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)' accepted
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:23.1|Debug|Parser|Parsing string 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:23.1|Debug|Parser|Episode Parsed. Ted Lasso - Season 01 
2026-08-30 19:55:23.1|Debug|Parser|Languages parsed: French
2026-08-30 19:55:23.1|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:23.1|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:55:23.1|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:23.1|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:23.1|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:23.1|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:55:23.1|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:23.1|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:23.1|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 01 WEBDL-1080p v1
2026-08-30 19:55:23.1|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:23.1|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:23.1|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:23.1|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:23.1|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 1x1-10, [Permanent] Wrong season
2026-08-30 19:55:25.1|Debug|ReleaseSearchService|Total of 0 reports were found for [Community : S02] from 2 indexers
2026-08-30 19:55:25.1|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:55:25
2026-08-30 19:55:25.2|Info|DownloadDecisionMaker|No results found
2026-08-30 19:55:25.2|Info|ReleaseSearchService|Searching indexers for [Community : S03]. 2 active indexers
2026-08-30 19:55:25.2|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=3
2026-08-30 19:55:25.2|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=3
2026-08-30 19:55:28.1|Warn|HttpClient|HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest (124 bytes)
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

2026-08-30 19:55:28.1|Warn|ProcessDownloadDecisions|Couldn't add release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from Indexer Torrent9 (Prowlarr) to download queue.

[v4.0.19.2979] NzbDrone.Core.Download.Clients.DownloadClientException: Failed to connect to qBittorrent, check your settings.
 ---> NzbDrone.Common.Http.HttpException: HTTP request failed: [400:BadRequest] [POST] at [http://decypharr:8282/api/v2/torrents/add]
   at NzbDrone.Common.Http.HttpClient.ExecuteAsync(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 119
   at NzbDrone.Common.Http.HttpClient.Execute(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 128
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

   --- End of inner exception stack trace ---
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.AddTorrentFromUrl(String torrentUrl, TorrentSeedConfiguration seedConfiguration, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 159
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrent.AddFromMagnetLink(RemoteEpisode remoteEpisode, String hash, String magnetLink) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrent.cs:line 84
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromMagnetUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String magnetUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 235
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromWebUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String torrentUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 158
   at NzbDrone.Core.Download.TorrentClientBase`1.Download(RemoteEpisode remoteEpisode, IIndexer indexer) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 124
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, IDownloadClient downloadClient) in ./Sonarr.Core/Download/DownloadService.cs:line 98
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/DownloadService.cs:line 63
   at NzbDrone.Core.Download.ProcessDownloadDecisions.ProcessDecisionInternal(DownloadDecision decision, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/ProcessDownloadDecisions.cs:line 204

2026-08-30 19:55:29.1|Debug|ReleaseSearchService|Total of 0 reports were found for [Community : S03] from 2 indexers
2026-08-30 19:55:29.1|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:55:29
2026-08-30 19:55:29.2|Info|DownloadDecisionMaker|No results found
2026-08-30 19:55:29.2|Info|ReleaseSearchService|Searching indexers for [Community : S04]. 2 active indexers
2026-08-30 19:55:29.2|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=4
2026-08-30 19:55:29.2|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=4
2026-08-30 19:55:29.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:29.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:29.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:29.4|Debug|Api|[GET] /api/v3/episodeFile?seriesId=2: 200.OK (2 ms)
2026-08-30 19:55:29.4|Debug|Api|[GET] /api/v3/queue/details?seriesId=2: 200.OK (2 ms)
2026-08-30 19:55:29.4|Debug|Api|[GET] /api/v3/episode?seriesId=2: 200.OK (5 ms)
2026-08-30 19:55:30.4|Warn|HttpClient|HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest (124 bytes)
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

2026-08-30 19:55:30.4|Warn|ProcessDownloadDecisions|Couldn't add release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from Indexer World-torrent (Prowlarr) to download queue.

[v4.0.19.2979] NzbDrone.Core.Download.Clients.DownloadClientException: Failed to connect to qBittorrent, check your settings.
 ---> NzbDrone.Common.Http.HttpException: HTTP request failed: [400:BadRequest] [POST] at [http://decypharr:8282/api/v2/torrents/add]
   at NzbDrone.Common.Http.HttpClient.ExecuteAsync(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 119
   at NzbDrone.Common.Http.HttpClient.Execute(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 128
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

   --- End of inner exception stack trace ---
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.AddTorrentFromUrl(String torrentUrl, TorrentSeedConfiguration seedConfiguration, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 159
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrent.AddFromMagnetLink(RemoteEpisode remoteEpisode, String hash, String magnetLink) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrent.cs:line 84
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromMagnetUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String magnetUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 235
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromWebUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String torrentUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 158
   at NzbDrone.Core.Download.TorrentClientBase`1.Download(RemoteEpisode remoteEpisode, IIndexer indexer) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 124
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, IDownloadClient downloadClient) in ./Sonarr.Core/Download/DownloadService.cs:line 98
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/DownloadService.cs:line 63
   at NzbDrone.Core.Download.ProcessDownloadDecisions.ProcessDecisionInternal(DownloadDecision decision, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/ProcessDownloadDecisions.cs:line 204

2026-08-30 19:55:30.5|Info|ReleaseSearchService|Searching indexers for [Ted Lasso : S03]. 2 active indexers
2026-08-30 19:55:30.5|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=3
2026-08-30 19:55:30.5|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=3
2026-08-30 19:55:32.3|Debug|ReleaseSearchService|Total of 0 reports were found for [Community : S04] from 2 indexers
2026-08-30 19:55:32.3|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:55:32
2026-08-30 19:55:32.3|Info|DownloadDecisionMaker|No results found
2026-08-30 19:55:32.3|Info|ReleaseSearchService|Searching indexers for [Community : S05]. 2 active indexers
2026-08-30 19:55:32.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=5
2026-08-30 19:55:32.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=5
2026-08-30 19:55:33.2|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=3
2026-08-30 19:55:34.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=3
2026-08-30 19:55:37.3|Debug|ReleaseSearchService|Total of 0 reports were found for [Community : S05] from 2 indexers
2026-08-30 19:55:37.3|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:55:37
2026-08-30 19:55:37.3|Info|DownloadDecisionMaker|No results found
2026-08-30 19:55:37.3|Info|ReleaseSearchService|Searching indexers for [Community : S06]. 2 active indexers
2026-08-30 19:55:37.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=6
2026-08-30 19:55:37.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Community&season=6
2026-08-30 19:55:40.3|Debug|ReleaseSearchService|Total of 14 reports were found for [Ted Lasso : S03] from 2 indexers
2026-08-30 19:55:40.3|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:55:40
2026-08-30 19:55:40.3|Info|DownloadDecisionMaker|Processing 14 releases
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.3|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:40.3|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:55:40.3|Debug|Parser|Languages parsed: French
2026-08-30 19:55:40.3|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:40.3|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:55:40.3|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.3|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.3|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:55:40.3|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.3|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:55:40.3|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.3|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.3|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.3|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.3|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:40.3|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:55:40.3|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.3|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:55:40.3|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:55:40.3|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.3|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.3|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:55:40.3|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.3|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:55:40.3|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.3|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.3|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.3|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.3|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.3|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:55:40.3|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.3|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.3|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.3|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.3|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:40.3|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.3|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.3|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.3|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.3|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.3|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.3|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:55:40.3|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.3|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.3|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.3|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.3|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:40.3|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.3|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.3|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.3|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.3|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.3|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.3|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:55:40.3|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.3|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.3|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.3|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.3|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:40.3|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.3|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.3|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.3|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.3|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season
2026-08-30 19:55:40.3|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.3|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.3|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:55:40.3|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.3|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.3|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.3|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.3|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.3|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.3|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.3|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.3|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:40.3|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.3|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.3|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:55:40.3|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.3|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.3|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.3|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.4|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.4|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:55:40.4|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.4|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.4|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.4|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:40.4|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.4|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.4|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.4|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.4|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.4|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.4|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:55:40.4|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.4|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.4|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.4|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:40.4|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.4|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.4|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.4|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.4|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.4|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:55:40.4|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:55:40.4|Debug|Parser|Languages parsed: French
2026-08-30 19:55:40.4|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:55:40.4|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|Parser|Release Group parsed: FW
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:40.4|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.4|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:55:40.4|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.4|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.4|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.4|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)' accepted
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.4|Debug|Parser|Parsing string 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:40.4|Debug|Parser|Episode Parsed. Ted Lasso - Season 02 
2026-08-30 19:55:40.4|Debug|Parser|Languages parsed: French
2026-08-30 19:55:40.4|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:40.4|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:40.4|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.4|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:55:40.4|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.4|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 02 WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.4|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.4|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.4|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 2x1-12, [Permanent] Wrong season
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:55:40.4|Debug|Parser|Parsing string 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:40.4|Debug|Parser|Episode Parsed. Ted Lasso - Season 01 
2026-08-30 19:55:40.4|Debug|Parser|Languages parsed: French
2026-08-30 19:55:40.4|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:55:40.4|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:40.4|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.4|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:55:40.4|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.4|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 01 WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.4|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.4|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.4|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 1x1-10, [Permanent] Wrong season
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:40.4|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.4|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:55:40.4|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.4|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.4|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.4|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:40.4|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.4|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.4|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.4|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.4|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:40.4|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.4|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:55:40.4|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:55:40.4|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:55:40.4|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.4|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:55:40.4|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.4|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:55:40.4|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:55:40.4|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.4|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.4|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'World-torrent (Prowlarr)'
2026-08-30 19:55:40.4|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:55:40.4|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:55:40.4|Debug|Parser|Languages parsed: French
2026-08-30 19:55:40.4|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:55:40.4|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|Parser|Release Group parsed: FW
2026-08-30 19:55:40.4|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:40.4|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:55:40.4|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:40.4|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:55:40.4|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:55:40.4|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:55:40.4|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:55:40.4|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:55:40.4|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:55:40.4|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:55:40.4|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:55:40.4|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'World-torrent (Prowlarr)' accepted
2026-08-30 19:55:42.8|Debug|ReleaseSearchService|Total of 0 reports were found for [Community : S06] from 2 indexers
2026-08-30 19:55:42.8|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:55:42
2026-08-30 19:55:42.8|Info|DownloadDecisionMaker|No results found
2026-08-30 19:55:42.8|Info|EpisodeSearchService|Completed search for 110 episodes. 0 reports downloaded.
2026-08-30 19:55:42.8|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:55:42.8|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:55:55.3|Warn|HttpClient|HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest (124 bytes)
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

2026-08-30 19:55:55.3|Warn|ProcessDownloadDecisions|Couldn't add release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from Indexer World-torrent (Prowlarr) to download queue.

[v4.0.19.2979] NzbDrone.Core.Download.Clients.DownloadClientException: Failed to connect to qBittorrent, check your settings.
 ---> NzbDrone.Common.Http.HttpException: HTTP request failed: [400:BadRequest] [POST] at [http://decypharr:8282/api/v2/torrents/add]
   at NzbDrone.Common.Http.HttpClient.ExecuteAsync(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 119
   at NzbDrone.Common.Http.HttpClient.Execute(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 128
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

   --- End of inner exception stack trace ---
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.AddTorrentFromUrl(String torrentUrl, TorrentSeedConfiguration seedConfiguration, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 159
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrent.AddFromMagnetLink(RemoteEpisode remoteEpisode, String hash, String magnetLink) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrent.cs:line 84
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromMagnetUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String magnetUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 235
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromWebUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String torrentUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 158
   at NzbDrone.Core.Download.TorrentClientBase`1.Download(RemoteEpisode remoteEpisode, IIndexer indexer) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 124
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, IDownloadClient downloadClient) in ./Sonarr.Core/Download/DownloadService.cs:line 98
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/DownloadService.cs:line 63
   at NzbDrone.Core.Download.ProcessDownloadDecisions.ProcessDecisionInternal(DownloadDecision decision, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/ProcessDownloadDecisions.cs:line 204

2026-08-30 19:55:56.8|Warn|HttpClient|HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest (124 bytes)
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

2026-08-30 19:55:56.8|Warn|ProcessDownloadDecisions|Couldn't add release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from Indexer Torrent9 (Prowlarr) to download queue.

[v4.0.19.2979] NzbDrone.Core.Download.Clients.DownloadClientException: Failed to connect to qBittorrent, check your settings.
 ---> NzbDrone.Common.Http.HttpException: HTTP request failed: [400:BadRequest] [POST] at [http://decypharr:8282/api/v2/torrents/add]
   at NzbDrone.Common.Http.HttpClient.ExecuteAsync(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 119
   at NzbDrone.Common.Http.HttpClient.Execute(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 128
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

   --- End of inner exception stack trace ---
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.AddTorrentFromUrl(String torrentUrl, TorrentSeedConfiguration seedConfiguration, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 159
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrent.AddFromMagnetLink(RemoteEpisode remoteEpisode, String hash, String magnetLink) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrent.cs:line 84
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromMagnetUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String magnetUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 235
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromWebUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String torrentUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 158
   at NzbDrone.Core.Download.TorrentClientBase`1.Download(RemoteEpisode remoteEpisode, IIndexer indexer) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 124
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, IDownloadClient downloadClient) in ./Sonarr.Core/Download/DownloadService.cs:line 98
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/DownloadService.cs:line 63
   at NzbDrone.Core.Download.ProcessDownloadDecisions.ProcessDecisionInternal(DownloadDecision decision, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/ProcessDownloadDecisions.cs:line 204

2026-08-30 19:55:56.8|Info|ReleaseSearchService|Searching indexers for [Ted Lasso : S04]. 2 active indexers
2026-08-30 19:55:56.8|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=4
2026-08-30 19:55:56.8|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=4
2026-08-30 19:55:58.6|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=4
2026-08-30 19:55:59.4|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=4
2026-08-30 19:56:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:00.0|Debug|Api|[POST] /api/v3/command?apikey=(removed) 201.Created (4 ms)
2026-08-30 19:56:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:00.0|Debug|Api|[GET] /api/v3/queue?apikey=(removed)&includeEpisode=true: 200.OK (4 ms)
2026-08-30 19:56:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:00.0|Debug|Api|[GET] /api/v3/queue/details?seriesId=2: 200.OK (1 ms)
2026-08-30 19:56:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:00.0|Debug|Api|[GET] /api/v3/queue/details?seriesId=2: 200.OK (1 ms)
2026-08-30 19:56:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:56:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:56:01.2|Debug|ReleaseSearchService|Total of 19 reports were found for [Ted Lasso : S04] from 2 indexers
2026-08-30 19:56:01.2|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:56:01
2026-08-30 19:56:01.2|Info|DownloadDecisionMaker|Processing 19 releases
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: FW
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso 2020 - Season 03 WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 3x1-12, [Permanent] Wrong season
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - Season 02 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 02 WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 2x1-12, [Permanent] Wrong season
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - Season 01 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 01 WEBDL-1080p v1
2026-08-30 19:56:01.2|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 1x1-10, [Permanent] Wrong season
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: French
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.2|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.2|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.2|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.2|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.2|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.2|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.2|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.2|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:01.2|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:56:01.2|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.2|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.2|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.2|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.2|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.2|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.2|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.3|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.3|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.3|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.3|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.3|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.3|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.3|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.3|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.3|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.3|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.3|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.3|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.3|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:01.3|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.3|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:56:01.3|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:01.3|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:01.3|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:01.3|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:01.3|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:01.3|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:01.3|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.3|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:01.3|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:01.3|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:01.3|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:01.3|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:01.3|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:01.3|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:01.3|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:01.3|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:01.3|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:01.3|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:01.3|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:01.3|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:01.3|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:01.3|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile
2026-08-30 19:56:01.3|Info|ReleaseSearchService|Searching indexers for [Ted Lasso : S01]. 2 active indexers
2026-08-30 19:56:01.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=1
2026-08-30 19:56:01.3|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=1
2026-08-30 19:56:02.7|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=1
2026-08-30 19:56:03.6|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050&extended=1&apikey=(removed)&offset=0&limit=100&q=Ted%20Lasso&season=1
2026-08-30 19:56:05.7|Debug|ReleaseSearchService|Total of 16 reports were found for [Ted Lasso : S01] from 2 indexers
2026-08-30 19:56:05.7|Debug|ReleaseSearchService|Setting last search time to: 08/30/2026 17:56:05
2026-08-30 19:56:05.7|Info|DownloadDecisionMaker|Processing 16 releases
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: French
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E04 Unknown v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vostfr.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile, [Permanent] Episode wasn't requested: 4x4, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E03 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E03 WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e03.Richmonds.Got.Talent.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x3, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E02 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E02 WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e02.Curiouser.And.Curiouser.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x2, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: French
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: FW
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso 2020 - Season 03 WEBDL-1080p v1
2026-08-30 19:56:05.7|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.7|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.7|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.7|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 3x1-12, [Permanent] Wrong season
2026-08-30 19:56:05.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.7|Debug|Parser|Parsing string 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:05.7|Debug|Parser|Episode Parsed. Ted Lasso - Season 02 
2026-08-30 19:56:05.7|Debug|Parser|Languages parsed: French
2026-08-30 19:56:05.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:05.7|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:05.7|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:56:05.7|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.7|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:56:05.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.7|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 02 WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.8|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.8|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.8|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 2x1-12, [Permanent] Wrong season
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)'
2026-08-30 19:56:05.8|Debug|Parser|Parsing string 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:05.8|Debug|Parser|Episode Parsed. Ted Lasso - Season 01 
2026-08-30 19:56:05.8|Debug|Parser|Languages parsed: French
2026-08-30 19:56:05.8|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:05.8|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:56:05.8|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.8|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:56:05.8|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.8|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.8|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.8|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'Torrent9 (Prowlarr)' accepted
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:05.8|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.8|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:56:05.8|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.8|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.8|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:05.8|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:05.8|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.8|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.8|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:05.8|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:05.8|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.8|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:56:05.8|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.8|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.8|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.8|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:05.8|Debug|Parser|Parsing string 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.8|Debug|Parser|Episode Parsed. Ted Lasso - S04E01 
2026-08-30 19:56:05.8|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:56:05.8|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor'
2026-08-30 19:56:05.8|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:56:05.8|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:56:05.8|Debug|AggregateLanguages|Language couldn't be parsed from release, fallback to series original language: English
2026-08-30 19:56:05.8|Debug|AggregateLanguages|Selected languages: English
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor, meets size constraints
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.8|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-480p v1
2026-08-30 19:56:05.8|Debug|QualityAllowedByProfileSpecification|Quality WEBDL-480p v1 rejected by Series' quality profile
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor] No restrictions apply, allowing
2026-08-30 19:56:05.8|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.8|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - S04E01 WEBDL-480p v1
2026-08-30 19:56:05.8|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.8|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.8|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.8|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e01.Home.Vostfr.Ad.Atv.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] WEBDL-480p is not wanted in profile, [Permanent] Episode wasn't requested: 4x1, [Permanent] Wrong season
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:05.8|Debug|Parser|Parsing string 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:56:05.8|Debug|Parser|Episode Parsed. Ted Lasso 2020 - Season 03 
2026-08-30 19:56:05.8|Debug|Parser|Languages parsed: French
2026-08-30 19:56:05.8|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW'
2026-08-30 19:56:05.8|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|Parser|Release Group parsed: FW
2026-08-30 19:56:05.8|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW, meets size constraints
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:05.8|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.8|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW] No restrictions apply, allowing
2026-08-30 19:56:05.8|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.8|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso 2020 - Season 03 WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.8|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.8|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.8|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.2020.S03.MULTI.VFF.1080p.WEB.EAC3.5.1.H264-FW' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 3x1-12, [Permanent] Wrong season
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:05.8|Debug|Parser|Parsing string 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:05.8|Debug|Parser|Episode Parsed. Ted Lasso - Season 02 
2026-08-30 19:56:05.8|Debug|Parser|Languages parsed: French
2026-08-30 19:56:05.8|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:05.8|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:56:05.8|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.8|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:56:05.8|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.8|Debug|EpisodeRequestedSpecification|Release rejected since the episode wasn't requested: Ted Lasso - Season 02 WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|SeasonMatchSpecification|Season number does not match searched season number, skipping.
2026-08-30 19:56:05.8|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.8|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.8|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S02.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Episode wasn't requested: 2x1-12, [Permanent] Wrong season
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)'
2026-08-30 19:56:05.8|Debug|Parser|Parsing string 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:05.8|Debug|Parser|Episode Parsed. Ted Lasso - Season 01 
2026-08-30 19:56:05.8|Debug|Parser|Languages parsed: French
2026-08-30 19:56:05.8|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR'
2026-08-30 19:56:05.8|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|Parser|Release Group parsed: BYOR
2026-08-30 19:56:05.8|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR, meets size constraints
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:56:05.8|Debug|FullSeasonSpecification|Checking if all episodes in full season release have aired. Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:56:05.8|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. WEBDL-1080p v1
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR
2026-08-30 19:56:05.8|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR] No restrictions apply, allowing
2026-08-30 19:56:05.8|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:56:05.8|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:56:05.8|Debug|SeriesSpecification|Checking if series matches searched series
2026-08-30 19:56:05.8|Debug|DelaySpecification|Ignoring delay for user invoked search
2026-08-30 19:56:05.8|Debug|HistorySpecification|Skipping history check during search
2026-08-30 19:56:05.8|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from 'World-torrent (Prowlarr)' accepted
2026-08-30 19:56:08.0|Warn|HttpClient|HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest (124 bytes)
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

2026-08-30 19:56:08.0|Warn|ProcessDownloadDecisions|Couldn't add release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from Indexer World-torrent (Prowlarr) to download queue.

[v4.0.19.2979] NzbDrone.Core.Download.Clients.DownloadClientException: Failed to connect to qBittorrent, check your settings.
 ---> NzbDrone.Common.Http.HttpException: HTTP request failed: [400:BadRequest] [POST] at [http://decypharr:8282/api/v2/torrents/add]
   at NzbDrone.Common.Http.HttpClient.ExecuteAsync(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 119
   at NzbDrone.Common.Http.HttpClient.Execute(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 128
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

   --- End of inner exception stack trace ---
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.AddTorrentFromUrl(String torrentUrl, TorrentSeedConfiguration seedConfiguration, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 159
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrent.AddFromMagnetLink(RemoteEpisode remoteEpisode, String hash, String magnetLink) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrent.cs:line 84
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromMagnetUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String magnetUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 235
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromWebUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String torrentUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 158
   at NzbDrone.Core.Download.TorrentClientBase`1.Download(RemoteEpisode remoteEpisode, IIndexer indexer) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 124
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, IDownloadClient downloadClient) in ./Sonarr.Core/Download/DownloadService.cs:line 98
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/DownloadService.cs:line 63
   at NzbDrone.Core.Download.ProcessDownloadDecisions.ProcessDecisionInternal(DownloadDecision decision, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/ProcessDownloadDecisions.cs:line 204

2026-08-30 19:56:09.5|Warn|HttpClient|HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest (124 bytes)
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

2026-08-30 19:56:09.5|Warn|ProcessDownloadDecisions|Couldn't add release 'Ted.Lasso.S01.MULTi.VFF.AD.1080p.WEB.EAC3.5.1.Atmos.H264-BYOR' from Indexer Torrent9 (Prowlarr) to download queue.

[v4.0.19.2979] NzbDrone.Core.Download.Clients.DownloadClientException: Failed to connect to qBittorrent, check your settings.
 ---> NzbDrone.Common.Http.HttpException: HTTP request failed: [400:BadRequest] [POST] at [http://decypharr:8282/api/v2/torrents/add]
   at NzbDrone.Common.Http.HttpClient.ExecuteAsync(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 119
   at NzbDrone.Common.Http.HttpClient.Execute(HttpRequest request) in ./Sonarr.Common/Http/HttpClient.cs:line 128
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebrid API error: Status: 451

   --- End of inner exception stack trace ---
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.ProcessRequest(HttpRequestBuilder requestBuilder, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 426
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrentProxyV2.AddTorrentFromUrl(String torrentUrl, TorrentSeedConfiguration seedConfiguration, QBittorrentSettings settings) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrentProxyV2.cs:line 159
   at NzbDrone.Core.Download.Clients.QBittorrent.QBittorrent.AddFromMagnetLink(RemoteEpisode remoteEpisode, String hash, String magnetLink) in ./Sonarr.Core/Download/Clients/QBittorrent/QBittorrent.cs:line 84
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromMagnetUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String magnetUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 235
   at NzbDrone.Core.Download.TorrentClientBase`1.DownloadFromWebUrl(RemoteEpisode remoteEpisode, IIndexer indexer, String torrentUrl) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 158
   at NzbDrone.Core.Download.TorrentClientBase`1.Download(RemoteEpisode remoteEpisode, IIndexer indexer) in ./Sonarr.Core/Download/TorrentClientBase.cs:line 124
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, IDownloadClient downloadClient) in ./Sonarr.Core/Download/DownloadService.cs:line 98
   at NzbDrone.Core.Download.DownloadService.DownloadReport(RemoteEpisode remoteEpisode, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/DownloadService.cs:line 63
   at NzbDrone.Core.Download.ProcessDownloadDecisions.ProcessDecisionInternal(DownloadDecision decision, Nullable`1 downloadClientId) in ./Sonarr.Core/Download/ProcessDownloadDecisions.cs:line 204

2026-08-30 19:56:09.5|Info|EpisodeSearchService|Completed search for 38 episodes. 0 reports downloaded.
2026-08-30 19:56:09.5|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:09.5|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:56:24.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:24.0|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:56:24.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:24.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:24.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:24.1|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:56:24.1|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:56:24.1|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:56:24.1|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:56:24.1|Debug|Api|[GET] /api/v3/rootfolder?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:56:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:30.4|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:56:30.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:30.4|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (0 ms)
2026-08-30 19:56:44.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:44.6|Debug|Api|[GET] /api/v3/system/status?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:56:44.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:44.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:44.6|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:56:44.6|Debug|Api|[GET] /api/v3/tag?apikey=(removed) 200.OK (1 ms)
2026-08-30 19:56:44.6|Debug|RootFolderService|Generating list of unmapped folders
2026-08-30 19:56:44.6|Debug|RootFolderService|0 unmapped folders detected.
2026-08-30 19:56:44.6|Debug|Api|[GET] /api/v3/qualityProfile?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:56:44.6|Debug|Api|[GET] /api/v3/rootfolder?apikey=(removed) 200.OK (2 ms)
2026-08-30 19:57:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:00.0|Debug|Api|[POST] /api/v3/command?apikey=(removed) 201.Created (7 ms)
2026-08-30 19:57:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:00.0|Debug|Api|[GET] /api/v3/queue?apikey=(removed)&includeEpisode=true: 200.OK (1 ms)
2026-08-30 19:57:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:00.0|Debug|Api|[GET] /api/v3/queue/details?seriesId=2: 200.OK (0 ms)
2026-08-30 19:57:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:00.0|Debug|Api|[GET] /api/v3/queue/details?seriesId=2: 200.OK (0 ms)
2026-08-30 19:57:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:57:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:57:09.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:09.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:09.9|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:57:09.9|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:09.9|Debug|Api|[GET] /api/v3/system/status: 200.OK (1 ms)
2026-08-30 19:57:09.9|Debug|Api|[GET] /api/v3/diskspace: 200.OK (5 ms)
2026-08-30 19:57:27.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:27.1|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:27.1|Debug|Api|[GET] /api/v3/indexer: 200.OK (2 ms)
2026-08-30 19:57:27.1|Debug|Api|[GET] /api/v3/config/indexer: 200.OK (4 ms)
2026-08-30 19:57:31.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:57:31.0|Debug|Api|[GET] /api/v3/indexer/schema: 200.OK (3 ms)
2026-08-30 19:58:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:00.0|Debug|Api|[POST] /api/v3/command?apikey=(removed) 201.Created (3 ms)
2026-08-30 19:58:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:00.0|Debug|Api|[GET] /api/v3/queue?apikey=(removed)&includeEpisode=true: 200.OK (1 ms)
2026-08-30 19:58:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:58:00.0|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:00.0|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:58:00.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:00.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:00.3|Debug|Api|[GET] /api/v3/config/downloadclient: 200.OK (0 ms)
2026-08-30 19:58:00.3|Debug|Api|[GET] /api/v3/downloadclient: 200.OK (2 ms)
2026-08-30 19:58:00.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:00.3|Debug|Api|[GET] /api/v3/remotepathmapping: 200.OK (1 ms)
2026-08-30 19:58:13.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:13.4|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)
2026-08-30 19:58:23.2|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:23.2|Warn|SonarrErrorPipeline|Invalid request Validation failed: 
 -- TvCategory: Can not contain '\', '//', or start/end with '/'
2026-08-30 19:58:23.2|Debug|Api|[POST] /api/v3/downloadclient/test: 400.BadRequest (19 ms)
2026-08-30 19:58:31.4|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:31.4|Debug|Api|[PUT] /api/v3/downloadclient/1: 202.Accepted (13 ms)
2026-08-30 19:58:35.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:35.7|Debug|Api|[GET] /api/v3/config/ui: 200.OK (0 ms)
2026-08-30 19:58:36.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:36.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:36.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:36.3|Debug|Api|[GET] /api/v3/health: 200.OK (0 ms)
2026-08-30 19:58:36.3|Debug|Api|[GET] /api/v3/system/status: 200.OK (1 ms)
2026-08-30 19:58:36.3|Debug|Api|[GET] /api/v3/diskspace: 200.OK (7 ms)
2026-08-30 19:58:40.3|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:40.3|Debug|Api|[GET] /api/v3/log/file: 200.OK (5 ms)
2026-08-30 19:58:43.4|Info|RssSyncService|Starting RSS Sync
2026-08-30 19:58:43.4|Debug|FetchAndParseRssService|Available indexers 2
2026-08-30 19:58:43.4|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/1/api?t=tvsearch&cat=5000&extended=1&apikey=(removed)&offset=0&limit=100
2026-08-30 19:58:43.4|Debug|Torznab|Downloading Feed http://172.20.115.225:9696/3/api?t=tvsearch&cat=5000,5050,5070&extended=1&apikey=(removed)&offset=0&limit=100
2026-08-30 19:58:44.8|Warn|Torznab|Indexer Torrent9 (Prowlarr) rss sync didn't cover the period between 08/30/2026 17:43:15 and 08/30/2026 17:58:44 UTC. Search may be required.
2026-08-30 19:58:45.6|Debug|FetchAndParseRssService|Found 40 reports
2026-08-30 19:58:45.6|Info|DownloadDecisionMaker|Processing 40 releases
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Processing release 'Average.Joe.S02e03.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.6|Debug|Parser|Parsing string 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:58:45.6|Debug|Parser|Episode Parsed. Average Joe - S02E03 
2026-08-30 19:58:45.6|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.6|Debug|QualityParser|Trying to parse quality for 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:58:45.6|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.6|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.6|Debug|Parser|Parsing string 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:58:45.6|Debug|ParsingService|No matching series Average Joe
2026-08-30 19:58:45.6|Debug|Parser|Parsing string 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Release 'Average.Joe.S02e03.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Processing release 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.6|Debug|Parser|Parsing string 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC'
2026-08-30 19:58:45.6|Debug|Parser|Episode Parsed. Trying - Season 05 
2026-08-30 19:58:45.6|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.6|Debug|QualityParser|Trying to parse quality for 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC'
2026-08-30 19:58:45.6|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:58:45.6|Debug|Parser|Release Group parsed: FRQC
2026-08-30 19:58:45.6|Debug|ParsingService|No matching series Trying
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Release 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Processing release 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.6|Debug|Parser|Parsing string 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:58:45.6|Debug|Parser|Episode Parsed. Trying - S05E08 
2026-08-30 19:58:45.6|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.6|Debug|QualityParser|Trying to parse quality for 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:58:45.6|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.6|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.6|Debug|ParsingService|No matching series Trying
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Release 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Processing release 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.6|Debug|Parser|Parsing string 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)'
2026-08-30 19:58:45.6|Debug|Parser|Episode Parsed. Women In Blue - S02E03 
2026-08-30 19:58:45.6|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.6|Debug|QualityParser|Trying to parse quality for 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)'
2026-08-30 19:58:45.6|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.6|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.6|Debug|ParsingService|No matching series Women In Blue
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Release 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.6|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.6|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:58:45.6|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:58:45.6|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.6|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:58:45.6|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.6|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.6|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:58:45.6|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:58:45.6|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:58:45.6|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:58:45.6|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:58:45.6|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:58:45.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:58:45.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:58:45.7|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:58:45.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:58:45.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:58:45.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:58:45.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:58:45.7|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:58:45.7|Debug|HistorySpecification|Performing history status check on report
2026-08-30 19:58:45.7|Debug|HistorySpecification|Checking current status of episode [47] in history
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Chicago.Fire.S14e01.Web.H264' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Chicago.Fire.S14e01.Web.H264'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Chicago Fire - S14E01 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Chicago.Fire.S14e01.Web.H264'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Chicago Fire
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Chicago.Fire.S14e01.Web.H264' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Furious.S01e07.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Furious.S01e07.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Furious - S01E07 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Furious.S01e07.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Furious
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Furious.S01e07.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Furious.S01e06.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Furious.S01e06.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Furious - S01E06 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Furious.S01e06.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Furious
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Furious.S01e06.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. The Walking Dead Dead City - S03E05 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series The Walking Dead Dead City
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. The Walking Dead Dead City - S03E04 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series The Walking Dead Dead City
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Lanterns - S01E02 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Mtlqc
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Lanterns
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Lanterns - S01E01 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Lanterns
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Gomorra.Origins.S01e02.Web.X264' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Gomorra.Origins.S01e02.Web.X264'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Gomorra Origins - S01E02 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Gomorra.Origins.S01e02.Web.X264'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Gomorra Origins
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Gomorra.Origins.S01e02.Web.X264' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Gomorra.Origins.S01e01.Web.X264' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Gomorra.Origins.S01e01.Web.X264'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Gomorra Origins - S01E01 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Gomorra.Origins.S01e01.Web.X264'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Gomorra Origins
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Gomorra.Origins.S01e01.Web.X264' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Stuart.Fails.To.Save.The.Universe.V.F.S01e06.Vostfr.Web.Ac3.5.1.H264' from 'Torrent9 (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Stuart.Fails.To.Save.The.Universe.V.F.S01e06.Vostfr.Web.Ac3.5.1.H264'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Stuart Fails To Save The Universe V F - S01E06 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Stuart.Fails.To.Save.The.Universe.V.F.S01e06.Vostfr.Web.Ac3.5.1.H264'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Stuart Fails To Save The Universe V F
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Stuart.Fails.To.Save.The.Universe.V.F.S01e06.Vostfr.Web.Ac3.5.1.H264' from 'Torrent9 (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Tip.Toe.S01e05.Final.Vff.Web.Eac3.5.1.H264' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Tip.Toe.S01e05.Final.Vff.Web.Eac3.5.1.H264'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Tip Toe - S01E05 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Tip.Toe.S01e05.Final.Vff.Web.Eac3.5.1.H264'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Tip Toe
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Tip.Toe.S01e05.Final.Vff.Web.Eac3.5.1.H264' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Star.Trek.Strange.New.Worlds.S04e06.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Star.Trek.Strange.New.Worlds.S04e06.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Star Trek Strange New Worlds - S04E06 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Star.Trek.Strange.New.Worlds.S04e06.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Star Trek Strange New Worlds
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Star.Trek.Strange.New.Worlds.S04e06.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'The.Shards.S01e07.Homecoming.Part.Two.Dsnp.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'The.Shards.S01e07.Homecoming.Part.Two.Dsnp.Web.H264-Byor'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. The Shards - S01E07 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'The.Shards.S01e07.Homecoming.Part.Two.Dsnp.Web.H264-Byor'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series The Shards
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'The.Shards.S01e07.Homecoming.Part.Two.Dsnp.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'The.Shards.S01e06.Homecoming.Part.One.Dsnp.Web.H264-Byor' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'The.Shards.S01e06.Homecoming.Part.One.Dsnp.Web.H264-Byor'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. The Shards - S01E06 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'The.Shards.S01e06.Homecoming.Part.One.Dsnp.Web.H264-Byor'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Byor
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series The Shards
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'The.Shards.S01e06.Homecoming.Part.One.Dsnp.Web.H264-Byor' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Special Ops Lioness - S03E05 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:58:45.7|Debug|SceneMappingService|Found scene mapping for: Special Ops Lioness. TVDB ID for mapping: 388589
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Special Ops Lioness
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:58:45.7|Debug|SceneMappingService|Found scene mapping for: Special Ops Lioness. TVDB ID for mapping: 388589
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Special.Ops.Lioness.S03e05.Web.H264 (Opérations Spéciales : Lioness)' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Special Ops Lioness matches an alias for series with TVDB ID: 388589
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Special Ops Lioness - S03E05 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:58:45.7|Debug|SceneMappingService|Found scene mapping for: Special Ops Lioness. TVDB ID for mapping: 388589
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Special Ops Lioness
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)'
2026-08-30 19:58:45.7|Debug|SceneMappingService|Found scene mapping for: Special Ops Lioness. TVDB ID for mapping: 388589
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Special.Ops.Lioness.S03e05.Vostfr.Web.H264 (Opérations Spéciales : Lioness)' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Special Ops Lioness matches an alias for series with TVDB ID: 388589
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag'
2026-08-30 19:58:45.7|Debug|Parser|Unable to parse The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag'
2026-08-30 19:58:45.7|Debug|Parser|Unable to parse The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series The.Exorcist.COMPLETE.MULTI.1080p.WEBDL.x265-NoTag
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'WWE.SmackDown.2026.08.28.NF.VOD.1080p.WEB.h265-HEEL' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'WWE.SmackDown.2026.08.28.NF.VOD.1080p.WEB.h265-HEEL'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. WWE SmackDown - 2026-08-28 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'WWE.SmackDown.2026.08.28.NF.VOD.1080p.WEB.h265-HEEL'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: HEEL
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series WWE SmackDown
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'WWE.SmackDown.2026.08.28.NF.VOD.1080p.WEB.h265-HEEL' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Diarra.From.Detroit.S02e06.Vff.Web.Eac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Diarra.From.Detroit.S02e06.Vff.Web.Eac3.5.1.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Diarra From Detroit - S02E06 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Diarra.From.Detroit.S02e06.Vff.Web.Eac3.5.1.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Diarra From Detroit
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Diarra.From.Detroit.S02e06.Vff.Web.Eac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Average.Joe.S02e03.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Average Joe - S02E03 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Average Joe
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Average.Joe.S02e03.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Average.Joe.S02e03.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Trying - Season 05 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-1080p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: FRQC
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Trying
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Trying.S05.MULTI.VFF.1080p.WEB.AC3.5.1.H264-FRQC' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Trying - S05E08 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Trying
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Trying.S05e08.Final.Vff.Web.Ac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Women In Blue - S02E03 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Women In Blue
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Women.In.Blue.S02e03.Vff.Web.Ac3.5.1.H264-Frqc (Las Azules)' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Ted Lasso - S04E04 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.7|Debug|AggregateLanguages|Selected languages: French
2026-08-30 19:58:45.7|Debug|AcceptableSizeSpecification|Beginning size check for: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:58:45.7|Debug|AcceptableSizeSpecification|Item: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc, meets size constraints
2026-08-30 19:58:45.7|Debug|AlreadyImportedSpecification|Performing already imported check on report
2026-08-30 19:58:45.7|Debug|AlreadyImportedSpecification|Skipping already imported check for episode without file
2026-08-30 19:58:45.7|Debug|MaximumSizeSpecification|Maximum size is not set.
2026-08-30 19:58:45.7|Debug|MinimumAgeSpecification|Not checking minimum age requirement for non-usenet report
2026-08-30 19:58:45.7|Debug|QualityAllowedByProfileSpecification|Checking if report meets quality requirements. Unknown v1
2026-08-30 19:58:45.7|Debug|QualityAllowedByProfileSpecification|Quality Unknown v1 rejected by Series' quality profile
2026-08-30 19:58:45.7|Debug|ReleaseRestrictionsSpecification|Checking if release meets restrictions: Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc
2026-08-30 19:58:45.7|Debug|ReleaseRestrictionsSpecification|[Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc] No restrictions apply, allowing
2026-08-30 19:58:45.7|Debug|RetentionSpecification|Not checking retention requirement for non-usenet report
2026-08-30 19:58:45.7|Debug|SceneMappingSpecification|No applicable scene mapping, skipping.
2026-08-30 19:58:45.7|Debug|DelaySpecification|Delay Profile does not require a waiting period before download for Torrent.
2026-08-30 19:58:45.7|Debug|HistorySpecification|Performing history status check on report
2026-08-30 19:58:45.7|Debug|HistorySpecification|Checking current status of episode [47] in history
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Ted.Lasso.S04e04.Vff.Web.Eac3.5.1.Atmos.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown is not wanted in profile
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Chicago.Fire.S14e01.Web.H264' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Chicago.Fire.S14e01.Web.H264'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Chicago Fire - S14E01 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Chicago.Fire.S14e01.Web.H264'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Chicago Fire
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Chicago.Fire.S14e01.Web.H264' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'President.Curtis.S01e05.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'President.Curtis.S01e05.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. President Curtis - S01E05 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'President.Curtis.S01e05.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series President Curtis
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'President.Curtis.S01e05.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'President.Curtis.S01e04.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'President.Curtis.S01e04.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. President Curtis - S01E04 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'President.Curtis.S01e04.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series President Curtis
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'President.Curtis.S01e04.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Furious.S01e07.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Furious.S01e07.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Furious - S01E07 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Furious.S01e07.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Furious
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Furious.S01e07.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Furious.S01e06.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Furious.S01e06.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Furious - S01E06 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Furious.S01e06.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Furious
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Furious.S01e06.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. The Walking Dead Dead City - S03E05 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series The Walking Dead Dead City
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'The.Walking.Dead.Dead.City.S03e05.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. The Walking Dead Dead City - S03E04 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Gl0p
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series The Walking Dead Dead City
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'The.Walking.Dead.Dead.City.S03e04.Web.H264-Gl0p' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Lanterns - S01E02 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Mtlqc
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Lanterns
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Lanterns.S01e02.Vff.Ad.Web.Ac3.5.1.H264-Mtlqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Lanterns - S01E01 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: French
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: Unknown v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: Frqc
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Lanterns
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Lanterns.S01e01.Vff.Web.Ac3.5.1.H264-Frqc' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Gomorra.Origins.S01e02.Web.X264' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Gomorra.Origins.S01e02.Web.X264'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Gomorra Origins - S01E02 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Gomorra.Origins.S01e02.Web.X264'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Gomorra Origins
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Gomorra.Origins.S01e02.Web.X264' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Processing release 'Gomorra.Origins.S01e01.Web.X264' from 'World-torrent (Prowlarr)'
2026-08-30 19:58:45.7|Debug|Parser|Parsing string 'Gomorra.Origins.S01e01.Web.X264'
2026-08-30 19:58:45.7|Debug|Parser|Episode Parsed. Gomorra Origins - S01E01 
2026-08-30 19:58:45.7|Debug|Parser|Languages parsed: Unknown
2026-08-30 19:58:45.7|Debug|QualityParser|Trying to parse quality for 'Gomorra.Origins.S01e01.Web.X264'
2026-08-30 19:58:45.7|Debug|Parser|Quality parsed: WEBDL-480p v1
2026-08-30 19:58:45.7|Debug|Parser|Release Group parsed: 
2026-08-30 19:58:45.7|Debug|ParsingService|No matching series Gomorra Origins
2026-08-30 19:58:45.7|Debug|DownloadDecisionMaker|Release 'Gomorra.Origins.S01e01.Web.X264' from 'World-torrent (Prowlarr)' rejected for the following reasons: [Permanent] Unknown Series
2026-08-30 19:58:45.7|Info|RssSyncService|RSS Sync Completed. Reports found: 40, Reports grabbed: 0
2026-08-30 19:58:45.7|Debug|PendingReleaseService|Removing failed releases from pending
2026-08-30 19:58:45.7|Debug|Sonarr.Http.Authentication.ApiKeyAuthenticationHandler|AuthenticationScheme: API was successfully authenticated.
2026-08-30 19:58:45.7|Debug|Api|[GET] /api/v3/command: 200.OK (0 ms)

  - *Conclusion retenue :* Le problème est identifié dans les logs à ces lignes clés : HTTP Error - Res: HTTP/1.1 [POST] http://decypharr:8282/api/v2/torrents/add: 400.BadRequest failed to process torrent: failed to submit torrent to debrid: failed to process torrent: realdebr...

- **Problématique / Instruction :** c'est en train de ma saouler la j'ai l'impression que c'est pas tres stable

  - *Conclusion retenue :* C'est tout à fait normal que ce soit frustrant : la chaîne Jellyseerr -> Sonarr -> Prowlarr -> Decypharr -> Real-Debrid -> Zurg -> Rclone -> Plex compte 7 intermédiaires . Dès qu'un maillon coince (ici Real-Debrid qui bloque un torrent précis via une...

- **Problématique / Instruction :** on va tester dmm

  - *Conclusion retenue :* C'est la solution la plus simple : tu gardes uniquement Zurg + Rclone et Plex . 1. Arrêter les services inutiles Pour alléger ta machine et éviter les conflits, tu peux couper les conteneurs de recherche automatique : docker compose stop decypharr pr...

- **Problématique / Instruction :** c'est vide

  - *Conclusion retenue :* Si le dossier reste vide après l'ajout sur DMM, vérifions l'état exact de Zurg et Rclone : 1. Regarder ce que voit le montage à la racine Exécute cette commande pour lister l'ensemble du point de montage : ls -la ~/debrid-stack/media Si tu vois des s...

- **Problématique / Instruction :** mvoies vide aussi

  - *Conclusion retenue :* Le montage FUSE de Rclone ne remonte pas sur l'hôte WSL car le volume n'a pas la propagation partagée ( rshared ) ou le conteneur Rclone n'a pas monté le bon sous-dossier. 1. Voir ce qui se trouve dans le conteneur Rclone Exécute cette commande pour ...

- **Problématique / Instruction :** ok du coup je revois toy story mais yá pas community

  - *Conclusion retenue :* Plex ignore le dossier Community parce qu'il se trouve dans la bibliothèque de Films (dans le dossier movies/ ) alors que sa structure de nommage correspond à une Série . Voici comment le rendre visible immédiatement : Solution la plus simple : Ajout...

- **Problématique / Instruction :** ok ça marchouille par contre le playback est un peu laggy

  - *Conclusion retenue :* Le lag en lecture avec Real-Debrid et Plex vient presque toujours de deux choses : le transcodage forcé (sur PS5) ou le buffer Rclone trop petit . Voici les réglages pour avoir une lecture fluide et instantanée : 1. Forcer le Direct Play sur la PS5 L...

- **Problématique / Instruction :** et du coup maintenant comment je fais pour le faire dpeuis mon telephone ?

  - *Conclusion retenue :* C'est encore plus simple depuis ton téléphone, car Debrid Media Manager est une Progressive Web App (PWA) parfaitement optimisée pour mobile. 1. Installer / Ouvrir Debrid Media Manager sur ton téléphone Ouvre le navigateur de ton téléphone (Safari su...

- **Problématique / Instruction :** ok mais pourquoi l ecran semble ne pas etre en fullscreen ? j'ai essayer dune ?

  - *Conclusion retenue :* La présence de bandes noires lors de la lecture de films comme Dune s'explique par deux causes principales : 1. Le ratio cinématographique d'origine (2.39:1) La quasi-totalité des films de cinéma (dont Dune ) est tournée au format cinémascope (2.35:1...

- **Problématique / Instruction :** j'ai pas mal de bufferiung ça dl le truc en lcoal ?

  - *Conclusion retenue :* Non, ça ne télécharge rien en local à l'avance : tu lis le fichier en streaming direct depuis les serveurs de Real-Debrid via le tunnel Rclone . Si tu as du buffering sur un gros fichier 4K (comme Dune ), c'est que le débit distant n'arrive pas assez...

- **Problématique / Instruction :** comment je supprime un fichier de plex ?

  - *Conclusion retenue :* Avec une stack Real-Debrid + Zurg , la suppression se fait directement à la source (sur Real-Debrid ou Debrid Media Manager), pas depuis Plex. Méthode 1 : Depuis Debrid Media Manager (Le plus rapide) Ouvre debridmediamanager.com sur ton téléphone ou ...

- **Problématique / Instruction :** Dernier petit souci comment je mets a jour la biblio depuis la ps5

  - *Conclusion retenue :* L'application Plex sur PS5 est un simple lecteur : elle ne possède pas de bouton administrateur pour forcer le serveur à rescanner le disque. Voici les deux manières simples de gérer ça depuis ton canapé sans retourner sur le PC : Méthode 1 : Forcer ...

- **Problématique / Instruction :** doc

  - *Conclusion retenue :* - image_bd6c05.png 30 août 2026, 18:51:10 CEST Tout est en ligne et sain ( healthy ). 1. Tester le streaming direct Va sur debridmediamanager.com et connecte ton compte Real-Debrid. Recherche un film ou une série populaire et clique sur Instant RD (o...

- **Problématique / Instruction :** ça cést les logs des tests

  - *Conclusion retenue :* - image_bc7f9e.png 30 août 2026, 18:16:12 CEST Les logs des trois dernières lignes donnent la solution exacte : /api/v1/webhook/jellyseerr renvoie 404 : la route n'existe pas dans Riven. /api/v1/webhook/overseerr renvoie 401 : la route est la bonne, ...

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Temps cumulé sur ce sujet :** 1182h11
> - **Sources épisodiques :**
>   - Session Gemini `6741935c6956aa2c` du 2026-08-30 (66 échanges, 698186 chars écrits)
> - **Connexions sémantiques :** [[Architecture_RAG]], [[Data_Engineering]]
