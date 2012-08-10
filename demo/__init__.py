# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.response import Response


def paas_env_view(request):
    env = request.paas_env
    return Response('<html><body><h2>PAAS ENV</h2>{0}</body></html>'\
        .format(env.__dict__))


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_view(paas_env_view)
    return config.make_wsgi_app()
