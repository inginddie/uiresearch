#!/bin/bash
# Start script for Railway deployment

# Use PORT from environment or default to 8000
PORT=${PORT:-8000}

echo "Starting UIResearch on port $PORT"

# Start uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
