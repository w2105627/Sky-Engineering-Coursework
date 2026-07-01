# Author : w2105627
"""
WSGI config for w2105627_group_cwk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'w2105627_group_cwk.settings')

application = get_wsgi_application()
