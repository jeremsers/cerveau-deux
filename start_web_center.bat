@echo off
setlocal enabledelayedexpansion
title Exocortex Web Command Center (FastAPI + GUI Web Moderne)

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] Python est introuvable dans le PATH. Veuillez installer Python 3.11+.
    pause
    exit /b 1
)

echo ============================================================
echo === EXOCORTEX // COGNITIVE COMMAND CENTER (v0.5.3 SOTA) ===
echo ===       Serveur Web FastAPI & Interface Web Moderne    ===
echo ============================================================
echo.
echo Demarrage du serveur sur http://127.0.0.1:8500...
echo Votre navigateur par defaut va s'ouvrir automatiquement.
echo.

python run_exocortex.py --web

pause

