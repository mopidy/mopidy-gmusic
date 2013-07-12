from __future__ import unicode_literals

import pykka

from mopidy.backends import base

from gmusicapi import Webclient

from .library import GMusicLibraryProvider
from .playback import GMusicPlaybackProvider
from .session import GMusicSession


class GMusicBackend(pykka.ThreadingActor, base.Backend):
    def __init__(self, config, audio):
        super(GMusicBackend, self).__init__()

        self.config = config

        self.library = GMusicLibraryProvider(backend=self)
        self.playback = GMusicPlaybackProvider(audio=audio, backend=self)
        self.playlists = None
        self.session = GMusicSession()

        self.uri_schemes = ['gmusic']

    def on_start(self):
        self.session.login(self.config['gmusic']['username'],
                           self.config['gmusic']['password'])
        self.songs = self.session.get_all_songs()

    def on_stop(self):
        self.session.logout()
