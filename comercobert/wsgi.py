"""
WSGI config for accessos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application
sys.path.append('/var/www/html/comercobert/comercobert')
sys.path.append('/var/www/html/comercobert/comercobert/comercobert')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comercobert.settings')
application = get_wsgi_application()