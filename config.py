import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xf6\xe1\xe3M\xaf-v\xc1t\xf4\xe8\xbfK\x107\x9e'

    MONGODB_SETTINGS = {'db' : 'UTA_Enrollment' }
    #UTA_Enrollment is the name of database