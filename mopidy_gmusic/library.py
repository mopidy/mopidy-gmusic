from __future__ import unicode_literals

import logging
import hashlib

from mopidy.backends import base
from mopidy.models import Artist, Album, Track, SearchResult

logger = logging.getLogger('mopidy.backends.gmusic')


class GMusicLibraryProvider(base.BaseLibraryProvider):

    def find_exact(self, query=None, uris=None):
        if query is None:
            query = {}
        self._validate_query(query)
        result_tracks = self.tracks.values()

        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip()

                uri_filter = lambda t: q == t.uri
                track_filter = lambda t: q == t.name
                album_filter = lambda t: q == getattr(t, 'album', Album()).name
                artist_filter = lambda t: filter(
                    lambda a: q == a.name, t.artists)
                date_filter = lambda t: q == t.date
                any_filter = lambda t: (
                    track_filter(t) or album_filter(t) or
                    artist_filter(t) or uri_filter(t))

                if field == 'uri':
                    result_tracks = filter(uri_filter, result_tracks)
                elif field == 'track':
                    result_tracks = filter(track_filter, result_tracks)
                elif field == 'album':
                    result_tracks = filter(album_filter, result_tracks)
                elif field == 'artist':
                    result_tracks = filter(artist_filter, result_tracks)
                elif field == 'date':
                    result_tracks = filter(date_filter, result_tracks)
                elif field == 'any':
                    result_tracks = filter(any_filter, result_tracks)
                else:
                    raise LookupError('Invalid lookup field: %s' % field)

        return SearchResult(uri='gmusic:search', tracks=result_tracks)

    def lookup(self, uri):
        if uri.startswith('gmusic:track:'):
            return self._lookup_track(uri)
        elif uri.startswith('gmusic:album:'):
            return self._lookup_album(uri)
        elif uri.startswith('gmusic:artist:'):
            return self._lookup_artist(uri)
        else:
            return []

    def _lookup_track(self, uri):
        try:
            return [self.tracks[uri]]
        except KeyError:
            logger.debug('Failed to lookup %r', uri)
            return []

    def _lookup_album(self, uri):
        try:
            album = self.albums[uri]
        except KeyError:
            logger.debug('Failed to lookup %r', uri)
            return []
        tracks = self.find_exact(
            dict(album=album.name,
                 artist=[artist.name for artist in album.artists],
                 date=album.date)).tracks
        return sorted(tracks, key=lambda t: (t.disc_no,
                                             t.track_no))

    def _lookup_artist(self, uri):
        try:
            artist = self.artists[uri]
        except KeyError:
            logger.debug('Failed to lookup %r', uri)
            return []
        tracks = self.find_exact(
            dict(artist=artist.name)).tracks
        return sorted(tracks, key=lambda t: (t.album.date,
                                             t.album.name,
                                             t.disc_no,
                                             t.track_no))

    def refresh(self, uri=None):
        self.tracks = {}
        self.albums = {}
        self.artists = {}
        for song in self.backend.session.get_all_songs():
            self._to_mopidy_track(song)

    def search(self, query=None, uris=None):
        if query is None:
            query = {}
        self._validate_query(query)
        result_tracks = self.tracks.values()

        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip().lower()

                uri_filter = lambda t: q in t.uri.lower()
                track_filter = lambda t: q in t.name.lower()
                album_filter = lambda t: q in getattr(
                    t, 'album', Album()).name.lower()
                artist_filter = lambda t: filter(
                    lambda a: q in a.name.lower(), t.artists)
                date_filter = lambda t: t.date and t.date.startswith(q)
                any_filter = lambda t: track_filter(t) or album_filter(t) or \
                    artist_filter(t) or uri_filter(t)

                if field == 'uri':
                    result_tracks = filter(uri_filter, result_tracks)
                elif field == 'track':
                    result_tracks = filter(track_filter, result_tracks)
                elif field == 'album':
                    result_tracks = filter(album_filter, result_tracks)
                elif field == 'artist':
                    result_tracks = filter(artist_filter, result_tracks)
                elif field == 'date':
                    result_tracks = filter(date_filter, result_tracks)
                elif field == 'any':
                    result_tracks = filter(any_filter, result_tracks)
                else:
                    raise LookupError('Invalid lookup field: %s' % field)

        result_artists = set()
        result_albums = set()
        for track in result_tracks:
            result_artists |= track.artists
            result_albums.add(track.album)

        return SearchResult(uri='gmusic:search',
                            tracks=result_tracks,
                            artists=result_artists,
                            albums=result_albums)

    def _validate_query(self, query):
        for (_, values) in query.iteritems():
            if not values:
                raise LookupError('Missing query')
            for value in values:
                if not value:
                    raise LookupError('Missing query')

    def _to_mopidy_track(self, song):
        uri = 'gmusic:track:' + song['id']
        track = Track(
            uri=uri,
            name=song['title'],
            artists=[self._to_mopidy_artist(song)],
            album=self._to_mopidy_album(song),
            track_no=song.get('trackNumber', 1),
            disc_no=song.get('discNumber', 1),
            date=unicode(song.get('year', 0)),
            length=int(song['durationMillis']),
            bitrate=320)
        self.tracks[uri] = track
        return track

    def _to_mopidy_album(self, song):
        artist = song['albumArtist']
        if artist.strip() == '':
            artist = song['artist']
        date = unicode(song.get('year', 0))
        uri = 'gmusic:album:' + self._create_id(artist + song['album'] + date)
        album = Album(
            uri=uri,
            name=song['album'],
            artists=[self._to_mopidy_artist(song)],
            num_tracks=song.get('totalTrackCount', 1),
            num_discs=song.get('totalDiscCount', song.get('discNumber', 1)),
            date=date)
        self.albums[uri] = album
        return album

    def _to_mopidy_artist(self, song):
        uri = 'gmusic:artist:' + self._create_id(song['artist'])
        artist = Artist(
            uri=uri,
            name=song['artist'])
        self.artists[uri] = artist
        return artist

    def _create_id(self, u):
        return hashlib.md5(u.encode('utf-8')).hexdigest()
