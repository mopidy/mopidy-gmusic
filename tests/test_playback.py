import logging

import time

import unittest

import mock

from mopidy.models import Track

from mopidy_gmusic.playback import GMusicPlaybackProvider

from mopidy_gmusic.session import GMusicSession


logger = logging.getLogger(__name__)


class PlaybackTest(unittest.TestCase):

    _track = Track(
        uri='gmusic:track:test_track',
        name='Test Track',
        length=1000  # 1s track length
    )

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

    def _setup_player(self):
        audio = mock.Mock()
        ext = mock.Mock()
        ext.session = mock.Mock()

        playback = GMusicPlaybackProvider(audio, ext)
        return playback

    def test_playback(self):
        playback = self._setup_player()
        playback.play(self._track)

        playback.backend.session.get_stream_url.assert_called_once()
        playback.audio.start_playback.assert_called_once_with()
        self.assertEqual(
            playback.backend.session.increment_song_playcount.call_count,
            0,
            'increment_song_playcount() was called')

    def test_stop_full_track(self):
        playback = self._setup_player()
        playback.play(self._track)
        # sleep for track length
        time.sleep(0.8)
        playback.stop()
        logger.debug(
            'call count: %d',
            playback.backend.session.increment_song_playcount.call_count)
        playback.backend.session.increment_song_playcount\
            .assert_called_once_with(u'test_track')

    def test_stop_skip(self):
        playback = self._setup_player()
        playback.play(self._track)
        # sleep for 1/3 of track length
        time.sleep(0.3)
        playback.stop()
        self.assertEqual(
            playback.backend.session.increment_song_playcount.call_count,
            0,
            'increment_song_playcount() was called')
