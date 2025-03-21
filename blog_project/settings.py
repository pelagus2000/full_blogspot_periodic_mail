"""
Django settings for blog_project project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-fallback-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'fpages',
    'post.apps.PostConfig',
    'category',
    'sign.apps.SignConfig',
    'author',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',
    'subscriber.apps.SubscriberConfig',
    'comment.apps.CommentConfig',
    'django_apscheduler',
    'django_celery_beat',
]

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'
# LOGIN_URL = 'sign/login/' #was for in by username
# LOGIN_REDIRECT_URL = '/' #was for in by username

SITE_ID=1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_METHODS = {"email"}

# ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'post.middlewares.TimezoneMiddleware',
    # 'django.middleware.timezone.TimeZoneMiddleware',

    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'author.context_processors.is_author',
                'django.template.context_processors.i18n'

            ],
        },
    },
]

WSGI_APPLICATION = 'blog_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql', # postgres1
        'NAME': 'djangodb',  # Database name postgres2
        'USER': 'postgres',  # Database username postgres3
        'PASSWORD': '1945',  # Database password postgres4
        'HOST': 'localhost',  # Set to 'localhost' or the server address postgres5
        'PORT': '5432',  # Default PostgreSQL port (5432) postgres6
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Русский')),
]


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [ BASE_DIR / 'static'
]

ACCOUNT_FORMS = {'signup': 'sign.forms.BasicSignupForm'}

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
# Это позволит вам видеть все попытки отправки писем в консоли, а не через реальный SMTP-сервер. После завершения настройки верните реальный SMTP-бэкенд:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'pelagus2000@yandex.ru'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = '************'  # пароль от почты
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC+3'  # Override according to your timezone

CACHES = {
    'default': {
        'TIMEOUT' : (60*5),
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache', # file_cache 1
        # 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',

        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # file_cache 2
    }
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'style': '{',  # Use `{}` for string formatting.
#     'formatters': {
#         'console_debug': {
#             'format': '%(asctime)s %(levelname)s %(message)s',
#         },
#         'console_warning': {
#             'format': '%(asctime)s %(levelname)s [%(pathname)s] %(message)s',
#         },
#         'console_error': {
#             'format': '%(asctime)s %(levelname)s [%(pathname)s] %(message)s %(exc_info)s',
#         },
#         'general_file': {
#             'format': '%(asctime)s %(levelname)s [%(module)s] %(message)s',
#         },
#         'error_file': {
#             'format': '%(asctime)s %(levelname)s [%(pathname)s] %(message)s %(exc_info)s',
#         },
#         'security_file': {
#             'format': '%(asctime)s %(levelname)s [%(module)s] %(message)s',
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#     },
#     'handlers': {
#         'console_debug': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'console_debug',
#         },
#         'console_warning': {
#             'level': 'WARNING',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'console_warning',
#         },
#         'console_error': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'console_error',
#         },
#         'general_file': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'general.log',
#             'formatter': 'general_file',
#         },
#         'errors_file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': 'errors.log',
#             'formatter': 'error_file',
#         },
#         'security_file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'security.log',
#             'formatter': 'security_file',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler',
#             'formatter': 'error_file',  # Same format as error logs but without stack info for emails.
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console_debug', 'console_warning', 'console_error', 'general_file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['errors_file', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.server': {
#             'handlers': ['errors_file', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.template': {
#             'handlers': ['errors_file'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.db.backends': {
#             'handlers': ['errors_file'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.security': {
#             'handlers': ['security_file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
# }

