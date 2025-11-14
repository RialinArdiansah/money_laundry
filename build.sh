#!/usr/bin/env bash
set -euo pipefail

# Build script for Vercel deployment
echo "Building Django static files..."

# Ensure Django uses production settings during build
export DJANGO_SETTINGS_MODULE=system_laundry.production_settings

# Install Python dependencies
if [ -f requirements.txt ]; then
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
else
  echo "requirements.txt not found!"
  exit 1
fi

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput --verbosity 2

# List output to help Vercel verify directory is not empty
echo "Staticfiles content:"
ls -la staticfiles || true

echo "Build completed!"
