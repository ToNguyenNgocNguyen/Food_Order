#!/bin/bash

# Load environment variables from .env file if it exists
[ -f .env ] && export $(grep -v '^#' .env | xargs)

# Default ports if not set in .env
BACKEND_PORT=${BACKEND_PORT:-5000}
FRONTEND_PORT=${FRONTEND_PORT:-3000}

# Start the FastAPI backend
echo "Starting FastAPI backend on port $BACKEND_PORT..."
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT &

# Start the React frontend
echo "Starting React frontend on port $FRONTEND_PORT..."
cd /app/frontend
npm install
npm run dev -- --port $FRONTEND_PORT
