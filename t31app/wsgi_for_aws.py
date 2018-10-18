"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
import site


# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/virtual_tasat31/tasat31_env/lib/python3.5/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/virtual_tasat31/t31app')

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "t31app.settings"

# Activate your virtual env
activate_env=os.path.expanduser("/var/www/virtual_tasat31/tasat31_env/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))
exec(open(activate_env).read(), dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
