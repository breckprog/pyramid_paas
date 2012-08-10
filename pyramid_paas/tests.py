# -*- coding: utf-8 -*-
import os
import unittest

import mock
import tempfile


class TestPaaSEnv(unittest.TestCase):

    def test_dotcloudenv_init(self):
        from pyramid_paas import DotCloudEnv

        here = os.path.dirname(os.path.abspath(__file__))
        envfile = os.path.join(here, 'test.json')
        env = DotCloudEnv(envfile)
        assert env.key == 'value'

    def test_get_paas_env(self):
        from pyramid_paas import IPaaSEnv
        from pyramid_paas import get_paas_env

        config = mock.Mock()
        config.registry = mock.Mock()
        queryUtility = mock.Mock()

        config.registry.queryUtility = queryUtility

        env = get_paas_env(config)
        queryUtility.assert_called_with(IPaaSEnv)

        assert env != None

    def test_get_paas_env_from_request(self):
        from pyramid_paas import IPaaSEnv
        from pyramid_paas import get_paas_env_from_request

        request = mock.Mock()
        request.registry = mock.Mock()
        queryUtility = mock.Mock()
        request.registry.queryUtility = queryUtility

        env = get_paas_env_from_request(request)
        queryUtility.assert_called_with(IPaaSEnv)

        assert env != None

    def test_includeme(self):
        from pyramid_paas import includeme
        from pyramid_paas import get_paas_env
        from pyramid_paas import get_paas_env_from_request

        config = mock.Mock()
        add_directive = mock.Mock()
        registerUtility = mock.Mock()
        set_request_property = mock.Mock()

        config.registry = mock.Mock()
        config.registry.registerUtility = registerUtility
        config.add_directive = add_directive
        config.set_request_property = set_request_property

        includeme(config)

        assert add_directive.call_args_list[0][0] == \
            ('get_paas_env', get_paas_env)

        assert set_request_property.call_args_list[0][0] == \
            (get_paas_env_from_request, 'paas_env')

    def test_detect_paas(self):
        from pyramid_paas import detect_paas
        from pyramid_paas import DOTCLOUD
        from pyramid_paas import HEROKU
        from pyramid_paas import STRIDER

        with tempfile.NamedTemporaryFile() as f:
            r = detect_paas(f.name)
            assert r == DOTCLOUD

        r = detect_paas(environ={"PORT":123})
        assert r == HEROKU

        r = detect_paas(environ={"PAAS_NAME":"STRIDER"})
        assert r == STRIDER

        r = detect_paas("/foo/doesn'texist", {})
        assert r == None

    def test_heroku_mongodb(self):
        from pyramid_paas import HerokuEnv

        url = "foo"
        he = HerokuEnv({"MONGOLAB_URL":url})
        r = he.get_mongodb_url()
        assert r == url

        he = HerokuEnv({"MONGOHQ_URL":url})
        r = he.get_mongodb_url()
        assert r == url

        he = HerokuEnv({"FOO":url})
        r = he.get_mongodb_url()
        assert r == None

    def test_heroku_postgresql(self):
        from pyramid_paas import HerokuEnv

        url = "foo"
        he = HerokuEnv({"DATABASE_URL":url})
        r = he.get_postgresql_url()
        assert r == url

        he = HerokuEnv({"FOO":url})
        r = he.get_postgresql_url()
        assert r == None

    def test_heroku_mysql(self):
        from pyramid_paas import HerokuEnv

        url = "foo"
        he = HerokuEnv({"CLEARDB_DATABASE_URL":url})
        r = he.get_mysql_url()
        assert r == url

        he = HerokuEnv({"XEROUND_DATABASE_INTERNAL_URL":url})
        r = he.get_mysql_url()
        assert r == url

        he = HerokuEnv({"FOO":url})
        r = he.get_mysql_url()
        assert r == None

    def test_heroku_redis(self):
        from pyramid_paas import HerokuEnv

        url = "foo"
        he = HerokuEnv({"REDISTOGO_URL":url})
        r = he.get_redis_url()
        assert r == url

        he = HerokuEnv({"OPENREDIS_URL":url})
        r = he.get_redis_url()
        assert r == url

        he = HerokuEnv({"FOO":url})
        r = he.get_redis_url()
        assert r == None


    def test_heroku_solr(self):
        from pyramid_paas import HerokuEnv

        url = "foo"
        he = HerokuEnv({"WEBSOLR_URL":url})
        r = he.get_solr_url()
        assert r == url

        he = HerokuEnv({"FOO":url})
        r = he.get_solr_url()
        assert r == None
