from __future__ import unicode_literals

from mopidy.backends import base


class GMusicPlaybackProvider(base.BasePlaybackProvider):

    def play(self, track):
        url = self.backend.session.get_stream_url(track.uri.split(':')[2])
        if url is None:
            return False
        self.audio.prepare_change()
        self.audio.set_uri(url).get()
        return self.audio.start_playback().get()
