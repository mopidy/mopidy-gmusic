import logging

from collections import OrderedDict

logger = logging.getLogger(__name__)


class LruCache(OrderedDict):
    def __init__(self, max_size=1024):
        if max_size <= 0:
            raise ValueError('Invalid size')
        OrderedDict.__init__(self)
        self._max_size = max_size
        self._check_limit()

    def get_max_size(self):
        return self._max_size

    def hit(self, key):
        if key in self:
            val = self[key]
            self[key] = val
            # logger.debug('HIT: %r -> %r', key, val)
            return val
        # logger.debug('MISS: %r', key)
        return None

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)
        self._check_limit()

    def _check_limit(self):
        while len(self) > self._max_size:
            # delete oldest entries
            k = self.keys()[0]
            del self[k]
