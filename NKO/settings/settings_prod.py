from NKO.settings.settings import *

SECRET_KEY = os.environ.get("SECRET_KEY", default='894pgirujos;kmldq[409rgjieomk;')

DEBUG = int(os.environ.get("DEBUG", default=False))
