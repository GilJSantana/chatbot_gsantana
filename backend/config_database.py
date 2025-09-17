'''Este programa carrega as configurações da base de dados. '''

import os


class ConfigDataDase:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, 'database/gsantana.db')}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
