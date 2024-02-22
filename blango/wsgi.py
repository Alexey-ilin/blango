"""
WSGI config for blango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blango.settings')

from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')


application = get_wsgi_application()
