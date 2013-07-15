from __future__ import unicode_literals

import logging

from mopidy.backends import base, listener
from mopidy.models import Playlist

from . import translator

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

        for subdir, entry in self.backend.session.get_all_playlist_ids().items():
            for name, ids in entry.items():
                for i in ids:
                    tracks = [translator.to_mopidy_track(track) for track in 
                              self.backend.session.get_playlist_songs(i)]
                  
                    playlist = Playlist(uri='gmusic:' + i, name=name, tracks=tracks)
                    playlists.append(playlist)

        self.playlists = playlists
        listener.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        pass  # TODO
