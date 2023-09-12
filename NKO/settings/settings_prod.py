from NKO.settings.settings import *

SECRET_KEY = os.environ.get("SECRET_KEY", default='894pgirujos;kmldq[409rgjieomk;')

DEBUG = int(os.environ.get("DEBUG", default=False))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'NAME': os.getenv('POSTGRES_DB', "postgres")
    }
}