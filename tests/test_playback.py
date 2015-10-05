from __future__ import unicode_literals

import logging

import mock

from mopidy_gmusic import playback


logger = logging.getLogger(__name__)


def test_translate_invalid_uri():
    backend = mock.Mock()
    backend.session.get_stream_url.return_value = None
    provider = playback.GMusicPlaybackProvider(audio=None, backend=backend)

    assert provider.translate_uri('gmusic:track:invalid_uri') is None


def test_change_track_valid():
    stream_url = 'http://stream.example.com/foo.mp3'
    backend = mock.Mock()
    backend.session.get_stream_url.return_value = stream_url
    provider = playback.GMusicPlaybackProvider(audio=None, backend=backend)

    assert provider.translate_uri('gmusic:track:valid_uri') == stream_url
