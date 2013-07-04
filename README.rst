Mopidy-GMusic
=============

`Mopidy <http://www.mopidy.com/>`_ extension for playing music from
`Google Play Music <https://play.google.com/music/>`_.


Usage
-----

#. You must register for a user account at http://www.soundcloud.com/

#. Install the Mopidy-Soundcloud extension by running::

    sudo pip install mopidy-gmusic

#. You need a SoundCloud authentication token for Mopidy from
   http://www.mopidy.com/authenticate

#. Add the authentication token to the ``mopidy.conf`` config file::

    [soundcloud]
    auth_key = 1-1111-1111111

#. Extra playlists from http://www.soundcloud.com/explore can be retrieved by
   setting the ``soundcloud/explore`` config value. For example, if you want
   Smooth Jazz from https://soundcloud.com/explore/jazz%2Bblues your entry
   would be "jazz%2Bblues/Smooth Jazz". Example config::

    [soundcloud]
    auth_key = 1-1111-1111111
    explore = electronic/Ambient, pop/New Wave, rock/Indie


Project resources
-----------------

- `Source code <https://github.com/dz0ny/mopidy-soundcloud>`_
- `Issue tracker <https://github.com/mopidy/mopidy-soundcloud/issues>`_
- `Download development snapshot
  <https://github.com/dz0ny/mopidy-soundcloud/tarball/develop#egg=mopidy-soundcloud-dev>`_
