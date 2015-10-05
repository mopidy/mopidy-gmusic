from __future__ import unicode_literals

import logging

from mopidy import backend

logger = logging.getLogger(__name__)


class GMusicPlaybackProvider(backend.PlaybackProvider):
    def translate_uri(self, uri):
        track_id = uri.rsplit(':')[-1]
        stream_uri = self.backend.session.get_stream_url(track_id)
        logger.debug('Translated: %s -> %s', uri, stream_uri)
        return stream_uri
