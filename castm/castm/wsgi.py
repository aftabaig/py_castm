from socket import gethostname
host_name = gethostname()

import sys
if host_name is "castm":
    sys.path.append('/var/www/castm/py_castm/castm/castm')
    sys.path.append('/var/www/castm/py_castm/castm')

import os
if host_name == "castm":
    os.environ["DJANGO_SETTINGS_MODULE"] = "production"
elif host_name == "":
    os.environ["DJANGO_SETTINGS_MODULE"] = "castm.staging"
else:
    os.environ["DJANGO_SETTINGS_MODULE"] = "castm.development"

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())