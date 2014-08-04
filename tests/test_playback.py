import unittest

import mock

from mopidy.models import Track

from mopidy_gmusic.playback import GMusicPlaybackProvider

from mopidy_gmusic.session import GMusicSession


class PlayTest(unittest.TestCase):

    def test_init(self):
        audio = mock.Mock()
        backend = mock.Mock()
        p = GMusicPlaybackProvider(audio, backend)
        self.assertIsNotNone(p)

    def test_play_invalid(self):
        audio = mock.Mock()
        audio.prepare_change = mock.Mock()
        audio.set_uri = mock.Mock()
        audio.start_playback = mock.Mock()
        backend = mock.Mock()
        backend.session = GMusicSession()
        p = GMusicPlaybackProvider(audio, backend)
        self.assertFalse(p.play(Track(uri='gmusic:track:invalid_uri')))
        self.assertEqual(p.audio.prepare_change.call_count, 0)
        self.assertEqual(p.audio.set_uri.call_count, 0)
        self.assertEqual(p.audio.start_playback.call_count, 0)

    def test_play_valid(self):
        audio = mock.Mock()
        audio.prepare_change = mock.Mock()
        audio.set_uri = mock.Mock()
        audio.start_playback = mock.Mock()
        backend = mock.Mock()
        backend.session.get_stream_url = mock.Mock(
            return_value='http://stream.example.com/foo.mp3')
        p = GMusicPlaybackProvider(audio, backend)
        self.assertIsNotNone(p.play(Track(uri='gmusic:track:valid_uri')))
        self.assertEqual(p.audio.prepare_change.call_count, 1)
        self.assertEqual(p.audio.set_uri.call_count, 1)
        self.assertEqual(p.audio.start_playback.call_count, 1)
