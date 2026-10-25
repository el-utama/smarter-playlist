# Combiners - Penggabung Stream

> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total 7 komponen dalam kategori ini.

Combiner menggabungkan dua input stream atau lebih menjadi satu stream baru, dengan strategi tertentu (interleave, acak, rasio campuran, atau sambung-sambung).

### Concatenate

**Label UI:** `Concatenate` | **Output:** track | **Judul tampilan node:** `concatenate`

Concatenate items from multiple streams

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The streams to concatenate

**Parameter:**


**Dokumentasi resmi (help):**

This component takes any number of input streams and produces tracks by retrieving all the tracks from the first stream, followed by all the tracks from the second stream, and so on.

---

### RandomSelector

**Label UI:** `Random` | **Output:** track | **Judul tampilan node:** `random`

Randomly select items from multiple streams

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The input streams

**Parameter:**

- **Fail Fast** - tipe: boolean, default: `true`. If true, stop as soon as any input stream is exhausted

**Dokumentasi resmi (help):**

This component takes any number of input streams and produces tracks by continuously selecting a random input stream and returning the next track from that stream. If 'fail fast' is set, it stops as soon as any selected source is exhausted.

---

### RandomStreamSelector

**Label UI:** `Random Stream` | **Output:** track | **Judul tampilan node:** `random stream`

Randomly pick one stream and use it

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The input streams

**Parameter:**


**Dokumentasi resmi (help):**

This component picks one input stream at random and uses that entire stream to produce tracks.

---

### MixIn

**Label UI:** `Mix In` | **Output:** track | **Judul tampilan node:** `mix in`

Mix two input streams with a configurable ratio

**Port input:**

- Port `green` - maks 1 (generic: track/artist/album) - The primary source of tracks
- Port `red` - maks 1 (generic: track/artist/album) - The mix-in source of tracks

**Parameter:**

- **Nskips** - tipe: integer, default: `1` (rentang: min 0). Number of green tracks in a row
- **Ntracks** - tipe: integer, default: `1` (rentang: min 0). Number of red tracks in a row
- **Initial Skip** - tipe: integer, default: `1` (rentang: min 0). Number of initial green tracks before first mix-in
- **Fail Fast** - tipe: boolean, default: `true`. If true, stop when either stream is exhausted

**Dokumentasi resmi (help):**

This component alternately selects tracks from the green and red streams. Tracks on the green port are the primary stream, and tracks on the red port are mixed in. It plays 'initial skip' green tracks first, then cycles through 'green tracks' from the green stream followed by 'red tracks' from the red stream. If 'fail fast' is set, the component stops when either stream runs out. If not set, it continues with whichever stream still has tracks.

---

### Mixer

**Label UI:** `Mixer` | **Output:** track | **Judul tampilan node:** `mixer`

Advanced multi-stream mixer with dedup and artist separation

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The input streams to mix
- Port `red` - multi-input (tipe: track) - Tracks to exclude
- Port `orange` - multi-input (tipe: track) - Artists to exclude

**Parameter:**

- **Fail Fast** - tipe: boolean, default: `true`. Stop when any stream is exhausted
- **Dedup** - tipe: boolean, default: `true`. Remove duplicate tracks
- **Min Artist Separation** - tipe: integer, default: `4` (rentang: min 0). Minimum gap between same-artist tracks (0 = no limit)
- **Max Tracks** - tipe: integer, default: `50` (rentang: min 1). Maximum number of output tracks

**Dokumentasi resmi (help):**

This component mixes tracks from multiple input streams while maintaining ordering rules. Input streams are on the green port, banned tracks are on the red port, and banned artists are on the orange port. If 'fail fast' is set, the order of input tracks is guaranteed to be preserved and the mixer stops when it can no longer satisfy the constraints. If 'fail fast' is not set, the mixer finds the next best track from the next input stream that best fits the constraints, and continues producing tracks as long as any stream has tracks remaining.

---

### Intersection

**Label UI:** `Intersection` | **Output:** track | **Judul tampilan node:** `intersection`

Output only tracks that appear in all input streams

**Port input:**

- Port `green` - multi-input (tipe: track) - The input streams to intersect

**Parameter:**


**Dokumentasi resmi (help):**

This component takes multiple input streams and outputs only the tracks that appear in every stream. The output order follows the first input stream.

---

### Annotator

**Label UI:** `Annotate` | **Output:** track | **Judul tampilan node:** `annotate` [tersembunyi]

Legacy passthrough — annotation is now automatic

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Type** - tipe: string, default: `audio`. Unused — kept for backward compatibility

**Dokumentasi resmi (help):**

This component is vestigial. Audio feature annotation now happens automatically in the pipeline. Existing programs that use this component will continue to work — it simply passes tracks through.

---

