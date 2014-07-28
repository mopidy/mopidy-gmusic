from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.models import Playlist

logger = logging.getLogger(__name__)


class GMusicPlaylistsProvider(backend.PlaylistsProvider):

    def __init__(self, *args, **kwargs):
        super(GMusicPlaylistsProvider, self).__init__(*args, **kwargs)
        self._show_radio_stations_playlist = \
            self.backend.config['gmusic']['show_radio_stations_playlist']
        self._max_radio_stations = \
            self.backend.config['gmusic']['max_radio_stations']
        self._max_radio_tracks = \
            self.backend.config['gmusic']['max_radio_tracks']

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

        # add thumbs up playlist
        tracks = []
        for track in self.backend.session.get_thumbs_up_songs():
            trackId = None
            if 'trackId' in track:
                trackId = track['trackId']
            elif 'storeId' in track:
                trackId = track['storeId']
            if trackId:
                tracks += self.backend.library.lookup(
                    'gmusic:track:' + trackId)
        if len(tracks) > 0:
            playlist = Playlist(uri='gmusic:playlist:thumbs_up',
                                name='Thumbs up',
                                tracks=tracks)
            playlists.append(playlist)

        # load user playlists
        for playlist in self.backend.session.get_all_user_playlist_contents():
            tracks = []
            for track in playlist['tracks']:
                if not track['deleted']:
                    tracks += self.backend.library.lookup('gmusic:track:' +
                                                          track['trackId'])

            playlist = Playlist(uri='gmusic:playlist:' + playlist['id'],
                                name=playlist['name'],
                                tracks=tracks)
            playlists.append(playlist)

        # load shared playlists
        for playlist in self.backend.session.get_all_playlists():
            if playlist.get('type') == 'SHARED':
                tracks = []
                tracklist = self.backend.session.get_shared_playlist_contents(
                    playlist['shareToken'])
                for track in tracklist:
                        tracks += self.backend.library.lookup('gmusic:track:' +
                                                              track['trackId'])
                playlist = Playlist(uri='gmusic:playlist:' + playlist['id'],
                                    name=playlist['name'],
                                    tracks=tracks)
                playlists.append(playlist)

        l = len(playlists)
        logger.info('Loaded %d playlists from Google Music', len(playlists))

        # load radios as playlists
        if self._show_radio_stations_playlist:
            logger.info('Starting to loading radio stations')
            stations = self.backend.session.get_radio_stations(
                self._max_radio_stations)
            for station in stations:
                tracks = []
                tracklist = self.backend.session.get_station_tracks(
                    station['id'],
                    self._max_radio_tracks)
                for track in tracklist:
                    tracks += self.backend.library.lookup('gmusic:track:' +
                                                          track['nid'])
                playlist = Playlist(uri='gmusic:playlist:' + station['id'],
                                    name=station['name'],
                                    tracks=tracks)
                playlists.append(playlist)
            logger.info('Loaded %d radios from Google Music',
                        len(playlists) - l)

        self.playlists = playlists
        backend.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        pass  # TODO
