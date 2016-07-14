import unittest

from mopidy.models import Ref

from mopidy_gmusic import backend as backend_lib

from tests.test_extension import ExtensionTest


class LibraryTest(unittest.TestCase):

    def setUp(self):
        config = ExtensionTest.get_config()
        self.backend = backend_lib.GMusicBackend(config=config, audio=None)

    def test_browse_radio_deactivated(self):
        config = ExtensionTest.get_config()
        config['gmusic']['radio_stations_in_browse'] = False
        self.backend = backend_lib.GMusicBackend(config=config, audio=None)

        refs = self.backend.library.browse('gmusic:directory')
        for ref in refs:
            self.assertNotEqual(ref.uri, 'gmusic:radio')

    def test_browse_none(self):
        refs = self.backend.library.browse(None)
        self.assertEqual(refs, [])

    def test_browse_invalid(self):
        refs = self.backend.library.browse('gmusic:invalid_uri')
        self.assertEqual(refs, [])

    def test_browse_root(self):
        refs = self.backend.library.browse('gmusic:directory')
        found = False
        for ref in refs:
            if ref.uri == 'gmusic:album':
                found = True
                break
        self.assertTrue(found, 'ref \'gmusic:album\' not found')
        found = False
        for ref in refs:
            if ref.uri == 'gmusic:artist':
                found = True
                break
        self.assertTrue(found, 'ref \'gmusic:artist\' not found')
        found = False
        for ref in refs:
            if ref.uri == 'gmusic:track':
                found = True
                break
        self.assertTrue(found, 'ref \'gmusic:track\' not found')
        found = False
        for ref in refs:
            if ref.uri == 'gmusic:radio':
                found = True
                break
        self.assertTrue(found, 'ref \'gmusic:radio\' not found')

    def test_browse_tracks(self):
        refs = self.backend.library.browse('gmusic:track')
        self.assertIsNotNone(refs)

    def test_browse_artist(self):
        refs = self.backend.library.browse('gmusic:artist')
        self.assertIsNotNone(refs)

    def test_browse_artist_id_invalid(self):
        refs = self.backend.library.browse('gmusic:artist:artist_id')
        self.assertIsNotNone(refs)
        self.assertEqual(refs, [])

    def test_browse_album(self):
        refs = self.backend.library.browse('gmusic:album')
        self.assertIsNotNone(refs)

    def test_browse_album_id_invalid(self):
        refs = self.backend.library.browse('gmusic:album:album_id')
        self.assertIsNotNone(refs)
        self.assertEqual(refs, [])

    def test_browse_radio(self):
        refs = self.backend.library.browse('gmusic:radio')
        # tests should be unable to fetch stations :(
        self.assertIsNotNone(refs)
        self.assertEqual(refs, [Ref.directory(uri='gmusic:radio:IFL',
                                              name="I'm Feeling Lucky")])

    def test_browse_station(self):
        refs = self.backend.library.browse('gmusic:radio:invalid_stations_id')
        # tests should be unable to fetch stations :(
        self.assertEqual(refs, [])

    def test_lookup_invalid(self):
        refs = self.backend.library.lookup('gmusic:invalid_uri')
        # tests should be unable to fetch any content :(
        self.assertEqual(refs, [])

    def test_lookup_invalid_album(self):
        refs = self.backend.library.lookup('gmusic:album:invalid_uri')
        # tests should be unable to fetch any content :(
        self.assertEqual(refs, [])

    def test_lookup_invalid_artist(self):
        refs = self.backend.library.lookup('gmusic:artis:invalid_uri')
        # tests should be unable to fetch any content :(
        self.assertEqual(refs, [])

    def test_lookup_invalid_track(self):
        refs = self.backend.library.lookup('gmusic:track:invalid_uri')
        # tests should be unable to fetch any content :(
        self.assertEqual(refs, [])

    def test_search(self):
        refs = self.backend.library.search({'artist': ['abba']})
        self.assertIsNotNone(refs)
