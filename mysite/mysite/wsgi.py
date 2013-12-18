"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

sys.environ.setdefault('/home/ubuntu/website/OST/mysite/')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
