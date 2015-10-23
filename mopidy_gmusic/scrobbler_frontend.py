from __future__ import unicode_literals

import logging

from mopidy import core, listener

import pykka


logger = logging.getLogger(__name__)


class GMusicScrobblerFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(GMusicScrobblerFrontend, self).__init__()

    def track_playback_ended(self, tl_track, time_position):
        track = tl_track.track

        duration = track.length and track.length // 1000 or 0
        time_position = time_position // 1000

        if time_position < duration // 2 and time_position < 240:
            logger.debug(
                'Track not played long enough too scrobble. (50% or 240s)')
            return

        track_id = track.uri.rsplit(':')[-1]
        logger.debug('Increasing play count: %s', track_id)
        listener.send(
            GMusicScrobblerListener,
            'increment_song_playcount', track_id=track_id)


class GMusicScrobblerListener(listener.Listener):
    def increment_song_playcount(self, track_id):
        pass
