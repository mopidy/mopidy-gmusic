from __future__ import unicode_literals

import logging

import gmusicapi


logger = logging.getLogger(__name__)


class GMusicSession(object):

    def __init__(self):
        super(GMusicSession, self).__init__()
        self.api = gmusicapi.Mobileclient()

    def login(self, username, password, device_id):
        if self.api.is_authenticated():
            self.api.logout()

        if device_id is None:
            device_id = gmusicapi.Mobileclient.FROM_MAC_ADDRESS

        authenticated = self.api.login(username, password, device_id)

        if authenticated:
            logger.info('Logged in to Google Music')
        else:
            logger.error('Failed to login to Google Music as "%s"', username)
        return authenticated

    def logout(self):
        if self.api.is_authenticated():
            return self.api.logout()
        else:
            return True

    def get_all_songs(self):
        if self.api.is_authenticated():
            return self.api.get_all_songs()
        else:
            return {}

    def get_stream_url(self, song_id):
        if self.api.is_authenticated():
            try:
                return self.api.get_stream_url(song_id)
            except gmusicapi.CallFailure as error:
                logger.error(u'Failed to lookup "%s": %s', song_id, error)

    def get_all_user_playlist_contents(self):
        if self.api.is_authenticated():
            return self.api.get_all_user_playlist_contents()
        else:
            return {}

    def get_shared_playlist_contents(self, shareToken):
        if self.api.is_authenticated():
            return self.api.get_shared_playlist_contents(shareToken)
        else:
            return {}

    def get_all_playlists(self):
        if self.api.is_authenticated():
            return self.api.get_all_playlists()
        else:
            return {}

    def get_promoted_songs(self):
        if self.api.is_authenticated():
            return self.api.get_promoted_songs()
        else:
            return {}

    def get_track_info(self, store_track_id):
        if self.api.is_authenticated():
            try:
                return self.api.get_track_info(store_track_id)
            except gmusicapi.CallFailure as error:
                logger.error(u'Failed to get All Access track info: %s', error)

    def get_album_info(self, albumid, include_tracks=True):
        if self.api.is_authenticated():
            try:
                return self.api.get_album_info(albumid, include_tracks)
            except gmusicapi.CallFailure as error:
                logger.error(u'Failed to get All Access album info: %s', error)

    def get_artist_info(
            self, artistid, include_albums=True, max_top_tracks=5,
            max_rel_artist=5):
        if self.api.is_authenticated():
            try:
                return self.api.get_artist_info(
                    artistid, include_albums, max_top_tracks, max_rel_artist)
            except gmusicapi.CallFailure as error:
                logger.error(
                    u'Failed to get All Access artist info: %s', error)

    def search_all_access(self, query, max_results=50):
        if self.api.is_authenticated():
            try:
                return self.api.search_all_access(query, max_results)
            except gmusicapi.CallFailure as error:
                logger.error(u'Failed to search All Access: %s', error)

    def get_all_stations(self):
        if self.api.is_authenticated():
            return self.api.get_all_stations()
        else:
            return []

    def get_radio_stations(self, num_stations=None):
        stations = self.get_all_stations()

        # Last played radio first
        stations.reverse()

        # Add IFL radio on top
        stations.insert(0, {'id': 'IFL', 'name': 'I\'m Feeling Lucky'})

        if num_stations is not None and num_stations > 0:
            # Limit radio stations
            stations = stations[:num_stations]

        return stations

    def get_station_tracks(self, station_id, num_tracks=25):
        if self.api.is_authenticated():
            return self.api.get_station_tracks(station_id, num_tracks)
        else:
            return {}

    def increment_song_playcount(self, song_id, plays=1, playtime=None):
        if self.api.is_authenticated():
            return self.api.increment_song_playcount(song_id, plays, playtime)
