import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# In production, this MUST be set via environment variable
if 'SECRET_KEY' not in os.environ:
    if os.environ.get('DEBUG', 'False').lower() == 'true':
        # Development fallback - NEVER use in production
        SECRET_KEY = 'django-insecure-dev-key-only-for-local-development-change-this'
    else:
        raise ValueError('SECRET_KEY environment variable is required in production')
else:
    SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Parse ALLOWED_HOSTS from environment variable or use defaults
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver')
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_STR.split(',')]

# Add Render domain
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Make sure this is included
    'whitenoise.runserver_nostatic',  # Add WhiteNoise
    'core',  # Your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Online_Course.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database configuration for Render
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Import dj_database_url only when DATABASE_URL is provided so local
    # environments without the package installed won't fail during manage
    # commands like collectstatic.
    try:
        import dj_database_url
    except ImportError:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            'DATABASE_URL is set but dj_database_url is not installed. '
            'Install dj-database-url or unset DATABASE_URL.'
        )

    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Security Settings - Production only (disabled in DEBUG mode for local dev)
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0  # 1 year in production
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Additional security settings
SECURE_BROWSER_XSS_FILTER = not DEBUG
X_FRAME_OPTIONS = 'DENY' if not DEBUG else 'SAMEORIGIN'
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": (
        "'self'",
        "cdn.jsdelivr.net",
        "cdnjs.cloudflare.com",
    ),
    "style-src": (
        "'self'",
        "'unsafe-inline'",
        "cdn.jsdelivr.net",
        "cdnjs.cloudflare.com",
    ),
    "img-src": (
        "'self'",
        "data:",
    ),
    "font-src": (
        "'self'",
        "cdnjs.cloudflare.com",
    ),
} if not DEBUG else {}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# First check if razorpay is available
try:
    import razorpay  # noqa: F401
    RAZORPAY_PACKAGE_AVAILABLE = True
except ImportError:
    print('Warning: razorpay package not installed. Install it with: pip install razorpay')
    RAZORPAY_PACKAGE_AVAILABLE = False

# Razorpay Configuration
RAZORPAY_SETTINGS = {
    'ENABLED': os.environ.get('RAZORPAY_ENABLED', 'true').lower() == 'true',
    'KEY_ID': os.environ.get('RAZORPAY_KEY_ID'),
    'KEY_SECRET': os.environ.get('RAZORPAY_KEY_SECRET'),
    'CURRENCY': os.environ.get('RAZORPAY_CURRENCY', 'INR')
}

# Direct settings for easier access in views
RAZORPAY_ENABLED = RAZORPAY_PACKAGE_AVAILABLE and RAZORPAY_SETTINGS['ENABLED']
RAZORPAY_KEY_ID = RAZORPAY_SETTINGS['KEY_ID']
RAZORPAY_KEY_SECRET = RAZORPAY_SETTINGS['KEY_SECRET']
RAZORPAY_CURRENCY = RAZORPAY_SETTINGS['CURRENCY']

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}