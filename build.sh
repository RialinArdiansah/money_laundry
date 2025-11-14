#!/bin/bash

# Build script for Vercel deployment
echo "Building Django static files..."

# Install Python dependencies
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  echo "requirements.txt not found!"
  exit 1
fi

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed!"
