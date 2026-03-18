@echo off
REM Quick Start Script for Nutrition AI

echo =====================================
echo   Nutrition AI - Quick Start
echo =====================================
echo.

REM Check if we're in the right directory
if not exist "backend\app.py" (
    echo Error: Please run this script from the Nutrition-AI root directory
    pause
    exit /b 1
)

echo Step 1: Starting Backend API Server...
echo =====================================
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Check if models exist
if not exist "models" (
    echo.
    echo Models not found. Running setup...
    echo This will take 5-10 minutes...
    python setup.py
)

echo.
echo Starting Flask API server...
start cmd /k "cd /d %CD% && venv\Scripts\activate.bat && python app.py"

timeout /t 3 /nobreak > nul

echo.
echo Step 2: Starting Frontend Development Server...
echo =====================================
cd ..\frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

echo.
echo Starting Vite dev server...
start cmd /k "cd /d %CD% && npm run dev"

timeout /t 3 /nobreak > nul

echo.
echo =====================================
echo   Nutrition AI is starting!
echo =====================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:5173
echo.
echo Press any key to exit this window...
echo (The servers will continue running in the other windows)
pause > nul
