---
id: "202608301552"
title: "ok bon jai deja un serveur plex"
type: "concept"
origin: ["gemini_takeout"]
semantic_topic: "Data_Engineering"
tags: ["data_engineering", "takeout_coldstart"]
created_at: "2026-08-30"
updated_at: "2026-08-30"
total_time_invested_min: 103
summary_1_line: "ok bon j'ai deja un serveur plex"
---

# ok bon jai deja un serveur plex

- **Problématique / Instruction :** ok bon j'ai deja un serveur plex

  - *Conclusion retenue :* Parfait, cela simplifie la démarche : tu n'as pas besoin de réinstaller ni de toucher à ton conteneur/binaire Plex actuel . Il suffit de lui brancher le disque virtuel et d'ajouter Riven. Ce qu'il te reste à déployer Tu as seulement 3 services légers...

- **Problématique / Instruction :** enfin ça tounr ejuste sur ma machine j'ai pas de serveur dedie

  - *Conclusion retenue :* Aucun problème, ça fonctionne exactement de la même manière sur ton PC principal. La seule différence par rapport à un serveur dédié, c'est que sous Windows , on s'épargne souvent la complexité de monter un système de fichiers virtuel FUSE via Docker...

- **Problématique / Instruction :** je veux un docker comme ça tout se lance en une commande

  - *Conclusion retenue :* Voici le pack complet pour tout lancer en une seule commande via Docker Desktop sur ton PC. Comme ton serveur Plex tourne déjà nativement sur ton PC Windows, les conteneurs Docker vont gérer : Zurg : l'intermédiaire avec l'API Real-Debrid. WebDAV / R...

- **Problématique / Instruction :** unable to get image 'spoked/riven:latest': error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.47/images/spoked/riven:latest/json": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.

  - *Conclusion retenue :* Cette erreur indique que le moteur Docker n'est pas démarré ou a planté sous Windows (le socket nommé dockerDesktopLinuxEngine est introuvable). Voici comment rétablir la connexion : 1. Démarrer Docker Desktop Lance l'application Docker Desktop depui...

- **Problématique / Instruction :** We've detected that you have an incompatible version of Windows.

Docker Desktop requires Windows 10 Pro/Enterprise/Home 22H2 (19045) or Windows 11 Pro/Enterprise/Home 23H2 (22631) or above.

To continue with the installation, upgrade Windows to a supported version and then re-run the installer.

  - *Conclusion retenue :* Deux options pour régler la situation : Option 1 : Mettre à jour Windows (pour conserver Docker) Docker Desktop bloque car ton build Windows est inférieur à la version minimale requise : Ouvre Paramètres Windows > Mise à jour et sécurité (Windows Upd...

- **Problématique / Instruction :** bah il me dit que je suis a jour windows update

  - *Conclusion retenue :* Windows Update indique parfois « À jour » alors que tu es bloqué sur une branche système plus ancienne (souvent Windows 10/11 version 21H2 ou 22H2 sans la mise à niveau de fonctionnalités proposée). Voici comment débloquer Docker sans attendre, ou ba...

- **Problématique / Instruction :** pas de .exe pour riven

  - *Conclusion retenue :* Riven est écrit en Python/TypeScript et n'est pas distribué sous forme de binaire Windows autonome (.exe). Pour lancer l'ensemble sous Windows sans machine virtuelle complexe, deux options directes s'offrent à toi : Option 1 : Utiliser plex_debrid (S...

- **Problématique / Instruction :** je regarde la doc https://riven.tv/docs/from-source et 'mca a l'air vachement casse couilles de passer sans docker

  - *Conclusion retenue :* En effet, compiler Riven depuis les sources ( Poetry , build du frontend avec Node/pnpm , gestion de la base de données) est fastidieux sous Windows. Si tu veux les avantages de Docker Compose sans subir le blocage de l'installateur Windows de Docker...

- **Problématique / Instruction :** https://github.com/debridmediamanager/debrid-media-manager ?

  - *Conclusion retenue :* Debrid Media Manager (DMM) est une excellente alternative, beaucoup plus simple et sans aucune maintenance locale. En réalité, tu n'as même pas besoin d'installer ou d'héberger DMM toi-même : il s'utilise directement via sa web app officielle gratuit...

- **Problématique / Instruction :** ouais mais du coiup je pourrais pas rechercher depuis la ps5

  - *Conclusion retenue :* C'est exactement la limite : avec Debrid Media Manager, ton smartphone devient ta télécommande de recherche, la PS5 ne servant que d'écran de lecture. Si tu veux impérativement tout faire à la manette depuis la PS5 (recherche Plex + Add to Watchlist ...

- **Problématique / Instruction :** sinon si j'updatea windows 11 ?

  - *Conclusion retenue :* Passer à Windows 11 (version 23H2 ou supérieure) règle définitivement le problème : Docker Desktop s'installera sans aucun blocage et supportera nativement WSL2. Tu pourras faire tourner la stack moderne Riven + Zurg + Rclone via un simple docker com...

- **Problématique / Instruction :** il y a toujours un unlocker pour windows 11 ? pour ''cracker''

  - *Conclusion retenue :* Pour l'activation de Windows 11 (passer d'une version non activée à une licence numérique permanente), la méthode de référence actuelle est le projet open source Microsoft-Activation-Scripts (MAS) . Il s'exécute directement via une commande PowerShel...

- **Problématique / Instruction :** j'ai un windows modifié du coup l'installer officiel ne marche pas je crois

  - *Conclusion retenue :* Les versions modifiées (AtlasOS, ReviOS, Tiny10/11 ou Ghost Spectre) suppriment souvent des composants système essentiels (services Windows Update, télémétrie, modules d'installation), ce qui bloque systématiquement l'installeur officiel Microsoft. D...

- **Problématique / Instruction :** Une distribution portant le nom fourni existe déjà. Utilisez --name pour choisir un autre nom.
Code d'erreur : Wsl/InstallDistro/ERROR_ALREADY_EXISTS

  - *Conclusion retenue :* Ubuntu est déjà installé sur ton WSL. Tu n'as pas besoin de le réinstaller. 1. Ouvrir directement Ubuntu Dans ton PowerShell ou invite de commandes, tape simplement : wsl (ou ouvre l'application Ubuntu directement depuis le menu Démarrer). Tu arrives...

- **Problématique / Instruction :** Échec de l’attachement du disque « C:\Users\Jijax\AppData\Local\wsl\{d99d32c7-fd1d-44be-a904-208b36ab2c95}\ext4.vhdx » à WSL2 : Le chemin d’accès spécifié est introuvable.Code d'erreur : Wsl/Service/CreateInstance/MountDisk/HCS/ERROR_PATH_NOT_FOUNDPS C:\windows\system32>

  - *Conclusion retenue :* Le fichier du disque virtuel ( ext4.vhdx ) a été supprimé ou déplacé, mais l'enregistrement de la distribution est resté dans le registre Windows. Voici comment réinitialiser l'enregistrement pour réinstaller proprement : 1. Lister les distributions ...

- **Problématique / Instruction :** Comment installer et démarrer Docker Engine dans la nouvelle instance Ubuntu ?

  - *Conclusion retenue :* Voici les commandes à exécuter directement dans ton terminal Ubuntu : 1. Mettre à jour les dépôts sudo apt update && sudo apt upgrade -y 2. Installer Docker Engine via le script officiel curl -fsSL https://get.docker.com -o get-docker.sh sudo sh get-...

- **Problématique / Instruction :** je viens de reinstaller tout a fonctionner mais j'ai fermer et relancer et j'ai ça PS C:\windows\system32> wsl
Échec de l’attachement du disque « C:\Users\Jijax\AppData\Local\wsl\{d99d32c7-fd1d-44be-a904-208b36ab2c95}\ext4.vhdx » à WSL2 : Le chemin d’accès spécifié est introuvable.
Code d'erreur : Wsl/Service/CreateInstance/MountDisk/HCS/ERROR_PATH_NOT_FOUND
PS C:\windows\system32> wsl ubuntu
Échec de l’attachement du disque « C:\Users\Jijax\AppData\Local\wsl\{d99d32c7-fd1d-44be-a904-208b36ab2c95}\ext4.vhdx » à WSL2 : Le chemin d’accès spécifié est introuvable.
Code d'erreur : Wsl/Service/CreateInstance/MountDisk/HCS/ERROR_PATH_NOT_FOUND
PS C:\windows\system32> wsl ubuntu-24.04
Échec de l’attachement du disque « C:\Users\Jijax\AppData\Local\wsl\{d99d32c7-fd1d-44be-a904-208b36ab2c95}\ext4.vhdx » à WSL2 : Le chemin d’accès spécifié est introuvable.
Code d'erreur : Wsl/Service/CreateInstance/MountDisk/HCS/ERROR_PATH_NOT_FOUND
PS C:\windows\system32>

  - *Conclusion retenue :* Ce problème survient fréquemment sur les Windows allégés : le dossier temporaire AppData\Local\wsl\ est nettoyé à la fermeture ou l'enregistrement dans le Registre Windows pointe vers un mauvais identifiant (GUID). Voici comment fixer définitivement ...

- **Problématique / Instruction :** Comment créer les dossiers et le docker-compose.yml pour Zurg et Riven dans Ubuntu WSL ?

  - *Conclusion retenue :* Voici les commandes à copier-coller dans ton terminal Ubuntu WSL pour créer l'arborescence, les fichiers de configuration et lancer la stack. 1. Créer l'arborescence des dossiers mkdir -p ~/debrid-stack/{zurg/data,rclone,riven/data,media} cd ~/debrid...

- **Problématique / Instruction :** comment je peux voir l'arborescence dans windows pour creer els fichiers ?

  - *Conclusion retenue :* Deux méthodes directes permettent d'ouvrir et manipuler l'arborescence Linux depuis Windows : Méthode 1 : Ouvrir l'Explorateur Windows depuis le terminal WSL (le plus rapide) Dans ton terminal Ubuntu, place-toi dans le dossier souhaité et tape : expl...

- **Problématique / Instruction :** j'ai lancer le compose et c'est bon c'est up

  - *Conclusion retenue :* Tout est en place. Il ne te reste que les 3 étapes de raccordement final : 1. Configurer Riven dans ton navigateur Ouvre http://localhost:3000 (ou http://IP_DE_TON_PC:3000 depuis ton téléphone). Renseigne ton token Real-Debrid . Clique sur Connect Pl...

- **Problématique / Instruction :** ça a l'air up mais j'ai pas acces a riven sur le port 3000

  - *Conclusion retenue :* Voici les causes possibles et comment résoudre le problème rapidement : 1. Vérifier les logs de Riven Riven prend souvent 20 à 30 secondes au premier démarrage (création de la base SQLite, migrations). Vérifie son statut dans le terminal Ubuntu : doc...

- **Problématique / Instruction :** redonner moi le docker coppose complet stp

  - *Conclusion retenue :* services: zurg: image: ghcr.io/debridmediamanager/zurg-testing:latest container_name: zurg restart: unless-stopped ports: - "9999:9999" volumes: - ./zurg/config.yml:/app/config.yml - ./zurg/data:/app/data rclone: image: rclone/rclone:latest container...

- **Problématique / Instruction :** il m'envoie pas d'api key

  - *Conclusion retenue :* Si la commande grep ne renvoie rien (les logs ont pu défiler ou être vidés), tu peux soit lire le fichier de configuration directement, soit définir toi-même une clé fixe dans ton docker-compose.yml . Méthode 1 : Lire la clé enregistrée dans le fichi...

- **Problématique / Instruction :** plex watchlist rss ?

  - *Conclusion retenue :* Si Riven te demande un champ Plex Watchlist RSS (ou si tu souhaites récupérer le flux RSS direct de ta Watchlist Plex) : Récupérer ton URL de flux RSS Plex Ouvre app.plex.tv dans ton navigateur et connecte-toi. Rends-toi dans l'onglet Liste de lectur...

- **Problématique / Instruction :** c'est obliger de l'ajouter ?

  - *Conclusion retenue :* Non, ce n'est pas obligatoire . Si tu as déjà connecté ton compte Plex via le bouton d'authentification / token à l'étape précédente, Riven communique directement via l'API Plex officielle. Le champ RSS sert uniquement de méthode alternative (de seco...

- **Problématique / Instruction :** ok c'est bon

  - *Conclusion retenue :* Tout est configuré côté Riven. Il ne te reste plus qu'à faire pointer tes bibliothèques Plex vers les dossiers de médias pour boucler la boucle. 1. Ajouter les dossiers dans Plex Media Server Sur ton serveur Plex (accessible sur http://localhost:3240...

- **Problématique / Instruction :** j'ai ajouter une serie a la watchlist mais rien ne se apsse

  - *Conclusion retenue :* Voici la méthode pour identifier immédiatement où la chaîne coince (Watchlist → Riven → Real-Debrid / Zurg → Plex) : 1. Suivre les logs de Riven en direct Dans ton terminal Ubuntu WSL, lance l'écoute des logs : docker compose logs -f riven Ensuite, e...

- **Problématique / Instruction :** riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.06s
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.04s
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.06s
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.02s
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.02s
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.04s
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.06s
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.07s
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | ❌ ERROR     | main.dispatch - Exception during request processing: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)
riven  | 26-08-30 14:58:36 | 👾 API       | main.dispatch - GET /api/v1/items - 500 - 0.10s
riven  | Exception in ASGI application
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  |
riven  | The above exception was the direct cause of the following exception:
riven  |
riven  | Traceback (most recent call last):
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 401, in run_asgi
riven  |     result = await app(  # type: ignore[func-returns-value]
riven  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
riven  |     return await self.app(scope, receive, send)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
riven  |     await super().__call__(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/applications.py", line 123, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
riven  |     await self.app(scope, receive, _send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 189, in __call__
riven  |     with collapse_excgroups():
riven  |   File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
riven  |     self.gen.throw(typ, value, traceback)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_utils.py", line 93, in collapse_excgroups
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 191, in __call__
riven  |     response = await self.dispatch_func(request, call_next)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/main.py", line 28, in dispatch
riven  |     response = await call_next(request)
riven  |                ^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 165, in call_next
riven  |     raise app_exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/base.py", line 151, in coro
riven  |     await self.app(scope, receive_or_disconnect, send_no_error)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
riven  |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 756, in __call__
riven  |     await self.middleware_stack(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 776, in app
riven  |     await route.handle(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 297, in handle
riven  |     await self.app(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 77, in app
riven  |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
riven  |     raise exc
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
riven  |     await app(scope, receive, sender)
riven  |   File "/app/.venv/lib/python3.11/site-packages/starlette/routing.py", line 72, in app
riven  |     response = await func(request)
riven  |                ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 278, in app
riven  |     raw_response = await run_endpoint_function(
riven  |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
riven  |     return await dependant.call(**values)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/riven/src/routers/secure/items.py", line 165, in get_items
riven  |     total_items = session.execute(
riven  |                   ^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
riven  |     return self._execute_internal(
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal
riven  |     conn = self._connection_for_bind(bind)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind
riven  |     return trans._connection_for_bind(engine, execution_options)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "<string>", line 2, in _connection_for_bind
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
riven  |     ret_value = fn(self, *arg, **kw)
riven  |                 ^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind
riven  |     conn = bind.connect()
riven  |            ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3277, in connect
riven  |     return self._connection_cls(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
riven  |     Connection._handle_dbapi_exception_noconnection(
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 2440, in _handle_dbapi_exception_noconnection
riven  |     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
riven  |     self._dbapi_connection = engine.raw_connection()
riven  |                              ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3301, in raw_connection
riven  |     return self.pool.connect()
riven  |            ^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 447, in connect
riven  |     return _ConnectionFairy._checkout(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
riven  |     fairy = _ConnectionRecord.checkout(pool)
riven  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
riven  |     rec = pool._do_get()
riven  |           ^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
riven  |     return self._create_connection()
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
riven  |     return _ConnectionRecord(self)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
riven  |     self.__connect()
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
riven  |     with util.safe_reraise():
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
riven  |     raise exc_value.with_traceback(exc_tb)
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
riven  |     self.dbapi_connection = connection = pool._invoke_creator(self)
riven  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 661, in connect
riven  |     return dialect.connect(*cargs, **cparams)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 629, in connect
riven  |     return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  |   File "/app/.venv/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
riven  |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
riven  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
riven  | sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  | connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
riven  |        Is the server running on that host and accepting TCP/IP connections?
riven  |
riven  | (Background on this error at: https://sqlalche.me/e/20/e3q8)

  - *Conclusion retenue :* L'erreur vient de la ligne Database Host au Step 1 : Riven a enregistré la valeur d'exemple PostgreSQL ( postgresql+psycopg2://... ), et tente de joindre un serveur PostgreSQL sur le port 5432 qui n'existe pas dans ta stack. Pour fonctionner sans bas...

- **Problématique / Instruction :** j'ai fermer powershell utu peux me donner le cd pour retourner dans le dossier debridstack

  - *Conclusion retenue :* Si tu ouvres PowerShell , lance d'abord WSL puis déplace-toi dans le dossier : wsl cd ~/debrid-stack Si tu es déjà dans ton terminal Ubuntu / WSL : cd ~/debrid-stack...

- **Problématique / Instruction :** ok j'ai mis a jour le settings.json

  - *Conclusion retenue :* Relance le conteneur pour charger la nouvelle configuration : docker compose restart riven Vérification du bon fonctionnement Vérifie les logs : docker compose logs -f riven Tu dois voir le démarrage propre sur SQLite sans aucune erreur de connexion ...

- **Problématique / Instruction :** ça demande vip et c'est payant

  - *Conclusion retenue :* Trakt a en effet verrouillé la création de nouvelles applications API derrière son abonnement VIP. Inutile de payer : tu peux soit utiliser un proxy public pour Trakt , soit basculer l'indexation sur TMDb / IMDb directement. Option 1 (La plus simple)...

- **Problématique / Instruction :** il me dit que j'ai pas set d'api key pour trakt

  - *Conclusion retenue :* Pour utiliser le proxy sans compte payant, Riven a simplement besoin d'une chaîne de caractères dans le champ de la clé pour valider le formulaire. Méthode 1 : Configurer le proxy avec un faux identifiant Dans Settings > Content Providers / Indexers ...

- **Problématique / Instruction :** les champs existant sont oauth client id et secret

  - *Conclusion retenue :* Remplis directement ces deux champs avec les identifiants publics suivants : OAuth Client ID : 353a8de972986be67a74797079234850e50e82c5f9408287532a26fae3cf55ff OAuth Client Secret : 9640824b611dc82221b6582379f60ff2084c7c64a4b4bb2e8fae84323678516d App...

- **Problématique / Instruction :** c'est fait mais il opcntinue d'essayer de passer par traktr

  - *Conclusion retenue :* Trakt est resté configuré comme indexeur par défaut dans la file d'attente interne de Riven ( TraktIndexer ). Pour forcer Riven à purger la tâche bloquée et basculer sur MDBList : 1. Vider la file d'attente bloquée et forcer l'indexeur Dans l'interfa...

- **Problématique / Instruction :** relation ''items'' does not exist

  - *Conclusion retenue :* La table s'appelle en réalité item (au singulier) dans le schéma PostgreSQL de Riven. Voici les commandes pour purger proprement la base sans erreur : 1. Purger la file d'attente Exécute cette commande dans ton terminal : docker compose exec postgres...

- **Problématique / Instruction :** yá pas de bouton authenticate with trakt

  - *Conclusion retenue :* Sur cette version de Riven, le bouton d'authentification Trakt n'apparaît que si l'API officielle de Riven est autorisée ou si le backend fournit un code d'activation PIN direct. Voici les deux solutions directes pour débloquer Trakt : Solution 1 : G...

- **Problématique / Instruction :** error client not found

  - *Conclusion retenue :* Trakt a révoqué les anciennes clés publiques génériques. Pour éviter le système d'API verrouillé de Trakt, utilise la clé TMDb (The Movie Database) ou les identifiants officiels actifs de Riven via une passerelle de métadonnées. Voici les deux soluti...

> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)
> - **Temps cumulé sur ce sujet :** 1h43
> - **Sources épisodiques :**
>   - Session Gemini `7b59d8d3da4143bb_s02_20260830` du 2026-08-30 (37 échanges, 230561 chars écrits)
> - **Connexions sémantiques :** [[Architecture_RAG]], [[Data_Engineering]]
