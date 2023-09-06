from NKO.settings.settings import *

SECRET_KEY = 'mytesttoken0997867'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}