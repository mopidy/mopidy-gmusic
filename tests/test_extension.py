import unittest
from unittest import mock

from mopidy_gmusic import Extension
from mopidy_gmusic import backend as backend_lib
from mopidy_gmusic import scrobbler_frontend


class ExtensionTest(unittest.TestCase):
    @staticmethod
    def get_config():
        config = {}
        config["username"] = "testuser@gmail.com"
        config["password"] = "secret_password"
        config["refresh_token"] = "0987654321"
        config["deviceid"] = "1234567890"
        config["all_access"] = False
        config["refresh_library"] = 1440
        config["refresh_playlists"] = 60
        config["radio_stations_in_browse"] = True
        config["radio_stations_as_playlists"] = False
        config["radio_stations_count"] = 0
        config["radio_tracks_count"] = 25
        config["top_tracks_count"] = 20
        return {"gmusic": config}

    def test_get_default_config(self):
        ext = Extension()

        config = ext.get_default_config()

        assert "[gmusic]" in config
        assert "enabled = true" in config
        assert "all_access =" in config
        assert "radio_stations_in_browse = true" in config
        assert "radio_stations_count =" in config
        assert "radio_tracks_count = 25" in config

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        assert "username" in schema
        assert "password" in schema
        assert "deviceid" in schema
        assert "refresh_library" in schema
        assert "refresh_playlists" in schema
        assert "all_access" in schema
        assert "radio_stations_in_browse" in schema
        assert "radio_stations_as_playlists" in schema
        assert "radio_stations_count" in schema
        assert "radio_tracks_count" in schema

    def test_get_backend_classes(self):
        registry = mock.Mock()

        ext = Extension()
        ext.setup(registry)

        assert (
            mock.call("backend", backend_lib.GMusicBackend)
            in registry.add.mock_calls
        )
        assert (
            mock.call("frontend", scrobbler_frontend.GMusicScrobblerFrontend)
            in registry.add.mock_calls
        )

    def test_init_backend(self):
        backend = backend_lib.GMusicBackend(ExtensionTest.get_config(), None)
        assert backend is not None
        backend.on_start()
        backend.on_stop()
