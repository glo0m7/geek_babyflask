import os

with open('LiUU.key') as LiUU:
    key = LiUU.read()



basedir = os.path.abspath(os.path.dirname(__file__))
sqlpath = os.path.join(basedir,'LiUU.db')
print(basedir)

class Config():
    SECRET_KEY = key

    #sql
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlpath