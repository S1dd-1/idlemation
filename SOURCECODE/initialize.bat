@echo off
setlocal enabledelayedexpansion

REM Script is running inside SourceCode/
REM Python files are in SourceCode/PythonFiles/
REM Assets are in SourceCode/Assets/
REM Output goes to ../idlemation/

echo ===== BUILD ENGINE =====
pyinstaller "PythonFiles\engine.pyw" --windowed --noconfirm ^
    --workpath "../idlemation/build/engine" ^
    --distpath "../idlemation/dist/" ^
    --specpath "../idlemation"

echo ===== BUILD IDLEMATION =====
pyinstaller "PythonFiles/idlemation.py" --noconsole --onefile ^
    --workpath "../idlemation/build/idlemation" ^
    --distpath "../idlemation/dist/engine" ^
    --specpath "../idlemation"

echo ===== COPY EXTRA FILES =====

REM Ensure output asset folders exist
if not exist "..\idlemation\dist\engine\Animations" mkdir "..\idlemation\dist\engine\Animations"

REM Copy animations folder
xcopy ".\Assets\Animations" "..\idlemation\dist\engine\Animations" /E /I /Y >nul

REM Copy icon
copy ".\Assets\idlemation_icon.ico" "..\idlemation\dist\engine" >nul

REM Copy README
copy ".\Assets\README.md" "..\idlemation\dist\engine" >nul

echo ===== ALL BUILDS DONE =====
pause

