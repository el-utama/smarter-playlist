# Selectors - Pemilih Item

> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total 9 komponen dalam kategori ini.

Selector memotong stream menjadi subset (N pertama, N terakhir, N acak, batas durasi, hingga paging antar-run). Berguna untuk mengontrol panjang playlist.

### Alternate

**Label UI:** `Alternator` | **Output:** track | **Judul tampilan node:** `alternate`

Alternate items from multiple input streams

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The input streams to alternate between

**Parameter:**

- **Fail Fast** - tipe: boolean, default: `true`. If true, stop as soon as any input stream is exhausted

**Dokumentasi resmi (help):**

This component takes any number of input streams and generates a single output stream by alternating between each of the input streams. It continues until all input sources are exhausted.

---

### First

**Label UI:** `First` | **Output:** track | **Judul tampilan node:** `first $sample_size`

Return the first items from a stream

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Sample Size** - tipe: integer, default: `10` (rentang: min 1). The number of items to return

**Dokumentasi resmi (help):**

This component passes through only the first 'count' items from the input stream. Use it to limit a stream to a fixed number of items.

---

### Last

**Label UI:** `Last` | **Output:** track | **Judul tampilan node:** `last $sample_size`

Return the last items from a stream

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Sample Size** - tipe: integer, default: `10` (rentang: min 1). The number of items to return

**Dokumentasi resmi (help):**

This component returns the last 'count' items from the input stream.

---

### Sample

**Label UI:** `Sample` | **Output:** track | **Judul tampilan node:** `sample $sample_size`

Randomly sample items from a stream

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Sample Size** - tipe: integer, default: `10` (rentang: min 1). The number of items to return

**Dokumentasi resmi (help):**

This component randomly samples up to 'count' items from the input stream. Sampled items may be returned in any order.

---

### AllButTheFirst

**Label UI:** `All But First` | **Output:** track | **Judul tampilan node:** `all but first $sample_size`

Return all but the first items from a stream

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Sample Size** - tipe: integer, default: `10` (rentang: min 0). The number of items to skip

**Dokumentasi resmi (help):**

This component skips the first 'count' items and passes through the rest.

---

### AllButTheLast

**Label UI:** `All But Last` | **Output:** track | **Judul tampilan node:** `all but last $sample_size`

Return all but the last items from a stream

**Port input:**

- Port `green` - multi-input (generic: track/artist/album) - The source of items

**Parameter:**

- **Sample Size** - tipe: integer, default: `10` (rentang: min 0). The number of items to drop from the end

**Dokumentasi resmi (help):**

This component passes through all items except the last 'count'.

---

### ShorterThan

**Label UI:** `No Longer Than` | **Output:** track | **Judul tampilan node:** `no longer than $time`

Limit stream to tracks fitting within a time duration

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Time** - tipe: integer, default: `900` (rentang: min 1). Maximum total duration

**Dokumentasi resmi (help):**

This component passes through the first N tracks whose total duration is no longer than the given time.

---

### LongerThan

**Label UI:** `No Shorter Than` | **Output:** track | **Judul tampilan node:** `no shorter than $time`

Accumulate tracks until total duration meets a minimum

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Time** - tipe: integer, default: `1800` (rentang: min 1). Minimum total duration

**Dokumentasi resmi (help):**

This component passes through the first N tracks needed to reach at least the given total duration.

---

### Pager

**Label UI:** `Pager` | **Output:** track | **Judul tampilan node:** `page $count`

Page through a source across multiple runs

**Port input:**

- Port `green` - maks 1 (generic: track/artist/album) - The source to page through

**Parameter:**

- **Count** - tipe: integer, default: `20` (rentang: min 1; max 10000). Number of tracks per page

**Dokumentasi resmi (help):**

Each time this component runs, it returns the next batch of items from the input source. On the first run it returns items 1 through N, on the second run items N+1 through 2N, and so on. When it reaches the end it wraps around to the beginning. This is useful with scheduled programs to progressively work through a large playlist.

---

