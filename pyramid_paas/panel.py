from operator import itemgetter

from pyramid_debugtoolbar.panels import DebugPanel

_ = lambda x: x


class PaaSDebugPanel(DebugPanel):
    """
    PaaS debug panel
    """
    name = 'PaaS'
    has_content = True

    def nav_title(self):
        return _('PaaS')

    def url(self):
        return ''

    def title(self):
        return _('PaaS')

    def content(self):
        env = [(k, v) for k, v in vars(self.request.paas_env).iteritems()]
        return self.render(
            'pyramid_paas:paas.dbtmako',
            {'env': sorted(env, key=itemgetter(0))},
            self.request
            )


def includeme(config):
    settings = config.registry.settings
    if 'debugtoolbar.panels' in settings:
        settings['debugtoolbar.panels'].append(PaaSDebugPanel)
        if not 'mako.directories' in settings:
            settings['mako.directories'] = []
