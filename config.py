SQLITE = "sqlite:///project.db"
POSTGRESQL = "postgresql+psycopg2://emelchor:Emelch0r1*@localhost:5432/credit_risk"
class Config:
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL
    CKEDITOR_PKG_TYPE = 'full'
