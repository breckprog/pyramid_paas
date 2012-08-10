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
        d = vars(self.request.paas_env)
        if d.get('env'):
            del d['env']
        if d.get('_settings'):
            del d['_settings']

        paas_name = d['PAAS_NAME']

        env = [(k, v) for k, v in d.iteritems()]
        return self.render(
            'pyramid_paas:paas.dbtmako',
            {   'paas': paas_name,
                'env': sorted(env, key=itemgetter(0))},
            self.request
            )


def includeme(config):
    settings = config.registry.settings
    if 'debugtoolbar.panels' in settings:
        settings['debugtoolbar.panels'].append(PaaSDebugPanel)
        if not 'mako.directories' in settings:
            settings['mako.directories'] = []
