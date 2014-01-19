import mock
import unittest

from mopidy_gmusic import GMusicExtension, actor as backend_lib


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = GMusicExtension()

        config = ext.get_default_config()

        self.assertIn('[gmusic]', config)
        self.assertIn('enabled = true', config)

    def test_get_config_schema(self):
        ext = GMusicExtension()

        schema = ext.get_config_schema()

        self.assertIn('username', schema)
        self.assertIn('password', schema)
        self.assertIn('deviceid', schema)

    def test_get_backend_classes(self):
        registry = mock.Mock()

        ext = GMusicExtension()
        ext.setup(registry)

        registry.add.assert_called_once_with(
            'backend', backend_lib.GMusicBackend)
