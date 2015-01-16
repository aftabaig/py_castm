# Django settings for cast'em project.

from defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Aftab Baig', 'aftabaig@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cast\'em',
        'USER': 'aftabaig',
        'PASSWORD': 'university',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', ]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'um': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'talent': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'casting': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'events': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'links': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'notifications': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'my_messages': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'organizations': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'schedules': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

CLOUDINARY = {
    'cloud_name': 'flash-solutions',
    'api_key': '242359747124272',
    'api_secret': 'If_a6ZxmJ-QZX775G1oo6DuLTIg'
}

UA = {
    'app_key': 'd6awtJp0T-Cyx5QRXUYr7Q',
    'app_secret': 'Ysd7JB36S8GugZ29-e5YhQ',
    'master_secret': 'tiEtq6i1Q-yZYZuyd1qSpg'
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '65bdf35749989106a3ee6b0419d160e032b63323', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aftab@techverx.com'
EMAIL_HOST_PASSWORD = 'Chaghi25BigMac'
EMAIL_PORT = 587