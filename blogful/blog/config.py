import os
import json
import sys
import urllib.parse




class DevelopmentConfig(object):
    try:
        with open("sqlconnection_config_blogful.json", 'r') as sqlcfg_file:
            sqlcfg = json.load(sqlcfg_file)
    except Exception as e:
        print("Error loading sql configuration file.  Please run sql_connection_config_script.py")
        print("Exception: {}".format(e))
        sys.exit()

    try:
        with open("blogful_env_variables.json", 'r') as blogful_cfg_file:
            blogful_env_variables = json.load(blogful_cfg_file)
    except Exception as e:
        print("Error loading blogful_env_variables.json")

    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        sqlcfg['user'],
        urllib.parse.quote(sqlcfg['password']), # Encodes weird passwords with spaces and whatnot for urls
        sqlcfg['host'],
        sqlcfg['port'],
        sqlcfg['dbname'])

    SECRET_KEY = blogful_env_variables['secret_key']
    SERVER_IP = blogful_env_variables['server_ip']

    DEBUG = True

class TestingConfig(object):
    try:
        with open("sqlconnection_config_blogful.json", 'r') as sqlcfg_file:
            sqlcfg = json.load(sqlcfg_file)
    except Exception as e:
        print("Error loading sql configuration file.  Please run sql_connection_config_script.py")
        print("Exception: {}".format(e))
        sys.exit()

    try:
        with open("blogful_env_variables.json", 'r') as blogful_cfg_file:
            blogful_env_variables = json.load(blogful_cfg_file)
    except Exception as e:
        print("Error loading blogful_env_variables.json")

    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        sqlcfg['user'],
        urllib.parse.quote(sqlcfg['password']), # Encodes weird passwords with spaces and whatnot for urls
        sqlcfg['host'],
        sqlcfg['port'],
        "blogful-test")

    SECRET_KEY = 'Not secret'
    SERVER_IP = blogful_env_variables['server_ip']

    DEBUG = True
