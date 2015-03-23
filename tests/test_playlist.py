import unittest

import mock

from mopidy.models import Playlist, Track

from mopidy_gmusic.playlists import GMusicPlaylistsProvider

from tests.test_extension import ExtensionTest


class PlaylistsTest(unittest.TestCase):

    def setUp(self):
        backend = mock.Mock()
        backend.config = ExtensionTest.get_config()
        self.provider = GMusicPlaylistsProvider(backend)
        self.provider._playlists = {
            'gmusic:playlist:foo': Playlist(
                uri='gmusic:playlist:foo',
                name='foo',
                tracks=[Track(uri='gmusic:track:test_track')]),
            'gmusic:playlist:boo': Playlist(
                uri='gmusic:playlist:boo', name='boo', tracks=[]),
        }

    def test_create(self):
        self.provider.create('foo')

    def test_delete(self):
        self.provider.delete('gmusic:playlist:foo')

    def test_save(self):
        self.provider.save(Playlist())

    def test_lookup_valid(self):
        result = self.provider.lookup('gmusic:playlist:foo')

        self.assertIsNotNone(result)

    def test_lookup_invalid(self):
        result = self.provider.lookup('gmusic:playlist:bar')

        self.assertIsNone(result)
