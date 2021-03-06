#!/usr/bin/python3
from configparser import ConfigParser


def ini_config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    p = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            p[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return p


class Config(object):
    SANDBOX_MTURK = "https://workersandbox.mturk.com/mturk/externalSubmit"
    MTURK = "https://www.mturk.com/mturk/externalSubmit"
    HOST = "0.0.0.0"
    DEBUG = True
    TESTING = True
    PROFILE = True
    SANDBOX = True
    db_conf = ini_config()
    aws_conf = ini_config(section='aws')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**db_conf) if 'password' in db_conf else 'postgresql://{user}@/{database}'.format(**db_conf)
    if 'aws' in SQLALCHEMY_DATABASE_URI:
        print("Using SSL for remote DB connection")
        SQLALCHEMY_DATABASE_URI += '?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 600
