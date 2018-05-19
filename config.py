import os

class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY")

    @staticmethod
    def init_app(app):
        pass

class Development(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}".format("mysql","pymysql",os.environ.get("USERNAME"),os.environ.get("PASSWORD"),"127.0.0.1","3306","python")
    SQLALCHEMY_TRACK_MODIFICATIONS=False


config={
    "default":Development,
    "Development":Development
}