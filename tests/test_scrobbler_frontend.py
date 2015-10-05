from __future__ import unicode_literals

import mock

from mopidy import models

import pytest

from mopidy_gmusic import scrobbler_frontend


@pytest.yield_fixture
def send_mock():
    patcher = mock.patch.object(scrobbler_frontend.listener, 'send')
    yield patcher.start()
    patcher.stop()


@pytest.fixture
def frontend(send_mock):
    return scrobbler_frontend.GMusicScrobblerFrontend(config={}, core=None)


def test_aborts_if_less_than_half_is_played(frontend, send_mock):
    track = models.Track(uri='gmusic:track:foo', length=60000)
    tl_track = models.TlTrack(tlid=17, track=track)

    frontend.track_playback_ended(tl_track, 20000)

    assert send_mock.call_count == 0


def test_scrobbles_if_more_than_half_is_played(frontend, send_mock):
    track = models.Track(uri='gmusic:track:foo', length=60000)
    tl_track = models.TlTrack(tlid=17, track=track)

    frontend.track_playback_ended(tl_track, 40000)

    send_mock.assert_called_once_with(
        mock.ANY, 'increment_song_playcount', track_id='foo')
