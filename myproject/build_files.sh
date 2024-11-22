#!/bin/bash

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Create the output directory for Vercel
echo "Preparing static files for Vercel..."
mkdir -p staticfiles_build
cp -R staticfiles/* staticfiles_build/
