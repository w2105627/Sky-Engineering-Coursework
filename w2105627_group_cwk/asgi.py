# Author : w2105627
"""
ASGI config for w2105627_group_cwk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'w2105627_group_cwk.settings')

application = get_asgi_application()
