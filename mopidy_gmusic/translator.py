from __future__ import unicode_literals

import logging

from mopidy.models import Artist, Album, Track

logger = logging.getLogger('mopidy.backends.gmusic')

track_cache = {}

def to_mopidy_track(track):
    if track is None:
        return
    uri = 'gmusic:' + track['id']
    if uri in track_cache:
        return track_cache[uri]
    track_cache[uri] = Track(
        uri = uri,
        name = track['name'],
        artists = [Artist(name = track['artist'])],
        album = to_mopidy_album(track),
        track_no = track['track'],
        disc_no = track['disc'],
        date = track['year'],
        length = track['durationMillis'],
        bitrate = track['bitrate'])
    return track_cache[uri]

def lookup_mopidy_track(uri):
    return track_cache[uri]

def to_mopidy_album(track):
    if track is None:
        return
    artist = track['albumArtist']
    if artist.strip() == '':
        artist = track['artist']
    return Album(
        name = track['album'],
        artists = [Artist(name = artist)],
        num_tracks = track['totalTracks'],
        num_discs = track['totalDiscs'],
        date = track['year'])
