from __future__ import unicode_literals

import logging

from mopidy.backends import base
from mopidy.models import Artist, Album, Track, Playlist
from gmusicapi import CallFailure

logger = logging.getLogger('mopidy.backends.gmusic')

class GMusicPlaybackProvider(base.BasePlaybackProvider):

    def play(self, track):
        self.audio.prepare_change()
        try:
            url = self.backend.api.get_stream_url(track.uri.split(':')[1])
        except CallFailure as error:
            logger.debug(u'Failed to lookup "%s": %s', track.uri, error)
            return False
        self.audio.set_uri(url).get()
        self.audio.set_metadata(track)
        return self.audio.start_playback().get()
