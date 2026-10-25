# Sources - Sumber Data

> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total 35 komponen dalam kategori ini.

Komponen sumber menghasilkan stream entitas (track, artist, atau album) dari Spotify, Last.fm, atau chart publik. Setiap sumber adalah titik awal alur data; tidak menerima input.

### SpotifyPlaylist

**Label UI:** `Playlist` | **Output:** track | **Judul tampilan node:** `$name`

Loads tracks from a Spotify playlist

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uri`, entitas `playlist`; pencarian nama: name -> `name`, user -> `user`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Uri** - tipe: string. The URI or URL of the playlist
- **Name** - tipe: string. Display name of the playlist (shown on node)
- **User** - tipe: string. Owner of the playlist

**Dokumentasi resmi (help):**

This component generates a stream of tracks from a Spotify playlist. Specify the playlist by its URI or URL. If no URI is given but a name is provided, Spotify will be searched for a matching playlist.

---

### MySavedTracks

**Label UI:** `My Saved Tracks` | **Output:** track | **Judul tampilan node:** `My Saved Tracks`

Tracks from your Liked Songs library

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Limit** - tipe: integer, default: `50` (rentang: min 1; max 10000). Maximum number of tracks to return (max 10000)

**Dokumentasi resmi (help):**

This component generates a stream of tracks from your saved (liked) tracks.

---

### MyTopTracks

**Label UI:** `My Top Tracks` | **Output:** track | **Judul tampilan node:** `Top tracks ($time_range)`

Your most-listened tracks from your listening history

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Limit** - tipe: integer, default: `50` (rentang: min 1; max 50). Maximum number of tracks to return (Spotify max: 50)
- **Time Range** - tipe: string, default: `medium_term`. Nilai: `short_term, medium_term, long_term`. The time period

**Dokumentasi resmi (help):**

This component generates a stream of your most listened to tracks. Top tracks are available over three time spans: short term (last month or so), medium term (last half year or so), and long term (last several years). Note: Spotify limits this to a maximum of 50 tracks.

---

### UserTopArtists

**Label UI:** `My Top Artists` | **Output:** artist | **Judul tampilan node:** `Top artists ($time_range)`

Your most-listened artists from your listening history

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Count** - tipe: integer, default: `20` (rentang: min 1; max 50). Number of artists to return
- **Time Range** - tipe: string, default: `medium_term`. Nilai: `short_term, medium_term, long_term`. The time period for top artists

**Dokumentasi resmi (help):**

This component produces your top artists from Spotify based on your listening history. Use 'time range' to choose the time period: short_term (last 4 weeks), medium_term (last 6 months), or long_term (all time). These are artist entities — connect them to an Expand component to get tracks from these artists.

---

### AlbumSource

**Label UI:** `Album` | **Output:** track | **Judul tampilan node:** `$title`

Tracks from a Spotify album

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uri`, entitas `album`; pencarian nama: title -> `title`, artist -> `artist`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Title** - tipe: string. The title of the album
- **Artist** - tipe: string. The name of the artist
- **Uri** - tipe: string. The URI of the album (takes precedence over title/artist)

**Dokumentasi resmi (help):**

This component generates tracks from a Spotify album. If a URI is specified, that album is loaded directly. Otherwise, the album is found by searching for the given title and artist.

---

### TrackSource

**Label UI:** `Track URIs` | **Output:** track | **Judul tampilan node:** `$name`

Specific tracks given their URIs

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uris`, entitas `track`; pencarian nama: name -> `name`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Uris** - tipe: string. Track URIs or URLs, separated by commas, spaces, or newlines
- **Name** - tipe: string. Display name (auto-filled from URI)

**Dokumentasi resmi (help):**

This component generates one or more tracks given their URIs or URLs. Paste URIs or URLs separated by commas, spaces, or newlines, e.g.

spotify:track:69JnEQF6OCntGndij5BTlq
https://open.spotify.com/track/00t1USAjV7tiTDwlN6U44I

---

### TrackSourceByName

**Label UI:** `Track` | **Output:** track | **Judul tampilan node:** `$title`

Search for a track by name

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Title** - tipe: string. The title and artist of the track

**Dokumentasi resmi (help):**

This component searches for the most popular track matching the given title and artist.

---

### ArtistByName

**Label UI:** `Artist` | **Output:** artist | **Judul tampilan node:** `$title`

Search for an artist by name

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Title** - tipe: string. The name of the artist

**Dokumentasi resmi (help):**

This component searches for an artist matching the given name. It fetches multiple results and picks the best name match to avoid personalization and popularity bias returning the wrong artist.

---

### ArtistURIs

**Label UI:** `Artist URIs` | **Output:** artist | **Judul tampilan node:** `$name`

Specific artists given their URIs

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uris`, entitas `artist`; pencarian nama: name -> `name`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Uris** - tipe: string. Artist URIs or URLs, separated by commas, spaces, or newlines
- **Name** - tipe: string. Display name (auto-filled from URI)

**Dokumentasi resmi (help):**

This component loads one or more artists given their URIs or URLs. Paste URIs or URLs separated by commas, spaces, or newlines, e.g.

spotify:artist:4Z8W4fKeB5YxbusRsdQVPb
https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb

---

### AlbumByName

**Label UI:** `Album Entity` | **Output:** album | **Judul tampilan node:** `$title`

Search for an album by name (as an album entity)

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Title** - tipe: string. The title of the album
- **Artist** - tipe: string. The name of the artist
- **Uri** - tipe: string. The URI of the album (takes precedence over title/artist)

**Dokumentasi resmi (help):**

This component searches for an album matching the given title and artist, and produces it as an album entity (not as tracks). Use a 'To Tracks' adapter downstream to get the album's tracks.

---

### AlbumURIs

**Label UI:** `Album URIs` | **Output:** album | **Judul tampilan node:** `$name`

Specific albums given their URIs

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uris`, entitas `album`; pencarian nama: name -> `name`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Uris** - tipe: string. Album URIs or URLs, separated by commas, spaces, or newlines
- **Name** - tipe: string. Display name (auto-filled from URI)

**Dokumentasi resmi (help):**

This component loads one or more albums given their URIs or URLs. Paste URIs or URLs separated by commas, spaces, or newlines, e.g.

spotify:album:6dVIqQ8qmQ5GBnJ9shOYGE
https://open.spotify.com/album/6dVIqQ8qmQ5GBnJ9shOYGE

---

### LabelAlbums

**Label UI:** `Label Albums` | **Output:** album | **Judul tampilan node:** `$label albums`

Albums from a record label

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Label** - tipe: string. The record label name (e.g. 'Warp Records', 'Sub Pop')
- **Count** - tipe: integer, default: `20` (rentang: min 1; max 50). Maximum number of albums to return
- **Order** - tipe: string, default: `most_popular`. Nilai: `most_popular, newest, oldest`. How to order the results

**Dokumentasi resmi (help):**

This component searches for albums released on a given record label. Spotify's search is fuzzy, so results are filtered to albums whose label matches the query. Use 'order' to sort by popularity or release date, and 'count' to limit the number of albums returned.

---

### ArtistTopTracks

**Label UI:** `Artist Top Tracks` | **Output:** track | **Judul tampilan node:** `Top $name tracks`

Top tracks by a given artist

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uri`, entitas `artist`; pencarian nama: name -> `name`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Name** - tipe: string. The name of the artist
- **Uri** - tipe: string. The URI of the artist (takes precedence over name)

**Dokumentasi resmi (help):**

Generates a collection of popular tracks by the given artist. You can specify the artist either by name or by URI. If both are given, the URI is used.

---

### ArtistTracks

**Label UI:** `Artist Tracks` | **Output:** track | **Judul tampilan node:** `$name tracks`

All tracks from an artist's albums

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uri`, entitas `artist`; pencarian nama: name -> `name`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Name** - tipe: string. The name of the artist
- **Uri** - tipe: string. The URI of the artist (takes precedence over name)

**Dokumentasi resmi (help):**

This component generates all tracks from an artist's albums (up to 50 albums). Unlike Artist Top Tracks which only returns the top 10, this returns every track across the artist's discography. You can specify the artist by name or URI.

---

### SpotifyArtistRadio

**Label UI:** `Artist Radio` | **Output:** track | **Judul tampilan node:** `$name radio`

Tracks by an artist and similar artists

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uri`, entitas `artist`; pencarian nama: name -> `name`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Name** - tipe: string. The name of the artist
- **Uri** - tipe: string. The URI of the artist (takes precedence over name)

**Dokumentasi resmi (help):**

Generates a mix of tracks by the given artist and similar artists, like a radio station seeded by the artist. Typically returns around 50 tracks.

---

### PlaylistRadio

**Label UI:** `Playlist Radio` | **Output:** track | **Judul tampilan node:** `$name radio` [tersembunyi]

Deprecated — use Artist Radio instead

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Name** - tipe: string. The name of the artist
- **Limit** - tipe: integer, default: `50` (rentang: min 1). Maximum number of tracks to return

**Dokumentasi resmi (help):**

This component is deprecated. Use Artist Radio instead. Generates tracks by an artist and similar artists.

---

### TracksByDescription

**Label UI:** `Tracks By Description` | **Output:** track | **Judul tampilan node:** `$description`

Find tracks matching a freeform description (experimental)

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Description** - tipe: string. A genre, mood, era, or activity (e.g. '70s classic rock', 'party', 'road trip', 'sad', 'workout', '60s soul', 'deep house', 'chill lo-fi')
- **Limit** - tipe: integer, default: `50` (rentang: min 1). Maximum number of tracks to return

**Dokumentasi resmi (help):**

This component returns tracks matching a freeform description (e.g. 'halloween party', 'chill lo-fi', 'wedding dance'). Great for discovering tracks around a mood or theme. Note: this component is experimental and its behavior may change.

---

### MyFollowedArtists

**Label UI:** `My Followed Artists` | **Output:** track | **Judul tampilan node:** `followed artists`

Top tracks from artists you follow

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Num Tracks** - tipe: integer, default: `1` (rentang: min 1; max 10). Number of top tracks per artist (Spotify max: 10)
- **Num Artists** - tipe: integer / null, default: `(kosong)`. Number of artists to include (blank = all)
- **Subset** - tipe: string, default: `most_recent`. Nilai: `most_recent, least_recent, random`. Which artists to select

**Dokumentasi resmi (help):**

This component generates top tracks from artists you follow on Spotify. You can control how many top tracks per artist are included (Spotify provides at most 10 per artist). Use 'num_artists' to limit the number of artists (blank = all), and 'subset' to choose which artists: most recently followed, least recently followed, or a random selection.

---

### MyArtistLibrary

**Label UI:** `My Artist Library` | **Output:** artist | **Judul tampilan node:** `artist library`

Artists from your followed artists

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Count** - tipe: integer / null, default: `(kosong)`. Number of artists (blank = all)
- **Subset** - tipe: string, default: `most_recent`. Nilai: `most_recent, least_recent, random`. Which artists to select

**Dokumentasi resmi (help):**

This component produces artist entities from your followed artists on Spotify. Use 'count' to limit the number of artists. Use 'subset' to choose which artists: most recently followed, least recently followed, or a random selection.

---

### MySavedAlbums

**Label UI:** `My Saved Albums` | **Output:** track | **Judul tampilan node:** `saved albums`

Tracks from your saved albums

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Num Tracks** - tipe: integer / null, default: `(kosong)`. Number of tracks per album (blank = all)
- **Num Albums** - tipe: integer / null, default: `(kosong)`. Number of albums to include (blank = all)
- **Subset** - tipe: string, default: `most_recent`. Nilai: `most_recent, least_recent, random`. Which albums to select

**Dokumentasi resmi (help):**

This component generates tracks from your saved albums on Spotify. Use 'num_tracks' to limit how many tracks per album (blank = all). Use 'num_albums' to limit the number of albums (blank = all), and 'subset' to choose which albums: most recently saved, least recently saved, or a random selection.

---

### MyAlbumLibrary

**Label UI:** `My Album Library` | **Output:** album | **Judul tampilan node:** `album library`

Albums from your saved library

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Count** - tipe: integer / null, default: `(kosong)`. Number of albums (blank = all)
- **Subset** - tipe: string, default: `most_recent`. Nilai: `most_recent, least_recent, random`. Which albums to select

**Dokumentasi resmi (help):**

This component produces album entities from your saved album library on Spotify. Use 'count' to limit the number of albums. Use 'subset' to choose which albums: most recently saved, least recently saved, or a random selection.

---

### DatedSpotifyPlaylist

**Label UI:** `Dated Playlist` | **Output:** track | **Judul tampilan node:** `$name`

Playlist tracks filtered by date added

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uri`, entitas `playlist`; pencarian nama: name -> `name`, user -> `user`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Uri** - tipe: string. The URI or URL of the playlist
- **Name** - tipe: string. Display name of the playlist
- **User** - tipe: string. Owner of the playlist
- **Order By Date Added** - tipe: boolean, default: `false`. Sort tracks by date added
- **Tracks Added Since** - tipe: string. Only include tracks added after this date (YYYY-MM-DD)
- **Tracks Added Before** - tipe: string. Only include tracks added before this date (YYYY-MM-DD)

**Dokumentasi resmi (help):**

This component loads tracks from a Spotify playlist and filters them by when they were added. Use absolute dates (YYYY-MM-DD) to define the range.

---

### RelativeDatedSpotifyPlaylist

**Label UI:** `Relative Dated Playlist` | **Output:** track | **Judul tampilan node:** `$name`

Playlist tracks filtered by relative dates

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Resolusi URI:** field `uri`, entitas `playlist`; pencarian nama: name -> `name`, user -> `user`

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Uri** - tipe: string. The URI or URL of the playlist
- **Name** - tipe: string. Display name of the playlist
- **User** - tipe: string. Owner of the playlist
- **Order By Date Added** - tipe: boolean, default: `false`. Sort tracks by date added
- **Tracks Added Since** - tipe: string. Only tracks added within this period (e.g. '7 days', '2 weeks')
- **Tracks Added Before** - tipe: string. Only tracks added before this period (e.g. '30 days')

**Dokumentasi resmi (help):**

This component loads tracks from a Spotify playlist and filters them by when they were added, using relative dates (e.g. '7 days', '2 weeks', '3 months'). The 'since' and 'before' fields accept values like: '7 days', '2 weeks', '1 month', '1 year'.

---

### RecentlyPlayed

**Label UI:** `Recently Played` | **Output:** track | **Judul tampilan node:** `Recently Played`

Tracks you've recently listened to on Spotify

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Limit** - tipe: integer, default: `50` (rentang: min 1; max 50). Maximum number of tracks (Spotify max: 50)
- **After** - tipe: string. Only plays after this time ago (e.g. '60m', '2 hours', '7 days')
- **Before** - tipe: string. Only plays before this time ago (e.g. '60m', '2 hours', '7 days')

**Dokumentasi resmi (help):**

This component returns tracks from your recent listening history on Spotify. Spotify typically provides the last ~50 tracks. Use 'after' to get only plays after a relative time (e.g. '60m', '2h', '2 hours', '7d', '7 days'). Use 'before' to get only plays before a relative time. Note: this component requires the 'Recently Played' permission — you may need to log out and log back in to grant it.

---

### LastFmRecentTracks

**Label UI:** `Last.fm User's Recent Tracks` | **Output:** track | **Judul tampilan node:** `Recent tracks for $user`

Loads a Last.fm user's recent scrobbles, resolved to Spotify tracks

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **User** - tipe: string. Last.fm username (blank = use Settings)
- **Limit** - tipe: integer, default: `200` (rentang: min 1; max 2000). Maximum number of scrobbles to fetch
- **From Date** - tipe: string. Only fetch scrobbles after this date (e.g. '7 days', '30d', '2024-01-01')

**Dokumentasi resmi (help):**

Fetches recent scrobbles from a Last.fm user's profile and resolves them to Spotify tracks. Tracks that can't be matched on Spotify are skipped. Leave username blank to use your Last.fm username from Settings. Use 'from_date' to limit how far back to look (e.g. '7 days', '30d', '2024-01-01').

---

### LastFmTopTracks

**Label UI:** `Last.fm User's Top Tracks` | **Output:** track | **Judul tampilan node:** `Top tracks for $user`

Loads a Last.fm user's most-played tracks, resolved to Spotify tracks

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **User** - tipe: string. Last.fm username (blank = use Settings)
- **Limit** - tipe: integer, default: `200` (rentang: min 1; max 2000). Maximum number of tracks to fetch
- **Period** - tipe: string, default: `overall`. Nilai: `overall, 7day, 1month, 3month, 6month, 12month`. Time period for chart

**Dokumentasi resmi (help):**

Fetches the top tracks for a Last.fm user over a given time period and resolves them to Spotify tracks. Tracks that can't be matched on Spotify are skipped. Leave username blank to use your Last.fm username from Settings. Results are ordered by play count (most played first).

---

### LastFmLovedTracks

**Label UI:** `Last.fm User's Loved Tracks` | **Output:** track | **Judul tampilan node:** `Loved tracks for $user`

Loads a Last.fm user's loved tracks, resolved to Spotify tracks

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **User** - tipe: string. Last.fm username (blank = use Settings)
- **Limit** - tipe: integer, default: `200` (rentang: min 1; max 2000). Maximum number of loved tracks to fetch

**Dokumentasi resmi (help):**

Fetches tracks that a Last.fm user has marked as loved and resolves them to Spotify tracks. Tracks that can't be matched on Spotify are skipped. Leave username blank to use your Last.fm username from Settings. Results are in reverse chronological order (most recently loved first).

---

### LastFmSimilarTracks

**Label UI:** `Last.fm Similar Tracks` | **Output:** track | **Judul tampilan node:** `Similar to $track by $artist`

Finds tracks similar to a given track using Last.fm listening data

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Artist** - tipe: string. Artist name
- **Track** - tipe: string. Track name
- **Limit** - tipe: integer, default: `50` (rentang: min 1; max 200). Maximum number of similar tracks

**Dokumentasi resmi (help):**

Uses Last.fm's listening data to find tracks similar to the specified track, then resolves them to Spotify tracks. Provide an artist and track name. Results are ordered by similarity (most similar first).

---

### LastFmTagTopTracks

**Label UI:** `Last.fm Tag Top Tracks` | **Output:** track | **Judul tampilan node:** `Top tracks for tag $tag`

Gets the top tracks for a Last.fm tag

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Tag** - tipe: string. Tag name (e.g. 'indie', 'shoegaze', 'piano')
- **Limit** - tipe: integer, default: `200` (rentang: min 1; max 2000). Maximum number of tracks

**Dokumentasi resmi (help):**

Fetches the most popular tracks tagged with a given tag on Last.fm (e.g. 'indie', 'shoegaze', 'piano'), then resolves them to Spotify tracks. Results are ordered by tag count (most tagged first).

---

### LastFmGlobalTopTracks

**Label UI:** `Last.fm Global Top Tracks` | **Output:** track | **Judul tampilan node:** `Last.fm Global Top Tracks`

Gets the top tracks from the Last.fm global chart

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Limit** - tipe: integer, default: `200` (rentang: min 1; max 2000). Maximum number of tracks

**Dokumentasi resmi (help):**

Fetches the current global top tracks chart from Last.fm, then resolves them to Spotify tracks. Results are ordered by popularity (most played first).

---

### LastFmGeoTopTracks

**Label UI:** `Last.fm Geo Top Tracks` | **Output:** track | **Judul tampilan node:** `Top tracks in $country`

Gets the top tracks for a country from Last.fm

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Country** - tipe: string. Country name (e.g. 'United States', 'Germany')
- **Location** - tipe: string. Optional metro name within the country
- **Limit** - tipe: integer, default: `200` (rentang: min 1; max 2000). Maximum number of tracks

**Dokumentasi resmi (help):**

Fetches the most popular tracks from the previous week in a given country (and optionally a metro area) from Last.fm, then resolves them to Spotify tracks. Country should be an ISO 3166-1 name (e.g. 'United States', 'Germany', 'Japan').

---

### CountryTopTracks

**Label UI:** `Country Top Tracks` | **Output:** track | **Judul tampilan node:** `Top tracks from $country`

Top tracks from artists of a given country (via MusicBrainz)

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Country** - tipe: string. Country name or ISO code (e.g. 'Finland', 'FI')
- **Limit** - tipe: integer, default: `50` (rentang: min 1; max 500). Maximum number of tracks to return
- **Artist Sample** (lanjutan) - tipe: integer, default: `200` (rentang: min 10; max 1000). How many uncached artists to sample when cache coverage is low

**Dokumentasi resmi (help):**

Finds artists from a given country using MusicBrainz metadata, ranks them by Spotify popularity, then returns the top tracks from the most popular artists. Enter a country name (e.g. 'Finland', 'Nigeria') or an ISO code (e.g. 'FI', 'NG'). Uses cached artist data when available to minimize API calls, and samples uncached artists to fill gaps (warming the cache for future runs).

---

### CountryTopArtists

**Label UI:** `Country Top Artists` | **Output:** artist | **Judul tampilan node:** `Top artists in $country`

Top charting artists in a given country

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Country** - tipe: string. Country name or ISO code (e.g. 'USA', 'UK', 'Japan')

**Dokumentasi resmi (help):**

Gets the unique artists from a country's Spotify chart playlist — the artists currently most streamed in that country. Enter a country name (e.g. 'USA', 'UK', 'Japan') or an ISO code. Artists are ordered by chart position (most streamed first).

---

### GenreArtists

**Label UI:** `Genre Artists` | **Output:** artist | **Judul tampilan node:** `$genre artists`

Artists tagged with a given genre (via MusicBrainz)

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Alias** (lanjutan) - tipe: string. Custom source label for track display and distribution objectives
- **Cache Mode** (lanjutan) - tipe: string, default: `auto`. Nilai: `auto, no-cache, short-term, long-term`. Cache: auto (default), no-cache (fresh), short-term (daily), long-term (weekly)
- **Genre** - tipe: string. Genre tag (e.g. 'shoegaze', 'ambient', 'j-pop')
- **Count** - tipe: integer, default: `20` (rentang: min 1; max 200). Number of artists to return
- **Primary Only** - tipe: boolean, default: `true`. Only include artists whose primary genre matches

**Dokumentasi resmi (help):**

Finds artists tagged with a specific genre in MusicBrainz, ranked by Spotify popularity. Enter a genre tag like 'shoegaze', 'post-punk', 'ambient', or 'j-pop'. Genre matching is case-insensitive.

By default, only artists whose PRIMARY genre matches are included — this avoids pop stars who happen to have a minor genre tag. Uncheck 'primary only' to include all artists tagged with the genre.

---

### DeprecatedSource

**Label UI:** `Deprecated Source` | **Output:** track | **Judul tampilan node:** `$original_type (deprecated)` [tersembunyi]

Placeholder for components that are no longer available

**Port input:**

Tidak ada input (sumber / bertanda parsial).

**Parameter:**

- **Original Type** - tipe: string. The original component type that was replaced
- **Message** - tipe: string. Why this component was deprecated

**Dokumentasi resmi (help):**

This component replaces a source type that is no longer available. It cannot produce any tracks. Replace it with an available source.

---

