#!/bin/sh

# Exit on error
set -e

echo "Database..."
sleep 5

echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000