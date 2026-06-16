@echo off
REM Git commit and push script for Vision Inspector
REM Requires: Git installed and added to PATH

setlocal enabledelayedexpansion

cd /d c:\code

echo ========================================
echo Vision Inspector - Git Commit & Push
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo After installing, re-run this batch file
    pause
    exit /b 1
)

echo [OK] Git found
echo.

REM Configure git user if not already set
git config user.name "Vision Inspector" >nul 2>&1
if errorlevel 1 (
    echo Configuring Git user...
    git config --global user.name "Vision Inspector"
    git config --global user.email "inspector@example.com"
)

REM Initialize repo if needed
if not exist .git (
    echo Initializing repository...
    git init
)

echo.
echo [1/3] Adding files...
git add .
if errorlevel 1 (
    echo [ERROR] Failed to add files
    pause
    exit /b 1
)
echo [OK] Files added

echo.
echo [2/3] Creating commit...
git commit -m "Initial Vision Inspector project setup with UI and configuration modules"
if errorlevel 1 (
    echo [ERROR] Commit failed. No changes to commit or other error.
    pause
    exit /b 1
)
echo [OK] Commit created

echo.
echo [3/3] Setting up remote and pushing...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/cjs944666-gif/inspector1.git
if errorlevel 1 (
    echo [ERROR] Failed to set remote
    pause
    exit /b 1
)

REM Try to set main branch
git branch -M main >nul 2>&1

echo Pushing to GitHub...
git push -u origin main
if errorlevel 1 (
    echo [ERROR] Push failed. You may need to authenticate.
    echo.
    echo Options:
    echo 1. If using HTTPS, you may be prompted for GitHub username/password
    echo 2. Or use a Personal Access Token
    echo 3. For SSH, ensure your SSH keys are configured
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Push completed successfully!
echo ========================================
echo Repository: https://github.com/cjs944666-gif/inspector1
echo.
pause
