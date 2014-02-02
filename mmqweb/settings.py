# Django settings for mmqweb project.

import os

DEBUG = os.getenv('PRODUCTION', 'False') == 'False'
TEMPLATE_DEBUG = DEBUG
print 'running with DEBUG=', DEBUG

ADMINS = (
    ('Xinruo Sun', 'xiaoruoruo@gmail.com'),
)

# email settings
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    OTP_SECRET = 'base32secret3232'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    from local_setting import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, SERVER_EMAIL, OTP_SECRET

MANAGERS = ADMINS

SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME' : os.path.join(SITE_ROOT, 'mmqweb.db')
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+6w5l6e8gvpzl=a$&e&_40n4+t%*)!#nm$4!hn)lbvn4mi9v0d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
        'django.template.loaders.app_directories.Loader',
    )
if not TEMPLATE_DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )

TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'club.views.AngularJsCsrfMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
)

ATOMIC_REQUESTS = True

HTML_MINIFY = True
EXCLUDE_FROM_MINIFYING = ('^static/',)
CSRF_COOKIE_NAME = 'XSRF-TOKEN'
INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'mmqweb.urls'

#TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#    os.path.join(SITE_ROOT,"templates/")
#)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'south',
    'tastypie',
    'reversion',
    'debug_toolbar',
# mmqweb's apps
    'namebook',
    'fight',
    'game',
    'club',
)

LOGIN_REDIRECT_URL = '/mmqweb/'
