# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/btctradingflask'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"


# class Config(object):
#     """
#     Common configurations
#     """
#
#     # Put any configurations here that are common across all environments
#
#
# class DevelopmentConfig(Config):
#     """
#     Development configurations
#     """
#
#     DEBUG = True
#     SQLALCHEMY_ECHO = True
#
#
# class ProductionConfig(Config):
#     """
#     Production configurations
#     """
#
#     DEBUG = False
#
#
# app_config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig
# }
