#!/bin/bash

# Build script for Vercel deployment
echo "Building Django static files..."

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed!"