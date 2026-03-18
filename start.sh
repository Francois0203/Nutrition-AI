#!/bin/bash

# Quick Start Script for Nutrition AI (macOS/Linux)

echo "====================================="
echo "  Nutrition AI - Quick Start"
echo "====================================="
echo ""

# Check if we're in the right directory
if [ ! -f "backend/app.py" ]; then
    echo "Error: Please run this script from the Nutrition-AI root directory"
    exit 1
fi

echo "Step 1: Starting Backend API Server..."
echo "====================================="
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if models exist
if [ ! -d "models" ]; then
    echo ""
    echo "Models not found. Running setup..."
    echo "This will take 5-10 minutes..."
    python setup.py
fi

echo ""
echo "Starting Flask API server..."
# Start backend in new terminal
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)' && source venv/bin/activate && python app.py"'
else
    # Linux
    gnome-terminal -- bash -c "cd $(pwd) && source venv/bin/activate && python app.py; exec bash"
fi

sleep 3

echo ""
echo "Step 2: Starting Frontend Development Server..."
echo "====================================="
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo ""
echo "Starting Vite dev server..."
# Start frontend in new terminal
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)' && npm run dev"'
else
    # Linux
    gnome-terminal -- bash -c "cd $(pwd) && npm run dev; exec bash"
fi

sleep 2

echo ""
echo "====================================="
echo "  Nutrition AI is starting!"
echo "====================================="
echo ""
echo "Backend API: http://localhost:5000"
echo "Frontend UI: http://localhost:5173"
echo ""
echo "Press Enter to exit..."
read
