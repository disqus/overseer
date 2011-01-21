import os.path

OVERSEER_ROOT = os.path.dirname(__import__('overseer').__file__)

DEBUG = True

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'overseer.sqlite'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'devserver',
    'overseer',
)

ADMIN_MEDIA_PREFIX = '/admin/media/'

ROOT_URLCONF = 'urls'

DEVSERVER_MODULES = ()

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(OVERSEER_ROOT, 'templates', 'overseer'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'overseer.context_processors.default',
)

try:
    from local_settings import *
except ImportError:
    pass