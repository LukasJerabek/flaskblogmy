import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') # database set up
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    # necessary to allow low security aplications in gmail
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') #from environment variable - os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') #from environment variable - os.environ.get('EMAIL_PASS')
