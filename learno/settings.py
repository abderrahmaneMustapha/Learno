"""
Django settings for learno project.

Generated by 'django-admin startproject' using Django 2.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure Django App for Heroku.

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gz0wegcw&7$z!v@^7^_!k#o%x2k1*&ke-mh^-bm25uh9aj0g7w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# DEBUG = (os.environ.get('HACKIDE_DEBUG') or "").lower() == "true"

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']





# Application definition

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'ide',
    'course',

    'django.contrib.admin',

    'bootstrap4',
    'colorful',

    'django_heroku',
    'rest_framework',
    'social_django',  # <--
    'tinymce',



]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <--
]

ROOT_URLCONF = 'learno.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '/accounts', 'templates',)],
        'APP_DIRS': True,
        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'learno.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learno',
        'USER': 'abderrahmane',
        'PASSWORD': '030898',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (


    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication

        'django.contrib.auth.backends.ModelBackend',
         'django.contrib.auth.backends.RemoteUserBackend',

)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
TINYMCE_DEFAULT_CONFIG = {
     'height': 720,
    'width': 1120,
    'theme': "advanced",
    'plugins': "style",
    'theme_advanced_buttons3_add': "|,spellchecker",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'menubar': True,
    'statusbar': True,
    }

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


#LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
SOCIAL_AUTH_URL_NAMESPACE = 'social'


"""
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
"""

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
"""
here we seve the media file in production
"""
SERVE_MEDIA_FILES = True

EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'learnoteam@gmail.com'
EMAIL_HOST_PASSWORD = 'LearnoTeam0033'
EMAIL_USE_TLS = True
EMAIL_USE_SSL= False
DEFAULT_FROM_EMAIL = 'TestSite Team <noreply@example.com>'


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = ''  # App Secret

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email' , 'password',]
SOCIAL_AUTH_RAISE_EXCEPTIONS = True
RAISE_EXCEPTIONS = True

GOOGLE_RECAPTCHA_SECRET_KEY = ''


"""
celery configuration
"""

# Celery application definition
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {

'task-number-one': {
        'task': 'accounts.tasks.calculate_rank_task',
        'schedule': 604800.0,
    },

}

"""
end of celery configuration

"""

import django_heroku
django_heroku.settings(locals())

TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
