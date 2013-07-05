from __future__ import unicode_literals

import logging

from mopidy.models import Artist, Album, Track, Playlist
from gmusicapi import CallFailure

logger = logging.getLogger('mopidy.backends.gmusic')

def to_mopidy_track(track):
    if track is None:
        return
    try:
        # This is too slow here ...
        # uri = self.backend.api.get_stream_url(track['id'])
        uri = "TBD"
    except CallFailure as error:
        uri = ''
        logger.debug(u'Failed to lookup "%s": %s', track['id'], error)
    return Track(
        uri = uri,
        name = track['name'],
        artists = [to_mopidy_artist(track)],
        album = to_mopidy_album(track),
        track_no = track['track'],
        disc_no = track['disc'],
        date = track['year'],
        length = track['durationMillis'],
        bitrate = track['bitrate'])

def to_mopidy_artist(track):
    if track is None:
        return
    return Artist(
        name = track['artist'])

def to_mopidy_album(track):
    if track is None:
        return
    return Album(
        name = track['album'],
        artists = [to_mopidy_artist(track)],
        num_tracks = track['totalTracks'],
        num_discs = track['totalDiscs'],
        date = track['year'])
        # Doesn't make sense when fetched from the client and not from mopidy
        # images = [track['albumArtUrl']])
