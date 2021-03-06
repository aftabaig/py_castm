DEBUG = True
TEMPLATE_DEBUG = DEBUG

from _base import *

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
    }
}

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
    'app_key': 'jy-ePUJGSQSkGRIepk-OBw',
    'app_secret': '3GlzFnowTGafLa0BxZ2IGA',
    'master_secret': '68AyBO-mRCiiBe_TVpDNrA'
}

STRIPE = {
    'secret_key': 'sk_test_Qd1gjkWYroLCb0T0vUJ8atb6',
    'publishable_key': 'pk_test_9ikeq7cbzVDaDfiIvISr5IBj'
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aftab@techverx.com'
EMAIL_HOST_PASSWORD = 'Chaghi25BigMac'
EMAIL_PORT = 587
