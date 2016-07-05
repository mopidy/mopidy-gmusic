from __future__ import unicode_literals

import hashlib

from mopidy.models import Ref


def album_to_ref(album):
    """Convert a mopidy album to a mopidy ref."""
    name = ''
    for artist in album.artists:
        if len(name) > 0:
            name += ', '
        name += artist.name
    if (len(name)) > 0:
        name += ' - '
    if album.name:
        name += album.name
    else:
        name += 'Unknown Album'
    return Ref.directory(uri=album.uri, name=name)


def artist_to_ref(artist):
    """Convert a mopidy artist to a mopidy ref."""
    if artist.name:
        name = artist.name
    else:
        name = 'Unknown artist'
    return Ref.directory(uri=artist.uri, name=name)


def track_to_ref(track, with_track_no=False):
    """Convert a mopidy track to a mopidy ref."""
    if with_track_no and track.track_no > 0:
        name = '%d - ' % track.track_no
    else:
        name = ''
    for artist in track.artists:
        if len(name) > 0:
            name += ', '
        name += artist.name
    if (len(name)) > 0:
        name += ' - '
    name += track.name
    return Ref.track(uri=track.uri, name=name)


def get_images(song):
    if 'albumArtRef' in song:
        return [art_ref['url']
                for art_ref in song['albumArtRef']
                if 'url' in art_ref]

    return []


def create_id(u):
    return hashlib.md5(u.encode('utf-8')).hexdigest()
