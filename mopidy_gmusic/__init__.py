from __future__ import unicode_literals

import os

from mopidy import config, exceptions, ext


__version__ = '0.2.2'


class GMusicExtension(ext.Extension):

    dist_name = 'Mopidy-GMusic'
    ext_name = 'gmusic'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(GMusicExtension, self).get_config_schema()
        schema['username'] = config.String()
        schema['password'] = config.Secret()
        schema['deviceid'] = config.String(optional=True)
        return schema

    def validate_environment(self):
        try:
            import gmusicapi  # noqa
        except ImportError as e:
            raise exceptions.ExtensionError('gmusicapi library not found', e)
        pass

    def get_backend_classes(self):
        from .actor import GMusicBackend
        return [GMusicBackend]
