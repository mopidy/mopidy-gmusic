from __future__ import unicode_literals

import logging
import time

from threading import Timer

from mopidy import backend

import pykka

from .library import GMusicLibraryProvider
from .playback import GMusicPlaybackProvider
from .playlists import GMusicPlaylistsProvider
from .session import GMusicSession

logger = logging.getLogger(__name__)


class GMusicBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(GMusicBackend, self).__init__()

        self._refresh_timer = None
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
        self.library.set_all_access(self.config['gmusic']['all_access'])
        # wait a few seconds to let mopidy settle
        # then refresh google music content asynchronously
        self._sched_refresh(5.0)

    def on_stop(self):
        if self._refresh_timer:
            self._refresh_timer.cancel()
            self._refresh_timer = None
        self.session.logout()

    def _refresh_content(self):
        logger.debug('Start refreshing gmusic content')
        t0 = round(time.time())
        self.library.refresh()
        self.playlists.refresh()
        # schedule next refresh
        refresh_playlists = self.config['gmusic']['refresh_playlists']
        if refresh_playlists > 0:
            self._sched_refresh(refresh_playlists * 60.0)
        t1 = round(time.time())
        logger.debug('Finished refreshing gmusic content, took %ds', t1 - t0)

    def _sched_refresh(self, seconds):
        self._refresh_timer = Timer(seconds, self._refresh_content)
        self._refresh_timer.start()
