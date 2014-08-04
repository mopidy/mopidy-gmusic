import unittest

import mock

from mopidy.models import Playlist, Track

from mopidy_gmusic.playlists import GMusicPlaylistsProvider

from tests.test_extension import ExtensionTest


class PlaylistsTest(unittest.TestCase):

    def test_create(self):
        backend = mock.Mock()
        backend.config = ExtensionTest.get_config()
        p = GMusicPlaylistsProvider(backend)
        p.create('foo')

    def test_delete(self):
        backend = mock.Mock()
        backend.config = ExtensionTest.get_config()
        p = GMusicPlaylistsProvider(backend)
        p.delete('gmusic:playlist:foo')

    def test_save(self):
        backend = mock.Mock()
        backend.config = ExtensionTest.get_config()
        p = GMusicPlaylistsProvider(backend)
        p.save(Playlist())

    def test_lookup_valid(self):
        backend = mock.Mock()
        backend.config = ExtensionTest.get_config()
        p = GMusicPlaylistsProvider(backend)
        p.playlists = [Playlist(uri='gmusic:playlist:foo',
                                name='foo',
                                tracks=[Track(uri='gmusic:track:test_track')])]
        pl = p.lookup('gmusic:playlist:foo')
        self.assertIsNotNone(pl)

    def test_lookup_invalid(self):
        backend = mock.Mock()
        backend.config = ExtensionTest.get_config()
        p = GMusicPlaylistsProvider(backend)
        p.playlists = [Playlist(uri='gmusic:playlist:foo',
                                name='foo',
                                tracks=[Track(uri='gmusic:track:test_track')])]
        pl = p.lookup('gmusic:playlist:bar')
        self.assertIsNone(pl)
