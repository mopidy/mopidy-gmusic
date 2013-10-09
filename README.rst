*************
Mopidy-GMusic
*************

.. image:: https://pypip.in/v/Mopidy-GMusic/badge.png
    :target: https://crate.io/packages/Mopidy-GMusic/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/Mopidy-GMusic/badge.png
    :target: https://crate.io/packages/Mopidy-GMusic/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/hechtus/mopidy-gmusic.png?branch=master
    :target: https://travis-ci.org/hechtus/mopidy-gmusic
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/hechtus/mopidy-gmusic/badge.png?branch=master
   :target: https://coveralls.io/r/hechtus/mopidy-gmusic?branch=master
   :alt: Test coverage

`Mopidy <http://www.mopidy.com/>`_ extension for playing music from
`Google Play Music <https://play.google.com/music/>`_.


Usage
-----

#. You must have a Google account and some music in your library

#. You must have an Android device registered for Google Play Music.

#. Install the `Google Music API
   <https://github.com/simon-weber/Unofficial-Google-Music-API>`_
   by running::
   
    pip install gmusicapi

#. Install the Mopidy-GMusic extension by running::

    pip install mopidy-gmusic

#. Before starting Mopidy, you must add your Google username,
   password, and Android mobile device ID to the Mopidy configuration
   file::

    [gmusic]
    username = alice
    password = secret
    deviceid = 0123456789abcdef
   
   The mobile device ID is a 16-digit hexadecimal string (without a
   '0x' prefix) identifying the Android device registered for Google
   Play Music. You can obtain this ID by dialing `*#*#8255#*#*` on
   your phone (see the aid) or using this `App
   <https://play.google.com/store/apps/details?id=com.evozi.deviceid>`_
   (see the Google Service Framework ID Key). You may also leave this
   field empty. Mopidy will try to find the ID by itself. See the
   Mopidy logs for more information.

Project resources
-----------------

- `Source code <https://github.com/hechtus/mopidy-gmusic>`_
- `Issue tracker <https://github.com/hechtus/mopidy-gmusic/issues>`_
- `Download development snapshot
  <https://github.com/hechtus/mopidy-gmusic/archive/develop.zip>`_
