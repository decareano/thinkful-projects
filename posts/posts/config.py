import os
import json
import sys
import urllib.parse


class DevelopmentConfig(object):
    try:
        with open("posts_sqlconnection_config.json", 'r') as sqlcfg_file:
            sqlcfg = json.load(sqlcfg_file)
    except Exception as e:
        print("Error loading sql configuration file.  Please run sql_connection_config_script.py")
        print("Exception: {}".format(e))
        sys.exit()

    try:
        with open("posts_env_variables.json", 'r') as env_variables:
            posts_env_variables = json.load(env_variables)
    except Exception as e:
        print("Error loading posts_env_variables.json")

    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        sqlcfg['user'],
        urllib.parse.quote(sqlcfg['password']), # Encodes weird passwords with spaces and whatnot for urls
        sqlcfg['host'],
        sqlcfg['port'],
        sqlcfg['dbname'])

    SECRET_KEY = posts_env_variables['secret_key']
    SERVER_IP = posts_env_variables['server_ip']

    DEBUG = True


class TestingConfig(object):
    try:
        with open("posts-test_sqlconnection_config.json", 'r') as sqlcfg_file:
            sqlcfg = json.load(sqlcfg_file)
    except Exception as e:
        print("Error loading sql configuration file.  Please run sql_connection_config_script.py")
        print("Exception: {}".format(e))
        sys.exit()

    try:
        with open("posts_env_variables.json", 'r') as env_variables:
            posts_env_variables = json.load(env_variables)
    except Exception as e:
        print("Error loading posts_env_variables.json")

    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        sqlcfg['user'],
        urllib.parse.quote(sqlcfg['password']), # Encodes weird passwords with spaces and whatnot for urls
        sqlcfg['host'],
        sqlcfg['port'],
        sqlcfg['dbname'])

    SECRET_KEY = posts_env_variables['secret_key']
    SERVER_IP = posts_env_variables['server_ip']

    DEBUG = True
