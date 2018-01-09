"""
Django settings for ozsales project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n(jg24woqhp5e-9%r@vbm249e5yeqj%8t!1l*h=x%%o4d73g$6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ('0.0.0.0', '127.0.0.1')

# Application definition
INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    # 'material',
    # 'material.frontend',
    # 'material.admin',
    'dal',
    'dal_select2',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_webtest',
    'django_nose',
    'dbsettings',
    'djcelery',
    'tinymce',
    'kombu.transport.django',

    # common app
    'core.commands',  # customized django commands
    'core.auth_user',
    'core.adminlte',
    'core.messageset',
    'core.autocode',
    'core.payments.stripe',

    'apps.member',
    'apps.express',
    'apps.customer',
    'apps.product',
    'apps.order',
    'apps.store',
    'apps.report',
    'apps.schedule',
    'apps.weixin',
    'core.sms',
    'utils',

    # third_app
    'mptt',
    'django_js_reverse',
    'activelink',
    'rest_framework',
    'rest_framework.authtoken',  # must come after accounts for migrations to work
    'taggit',
    'djstripe',
    'stdimage',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.django.middleware.ProfileAuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'core.libs.middleware.ApiPermissionCheck',
    # 'core.libs.middleware.MenuMiddleware',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ozsales',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

SITE_ID = 1
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

LANGUAGES = [
    ('cn', _('Simplified Chinese')),
    ('en', _('English')),
]

TIME_ZONE = 'Australia/Melbourne'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

DATE_FORMAT = 'Y/m/j'
DATETIME_FORMAT = 'Y/m/j H:i:s'
TIME_FORMAT = 'H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'env', 'collectstatic')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
MEDIA_URL = '/media/'

TEMP_ROOT = os.path.join(MEDIA_ROOT, 'temp')

# Templates
# List of callables that know how to import templates from various sources.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # 'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'dev@luotao.net'

# Auth
AUTH_USER_MODEL = 'auth_user.AuthUser'
AUTH_PROFILE_MODULE = 'member.seller'
AUTHENTICATION_BACKENDS = ['core.auth_user.backend.AuthUserAuthenticateBackend']
LOGIN_URL = '/member/login/'

LOGOUT_URL = '/member/logout/'

LOGIN_REDIRECT_URL = '/member/profile/'

SESSION_COOKIE_AGE = 604800 * 4  # 1 week

# registration
# ACCOUNT_ACTIVATION_DAYS=7
# REGISTRATION_OPEN=True
# REGISTRATION_SALT='IH*&^AGBIovalaft1AXbas2213klsd73'


# Others
ID_PHOTO_FOLDER = 'id'

PRODUCT_PHOTO_FOLDER = 'product'

# for django-guardian
ANONYMOUS_USER_ID = -1

# Test
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

# ----------------------------------------- CELERY -----------------------------------------------

import djcelery

djcelery.setup_loader()

BROKER_URL = 'redis://127.0.0.1:6379'
BROKER_TRANSPORT = 'redis'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 604800}
CELERY_RESULT_BACKEND = BROKER_URL

CELERY_TASK_RESULT_EXPIRES = datetime.timedelta(days=1)  # Take note of the CleanUp task in middleware/tasks.py
CELERY_MAX_CACHED_RESULTS = 1000
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_TRACK_STARTED = True
CELERY_SEND_EVENTS = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

REDIS_CONNECT_RETRY = True
REDIS_DB = 0
BROKER_POOL_LIMIT = 2
CELERYD_CONCURRENCY = 1
CELERYD_TASK_TIME_LIMIT = 600

# ----------------------------------------- TINYMCE -----------------------------------------------

TINYMCE_JS_URL = '/static/tinymce/js/tinymce/tinymce.min.js'
TINYMCE_SPELLCHECKER = False
TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': 'link image preview codesample contextmenu table code',
    'toolbar1': 'bold italic underline | alignleft aligncenter alignright alignjustify '
                '| bullist numlist | outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'inline': False,
    'statusbar': False,
    'height': 200,
    'language': 'zh_CN'
}

# ----------------------------------------- REST_FRAMEWORK -----------------------------------------------

REST_FRAMEWORK = {
    # 'ORDERING_PARAM' : 'order_by', # Renaming ordering to order_by like sql convention
    'PAGE_SIZE': 15,
    'PAGINATE_BY_PARAM': 'limit',  # Allow client to override, using `?limit=xxx`.
    'MAX_PAGINATE_BY': 999,  # Maximum limit allowed when using `?limit=xxx`.
    'UNICODE_JSON': True,
    'DEFAULT_PAGINATION_CLASS': 'core.api.pagination.CommonPageNumberPagination',

    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATETIME_INPUT_FORMATS': ('%Y-%m-%d %H:%M:%S',),
    'DATE_FORMAT': '%Y-%m-%d',
    'DATE_INPUT_FORMATS': ('%Y-%m-%d',),
    'TIME_FORMAT': '%H:%M:%S',
    'TIME_INPUT_FORMATS': ('%H:%M:%S',),
    'LANGUAGES': (
        ('zh-hans', 'Simplified Chinese'),
    ),

    'LANGUAGE_CODE': 'zh-hans',
    'NON_FIELD_ERRORS_KEY': 'detail',

    'DEFAULT_RENDERER_CLASSES': [
        'core.api.renders.UTF8JSONRenderer',
        # 'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoObjectPermissions',
        # 'utils.api.permission.ObjectPermissions',
        'core.api.permission.CommonAPIPermissions',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        # 'rest_framework.filters.DjangoObjectPermissionsFilter', #Will exclusively use guardian tables for access
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    )
}

# ----------------------------------------- CONSTANTS -----------------------------------------------
SITE_NAME = 'OZ SALE'

# ----------------------------------------- Stripe payment -----------------------------------------------
STRIPE_LIVE_PUBLIC_KEY = ''
STRIPE_LIVE_SECRET_KEY = ''
STRIPE_TEST_PUBLIC_KEY = 'pk_test_vEaCFE2a2NpcE6vDvRrvcf1T'
STRIPE_TEST_SECRET_KEY = 'sk_test_AZbVO3pCQDtSozlrTUL9BhO0'
STRIPE_LIVE_MODE = False

# ----------------------------------------- Telstra SMS API KEY-----------------------------------------------
TELSTRA_CONSUMER_KEY = "ZDuzM5gKWl9IM8G4e0VMH2bKorRIU33t"
TELSTRA_CONSUMER_SECRET = "AUbyh8CJy8gASog1"
ADMIN_MOBILE_NUMBER='0413725868'

# ----------------------------------------- 1Forge API KEY-----------------------------------------------
ONE_FORGE_API_KEY = 'k8gjMiRhU8LuhmewMftPUxthMZ3BQnIr'

# ----------------------------------------- CACHES -----------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# ----------------------------------------- DBSETTINGS -----------------------------------------------

# for local settings
if os.path.exists(os.path.join(os.path.dirname(__file__), "local.py")):
    from .local import *