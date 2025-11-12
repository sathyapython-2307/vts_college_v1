# VTS College - Online Learning Platform

A Django-based online course delivery platform with integrated payment processing, course management, and progress tracking.

## Features

- **Course Management**: Browse, search, and enroll in courses
- **User Authentication**: Secure login and registration
- **Payment Integration**: Razorpay integration for course payments
- **Progress Tracking**: Track course progress and completion
- **Certificate Generation**: Generate and download certificates
- **Admin Dashboard**: Comprehensive admin panel for course and user management
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Static File Optimization**: WhiteNoise for efficient static file serving

## Technology Stack

### Backend
- **Framework**: Django 4.2.13
- **Database**: PostgreSQL (production), SQLite (development)
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise

### Frontend
- **CSS**: Bootstrap 5, Custom CSS
- **JavaScript**: Vanilla JS, Bootstrap JS
- **Icons**: Font Awesome 6

### Payment
- **Gateway**: Razorpay

### Deployment
- **Platform**: Render.com
- **Database**: PostgreSQL (Render managed)

## Project Structure

```
vts_college-main/
├── Online_Course/          # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── core/                  # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # Request handlers
│   ├── urls.py            # App URL routing
│   ├── admin.py           # Admin customization
│   └── migrations/        # Database migrations
├── templates/             # HTML templates
├── static/               # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── media/                # User uploads
├── requirements.txt      # Python dependencies (pinned versions)
├── manage.py            # Django management script
├── Procfile             # Render deployment config
├── render.yaml          # Render infrastructure config
├── build.sh             # Build script for deployment
├── runtime.txt          # Python version specification
├── .env.example         # Environment variables template
└── DEPLOYMENT_GUIDE.md  # Deployment documentation
```

## Installation

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Virtual environment (venv)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vts_college-main
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (macOS/Linux)
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   ```
   DEBUG=true
   SECRET_KEY=your-local-secret-key
   DATABASE_URL=sqlite:///db.sqlite3
   RAZORPAY_ENABLED=false
   ```

5. **Initialize database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Visit http://localhost:8000

## Configuration

### Environment Variables

See `.env.example` for all available variables:

| Variable | Purpose | Required |
|----------|---------|----------|
| `DEBUG` | Enable debug mode | Development only |
| `SECRET_KEY` | Django secret key | Production (auto-generated) |
| `DATABASE_URL` | Database connection string | Production |
| `ALLOWED_HOSTS` | Allowed hostnames | Production |
| `RAZORPAY_ENABLED` | Enable payment processing | If using payments |
| `RAZORPAY_KEY_ID` | Razorpay API key | If using payments |
| `RAZORPAY_KEY_SECRET` | Razorpay secret key | If using payments |

### Static Files

Static files are configured to use WhiteNoise for efficient serving in production.

**Development**: Django automatically serves static files when `DEBUG=true`

**Production**: Run `python manage.py collectstatic --noinput` during build

## Deployment to Render

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for complete deployment instructions.

### Quick Deploy Checklist

1. ✅ Ensure all code committed to Git
2. ✅ Verify `requirements.txt` has pinned versions
3. ✅ Set `DEBUG=false` in production environment
4. ✅ Ensure `SECRET_KEY` is set in Render environment
5. ✅ Configure database connection (PostgreSQL)
6. ✅ Set API keys (Razorpay, etc.) as encrypted environment variables
7. ✅ Deploy using Render's GitHub integration

**Expected URL after deployment**:
```
https://vts-college.onrender.com
```

## Testing

### Database Migrations

```bash
# Check pending migrations
python manage.py migrate --plan

# Apply migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations
```

### Admin Interface

```bash
# Access admin panel
# Visit http://localhost:8000/admin
# Login with superuser credentials created during setup
```

### Static Files

```bash
# Find specific static file
python manage.py findstatic css/style.css

# List all static files
python manage.py findstatic --list
```

## Development Workflow

### Add a New Feature

1. Create migrations if changing models:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Test locally:
   ```bash
   python manage.py runserver
   ```

3. Test with production settings:
   ```bash
   DEBUG=false python manage.py collectstatic --noinput
   gunicorn Online_Course.wsgi:application --bind 0.0.0.0:8000
   ```

4. Commit and push:
   ```bash
   git add .
   git commit -m "Add feature description"
   git push origin main
   ```

### Debugging

Enable debug logging:
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'DEBUG'},
    },
}
```

Access Django shell:
```bash
python manage.py shell
```

## Troubleshooting

### "Static files not loading (404 errors)"

1. Ensure WhiteNoise is in MIDDLEWARE:
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
       ...
   ]
   ```

2. Run collectstatic:
   ```bash
   python manage.py collectstatic --clear --noinput
   ```

3. Verify STATIC_ROOT and STATICFILES_DIRS in settings.py

### "SECRET_KEY environment variable required"

This occurs in production (DEBUG=false) when SECRET_KEY is not set:
```bash
# Set in Render environment variables
# Or locally:
export SECRET_KEY="your-secret-key"
```

### "Database connection refused"

1. Verify DATABASE_URL is set
2. Check PostgreSQL is running (if using local DB)
3. Verify credentials in DATABASE_URL

## Performance Optimization

### Static File Optimization
- WhiteNoise caches static files with compression
- CSS and JS are minified
- Images are optimized

### Database Optimization
- Use database indexes for frequently queried fields
- Consider caching with Redis (future enhancement)

### Server Configuration
- Gunicorn configured with multiple workers
- Connection pooling for database
- Session timeout optimized

## Security

### Configuration
- ✅ DEBUG disabled in production
- ✅ SECURE_SSL_REDIRECT enabled in production
- ✅ CSRF protection enabled
- ✅ XSS protection enabled
- ✅ HSTS headers enabled
- ✅ Secure cookies enabled
- ✅ Content Security Policy configured

### Secrets Management
- ✅ SECRET_KEY generated and not in version control
- ✅ API keys encrypted in environment variables
- ✅ Database credentials via DATABASE_URL
- ✅ No credentials in `.env.example` file

### Data Protection
- ✅ User passwords hashed with Django's strong algorithms
- ✅ CSRF tokens on all forms
- ✅ SQL injection prevention via ORM
- ✅ XSS protection via template escaping

## Performance Metrics

- ✅ Homepage load time: < 2 seconds
- ✅ Static file serving: < 100ms
- ✅ Database queries optimized with select_related/prefetch_related
- ✅ Responsive design works on all devices

## Contributing

1. Create a new branch for your feature
2. Make changes and test locally
3. Push to GitHub
4. Create a Pull Request
5. Code review and merge to main

## Documentation

- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Complete deployment and rollback guide
- [.env.example](./.env.example) - Environment variables reference
- Django docs: https://docs.djangoproject.com/
- Render docs: https://render.com/docs

## Support

For issues or questions:
1. Check the DEPLOYMENT_GUIDE.md troubleshooting section
2. Review error logs in Render Dashboard
3. Check Django documentation
4. Review code comments and docstrings

## License

[Add your license here]

## Changelog

### v1.0 (Current)
- ✅ Complete production configuration
- ✅ WhiteNoise static file serving
- ✅ Gunicorn WSGI server
- ✅ PostgreSQL database support
- ✅ Environment variable configuration
- ✅ Comprehensive deployment guide
- ✅ Security hardening

---

**Last Updated**: November 2025
**Maintained By**: VTS College Team
