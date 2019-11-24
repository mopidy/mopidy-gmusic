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

        self.assertIn("[gmusic]", config)
        self.assertIn("enabled = true", config)
        self.assertIn("all_access =", config)
        self.assertIn("radio_stations_in_browse = true", config)
        self.assertIn("radio_stations_count =", config)
        self.assertIn("radio_tracks_count = 25", config)

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        self.assertIn("username", schema)
        self.assertIn("password", schema)
        self.assertIn("deviceid", schema)
        self.assertIn("refresh_library", schema)
        self.assertIn("refresh_playlists", schema)
        self.assertIn("all_access", schema)
        self.assertIn("radio_stations_in_browse", schema)
        self.assertIn("radio_stations_as_playlists", schema)
        self.assertIn("radio_stations_count", schema)
        self.assertIn("radio_tracks_count", schema)

    def test_get_backend_classes(self):
        registry = mock.Mock()

        ext = Extension()
        ext.setup(registry)

        self.assertIn(
            mock.call("backend", backend_lib.GMusicBackend),
            registry.add.mock_calls,
        )
        self.assertIn(
            mock.call("frontend", scrobbler_frontend.GMusicScrobblerFrontend),
            registry.add.mock_calls,
        )

    def test_init_backend(self):
        backend = backend_lib.GMusicBackend(ExtensionTest.get_config(), None)
        self.assertIsNotNone(backend)
        backend.on_start()
        backend.on_stop()
