#!/usr/bin/env bash
# Test script to verify production build locally

echo "=== VTS College Production Build Test ==="
echo ""

echo "1. Setting environment variables..."
export DEBUG=false

echo "2. Cleaning old static files..."
python manage.py collectstatic --clear --noinput > /dev/null 2>&1

echo "3. Running migrations..."
python manage.py migrate --noinput > /dev/null 2>&1

echo "4. Checking admin functionality..."
python manage.py shell -c "
from django.contrib.auth.models import User
print(f'✓ Admin users in database: {User.objects.filter(is_staff=True).count()}')
"

echo "5. Testing static file collection..."
STATIC_FILES=$(find staticfiles -type f | wc -l)
echo "✓ Static files collected: $STATIC_FILES files"

echo "6. Verifying key static files..."
REQUIRED_FILES=(
    "staticfiles/css/style.css"
    "staticfiles/js/main.js"
    "staticfiles/images/logo.png"
)

for FILE in "${REQUIRED_FILES[@]}"; do
    if [ -f "$FILE" ]; then
        echo "✓ Found: $FILE"
    else
        echo "✗ Missing: $FILE"
    fi
done

echo ""
echo "=== Build Test Complete ==="
echo ""
echo "To start production server, run:"
echo "  gunicorn --bind 0.0.0.0:8000 Online_Course.wsgi:application --workers 4"
echo ""
