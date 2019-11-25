
*********
Changelog
*********


v4.0.0rc1 (UNRELEASED)
======================

- Require Mopidy >= 3.0.0a5. (PR: #227)
- Require Python >= 3.7. (Fixes: #226, PR: #227)
- Require gmusicapi >= 12.1.
- Switch from username/password to OAuth flow.
- Change name of the "Promoted" playlist to "Top".
- Update project setup. (PR: #227)


v3.0.0 (2018-06-27)
===================

- Add Top Tracks to Artists.
- Work around broken track IDs returned by Google.
- Require Device ID to be set in the config.


v2.0.0 (2016-11-2)
===================

- Require gmusicapi >= 10.1.
- Make search work for gmusicapi >= 10.0. (Fixes: #116, PR: #117)
- Enable search for accounts without All Access. (PR: #117)
- Require cachetools. (PR: #119)
- Caching should be more consistent. (Fixes: #63, PR: #122)
- Autodetect All Access if not specified in config. (PR: #123)
- General refactoring. (PR: #120, #121)
- Much faster playlist loading. (PR: #130)
- Library browse rewrite. (PR: #131)
- Add IFL playlist and improve radio caching. (PR: #135)


v1.0.0 (2015-10-23)
===================

- Require Mopidy >= 1.0.
- Require gmusicapi >= 6.0.
- Update to work with new playback API in Mopidy 1.0. (PR: #75)
- Update to work with new search API in Mopidy 1.0.
- Fix crash when tracks lack album or artist information. (Fixes: #74, PR: #24,
  also thanks to PRs #27, #64)
- Log error on login failure instead of swallowing the error. (PR: #36)
- Add support for All Access search and lookup (PR: #34)
- Add dynamic playlist based on top rated tracks.
- Add support for radio stations in browser and/or as playlists.
- Add support for browsing artists and albums in the cached library.
- Add cover art to ``Album.images`` model field.
- Add background refreshing of library and playlists. (Fixes: #21)
- Fix authentication issues. (Fixes: #82, #87)
- Add LRU cache for All Access albums and tracks.
- Increment Google's play count if 50% or 240s of the track has been played.
  (PR: #51, and later changes)
- Let gmusicapi use the device's MAC address as device ID by default.
- Fix increasing of play counts in Google Play Music. (Fixes: #96)
- Fix scrobbling of tracks to Last.fm through Mopidy-Scrobbler. (Fixes: #60)
- Fix unhandled crashes on network connectivity issues. (Fixes: #85)
- Add ``gmusic/bitrate`` config to select streaming bitrate.


v0.3.0 (2014-01-28)
===================

- Issue #19: Public playlist support
- Issue #16: All playlist files are playable now
- Require Mopidy >= 0.18.


v0.2.2 (2013-11-11)
===================

- Issue #17: Fixed a bug regarding various artist albums
  (compilations)
- Issue #18: Fixed Google Music API playlist call for version 3.0.0
- Issue #16 (partial): All Access tracks in playlists are playable now


v0.2.1 (2013-10-11)
===================

- Issue #15: Fixed a bug regarding the translation of Google album
  artists to Mopidy album artists


v0.2 (2013-10-11)
=================

- Issue #12: Now able to play music from Google All Access
- Issue #9: Switched to the Mobileclient API of Google Music API
- Issue #4: Generate Album and Artist Search Results


v0.1.1 (2013-09-23)
===================

- Issue #11: Browsing the library fixed by implementing find_exact()


v0.1 (2013-09-16)
=================

- Initial release
