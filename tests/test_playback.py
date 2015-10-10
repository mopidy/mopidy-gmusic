from __future__ import unicode_literals

import mock

import pytest

from mopidy_gmusic import playback


@pytest.fixture
def backend():
    backend_mock = mock.Mock()
    backend_mock.config = {
        'gmusic': {
            'bitrate': 160,
        }
    }
    return backend_mock


@pytest.fixture
def provider(backend):
    return playback.GMusicPlaybackProvider(audio=None, backend=backend)


def test_translate_invalid_uri(backend, provider):
    backend.session.get_stream_url.return_value = None

    assert provider.translate_uri('gmusic:track:invalid_uri') is None


def test_change_track_valid(backend, provider):
    stream_url = 'http://stream.example.com/foo.mp3'
    backend.session.get_stream_url.return_value = stream_url

    assert provider.translate_uri('gmusic:track:valid_uri') == stream_url
    backend.session.get_stream_url.assert_called_once_with(
        'valid_uri', quality='med')


def test_changed_bitrate(backend, provider):
    stream_url = 'http://stream.example.com/foo.mp3'
    backend.session.get_stream_url.return_value = stream_url
    backend.config['gmusic']['bitrate'] = 320

    assert provider.translate_uri('gmusic:track:valid_uri') == stream_url
    backend.session.get_stream_url.assert_called_once_with(
        'valid_uri', quality='hi')
