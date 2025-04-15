import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
tmpdir = os.path.join(basedir, 'tmp')

load_dotenv(os.path.join(basedir,'.env'), override=True)

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_SCHEMA = os.environ.get('SQLALCHEMY_SCHEMA')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = os.environ.get('BLUECODE_SECRET_KEY')