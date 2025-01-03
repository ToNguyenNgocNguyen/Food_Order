#!/bin/bash

# Load environment variables from .env file if it exists
[ -f .env ] && export $(grep -v '^#' .env | xargs)

# Default to port 5000 if PORT is not set
PORT=${PORT:-5000}

# Start the FastAPI backend
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port $PORT &

# Start the React frontend
cd /app/frontend
npm install && npm run dev
