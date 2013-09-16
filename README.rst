Mopidy-GMusic
=============

`Mopidy <http://www.mopidy.com/>`_ extension for playing music from
`Google Play Music <https://play.google.com/music/>`_.


Usage
-----

#. You must have a Google account and some music in your library

#. Install the `Google Music API
   <https://github.com/simon-weber/Unofficial-Google-Music-API>`_
   by running::
   
    sudo pip install gmusicapi

#. Install the Mopidy-GMusic extension by running::

    sudo pip install mopidy-gmusic

#. Before starting Mopidy, you must add your Google username and
   password to the Mopidy configuration file::

    [gmusic]
    username = alice
    password = secret
   
Project resources
-----------------

- `Source code <https://github.com/hechtus/mopidy-gmusic>`_
- `Issue tracker <https://github.com/hechtus/mopidy-gmusic/issues>`_
- `Download development snapshot
  <https://github.com/hechtus/mopidy-gmusic/archive/master.zip>`_
