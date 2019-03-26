from .base import *  # noqa

if os.getenv('HOST_ENV') == 'HEROKU':  # noqa
    import django_heroku
    # Activate Django-Heroku.
    django_heroku.settings(locals())
