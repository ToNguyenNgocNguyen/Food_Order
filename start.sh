#!/bin/bash

# Start the FastAPI backend
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 5000 --reload &

# Start the React frontend
cd /app/frontend
npm install && npm run dev
