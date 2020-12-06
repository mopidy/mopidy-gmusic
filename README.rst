*******
WARNING
*******

As of December 2020, **the Google Play Music service is no longer operational**.
Thus, the maintenance of this extension has been stopped.
The ``mopidy-gmusic`` package has been removed from Debian/Ubuntu,
and the Git repo is put into archive mode.

----

*************
Mopidy-GMusic
*************

.. image:: https://img.shields.io/pypi/v/Mopidy-GMusic
    :target: https://pypi.org/project/Mopidy-GMusic/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/circleci/build/gh/mopidy/mopidy-gmusic
    :target: https://circleci.com/gh/mopidy/mopidy-gmusic
    :alt: CircleCI build status

.. image:: https://img.shields.io/codecov/c/gh/mopidy/mopidy-gmusic
    :target: https://codecov.io/gh/mopidy/mopidy-gmusic
    :alt: Test coverage

`Mopidy <https://mopidy.com/>`_ extension for playing music from
`Google Play Music <https://play.google.com/music/>`_.


Dependencies
============

You must have a Google account, and either:

- have some music uploaded to your Google Play Music library, or
- have a paid subscription for Google Play Music.


Installation
============

Install by running::

    sudo python3 -m pip install Mopidy-GMusic

See https://mopidy.com/ext/gmusic/ for alternative installation methods


Configuration
=============

Run ``mopidy gmusic login`` to obtain a refresh token, and then include it in
your config file::

   [gmusic]
   refresh_token = <your refresh token>

Google Play Music now requires all clients to provide a device ID. In the past,
Mopidy-GMusic generated one automatically from your MAC address, but Google
seems to have changed their API in a way that prevents this from working.
Therefore you will need to configure one manually.

If no device ID is configured, Mopidy-GMusic will output a list of registered
devices and their IDs. You can either use one of those IDs in your config file,
or use the special value ``mac`` if you want gmusicapi to use the old method of
generating an ID from your MAC address::

    [gmusic]
    deviceid = 0123456789abcdef
    # or
    deviceid = mac

By default, All Access will be enabled automatically if you subscribe. You may
force enable or disable it by using the ``all_access`` option::

    [gmusic]
    all_access = true

By default, the bitrate is set to 160 kbps. You can change this to either 128
or 320 kbps by setting::

    [gmusic]
    bitrate = 320

All Access radios are available as browsable content or playlist. The following
are the default config values::

    [gmusic]
    # Show radio stations in content browser
    radio_stations_in_browse = true
    # Show radio stations as playlists
    radio_stations_as_playlists = false
    # Limit the number of radio stations, unlimited if unset
    radio_stations_count =
    # Limit the number or tracks for each radio station
    radio_tracks_count = 25

The library and playlists are automatically refresh at regular intervals.
Refreshing can be CPU intensive on very low-powered machines, e.g. Raspberry Pi
Zero. The refresh intervals can be configured::

    [gmusic]
    # How often to refresh the library, in minutes
    refresh_library = 1440
    # How often to refresh playlists, in minutes
    refresh_playlists = 60

Usage
=====

The extension is enabled by default if all dependencies are
available. You can simply browse through your library and search for
tracks, albums, and artists. Google Play Music playlists are imported
as well. You can even add songs from your All Access subscription to
your library. Mopidy will able to play them.


Project resources
=================

- `Source code <https://github.com/mopidy/mopidy-gmusic>`_
- `Issue tracker <https://github.com/mopidy/mopidy-gmusic/issues>`_
- `Changelog <https://github.com/mopidy/mopidy-gmusic/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Ronald Hecht <https://github.com/hechtus>`_
- Current maintainer: `Kaleb Elwert <https://github.com/belak>`_
- `Contributors <https://github.com/mopidy/mopidy-gmusic/graphs/contributors>`_
