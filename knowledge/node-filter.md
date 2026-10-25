# Filters - Penyaring

> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total 22 komponen dalam kategori ini.

Filter mengurangi stream: membuang item yang tidak memenuhi syarat. Port merah/oranye umumnya adalah daftar eksklusi (dibandingkan port hijau utama).

### DeDup

**Label UI:** `Remove Duplicates` | **Output:** track | **Judul tampilan node:** `dedup`

Remove duplicate items from a stream

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - Items to de-duplicate

**Parameter:**

- **By Name** - tipe: boolean, default: `true`. If true, match by name and artist; otherwise match by track ID only

**Dokumentasi resmi (help):**

This component removes duplicate items from the stream. Works on tracks, artists, and albums.

If 'By Name' is set, items are matched by name: tracks and albums by title + artist, artists by name alone. This catches different versions of the same item. Otherwise items are matched by their Spotify ID.

---

### AttributeRangeFilter

**Label UI:** `Range Filter` | **Output:** track | **Judul tampilan node:** `filter $attr`

Filter items by an attribute range

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Attr** - tipe: string, default: `popularity`. Nilai: `acousticness, album_popularity, artist_end_year, artist_followers, artist_popularity, artist_start_year, camelot_num, danceability, disc_number, duration_ms, energy, followers, instrumentalness, key, liveness, loudness, mo_score, mode, popularity, random, release_decade, release_year, source_count, speechiness, tempo, time_signature, total_tracks, track_number, valence`. The attribute to filter on
- **Min Val** - tipe: number / null, default: `0`. Minimum value (inclusive)
- **Max Val** - tipe: number / null, default: `100`. Maximum value (inclusive)
- **Match** - tipe: string. Match expression

**Dokumentasi resmi (help):**

This component filters the input stream and only passes through tracks whose attribute value falls within the specified range.

---

### TrackFilter

**Label UI:** `Track Filter` | **Output:** track | **Judul tampilan node:** ``

Remove tracks from a stream

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks
- Port `red` - multi-input (tipe: track) - Tracks to remove

**Parameter:**

- **Invert** - tipe: boolean, default: `false`. If true, only tracks on both streams are passed through
- **By Name** - tipe: boolean, default: `true`. If true, also match by artist and title in addition to track ID

**Dokumentasi resmi (help):**

This component takes two input streams. It produces tracks from the green input stream with the tracks on the red input stream removed. If 'invert' is set, only tracks that appear on both streams are passed through. If 'By Name' is set, tracks are matched by artist and title in addition to track ID.

---

### TextFilter

**Label UI:** `Title Filter` | **Output:** track | **Judul tampilan node:** `$text`

Filter tracks with titles matching a given string

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Text** - tipe: string. Regular expression to match against track title
- **Ignore Case** - tipe: boolean, default: `true`. If true, matching ignores letter case
- **Invert** - tipe: boolean, default: `false`. If true, pass through non-matching tracks

**Dokumentasi resmi (help):**

This component passes through tracks whose title matches the given text string. The text is treated as a regular expression. Set 'invert' to pass through only non-matching tracks. Set 'ignore case' to make the match case-insensitive.

---

### MatchFilter

**Label UI:** `Match Filter` | **Output:** track | **Judul tampilan node:** `$attr $ternary(invert, doesn't match, matches) $value`

Filter items by matching a string attribute against a pattern

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Attr** - tipe: string, default: `name`. Nilai: `album, album_type, artist, artist_area, artist_country, artist_gender, artist_type, camelot, label, name, relinked_id, source, uri`. The attribute to match against
- **Match Type** - tipe: string, default: `substring`. Nilai: `exact, substring, regex`. How to match: exact, substring, or regex
- **Value** - tipe: string. The value to match
- **Ignore Case** - tipe: boolean, default: `true`. If true, matching ignores letter case
- **Invert** - tipe: boolean, default: `false`. If true, pass through non-matching items

**Dokumentasi resmi (help):**

This component filters tracks based on whether a string attribute (title, artist, or album) matches a given value. You can choose exact match, substring match, or regex match. Use 'invert' to pass through only non-matching tracks. Useful for filtering out remixes, live versions, etc.

---

### Explicit

**Label UI:** `Explicit` | **Output:** track | **Judul tampilan node:** `explicit`

Filter tracks by their explicit attribute

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Explicit** - tipe: boolean, default: `false`. If true, only explicit tracks pass; if false, only clean tracks pass

**Dokumentasi resmi (help):**

This component filters tracks based on whether they are marked as explicit. If 'explicit' is true, only explicit tracks pass through. If false, only clean tracks pass through.

---

### ArtistDeDup

**Label UI:** `Artist De-Dup` | **Output:** track | **Judul tampilan node:** `artist dedup`

Ensure only unique artists appear in the stream

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - Items to de-duplicate

**Parameter:**


**Dokumentasi resmi (help):**

This component removes items with duplicate artists from the stream. Works on tracks, artists, and albums — the first item for each artist is kept, subsequent duplicates are removed.

---

### MaxTracksPerArtist

**Label UI:** `Max Tracks Per Artist` | **Output:** track | **Judul tampilan node:** `max $max_tracks per artist`

Limit the number of tracks by any single artist

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Max Tracks** - tipe: integer, default: `1` (rentang: min 1). Maximum number of tracks allowed per artist

**Dokumentasi resmi (help):**

This component limits how many tracks by the same artist can pass through. Once an artist has reached the maximum, any further tracks by that artist are removed.

---

### ArtistSeparation

**Label UI:** `Artist Separation` | **Output:** track | **Judul tampilan node:** `artist separation`

Enforce a minimum gap between tracks by the same artist

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Min Separation** - tipe: integer, default: `4` (rentang: min 0). Minimum number of tracks between tracks by the same artist
- **Reorder** - tipe: boolean, default: `true`. If true, reorder tracks to enforce separation instead of removing them

**Dokumentasi resmi (help):**

This component guarantees that tracks by the same artist will not appear closer together than the given minimum separation. If 'reorder' is set, tracks may be reordered to enforce the separation; otherwise offending tracks are removed.

---

### SimpleArtistFilter

**Label UI:** `Simple Artist Filter` | **Output:** track | **Judul tampilan node:** `remove $artistNames`

Remove tracks by the given artists

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Artistnames** - tipe: string. Comma-separated list of artist names to remove

**Dokumentasi resmi (help):**

This component removes tracks from the input stream that are by the given set of artists. Artists are specified as a comma-separated list.

---

### ArtistFilter

**Label UI:** `Artist Filter` | **Output:** track | **Judul tampilan node:** `artist filter`

Filter any stream by artist

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - Items to filter
- Port `red` - multi-input (generic: track/artist/album) - Artists to remove

**Parameter:**

- **Invert** - tipe: boolean, default: `false`. If true, only items by artists on the red stream are passed through

**Dokumentasi resmi (help):**

This component takes two input streams. It removes items from the green stream whose artist appears on the red stream. If 'invert' is set, only items by artists on the red stream are passed through.

Both inputs accept any entity type — tracks, artists, or albums. Artist names are extracted automatically: from the artist name for artist entities, and from the track/album artist field for tracks and albums.

---

### ReleaseDateFilter

**Label UI:** `Date Filter` | **Output:** track | **Judul tampilan node:** `released after $min_val before $max_val`

Filter items by release date range

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Min Val** - tipe: string. Earliest release date (e.g. '2020', '2020-06', '2020-06-15', '6 months')
- **Max Val** - tipe: string. Latest release date (e.g. '2024', '2024-12', '30 days')

**Dokumentasi resmi (help):**

This component filters the input stream and only passes through items whose release date falls within the specified range. Works on tracks and albums. Dates can be absolute (e.g. '2020', '2020-06', '2020-06-15') or relative (e.g. '6 months', '1 year', '30 days').

---

### Danceable

**Label UI:** `Danceable` | **Output:** track | **Judul tampilan node:** `$scale danceable`

Filter tracks by danceability

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Scale** - tipe: string, default: `more`. Nilai: `most, more, less, least, all`. How danceable: most, more, less, least, or all

**Dokumentasi resmi (help):**

This component filters tracks by their danceability score. Scale: most (0.75-1.0), more (0.5-1.0), less (0-0.5), least (0-0.25), all (no filter).

---

### Energy

**Label UI:** `Energy` | **Output:** track | **Judul tampilan node:** `$scale energy`

Filter tracks by energy level

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Scale** - tipe: string, default: `more`. Nilai: `most, more, less, least, all`. How energetic: most, more, less, least, or all

**Dokumentasi resmi (help):**

This component filters tracks by their energy score. Scale: most (0.75-1.0), more (0.5-1.0), less (0-0.5), least (0-0.25), all (no filter).

---

### Live

**Label UI:** `Live` | **Output:** track | **Judul tampilan node:** `$scale live`

Filter tracks by liveness

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Scale** - tipe: string, default: `more`. Nilai: `most, more, less, least, all`. How live: most, more, less, least, or all

**Dokumentasi resmi (help):**

This component filters tracks by their liveness score. Higher values indicate the track was likely performed live.

---

### Spoken Word

**Label UI:** `Spoken Word` | **Output:** track | **Judul tampilan node:** `$scale spoken`

Filter tracks by speechiness

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Scale** - tipe: string, default: `more`. Nilai: `most, more, less, least, all`. How speech-like: most, more, less, least, or all

**Dokumentasi resmi (help):**

This component filters tracks by their speechiness score. Higher values indicate more spoken word content (talk shows, podcasts, rap).

---

### GenreFilter

**Label UI:** `Genre Filter` | **Output:** track | **Judul tampilan node:** `genre $ternary(invert, excludes, matches) $genre`

Filter tracks by MusicBrainz genre

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Genre** - tipe: string. Genre to match (e.g. 'rock', 'electronic', 'hip hop')
- **Match Type** - tipe: string, default: `substring`. Nilai: `substring, exact`. How to match: substring or exact
- **Primary Genre Only** - tipe: boolean, default: `false`. Only match the artist's primary (first) genre, ignoring minor genre tags
- **Invert** - tipe: boolean, default: `false`. If true, exclude matching tracks instead

**Dokumentasi resmi (help):**

This component filters tracks by genre using MusicBrainz genre data. Enter a genre like 'rock', 'electronic', or 'hip hop'. By default, substring matching is used so 'rock' matches 'alternative rock', 'art rock', etc. Use exact matching for precise genre names. Set 'invert' to exclude matching tracks instead.

Enable 'primary genre only' to match only the artist's first (most relevant) genre instead of the full list. This avoids false positives from deep genre tags — e.g. filtering by 'jazz' won't match a pop artist who happens to have 'jazz' as a minor genre.

---

### GenderFilter

**Label UI:** `Gender Filter` | **Output:** track | **Judul tampilan node:** `gender $ternary(invert, excludes, is) $gender`

Filter tracks by artist/vocalist gender

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Gender** - tipe: string, default: `female`. Nilai: `male, female, mixed, instrumental, other, unknown`. Gender to filter for
- **Invert** - tipe: boolean, default: `false`. If true, exclude matching tracks instead

**Dokumentasi resmi (help):**

Filter tracks by the gender of the artist or vocalist. For solo artists, this is their gender directly. For bands, this reflects the vocalist(s): male, female, or mixed. Groups with no vocalist data show as 'unknown'. Orchestras are classified as 'instrumental'.

---

### CountryFilter

**Label UI:** `Country Filter` | **Output:** track | **Judul tampilan node:** `country $ternary(invert, excludes, is) $country`

Filter tracks by artist country

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Country** - tipe: string. ISO country code (e.g. US, GB, JP)
- **Invert** - tipe: boolean, default: `false`. If true, exclude matching tracks instead

**Dokumentasi resmi (help):**

Filter tracks by the artist's country of origin using ISO 3166-1 alpha-2 codes (e.g. US, GB, JP, SE, DE). Country data comes from MusicBrainz.

---

### Tempo

**Label UI:** `Tempo` | **Output:** track | **Judul tampilan node:** `$min_tempo-$max_tempo BPM`

Filter tracks by BPM range

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Min Tempo** - tipe: number, default: `60` (rentang: min 20; max 400). Minimum tempo in BPM
- **Max Tempo** - tipe: number, default: `180` (rentang: min 20; max 400). Maximum tempo in BPM

**Dokumentasi resmi (help):**

This component filters tracks by their tempo (beats per minute).

---

### SimilarTracks

**Label UI:** `Similar Tracks` | **Output:** track | **Judul tampilan node:** `$count similar`

For each input track, find tracks by similar artists

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Count** - tipe: integer, default: `3` (rentang: min 1; max 20). Number of similar tracks to find per input track
- **Max Tracks** - tipe: integer, default: `50` (rentang: min 1; max 500). Maximum total output tracks
- **Exclude Same Artist** - tipe: boolean, default: `true`. Exclude tracks by the same artist as the input track

**Dokumentasi resmi (help):**

For each input track, finds tracks by similar artists. Use it to expand a small seed playlist into a larger collection of related music. By default, tracks by the same artist as the input track are excluded. Tracks are deduplicated across all inputs, and input tracks themselves are never included in the output.

---

### PlayableFilter

**Label UI:** `Playable Filter` | **Output:** track | **Judul tampilan node:** `playable only`

Remove tracks that are not playable in your market

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Relink** - tipe: boolean, default: `false`. Replace unplayable tracks with playable alternatives when available

**Dokumentasi resmi (help):**

Removes tracks that Spotify reports as unplayable in your country/market. Some tracks are region-locked and won't play even if they appear in playlists. Enable 'relink' to replace unplayable tracks with market-appropriate alternatives when Spotify provides them, instead of dropping them.

---

