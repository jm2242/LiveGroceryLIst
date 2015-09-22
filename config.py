import os

# default config

class BaseConfig(object):
	DEBUG = False
	SECRET_KEY =  "\x9f\xd3LK\xb3\xd8\xf8\xd8'\x8a?O\xe0\xb6\xfd\xb74\x1c\xd7s~\xe3,R"
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(BaseConfig):
	DEBUG = True


class ProductionConfig(BaseConfig):
	DEBUG = False
