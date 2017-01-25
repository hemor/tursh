from .base_settings import *


SECRET_KEY = os.environ.get('TURSH_SK', '');

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('TURSH_DB_ENGINE', ''),
        'NAME': os.environ.get('TURSH_DB_NAME', ''),
        'USER': os.environ.get('TURSH_DB_USER', ''),
        'PASSWORD': os.environ.get('TURSH_DB_PASSWORD', ''),
        'HOST': os.environ.get('TURSH_DB_HOST', ''),
        'PORT': os.environ.get('TURSH_DB_PORT', '')
    }
}

DEBUG = False

ALLOWED_HOSTS = ['localhost', 'tursh.net', 'www.tursh.net', 'http://ec2-54-202-172-151.us-west-2.compute.amazonaws.com/']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')