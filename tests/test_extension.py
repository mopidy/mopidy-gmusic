import unittest

import mock

from mopidy_gmusic import (
    GMusicExtension, actor as backend_lib, scrobbler_frontend)


class ExtensionTest(unittest.TestCase):

    @staticmethod
    def get_config():
        config = {}
        config['username'] = 'testuser@gmail.com'
        config['password'] = 'secret_password'
        config['deviceid'] = '1234567890'
        config['all_access'] = False
        config['show_radio_stations_browse'] = True
        config['show_radio_stations_playlist'] = False
        config['max_radio_stations'] = 0
        config['max_radio_tracks'] = 25
        config['refresh_library'] = 1440
        config['refresh_playlists'] = 60
        return {'gmusic': config}

    def test_get_default_config(self):
        ext = GMusicExtension()

        config = ext.get_default_config()

        self.assertIn('[gmusic]', config)
        self.assertIn('enabled = true', config)
        self.assertIn('all_access = false', config)
        self.assertIn('show_radio_stations_browse = true', config)
        self.assertIn('max_radio_stations = 0', config)
        self.assertIn('max_radio_tracks = 25', config)

    def test_get_config_schema(self):
        ext = GMusicExtension()

        schema = ext.get_config_schema()

        self.assertIn('username', schema)
        self.assertIn('password', schema)
        self.assertIn('deviceid', schema)
        self.assertIn('refresh_library', schema)
        self.assertIn('refresh_playlists', schema)
        self.assertIn('all_access', schema)
        self.assertIn('show_radio_stations_browse', schema)
        self.assertIn('show_radio_stations_playlist', schema)
        self.assertIn('max_radio_stations', schema)
        self.assertIn('max_radio_tracks', schema)

    def test_get_backend_classes(self):
        registry = mock.Mock()

        ext = GMusicExtension()
        ext.setup(registry)

        self.assertIn(
            mock.call('backend', backend_lib.GMusicBackend),
            registry.add.mock_calls)
        self.assertIn(
            mock.call('frontend', scrobbler_frontend.GMusicScrobblerFrontend),
            registry.add.mock_calls)

    def test_init_backend(self):
        backend = backend_lib.GMusicBackend(
            ExtensionTest.get_config(), None)
        self.assertIsNotNone(backend)
        backend.on_start()
        backend.on_stop()
