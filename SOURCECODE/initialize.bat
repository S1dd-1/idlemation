@echo off
setlocal enabledelayedexpansion

echo ===== BUILD ENGINE =====
pyinstaller "PythonFiles\engine.pyw" --windowed --noconfirm ^
    --workpath "../IDLEMATION/build/engine" ^
    --distpath "../IDLEMATION/dist/" ^
    --specpath "../IDLEMATION"

echo ===== BUILD IDLEMATION =====
pyinstaller "PythonFiles/idlemation.py" --noconsole --onefile ^
    --workpath "../IDLEMATION/build/idlemation" ^
    --distpath "../IDLEMATION/dist/engine" ^
    --specpath "../IDLEMATION"

echo ===== COPY EXTRA FILES =====

REM Ensure output asset folders exist
if not exist "..\idlemation\dist\engine\Animations" mkdir "..\IDLEMATION\dist\engine\Animations"

REM Copy animations folder
xcopy ".\Assets\Animations" "..\IDLEMATION\dist\engine\Animations" /E /I /Y >nul

REM ===== ANIMATIONS FOLDER SUCCESSFUL =====

REM Copy icon
copy ".\Assets\idlemation_icon.ico" "..\IDLEMATION\dist\engine" >nul

REM ===== ICON SUCCESSFUL =====

REM Copy README
copy ".\README.md" "..\IDLEMATION" >nul

REM ===== README SUCCESSFUL =====

echo ===== ALL BUILDS DONE =====
pause
