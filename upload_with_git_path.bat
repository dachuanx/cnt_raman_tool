@echo off
echo ============================================================
echo 1D Materials Analysis Tool - GitHub Upload Script
echo ============================================================
echo.

REM Set git path
set GIT_PATH="D:\Program Files\Git\bin\git.exe"
echo Using git from: %GIT_PATH%
echo.

REM Check if git exists at the specified path
if not exist %GIT_PATH% (
    echo ERROR: Git not found at %GIT_PATH%
    echo Please check the path is correct.
    pause
    exit /b 1
)

REM Change to project directory
cd /d "G:\doctorcode\1DMaterialsAnalysisTool"

REM Step 1: Initialize git repository
echo Step 1: Initializing git repository...
if exist ".git" (
    echo   .git directory already exists
) else (
    %GIT_PATH% init
    if %errorlevel% neq 0 (
        echo   ERROR: Failed to initialize git repository
        pause
        exit /b 1
    )
    echo   ✓ Git repository initialized
)

REM Step 2: Add all files
echo.
echo Step 2: Adding files to git...
%GIT_PATH% add .
if %errorlevel% neq 0 (
    echo   ERROR: Failed to add files
    pause
    exit /b 1
)
echo   ✓ Files added to staging area

REM Step 3: Check if there are changes to commit
echo.
echo Step 3: Checking for changes to commit...
%GIT_PATH% status --porcelain > temp_status.txt
set /p changes=<temp_status.txt
del temp_status.txt

if "%changes%"=="" (
    echo   No changes to commit
    goto :setup_remote
)

REM Step 4: Commit changes
echo.
echo Step 4: Committing changes...
%GIT_PATH% commit -m "Initial commit: 1D Materials Analysis Tool with Raman and Absorption analysis"
if %errorlevel% neq 0 (
    echo   ERROR: Failed to commit changes
    pause
    exit /b 1
)
echo   ✓ Changes committed

:setup_remote
REM Step 5: Setup GitHub remote
echo.
echo Step 5: Setting up GitHub remote...
%GIT_PATH% remote -v | findstr "origin" >nul
if %errorlevel% equ 0 (
    echo   Remote 'origin' already exists, updating URL...
    %GIT_PATH% remote set-url origin https://github.com/dachuanx/cnt_raman_tool.git
) else (
    echo   Adding remote 'origin'...
    %GIT_PATH% remote add origin https://github.com/dachuanx/cnt_raman_tool.git
)

if %errorlevel% neq 0 (
    echo   ERROR: Failed to setup remote
    pause
    exit /b 1
)
echo   ✓ GitHub remote configured

REM Step 6: Push to GitHub
echo.
echo Step 6: Pushing to GitHub...
echo   Note: You may be prompted for GitHub credentials
echo.

REM Try to push to main branch
echo   Trying to push to 'main' branch...
%GIT_PATH% push -u origin main
if %errorlevel% neq 0 (
    echo   Failed to push to 'main', trying 'master' branch...
    
    REM Try master branch
    %GIT_PATH% push -u origin master
    if %errorlevel% neq 0 (
        echo   Failed to push to 'master', creating 'main' branch...
        
        REM Create main branch and push
        %GIT_PATH% branch -M main
        %GIT_PATH% push -u origin main
        if %errorlevel% neq 0 (
            echo   ERROR: Failed to push to GitHub
            echo.
            echo Possible reasons:
            echo 1. GitHub repository might not exist yet
            echo 2. Authentication issues (need GitHub credentials)
            echo 3. Network connectivity issues
            echo.
            echo Please check the repository exists at:
            echo   https://github.com/dachuanx/cnt_raman_tool
            echo.
            echo If the repository doesn't exist, create it first.
            echo You can create it at: https://github.com/new
            echo Repository name: cnt_raman_tool
            echo.
            echo After creating the repository, run this script again.
            pause
            exit /b 1
        )
    )
)

echo.
echo ============================================================
echo ✅ SUCCESS: Project uploaded to GitHub!
echo ============================================================
echo.
echo Repository URL: https://github.com/dachuanx/cnt_raman_tool
echo.
echo Summary of uploaded files:
echo - README.md (Project documentation in English)
echo - requirements.txt (Python dependencies)
echo - .gitignore (Git ignore rules)
echo - 1Dtool.py (Main application entry point)
echo - pages/ (Analysis modules)
echo   • page_raman.py (Raman spectroscopy analysis interface)
echo   • page_absorption.py (UV-Vis absorption analysis interface)
echo   • page_transmittance.py (Transmittance analysis interface)
echo - dist/1D_Materials_Analysis_Tool.exe (Windows executable, 112MB)
echo - upload_with_git_path.bat (This upload script)
echo.
echo Next steps:
echo 1. Visit https://github.com/dachuanx/cnt_raman_tool
echo 2. Verify all files are uploaded correctly
echo 3. Add a repository description
echo 4. Consider adding tags/releases for versioning
echo.
echo Project features:
echo • Raman spectroscopy analysis with peak detection
echo • UV-Vis absorption spectroscopy analysis
echo • Modern PyQt5-based user interface
echo • Dark/Light theme support
echo • Multi-file import and comparison
echo.
pause