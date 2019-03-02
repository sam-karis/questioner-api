import logging

from .base import *  # noqa


DEBUG = False
TEMPLATE_DEBUG = False

logging.disable(logging.CRITICAL)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
