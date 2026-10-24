@echo off
title Arret de l'Exocortex
echo ============================================================
echo ===            ARRET DE L'EXOCORTEX EN COURS             ===
echo ============================================================
echo.

cd /d "%~dp0"

:: v0.5.6 (E4) : arret propre. Les demons recoivent un signal (fichier stop_daemons.flag),
:: sauvegardent la fenetre en cours puis s'arretent ; le serveur web et Streamlit sont
:: ensuite arretes. Plus de dependance a wmic (absent de Windows 11 recents).
python run_exocortex.py --stop

echo.
echo [OK] Demons, serveur web et dashboard Exocortex arretes.
echo.
pause
