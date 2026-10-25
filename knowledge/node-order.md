# Orders - Pengurutan

> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total 7 komponen dalam kategori ini.

Komponen urutan mengatur susunan item: sort deterministik, shuffle acak, shuffle tertimbang, hingga sequencer cerdas (Smart Mix dan Multi-Objective Sequencer).

### Shuffler

**Label UI:** `Shuffle` | **Output:** track | **Judul tampilan node:** `shuffle`

Randomly shuffle items from input streams

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of tracks

**Parameter:**


**Dokumentasi resmi (help):**

This component randomly re-orders the input tracks.

---

### Sorter

**Label UI:** `Sort` | **Output:** track | **Judul tampilan node:** `sort by $attr`

Sort items by a given attribute

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Attr** - tipe: string, default: `name`. Nilai: `acousticness, album, album_popularity, album_release_date, album_type, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, followers, instrumentalness, key, label, liveness, loudness, mo_score, mode, name, popularity, random, release_date, release_decade, release_year, relinked_id, source, source_count, speechiness, tempo, time_signature, total_tracks, track_number, uri, valence`. The attribute to sort on
- **Reverse** - tipe: boolean, default: `false`. If true, reverse the sort order

**Dokumentasi resmi (help):**

This component orders tracks based on the given attribute. The sort can be reversed by selecting the 'reverse' option.

---

### Reverse

**Label UI:** `Reverse` | **Output:** track | **Judul tampilan node:** `reverse`

Reverse the order of items in a stream

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of tracks

**Parameter:**


**Dokumentasi resmi (help):**

This component reverses the order of the input tracks.

---

### Weighted Shuffler

**Label UI:** `Weighted Shuffle` | **Output:** track | **Judul tampilan node:** `weighted shuffle`

Shuffle items with controllable randomness

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Factor** - tipe: number, default: `0.1` (rentang: min 0; max 1). Amount of randomness (0=original order, 1=fully random)

**Dokumentasi resmi (help):**

This component randomly re-orders the input items. The amount of re-ordering is controlled by the randomness factor (0 to 1). Closer to 1 means more random; closer to 0 retains more of the original order. A factor of 0.1 will lightly shuffle.

---

### SeparateArtists

**Label UI:** `Separate Artists` | **Output:** track | **Judul tampilan node:** `separate artists`

Reorder to maximize distance between same-artist tracks

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**


**Dokumentasi resmi (help):**

Reorders tracks so that each artist's songs are spread as far apart as possible. Every artist's tracks are scheduled at evenly-spaced ideal positions across the whole playlist, and back-to-back tracks by the same artist are avoided whenever possible. The relative order of tracks within each artist is preserved.

---

### SmartMix

**Label UI:** `Smart Mix` | **Output:** track | **Judul tampilan node:** `smart mix $limit`

Reorder tracks for smooth DJ-style transitions

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Limit** - tipe: integer, default: `50` (rentang: min 1). Maximum number of output tracks
- **Genre Weight** - tipe: string, default: `highest`. Nilai: `highest, high, medium, low, off`. Genre similarity
- **Energy Weight** - tipe: string, default: `high`. Nilai: `highest, high, medium, low, off`. Energy smoothness
- **Camelot Weight** - tipe: string, default: `medium`. Nilai: `highest, high, medium, low, off`. Harmonic compatibility (Camelot wheel)
- **Tempo Weight** - tipe: string, default: `low`. Nilai: `highest, high, medium, low, off`. Tempo smoothness

**Dokumentasi resmi (help):**

Reorders tracks to minimize jarring transitions using a greedy nearest-neighbor algorithm. Considers genre similarity, energy flow, harmonic compatibility (Camelot wheel), and tempo smoothness. Adjust the weights to prioritize what matters most for your mix. Feed in more tracks than the limit to give the algorithm a larger pool to find good matches.

---

### MultiObjectiveSequencer

**Label UI:** `Multi-Objective Sequencer` | **Output:** track | **Judul tampilan node:** `MOS $limit · $objectives`

Sequence tracks using multiple weighted objectives

**Port input:**

- Port `green` - multi-input (tipe: track) - Pool of tracks to sequence

**Parameter:**

- **Limit** - tipe: integer, default: `50` (rentang: min 1). Maximum output tracks
- **Objectives** - tipe: array. List of scoring objectives

**Dokumentasi resmi (help):**

Sequences tracks from the input pool by greedily selecting the best-scoring track at each step. Add multiple objectives (maximize, minimize, range, min-separation) to control which tracks are preferred and in what order. Each objective has a weight that controls its importance. The 'unbreakable' weight means the sequencer stops if no candidate satisfies that objective.

---

