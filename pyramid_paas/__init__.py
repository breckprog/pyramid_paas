# -*- coding: utf-8 -*-
import json
import os
from zope.interface import Interface

DOTCLOUD = "DOTCLOUD"
HEROKU = "HEROKU"
STRIDER = "STRIDER"

DOTCLOUD_FILE_PATH = '/home/dotcloud/environment.json'

class IPaaSEnv(Interface):
    pass

class NoEnv(object):
    pass

class DotCloudEnv(object):
    """DotCloud environment for Pyramid. See http://docs.dotcloud.com/firststeps/platform-overview/ """
    def __init__(self, path=DOTCLOUD_FILE_PATH, env=None):
        if os.path.isfile(path):
            with open(path) as f:
                env = json.load(f)
                for item in env:
                    setattr(self, item, env[item])
                self.env = env

        if env:
            self.env = env

    def lookup(self, key):
        for k, val in self.env.iteritems():
            if k.startswith("DOTCLOUD") and k.endswith(key):
                return val

    def get_mysql_url(self):
        return self.lookup("MYSQL_URL");

    def get_postgresql_url(self):
        # underscore prevents us from confusing with a MYSQL_URL
        return self.lookup("_SQL_URL");

    def get_mongodb_url(self):
        return self.lookup("MONGODB_URL");

    def get_redis_url(self):
        return self.lookup("REDIS_URL");

    def get_solr_url(self):
        # XXX not sure how to implement this for DotCloud yet:
        # http://docs.dotcloud.com/services/solr/
        pass


class HerokuEnv(object):
    """ Heroku environment for Pyramid. See https://addons.heroku.com """

    def __init__(self, env=None):
        if not env:
            self.env = os.environ
        else:
            self.env = env
        for item in self.env:
            setattr(self, item, self.env[item])

    def get_mysql_url(self):
        # ClearDB and Xeround options for MySQL
        if 'CLEARDB_DATABASE_URL' in self.env:
            return self.env['CLEARDB_DATABASE_URL']
        if 'XEROUND_DATABASE_INTERNAL_URL' in self.env:
            return self.env['XEROUND_DATABASE_INTERNAL_URL']

    def get_postgresql_url(self):
        if 'DATABASE_URL' in self.env:
            return self.env['DATABASE_URL']

    def get_mongodb_url(self):
        # MongoHQ and MongoLab options for MongoDB
        if 'MONGOHQ_URL' in self.env:
            return self.env['MONGOHQ_URL']
        if 'MONGOLAB_URL' in self.env:
            return self.env['MONGOLAB_URL']

    def get_redis_url(self):
        # Redis To Go and Open Redis options for Redis
        if 'REDISTOGO_URL' in self.env:
            return self.env['REDISTOGO_URL']
        if 'OPENREDIS_URL' in self.env:
            return self.env['OPENREDIS_URL']

    def get_solr_url(self):
        # Web Solr options for Solr
        if 'WEBSOLR_URL' in self.env:
            return self.env['WEBSOLR_URL']

def get_paas_env(config):
    return config.registry.queryUtility(IPaaSEnv)


def get_paas_env_from_request(request):
    """Obtain a DotCloudEnv object previously registered via
    ``config.include('pyramid_paas')``
    """
    return request.registry.queryUtility(IPaaSEnv)

def detect_paas(dotcloud_env_path=DOTCLOUD_FILE_PATH, environ=os.environ):
    if os.path.isfile(dotcloud_env_path):
        return DOTCLOUD
    try:
        environ['PORT']
        return HEROKU
    except KeyError:
        pass
    try:
        paas = environ['PAAS_NAME']
        if paas == "STRIDER":
            return STRIDER
    except KeyError:
        pass

    # We don't think this is running on a PaaS
    return None


def includeme(config):
    paas = detect_paas()
    if paas == DOTCLOUD:
        config.registry.registerUtility(DotCloudEnv(), IPaaSEnv)
    # Strider exports same vars as Heroku so can just re-use that impl.
    elif paas in (HEROKU, STRIDER):
        config.registry.registerUtility(HerokuEnv(), IPaaSEnv)
    else:
        config.registry.registerUtility(NoEnv(), IPaaSEnv)


    config.add_directive('get_paas_env', get_paas_env)
    config.set_request_property(
        get_paas_env_from_request,
        'paas_env',
        reify=True
        )
    config.include('.panel')
