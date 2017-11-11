# File: local_settings.py
import os

project_dir = os.path.dirname(os.path.realpath(__file__))

# Customized Django settings to over-ride those specified in
# the 'stock' settings.py:

# Agreed on the following:
DEBUG = True
TIME_ZONE = 'America/Los_Angeles'

# In my version, not mentioned in yours:
# STATIC_URL = '/library/static/'
# FORCE_SCRIPT_NAME = '/library'
# LOGIN_REDIRECT_URL = FORCE_SCRIPT_NAME

# In your version, not mentioned in what I had:
STATIC_ROOT=os.path.join(project_dir, 'staticfiles')
MEDIA_ROOT='/var/www/pathagar_media'

# Your version extends what I already had => 1 question:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pathagar',
        'USER': 'pathagar',
        'PASSWORD': 'MYSQL_PASSWORD',
        # I assume that only pathagar will be 'listening'
        # to 'localhost:3306' using this way of communicating
        # with its data base, is that correct?
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
