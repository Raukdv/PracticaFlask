from decouple import config

class Config:
	SECRET_KEY = 'RKT.dv_99' #PuedesCambiarla

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:ClaveSiPoseeUsuarioRootConClave@127.0.0.1/NombreDelaDB'
	SQLALCHEMY_TRACK_MODIFICATIONS= False

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587 #tls
	MAIL_USE_TLS = True
	MAIL_USERNAME = ''
	MAIL_PASSWORD = config('MAIL_PASSWORD')#Variable de Entorno

#Para Usar Mailgun Server
#MAIL_SERVER = 'smtp.mailgun.org'
#MAIL_PORT = 587 #tls
#MAIL_USE_TLS = True
#MAIL_USERNAME = ''
#MAIL_PASSWORD = ''

class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:ClaveSiPoseeUsuarioRootConClave@127.0.0.1/NombreDelaDB_test'
	SQLALCHEMY_TRACK_MODIFICATIONS= False
	TEST = True

config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig,
	'test': TestConfig
}
