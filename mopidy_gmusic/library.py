from __future__ import unicode_literals

import logging
import urlparse

from mopidy.backends import base
from mopidy.models import SearchResult

from . import translator

logger = logging.getLogger('mopidy.backends.gmusic')

class GMusicLibraryProvider(base.BaseLibraryProvider):

    def find_exact(self, query=None, uris=None):
        return self.search(query=query, uris=uris)

    def lookup(self, uri):
        return [translator.lookup_mopidy_track(uri)]

    def refresh(self, uri=None):
        self.songs = self.backend.session.get_all_songs()

    def search(self, query=None, uris=None):
        if query is None:
            query = {}
        self._validate_query(query)
        result_tracks = self.songs
        
        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip().lower()

                uri_filter = lambda t: q in 'gmusic:' + t['id']
                track_filter = lambda t: q in t['name'].lower()
                album_filter = lambda t: q in t['album'].lower()
                artist_filter = lambda t: q in t['artist'].lower()
                date_filter = lambda t: q in str(t['year'])
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
                
        return SearchResult(uri = 'gmusic:search',
                            tracks = [translator.to_mopidy_track(track) for track in result_tracks])
              
    def _validate_query(self, query):
        for (_, values) in query.iteritems():
            if not values:
                raise LookupError('Missing query')
            for value in values:
                if not value:
                    raise LookupError('Missing query')
