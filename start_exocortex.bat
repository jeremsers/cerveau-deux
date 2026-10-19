@echo off
setlocal enabledelayedexpansion
title Exocortex & Telemetrie Cognitive - Lanceur Windows

:: Optimisations VRAM pour Ollama sur NVIDIA RTX 4070 Ti Super 16 Go
set OLLAMA_FLASH_ATTENTION=1
set OLLAMA_KV_CACHE_TYPE=q8_0
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_NUM_PARALLEL=1

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

echo [0/3] Provisioning des modeles GGUF locaux dans Ollama...
python run_exocortex.py --init-models

echo.
echo [1/3] Demarrage silencieux du Demon de Telemetrie Temps Reel (Module 2)...
start "" %PYTHONW_EXE% -m src.daemons.telemetry_daemon

echo [2/3] Demarrage silencieux de l'Injecteur Hippocampe Alt+Espace (Module 5)...
start "" %PYTHONW_EXE% -m src.daemons.hippocampus_hotkey

echo [3/3] Lancement du Dashboard Analytique Streamlit "Bandeur de Stats" (Module 6)...
echo.
echo Les demons d'arriere-plan tournent silencieusement (0 Mo VRAM, 0%% CPU au repos).
echo Pour stopper les demons d'arriere-plan, executez 'stop_exocortex.bat'.
echo.
echo Ouverture du tableau de bord dans votre navigateur...
echo ============================================================

python -m streamlit run src/dashboard/app.py --server.headless=false --theme.base=dark

pause

