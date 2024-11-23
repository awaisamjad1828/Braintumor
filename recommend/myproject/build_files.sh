#!/bin/bash

# Collect static files into STATIC_ROOT
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Create the output directory for Vercel
echo "Preparing static files for Vercel..."
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/
