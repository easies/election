# Django settings for acm_election project.

from os.path import normpath, join, dirname, abspath

ROOT = lambda *base : normpath(join(dirname(__file__), *base)).replace('\\','/')
MODULE = normpath(abspath(dirname(__file__))).replace('\\','/').split('/')[-1]

DEBUG = False 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('John', 'jmendel@ccs.neu.edu'),
    ('Alex', 'lee@ccs.neu.edu'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'       # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'acm_election2009' # Or path to database file if using sqlite3.
DATABASE_USER = 'root'                # Not used with sqlite3.
DATABASE_PASSWORD = 'singlesignon'            # Not used with sqlite3.
DATABASE_HOST = ''                # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: '/home/media/media.lawrence.com/'
MEDIA_ROOT = ROOT('media') + '/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: 'http://media.lawrence.com', 'http://example.com/media/'
MEDIA_URL = 'http://acm.ccs.neu.edu/election/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: 'http://foo.com/media/', '/media/'.
ADMIN_MEDIA_PREFIX = '/library/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#wi=h%hd$r1pfefn+co@la4f9j(4mzy+yha!74ulmxwp9cstw-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_cas.middleware.CASMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = MODULE + '.stagedurls'

TEMPLATE_DIRS = (
   ROOT('templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    MODULE + '.candidates',
    MODULE + '.voting',
)

AUTHENTICATION_BACKENDS = (
    ##'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

LOGIN_URL = '/election/login/'
LOGOUT_URL = '/election/logout/'
LOGIN_REDIRECT_URL = '/election/'
CAS_SERVER_URL = 'https://vzcgi.ccs.neu.edu/sso/cas/'

AUDIT_LOG = ROOT('audit.log')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    MODULE + '.util.context_processors.acm_election'
)

