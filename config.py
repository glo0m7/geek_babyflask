import os
import requests

key = '123456'#str(requests.get('127.0.0.1:10000').text)


basedir = os.path.abspath(os.path.dirname(__file__))
sqlpath = os.path.join(basedir,'admin.db')
print(basedir)

class Config():
    SECRET_KEY = key

    #sql
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlpath