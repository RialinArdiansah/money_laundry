#!/bin/bash
set -e

# Build script for Vercel deployment
echo "Building Django static files..."

# Install Python dependencies
if [ -f requirements.txt ]; then
  python -m pip install -r requirements.txt
else
  echo "requirements.txt not found!"
  exit 1
fi

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files using production settings
python manage.py collectstatic --noinput --settings=system_laundry.production_settings --verbosity 2

echo "Build completed!"
