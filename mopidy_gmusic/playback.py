from __future__ import unicode_literals

from mopidy import backend


class GMusicPlaybackProvider(backend.PlaybackProvider):

    def play(self, track):
        url = self.backend.session.get_stream_url(track.uri.split(':')[2])
        if url is None:
            return False
        self.audio.prepare_change()
        self.audio.set_uri(url).get()
        return self.audio.start_playback().get()
