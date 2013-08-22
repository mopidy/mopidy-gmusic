from __future__ import unicode_literals

import logging

from gmusicapi import Webclient, CallFailure

logger = logging.getLogger('mopidy.backends.gmusic')


class GMusicSession(object):

    def __init__(self):
        super(GMusicSession, self).__init__()
        logger.info('Mopidy uses Google Music')
        self.api = Webclient()

    def login(self, username, password):
        if self.api.is_authenticated():
            self.api.logout()
        try:
            self.api.login(username, password)
        except CallFailure as error:
            logger.error(u'Failed to login as "%s": %s', username, error)
        return self.api.is_authenticated()

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
                return self.api.get_stream_urls(song_id)[0]
            except CallFailure as error:
                logger.error(u'Failed to lookup "%s": %s', song_id, error)

    def get_all_playlist_ids(self):
        if self.api.is_authenticated():
            return self.api.get_all_playlist_ids()
        else:
            return {}

    def get_playlist_songs(self, playlist_id):
        if self.api.is_authenticated():
            return self.api.get_playlist_songs(playlist_id)
        else:
            return {}
