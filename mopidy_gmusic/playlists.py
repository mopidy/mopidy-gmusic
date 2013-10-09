from __future__ import unicode_literals

import logging

from mopidy.backends import base, listener
from mopidy.models import Playlist

logger = logging.getLogger('mopidy.backends.gmusic')


class GMusicPlaylistsProvider(base.BasePlaylistsProvider):

    def create(self, name):
        pass  # TODO

    def delete(self, uri):
        pass  # TODO

    def lookup(self, uri):
        for playlist in self.playlists:
            if playlist.uri == uri:
                return playlist

    def refresh(self):
        playlists = []

        for playlist in self.backend.session.get_all_playlist_contents():
            tracks = []
            for track in playlist['tracks']:
                if not track['deleted']:
                    tracks += self.backend.library.lookup('gmusic:track:' +
                                                          track['trackId'])

            playlist = Playlist(uri='gmusic:playlist:' + playlist['id'],
                                name=playlist['name'],
                                tracks=tracks)
            playlists.append(playlist)

        self.playlists = playlists
        listener.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        pass  # TODO
