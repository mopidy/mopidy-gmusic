from __future__ import unicode_literals

import logging
import urlparse

import pykka

from mopidy import audio as audio_lib
from mopidy.backends import base
from mopidy.models import Track, Album, SearchResult

from gmusicapi import Webclient

from .library import GMusicLibraryProvider
from .playback import GMusicPlaybackProvider

logger = logging.getLogger('mopidy.backends.gmusic')


class GMusicBackend(pykka.ThreadingActor, base.Backend):
    def __init__(self, config, audio):
        super(GMusicBackend, self).__init__()

        self.config = config

        self.library = GMusicLibraryProvider(backend=self)
        self.playback = GMusicPlaybackProvider(audio=audio, backend=self)
        self.playlists = None

        self.uri_schemes = ['gmusic']

    def on_start(self):
        logger.info('Mopidy uses Google Music')
        logger.debug('Connecting to Google Music')
        self.api = Webclient()
        self.api.login(self.config['gmusic']['username'],
                       self.config['gmusic']['password'])
        self.songs = self.api.get_all_songs()

    def on_stop(self):
        self.api.logout()
