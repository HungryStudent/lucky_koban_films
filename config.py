import configparser

config = configparser.ConfigParser()
config.read("settings.ini")


class DB:
    username = config['db']['username']
    password = config['db']['password']
    host = config['db']['host']
    port = config['db']['port']
    database = config['db']['database']


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB.username}:{DB.password}@{DB.host}:{DB.port}/{DB.database}"
