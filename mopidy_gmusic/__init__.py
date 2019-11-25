import pathlib

import pkg_resources

from mopidy import config, ext

__version__ = pkg_resources.get_distribution("Mopidy-GMusic").version


class Extension(ext.Extension):

    dist_name = "Mopidy-GMusic"
    ext_name = "gmusic"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()

        schema["username"] = config.Deprecated()
        schema["password"] = config.Deprecated()

        schema["refresh_token"] = config.Secret(optional=True)

        schema["bitrate"] = config.Integer(choices=(128, 160, 320))

        schema["deviceid"] = config.String(optional=True)

        schema["all_access"] = config.Boolean(optional=True)

        schema["refresh_library"] = config.Integer(minimum=-1, optional=True)
        schema["refresh_playlists"] = config.Integer(minimum=-1, optional=True)

        schema["radio_stations_in_browse"] = config.Boolean(optional=True)
        schema["radio_stations_as_playlists"] = config.Boolean(optional=True)
        schema["radio_stations_count"] = config.Integer(
            minimum=1, optional=True
        )
        schema["radio_tracks_count"] = config.Integer(minimum=1, optional=True)

        schema["top_tracks_count"] = config.Integer(minimum=1, optional=True)

        return schema

    def setup(self, registry):
        from .backend import GMusicBackend
        from .scrobbler_frontend import GMusicScrobblerFrontend

        registry.add("backend", GMusicBackend)
        registry.add("frontend", GMusicScrobblerFrontend)

    def get_command(self):
        from .commands import GMusicCommand

        return GMusicCommand()
