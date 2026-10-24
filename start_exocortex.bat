@echo off
setlocal enabledelayedexpansion
title Exocortex & Telemetrie Cognitive - Lanceur Windows

:: Optimisations VRAM pour Ollama (RTX 4070 Ti Super 16 Go) : ces variables doivent etre vues par
:: le SERVEUR Ollama, qui tourne dans son propre processus. Les poser ici (set) n'a aucun effet
:: (v0.5.7, C1). A faire une fois, puis redemarrer Ollama :
::   setx OLLAMA_FLASH_ATTENTION 1
::   setx OLLAMA_KV_CACHE_TYPE q8_0
::   setx OLLAMA_MAX_LOADED_MODELS 1
::   setx OLLAMA_NUM_PARALLEL 1
:: L'etape [0/3] ci-dessous verifie la configuration reelle du serveur et previent si elle manque.

echo ============================================================
echo ===      EXOCORTEX & TELEMETRIE COGNITIVE (V2.0)         ===
echo ===       Architecture Locale & Infrence Hybride        ===
echo ============================================================
echo.

cd /d "%~dp0"

:: Verification de Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] Python est introuvable dans le PATH. Veuillez installer Python 3.11+.
    pause
    exit /b 1
)

:: Determination de l'executable pythonw (arriere-plan silencieux sans console)
set PYTHONW_EXE=pythonw.exe
where %PYTHONW_EXE% >nul 2>nul
if %errorlevel% neq 0 (
    set PYTHONW_EXE=python.exe
)

echo [0/3] Verification du serveur Ollama et provisioning des modeles GGUF locaux...
python run_exocortex.py --init-models

echo.
echo [1/3] Demarrage silencieux du Demon de Telemetrie Temps Reel (Module 2)...
start "" %PYTHONW_EXE% -m src.daemons.telemetry_daemon

echo [2/3] Demarrage silencieux de l'Injecteur Hippocampe (Ctrl+Alt+Espace, Module 5)...
start "" %PYTHONW_EXE% -m src.daemons.hippocampus_hotkey

echo [3/3] Lancement du Command Center Web (interface principale depuis v0.5.0)...
echo.
echo Les demons d'arriere-plan tournent silencieusement (0 Mo VRAM, 0%% CPU au repos).
echo Pour tout arreter proprement, executez 'stop_exocortex.bat'.
echo Le dashboard Streamlit historique reste disponible : python run_exocortex.py --dashboard
echo.
echo Ouverture du Command Center dans votre navigateur (http://127.0.0.1:8500)...
echo ============================================================

python run_exocortex.py --web

pause
