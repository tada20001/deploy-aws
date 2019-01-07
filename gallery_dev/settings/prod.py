from .common import *

ALLOWED_HOSTS = ['*']  # 실서비스 도메인 입력

DEBUG = False

import os

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql'),
#         'HOST': os.environ.get('DATABASE_HOST', None),
#         'NAME': os.environ.get('DATABASE_NAME', None),
#         'USER': os.environ.get('DATABASE_USER', None),
#         'PASSWORD': os.environ.get('DATABASE_PASSWORD', None),
#     }
# }
