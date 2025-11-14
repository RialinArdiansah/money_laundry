"""
WSGI config for system_laundry project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use production settings for deployment
settings_module = 'system_laundry.production_settings' if 'VERCEL' in os.environ else 'system_laundry.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()

# Vercel compatibility
app = application