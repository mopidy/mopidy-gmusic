*************
Mopidy-GMusic
*************

.. image:: https://pypip.in/v/Mopidy-GMusic/badge.png
    :target: https://pypi.python.org/pypi/Mopidy-GMusic/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/Mopidy-GMusic/badge.png
    :target: https://pypi.python.org/pypi/Mopidy-GMusic/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/hechtus/mopidy-gmusic.png?branch=master
    :target: https://travis-ci.org/hechtus/mopidy-gmusic
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/hechtus/mopidy-gmusic/badge.png?branch=master
   :target: https://coveralls.io/r/hechtus/mopidy-gmusic?branch=master
   :alt: Test coverage

`Mopidy <http://www.mopidy.com/>`_ extension for playing music from
`Google Play Music <https://play.google.com/music/>`_.


Dependencies
============

- You must have a Google account and some music and playlists in your
  library.

- You must have an Android device registered for Google Play Music.

- The `Unofficial Google Music API
  <https://github.com/simon-weber/Unofficial-Google-Music-API>`_ is
  needed to access Google Play Music. It will automatically be installed
  together with Mopidy-GMusic.


Installation
============

Install the Mopidy-GMusic extension by running::

    pip install mopidy-gmusic

Configuration
=============

Before starting Mopidy, you must add your Google username, password,
and Android mobile device ID to your Mopidy configuration file::

    [gmusic]
    username = alice
    password = secret
    deviceid = 0123456789abcdef

The mobile device ID is a 16-digit hexadecimal string (without a '0x'
prefix) identifying the Android device registered for Google Play
Music. You can obtain this ID by dialing ``*#*#8255#*#*`` on your
phone (see the aid) or using this `App
<https://play.google.com/store/apps/details?id=com.evozi.deviceid>`_
(see the Google Service Framework ID Key). You may also leave this
field empty. Mopidy will try to find the ID by itself. See the Mopidy
logs for more information.

All Access subscribers may enable All Access integration by adding this line::

    [gmusic]
    all_access = true

Usage
=====

The extension is enabled by default if all dependencies are
available. You can simply browse through your library and search for
tracks, albums, and artists. Google Play Music playlists are imported
as well. You can even add songs from your All Access subscription to
your library. Mopidy will able to play them.


Project resources
=================

- `Source code <https://github.com/hechtus/mopidy-gmusic>`_
- `Issue tracker <https://github.com/hechtus/mopidy-gmusic/issues>`_
- `Download development snapshot
  <https://github.com/hechtus/mopidy-gmusic/archive/develop.zip>`_


Changelog
=========

v0.3.0 (2014-01-28)
-------------------

- Issue #19: Public playlist support
- Issue #16: All playlist files are playable now
- Require Mopidy >= 0.18.


v0.2.2 (2013-11-11)
-------------------

- Issue #17: Fixed a bug regarding various artist albums
  (compilations)
- Issue #18: Fixed Google Music API playlist call for version 3.0.0
- Issue #16 (partial): All Access tracks in playlists are playable now


v0.2.1 (2013-10-11)
-------------------

- Issue #15: Fixed a bug regarding the translation of Google album
  artists to Mopidy album artists


v0.2 (2013-10-11)
-----------------

- Issue #12: Now able to play music from Google All Access
- Issue #9: Switched to the Mobileclient API of Google Music API
- Issue #4: Generate Album and Artist Search Results


v0.1.1 (2013-09-23)
-------------------

- Issue #11: Browsing the library fixed by implementing find_exact()


v0.1 (2013-09-16)
-----------------

- Initial release
