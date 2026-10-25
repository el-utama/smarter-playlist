# Adapters - Konversi Tipe Entitas

> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total 6 komponen dalam kategori ini.

Adapter mengubah tipe entitas di dalam stream: track <-> artist <-> album, atau menghitung entitas terkait (misal artis serupa). Ini yang membuat program dapat berjalan lintas tipe: mulai dari artis, ekstrak album, lalu ubah kembali ke track.

### ToTracks

**Label UI:** `To Tracks` | **Output:** track | **Judul tampilan node:** `$select tracks`

Convert artists or albums into their tracks

**Port input:**

- Port `green` - multi-input (tipe: artist, album) - Artists or albums

**Parameter:**

- **Select** - tipe: string, default: `most_popular`. Nilai: `album_order, first_n, last_n, least_popular, most_popular, newest, oldest, random`. How to select tracks from each input item
- **Count** - tipe: integer, default: `5` (rentang: min 1; max 50). Tracks per input item
- **Limit** - tipe: integer, default: `0` (rentang: min 0). Overall max tracks (0 = unlimited)

**Dokumentasi resmi (help):**

This component takes artist or album entities and produces tracks. The available selection modes depend on the input type. For artists: most popular, least popular, newest, oldest, or random. For albums: album order, random, first N, or last N. Use 'count' to control how many tracks per input item, and 'limit' to cap the total output.

---

### ToArtists

**Label UI:** `To Artists` | **Output:** artist | **Judul tampilan node:** `to artists ($order)`

Extract unique artists from tracks or albums

**Port input:**

- Port `green` - multi-input (tipe: track, album) - Tracks or albums

**Parameter:**

- **Order** - tipe: string, default: `input_order`. Nilai: `input_order, least_common, most_common`. How to order the extracted artists
- **Include Featured** - tipe: boolean, default: `false`. Include featured/secondary artists, not just the primary

**Dokumentasi resmi (help):**

This component extracts unique artists from a stream of tracks or albums. For tracks: artists are extracted by artist ID and optionally ordered by frequency. For albums: the primary artist of each album is extracted. Enable 'include featured' to also include featured/secondary artists.

---

### ToAlbums

**Label UI:** `To Albums` | **Output:** album | **Judul tampilan node:** `to albums ($order)`

Extract albums from tracks, or fetch an artist's albums

**Port input:**

- Port `green` - multi-input (tipe: track, artist) - Tracks or artists

**Parameter:**

- **Order** - tipe: string, default: `input_order`. Nilai: `input_order, least_common, most_common, most_popular, newest, oldest`. How to order the albums
- **Count** - tipe: integer, default: `5` (rentang: min 1; max 50). Albums per artist (artist input only)
- **Album Types** - tipe: string, default: `album`. Album types to include (comma-separated: album, single, compilation, appears_on)

**Dokumentasi resmi (help):**

This component produces album entities. From tracks: extracts unique albums by album ID. From artists: fetches each artist's albums from Spotify. Use 'count' to limit albums per artist. Use 'album types' to filter by type (album, single, compilation, appears_on).

---

### SimilarArtists

**Label UI:** `Similar Artists` | **Output:** artist | **Judul tampilan node:** `$count similar artists`

Find similar artists for each input artist

**Port input:**

- Port `green` - multi-input (tipe: artist) - Input artists

**Parameter:**

- **Count** - tipe: integer, default: `5` (rentang: min 1; max 50). Similar artists per input artist
- **Limit** - tipe: integer, default: `0` (rentang: min 0). Overall max artists (0 = unlimited)

**Dokumentasi resmi (help):**

This component takes a stream of artists and produces similar artists for each one, using Spotify's artist radio playlists to discover related artists. Use 'count' to control how many similar artists per input, and 'limit' to cap the total output. The input artist is excluded from the results.

---

### Expand

**Label UI:** `Expand` | **Output:** track | **Judul tampilan node:** `$select tracks` [tersembunyi]

Convert artists or albums into their tracks

**Port input:**

- Port `green` - multi-input (tipe: artist, album) - Artists or albums

**Parameter:**

- **Select** - tipe: string, default: `most_popular`. Nilai: `album_order, first_n, last_n, least_popular, most_popular, newest, oldest, random`. How to select tracks from each input item
- **Count** - tipe: integer, default: `5` (rentang: min 1; max 50). Tracks per input item
- **Limit** - tipe: integer, default: `0` (rentang: min 0). Overall max tracks (0 = unlimited)

**Dokumentasi resmi (help):**

This component takes artist or album entities and produces tracks. The available selection modes depend on the input type. For artists: most popular, least popular, newest, oldest, or random. For albums: album order, random, first N, or last N. Use 'count' to control how many tracks per input item, and 'limit' to cap the total output.

---

### Collapse

**Label UI:** `Collapse` | **Output:** artist | **Judul tampilan node:** `to artists ($order)` [tersembunyi]

Extract unique artists from tracks or albums

**Port input:**

- Port `green` - multi-input (tipe: track, album) - Tracks or albums

**Parameter:**

- **Order** - tipe: string, default: `input_order`. Nilai: `input_order, least_common, most_common`. How to order the extracted artists
- **Include Featured** - tipe: boolean, default: `false`. Include featured/secondary artists, not just the primary

**Dokumentasi resmi (help):**

This component extracts unique artists from a stream of tracks or albums. For tracks: artists are extracted by artist ID and optionally ordered by frequency. For albums: the primary artist of each album is extracted. Enable 'include featured' to also include featured/secondary artists.

---

