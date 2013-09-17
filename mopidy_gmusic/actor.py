from __future__ import unicode_literals

import pykka

from mopidy.backends import base

from .library import GMusicLibraryProvider
from .playback import GMusicPlaybackProvider
from .playlists import GMusicPlaylistsProvider
from .session import GMusicSession


class GMusicBackend(pykka.ThreadingActor, base.Backend):
    def __init__(self, config, audio):
        super(GMusicBackend, self).__init__()

        self.config = config

        self.library = GMusicLibraryProvider(backend=self)
        self.playback = GMusicPlaybackProvider(audio=audio, backend=self)
        self.playlists = GMusicPlaylistsProvider(backend=self)
        self.session = GMusicSession()

        self.uri_schemes = ['gmusic']

    def on_start(self):
        self.session.login(self.config['gmusic']['username'],
                           self.config['gmusic']['password'],
                           self.config['gmusic']['deviceid'])
        self.library.refresh()
        self.playlists.refresh()

    def on_stop(self):
        self.session.logout()
