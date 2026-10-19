@echo off
title Arret des Demons Exocortex
echo ============================================================
echo ===         ARRET DES DEMONS EXOCORTEX EN COURS          ===
echo ============================================================
echo.

echo Recherche et arret des processus telemetry_daemon et hippocampus_hotkey...

wmic process where "commandline like '%%src.daemons.telemetry_daemon%%' and name like 'python%%'" call terminate >nul 2>nul
wmic process where "commandline like '%%src.daemons.hippocampus_hotkey%%' and name like 'python%%'" call terminate >nul 2>nul

powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*src.daemons.telemetry_daemon*' -or $_.CommandLine -like '*src.daemons.hippocampus_hotkey*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>nul

echo.
echo [OK] Tous les demons d'arriere-plan Exocortex ont ete arretes avec succes.
echo Empreinte memoire et CPU liberees.
echo.
pause

