DB_PORT = 27017
DB_HOST = "localhost"
DB_NAME = "splitwise"


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SITE_NAME = "Splitwise"
    SECRET_KEY = "c219d4e3-3ea8-4dbb-8641-8bbfc644aa18"
    MONGO_URI = f"mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
