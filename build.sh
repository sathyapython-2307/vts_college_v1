#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files (WhiteNoise will serve these)
python manage.py collectstatic --no-input

# Display success message
echo "Build completed successfully!"
echo "Static files collected in: $(python manage.py findstatic css/style.css | head -1)"
