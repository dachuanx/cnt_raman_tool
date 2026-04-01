@echo off
echo ============================================================
echo 1D Materials Analysis Tool - GitHub Upload Script
echo ============================================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH.
    echo Please install Git from: https://git-scm.com/download/win
    echo Then run this script again.
    pause
    exit /b 1
)

echo Git found. Starting upload process...
echo.

REM Change to project directory
cd /d "G:\doctorcode\1DMaterialsAnalysisTool"

REM Step 1: Initialize git repository
echo Step 1: Initializing git repository...
if exist ".git" (
    echo   .git directory already exists
) else (
    git init
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
git add .
if %errorlevel% neq 0 (
    echo   ERROR: Failed to add files
    pause
    exit /b 1
)
echo   ✓ Files added to staging area

REM Step 3: Check if there are changes to commit
echo.
echo Step 3: Checking for changes to commit...
git status --porcelain > temp_status.txt
set /p changes=<temp_status.txt
del temp_status.txt

if "%changes%"=="" (
    echo   No changes to commit
    goto :setup_remote
)

REM Step 4: Commit changes
echo.
echo Step 4: Committing changes...
git commit -m "Initial commit: 1D Materials Analysis Tool with Raman and Absorption analysis"
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
git remote -v | findstr "origin" >nul
if %errorlevel% equ 0 (
    echo   Remote 'origin' already exists, updating URL...
    git remote set-url origin https://github.com/dachuanx/cnt_raman_tool.git
) else (
    echo   Adding remote 'origin'...
    git remote add origin https://github.com/dachuanx/cnt_raman_tool.git
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

REM Try to push to main branch
git push -u origin main
if %errorlevel% neq 0 (
    echo   Trying alternative approaches...
    
    REM Try master branch
    git push -u origin master
    if %errorlevel% neq 0 (
        REM Create main branch and push
        git branch -M main
        git push -u origin main
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
echo Files uploaded:
echo - README.md (Project documentation)
echo - requirements.txt (Dependencies)
echo - .gitignore (Git ignore file)
echo - 1Dtool.py (Main application)
echo - pages/ (Analysis modules)
echo   - page_raman.py (Raman spectroscopy analysis)
echo   - page_absorption.py (Absorption spectroscopy analysis)
echo   - page_transmittance.py (Transmittance analysis)
echo - dist/1D_Materials_Analysis_Tool.exe (Windows executable)
echo.
echo Next steps:
echo 1. Visit https://github.com/dachuanx/cnt_raman_tool
echo 2. Verify all files are uploaded correctly
echo 3. Update repository description if needed
echo.
pause