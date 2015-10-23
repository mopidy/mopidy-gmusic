import unittest

from mopidy_gmusic.lru_cache import LruCache


class ExtensionTest(unittest.TestCase):

    def test_init(self):
        c = LruCache()
        self.assertIsNotNone(c)
        self.assertTrue(c.get_max_size() > 0,
                        'Size should be greater then zero!')

    def test_init_size(self):
        c = LruCache(5)
        self.assertEqual(c.get_max_size(), 5)

    def test_init_error(self):
        for size in [0, -1]:
            self.assertRaises(ValueError, LruCache, size)

    def test_add(self):
        c = LruCache(2)
        c['a'] = 1
        c['b'] = 2
        c['c'] = 3
        self.assertNotIn('a', c)
        self.assertIn('b', c)
        self.assertIn('c', c)

    def test_update(self):
        c = LruCache(2)
        c['a'] = 1
        c['b'] = 2
        c['a'] = 4
        c['c'] = 3
        self.assertIn('a', c)
        self.assertNotIn('b', c)
        self.assertIn('c', c)

    def test_hit(self):
        c = LruCache(2)
        c['a'] = 1
        c['b'] = 2
        self.assertEqual(c.hit('a'), 1)
        c['c'] = 3
        self.assertIn('a', c)
        self.assertNotIn('b', c)
        self.assertIn('c', c)

    def test_miss(self):
        c = LruCache(2)
        c['a'] = 1
        c['b'] = 2
        self.assertIsNone(c.hit('c'))
