# Smart Playlist 120 — Template & Config

Dokumen ini menjelaskan template, config, dan program generator untuk **120 playlist** (4 kategori × 30) di SmarterPlaylists.

> **Status saat ini:** taxonomy sudah **disetujui**; judul playlist dan deskripsi memakai **bahasa Inggris** yang marketable dan profesional. Template + config + 21 pool + 4 sample generator JSON lokal sudah dibuat. **Belum ada** program SmarterPlaylists yang diimpor/dijalankan dan **belum ada** playlist Spotify baru yang dibuat.

---

## 1. Ringkasan rencana

| Item | Nilai |
|---|---|
| Jumlah playlist | 120 = 4 kategori × 30 |
| Status taxonomy | **Disetujui (2026-10-24)** |
| Kategori | Morning (Pagi), Midday (Siang), Afternoon (Sore), Night (Malam) |
| Bahasa judul & deskripsi | **English** (marketable, professional) |
| Deskripsi playlist | Ditulis ke Spotify via node `PlaylistSave` (limit 300 karakter) |
| Genre per kategori | 5 |
| Mood per kategori | 6 |
| Batas durasi | **6 jam = 21.600 detik** (hard cap) |
| Artist priority | 25 artist No Detours + **eL Utama** = 26 |
| Rotasi | **60% priority / 40% global** (objective MOS) |
| Urutan kandidat priority | popularity paling rendah dulu, lalu release date terbaru |
| Artis berurutan | **tidak boleh ada 2 track berturut-turut oleh artis yang sama** |
| Explicit Morning/Midday | clean only |
| Explicit Afternoon/Night | boleh explicit |
| Sumber global | Last.fm tags + MusicBrainz genres + Spotify Artist Radio + Tracks by Description |
| Series exclusion | hanya untuk pool global, **bukan** pool priority |

### Struktur kategori

| Kategori | Genre | Mood |
|---|---|---|
| **Morning** (Pagi) | Acoustic & Folk, Indie Pop, Jazz & Soul, Classical & Piano, Lo-Fi & Chillhop | Fresh, Calm, Hopeful, Warm, Focused, Gentle |
| **Midday** (Siang) | Pop, Dance & Electronic, Hip-Hop & R&B, Rock & Alternative, Funk & Groove | Upbeat, Energetic, Confident, Bright, Groovy, Motivational |
| **Afternoon** (Sore) | Indie & Alternative, Soul & R&B, Jazz & Blues, Chillout & Downtempo, Singer-Songwriter | Mellow, Romantic, Nostalgic, Relaxed, Golden, Reflective |
| **Night** (Malam) | Ambient & Electronic, Lo-Fi & Chillhop, Piano & Classical, Dream Pop & Shoegaze, R&B & Soul | Sleepy, Dreamy, Melancholic, Intimate, Cinematic, Nocturnal |

Setiap kategori menghasilkan 5 genre × 6 mood = **30 playlist**. Total **120**.

Contoh nama:
- `Morning 01 — Acoustic & Folk · Fresh`
- `Midday 01 — Pop · Upbeat`
- `Afternoon 01 — Indie & Alternative · Mellow`
- `Night 01 — Ambient & Electronic · Sleepy`

Daftar lengkap ada di `config/plan_120.md` (tabel untuk review), `config/playlist_copy_120.md` (120 judul + deskripsi English untuk review copy), dan `config/playlists_120.draft.json` (data untuk generator).

---

## 2. File penting

### Config

| File | Isi |
|---|---|
| `config/taxonomy.draft.json` | 4 kategori × 5 genre × 6 mood, base range audio, dan mood modifier. **Edit di sini** untuk mengubah taxonomy. |
| `config/rules.json` | Aturan global: 60/40, slice, offset, explicit, filter durasi/judul, series exclusion, nama template. |
| `config/priority_artists.json` | 25 artist No Detours + eL Utama, URI, dan nama untuk `SimpleArtistFilter`. |
| `config/priority_tracks.csv` | 1.383 track priority, sudah difilter dan diurutkan. Referensi/audit. |
| `config/priority_summary.json` | Ringkasan jumlah track priority dan filter yang dipakai. |
| `config/series_exclusion_uris.txt` | 240 URI track dari 16 series yang dikecualikan dari pool global. |
| `config/pool_manifest.json` | Definisi 21 pool: 1 priority + 20 genre. |
| `config/pool_uris.json` | **Satu-satunya tempat mengisi URI playlist pool** setelah pool dibuat. |
| `config/playlists_120.draft.json` | 120 entry playlist + 21 pool + rules yang sudah di-resolve. |
| `config/plan_120.md` | Rencana 120 playlist + 21 pool dalam bentuk tabel Markdown untuk review manusia. |
| `config/playlist_copy_120.md` | 120 judul + deskripsi English untuk review copy sebelum build pool. |

### Template

| File | Isi |
|---|---|
| `templates/TEMPLATE_POOL_PRIORITY.json` | Template program `POOL Priority`. |
| `templates/TEMPLATE_POOL_CATEGORY.json` | Template program pool genre (dipakai 20×). |
| `templates/TEMPLATE_GENERATOR_6H.json` | Template generator 6 jam dengan 14 objective MOS. |

Template memakai placeholder `__NAMA__`. Jangan diedit langsung untuk playlist tertentu; edit config lalu generate ulang.

### Tools

| File | Fungsi |
|---|---|
| `tools/build_config.py` | Membangun ulang `priority_artists.json`, `series_exclusion_uris.txt`, `priority_tracks.csv`, `priority_summary.json`, `pool_manifest.json`, `pool_uris.json`, dan `playlists_120.draft.json` dari taxonomy + rules + export. |
| `tools/validate_config.py` | Validasi config: jumlah kategori/genre/mood/playlist, range audio, offset, URI, sorting priority, dll. |
| `tools/generate_programs.py` | Generate JSON program pool dan generator dari template. |
| `tools/validate_programs.py` | Validasi graph dan invariant setiap program JSON. |
| `tools/extract_component_samples.py` | Ambil 1 contoh per tipe komponen untuk validasi ke API SmarterPlaylists. |
| `tools/export_plan_md.py` | Export `config/plan_120.md` dari config untuk review taxonomy dan nama playlist. |

### Output lokal

| Folder | Isi |
|---|---|
| `programs/pools/` | 21 program pool JSON. |
| `programs/generated/` | 4 sample generator: Morning 01, Midday 01, Afternoon 01, Night 01. |
| `programs/manifest.json` | Daftar file yang dihasilkan + warning. |
| `programs/component_samples.json` | 25 contoh komponen untuk validasi API. |

Semua file di `programs/` adalah **output lokal**. Belum diimpor ke SmarterPlaylists.

---

## 3. Cara kerja pool

### 3.1 `POOL Priority` (1 pool)

Tujuan: mengumpulkan **semua track** dari 26 artist priority, tanpa series exclusion.

Alur:

```
25 ArtistURIs ──► ToAlbums (newest, 50) ──► ToTracks (album_order, 50) ─┐
                                                                        ├──► DeDup ──► dur ──► clean ──► Sorter(release_date desc)
25 ArtistURIs ──► ToTracks (least_popular, 50) ────────────────────────┘                                      │
eL Utama playlist ─────────────────────────────────────────────────────┘                                      ▼
                                                                                                    Sorter(popularity asc)
                                                                                                              │
                                                                                                              ▼
                                                                                                     SeparateArtists
```

- `ToAlbums` mengambil 50 album/single/compilation terbaru per artist.
- `ToTracks` mengambil track album order dan track least popular.
- `DeDup` membuang duplikat.
- `dur` membuang track < 60 detik atau > 10 menit.
- `clean` membuang judul live/karaoke/cover/sped up/slowed/reverb/instrumental version/commentary.
- `Sorter` pertama: release date terbaru dulu.
- `Sorter` kedua: popularity paling rendah dulu.
- `SeparateArtists` menyebar artist, tetapi **urutan relatif dalam satu artist tetap terjaga**.
- **Tidak ada** `used_series`/`fresh` di pool priority. Ini disengaja agar 219 track priority yang pernah muncul di series tetap masuk pool.

Ukuran saat ini: **1.383 track** (±88 jam). Angka ini bisa berubah sedikit jika Spotify mengembalikan rilis baru.

### 3.2 Pool genre (20 pool)

Satu pool per kategori × genre. Tujuan: kandidat global yang cocok genre + mood + kategori.

Sumber:

1. **3 Last.fm tag** (contoh: `acoustic`, `folk`, `singer-songwriter`).
2. **MusicBrainz GenreArtists** (contoh: `folk`, 50 artist) → `ToTracks least_popular` 10 per artist.
3. **2 Tracks by Description** (contoh: `morning acoustic folk`, `warm acoustic folk`).
4. **3 Spotify Artist Radio** dari artist priority (rotasi seed per pool).

Filter keras:

- `Explicit` (clean untuk Morning/Midday; bypass untuk Afternoon/Night).
- `TextFilter` membuang judul live/karaoke/cover/sped up/slowed/reverb/instrumental version/commentary.
- `SimpleArtistFilter` membuang **26 artist priority** dari pool global (agar tidak dobel dengan pool priority).
- `TrackFilter` membuang 240 track series (by URI atau artist+title).
- `GenreFilter` (jika pool punya `filter`; untuk Lo-Fi & Chillhop dan Dream Pop & Shoegaze, hard filter genre sengaja dilewati, tetapi `artist_genre` tetap dipakai untuk MusicBrainz).
- `AttributeRangeFilter`: energy, valence, tempo, danceability, acousticness sesuai kategori.
- `AttributeRangeFilter` durasi 60 detik–10 menit.
- `MaxTracksPerArtist` 3 (global).
- `First` 3.000 track.
- `SeparateArtists`.

Catatan: `First` **tidak menambah** track. Jika sumber hanya menghasilkan 1.200 track, pool berisi 1.200 track. Karena itu, setelah pool dibuat, cek ukuran pool terkecil dan sesuaikan `global_pool_size_estimate` di `config/rules.json` (lihat bagian 8).

### 3.3 Genre yang memakai `artist_genre`

Tiga pool memakai `filter` kosong karena nama genrenya gabungan:

| Pool | `filter` (hard) | `artist_genre` (MusicBrainz) |
|---|---|---|
| `POOL Morning - Lo-Fi & Chillhop` | *(kosong)* | `lo-fi` |
| `POOL Night - Lo-Fi & Chillhop` | *(kosong)* | `lo-fi` |
| `POOL Night - Dream Pop & Shoegaze` | *(kosong)* | `dream pop` |

Untuk tiga pool ini, `GenreFilter` dilewati agar track chillhop/shoegaze yang tidak punya tag genre persis tetap bisa masuk. `GenreArtists` tetap memakai `artist_genre` untuk menemukan artist yang relevan. Objective MOS `contains` memakai `genre_match_value` (`lo-fi`/`dream pop`).

---

## 4. Cara kerja generator 6 jam

Setiap playlist punya satu program generator. Alur:

```
POOL Priority ──► DeDup ──► Concatenate(2×) ──► AllButTheFirst(priority_offset) ──► First(200) ──► MaxTracksPerArtist(8) ─┐
                                                                                                                        ├──► Concatenate ──► DeDup ──► Explicit* ──► MOS(14 objectives) ──► ShorterThan(21600) ──► PlaylistSave
POOL Genre ─────► DeDup ──► Concatenate(2×) ──► AllButTheFirst(global_offset) ────► First(300) ──► MaxTracksPerArtist(3) ─┘
```

\* `Explicit` hanya ada untuk Morning/Midday (clean). Afternoon/Night bypass node ini.

`PlaylistSave` adalah **main output**. Node ini menggantikan auto-save (tidak membuat playlist duplikat) dan menulis judul + deskripsi Inggris ke Spotify.

### 4.1 Rotasi offset

- Priority: `priority_offset = (index - 1) × 200 mod 1.383`
- Global: `global_offset = (index - 1) × 300 mod 3.000`

`Concatenate(2×)` menduplikasi pool agar `AllButTheFirst` tetap punya cukup track ketika offset mendekati akhir pool. `DeDup` setelah combine memastikan tidak ada track dobel **di dalam satu playlist**.

Offset membuat setiap playlist mulai dari titik berbeda di pool. Ini mengurangi overlap antar playlist, tetapi tidak menghilangkan overlap sepenuhnya. Overlap **diperlukan** untuk mencapai 60/40 (lihat bagian 5).

### 4.2 14 objective MOS

| Objective | Field | Nilai | Weight | Fungsi |
|---|---|---|---|---|
| `match-max-run` | artist | `max_run=1`, `separation=2` | **unbreakable** | Tidak ada 2 track berturut-turut oleh artis yang sama. |
| `min-separation` | artist | `separation=2` | high | Memperlebar jarak antar track artis yang sama. |
| `distribution` | source | `priority(60%) global(40%)` | high | Target rotasi 60/40. |
| `match` | artist | `eL Utama` | high | eL Utama sedikit lebih diprioritaskan dari 25 artist lain. |
| `minimize` | popularity | — | **highest** | Pilih track yang kurang populer. |
| `maximize` | release_year | — | high | Pilih rilis yang lebih baru. |
| `max-match` | artist | `max_count=8` | medium | Batas lunak 8 track per artis. |
| `contains` | mb_genres | genre pool | medium | Dorong kecocokan genre. |
| `range` | energy | range kategori+mood | medium | Kecocokan energi. |
| `range` | valence | range kategori+mood | medium | Kecocokan mood. |
| `range` | tempo | range kategori+mood | low | Kecocokan tempo. |
| `range` | danceability | range kategori+mood | low | Kecocokan danceability. |
| `range` | acousticness | range kategori+mood | low | Kecocokan akustik. |
| `variety` | mb_genres | — | low | Variasi genre. |

`match-max-run` adalah **hard constraint** (unbreakable). `distribution` adalah **soft objective**: MOS berusaha mendekati 60/40, tetapi hasil akhir bisa sedikit berbeda, terutama setelah `ShorterThan` memotong durasi.

### 4.3 Hard cap 6 jam

`ShorterThan` dengan `time=21600` adalah pengaman terakhir. MOS diberi `limit=120` track kandidat; jika total durasi kandidat > 6 jam, `ShorterThan` memotong dari akhir. Jika hasil sering jauh di bawah 6 jam, naikkan `mos_limit` atau `global_slice`/`priority_slice`. Jika hasil sering terpotong terlalu banyak, turunkan `mos_limit`.

**Jangan hapus atau ubah `ShorterThan` tanpa memahami efeknya.** Ini satu-satunya yang menjamin playlist tidak pernah > 6 jam.

### 4.4 Explicit

| Kategori | Pool global | Generator |
|---|---|---|
| Morning | `Explicit false` | `Explicit false` (clean) |
| Midday | `Explicit false` | `Explicit false` (clean) |
| Afternoon | bypass | bypass |
| Night | bypass | bypass |

Pool priority selalu berisi semua track (explicit dan clean). Generator yang menyaring sesuai kategori. Jadi track explicit dari artist priority tetap bisa muncul di Afternoon/Night, tetapi tidak di Morning/Midday.

### 4.5 Judul dan deskripsi playlist

**Judul** mengikuti format:

```
{Category} {index:02d} — {Genre} · {Mood}
```

Contoh: `Morning 01 — Acoustic & Folk · Fresh`.

**Deskripsi** mengikuti template:

```
{Category intro} a/an {mood} {genre} mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}.
```

Contoh:
- `Morning 01` — "Start your morning with a fresh acoustic & folk mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}."
- `Midday 01` — "Power through midday with an upbeat pop mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}."
- `Afternoon 01` — "Soundtrack your afternoon with a mellow indie & alternative mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}."
- `Night 01` — "Unwind into the night with a sleepy ambient & electronic mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}."

Deskripsi ditulis ke Spotify oleh node `PlaylistSave` (main output). Batas Spotify: **300 karakter**. `${NUM_TRACKS}` dan `${DURATION}` diisi otomatis saat run.

---

## 5. Kenapa 60/40 butuh pengulangan

- Priority pool: **1.383 track / ±88,2 jam**.
- 120 playlist × 6 jam = **720 jam**.
- Tanpa pengulangan, porsi priority hanya **88,2 / 720 = 12,25%** (±44 menit per playlist).
- Untuk mencapai 60% priority (432 jam dari 720 jam), pool priority harus dipakai ulang sekitar **4,9×** across 120 playlist.
- Untuk 50/50, pengulangan sekitar **4,1×**.

Itu sebabnya:
- Offset rotasi berbeda per playlist.
- `Concatenate(2×)` menduplikasi pool sebelum dipotong.
- `DeDup` hanya mencegah duplikat **di dalam satu playlist**, bukan antar playlist.
- Track priority yang sama akan muncul di beberapa playlist berbeda. Ini konsekuensi langsung dari target 60/40 dan ukuran katalog priority.

---

## 6. Cara edit taxonomy

1. Buka `config/taxonomy.draft.json`.
2. Edit bagian `categories`.
   - Setiap kategori harus punya **5 genre** dan **6 mood**.
   - Setiap genre punya:
     - `name`: nama tampilan.
     - `filter`: genre untuk `GenreFilter` (boleh kosong).
     - `artist_genre` (opsional): genre untuk `GenreArtists` jika `filter` kosong.
     - `tags`: tepat 3 tag Last.fm.
     - `descriptions`: tepat 2 deskripsi.
   - Setiap mood punya `modifiers` untuk `energy`, `valence`, `tempo`, `danceability`, `acousticness`.
3. Edit `config/rules.json` jika ingin mengubah 60/40, slice, batas durasi, regex judul, atau kebijakan explicit.
4. Jalankan:

```powershell
python tools/build_config.py
python tools/validate_config.py
python tools/export_plan_md.py
```

5. Generate ulang program:

```powershell
python tools/generate_programs.py --mode samples --clean
python tools/validate_programs.py
```

Setelah judul/deskripsi disetujui dan pool URI terisi, generate semua 120:

```powershell
python tools/generate_programs.py --mode all --clean
python tools/validate_programs.py
```

**Catatan:** `--clean` menghapus file JSON lama di `programs/pools/` dan `programs/generated/` agar tidak ada file dengan nama Indonesia yang tertinggal.

**Catatan:** mengubah `name` genre/mood akan mengubah nama playlist dan slug file. Karena belum ada playlist yang dibuat, ini aman. Jika nanti sudah ada playlist, rename akan membuat program baru, bukan mengganti playlist lama.

---

## 7. Cara generate program

```powershell
# 21 pool + 4 sample generator (default)
python tools/generate_programs.py --mode samples --clean

# 21 pool + 120 generator
python tools/generate_programs.py --mode all --clean

# hanya 21 pool
python tools/generate_programs.py --mode pools-only --clean
```

`--clean` menghapus file JSON lama di `programs/pools/` dan `programs/generated/` sebelum generate. Selalu pakai `--clean` saat regenerate setelah rename, agar file lama tidak tertinggal.

Output:
- `programs/pools/*.json` — 21 program pool.
- `programs/generated/*.json` — generator (4 sample atau 120).
- `programs/manifest.json` — daftar file + warning.

Validasi lokal:

```powershell
python tools/validate_programs.py
```

Warning `placeholder playlist URI` **normal** selama `config/pool_uris.json` masih berisi `REPLACE_ME`. Warning ini akan hilang setelah URI pool diisi.

Validasi komponen ke API SmarterPlaylists (read-only, tidak membuat program):

```powershell
python tools/extract_component_samples.py
```

Lalu buka `programs/component_samples.json` dan kirim satu per satu ke `POST /api/programs/validate-component` dari sesi SmarterPlaylists. Saat ini **26 tipe komponen sudah divalidasi dan semuanya `valid: true`**, termasuk `PlaylistSave`.

---

## 8. Fase berikutnya: build 21 pool

> Jangan mulai fase ini sebelum taxonomy dan judul/deskripsi disetujui. Pool yang sudah dibuat akan memakai nama dan filter dari taxonomy saat itu.

### Langkah 1 — Import 21 program pool

Import file dari `programs/pools/` ke SmarterPlaylists. Bisa lewat UI (Import/JSON) atau API:

```
POST /api/programs/
Body: { "name": "<program name>", "program_json": <isi file JSON> }
```

Sesi SmarterPlaylists yang sudah login dipakai untuk auth. Tidak perlu Spotify Developer app.

### Langkah 2 — Run setiap pool

Run `POOL Priority` dan 20 pool genre satu kali. Auto-save akan membuat playlist dengan nama program.

- Pool ini **internal**. Tidak perlu di-follow.
- Bisa diset private/unlisted.
- Jangan tambahkan track manual; isi pool sepenuhnya dari program.

### Langkah 3 — Isi URI pool

Buka `config/pool_uris.json`. Ganti `spotify:playlist:REPLACE_ME` dengan URI playlist hasil run, di key yang sesuai:

```json
{
  "POOL Priority": "spotify:playlist:xxxxxxxxxxxxxxxxxxxxxx",
  "POOL Morning - Acoustic & Folk": "spotify:playlist:yyyyyyyyyyyyyyyyyyyyyy",
  ...
}
```

Key harus **persis sama** dengan `program_name` di `config/pool_manifest.json`.

### Langkah 4 — Cek ukuran pool global

Cek jumlah track setiap pool genre. Cari pool terkecil. Kemudian set `global_pool_size_estimate` di `config/rules.json` ke angka yang aman (misalnya ukuran pool terkecil, atau sedikit di bawahnya):

```json
"global_pool_size_estimate": 1500
```

Kenapa? Offset global dihitung `(index-1) × 300 mod global_pool_size_estimate`. Jika estimate 3.000 tetapi pool sebenarnya hanya 1.500, offset 2.700 akan menghasilkan slice kosong. Menurunkan estimate membuat offset berputar lebih awal dan tetap menghasilkan kandidat.

Untuk priority pool, `priority_pool_size` dihitung otomatis dari `config/priority_tracks.csv` (1.383), bukan dari `priority_pool_size_estimate`. Jika hasil run priority pool berbeda jauh, periksa filter/sumber di template priority pool dan `config/priority_tracks.csv`; setelah CSV/filter diperbarui, jalankan ulang `build_config.py`. Field `priority_pool_size_estimate` di `rules.json` hanya referensi.

### Langkah 5 — Propagate URI dan generate semua

```powershell
python tools/build_config.py
python tools/validate_config.py
python tools/generate_programs.py --mode all
python tools/validate_programs.py
```

Setelah URI terisi, warning placeholder harus hilang.

### Langkah 6 — Import dan run 120 generator

Import 120 file dari `programs/generated/`. Untuk setiap program:

1. **Preview** dulu (run tanpa save) untuk cek durasi, urutan, dan tidak ada artis berurutan.
2. Jika sudah cocok, **Run** untuk menyimpan.
3. Node `PlaylistSave` (main output) membuat playlist pertama kali, mengganti isinya pada run berikutnya, dan menulis deskripsi Inggris.
4. Deskripsi diatur otomatis; tidak perlu edit manual di Spotify.

Jangan jalankan semua 120 sekaligus tanpa preview. Preview membantu menangkap pool yang kosong, offset yang salah, atau filter yang terlalu ketat.

---

## 9. Troubleshooting

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| Playlist < 6 jam jauh | Pool terlalu kecil, slice terlalu kecil, atau filter terlalu ketat | Naikkan `global_slice`/`priority_slice`, turunkan filter, atau naikkan `mos_limit`. |
| Playlist terpotong di akhir dan 60/40 melenceng | `mos_limit` terlalu tinggi sehingga `ShorterThan` memotong banyak | Turunkan `mos_limit` (mis. 90–100) atau naikkan weight `distribution`. |
| Ada 2 track artis sama berurutan | `match-max-run` dihapus/diubah, atau pool punya track dengan metadata artist berbeda | Pastikan `match-max-run` weight `unbreakable`, `max_run=1`. Cek metadata artist. |
| Pool global kosong | `GenreFilter` terlalu sempit, audio range terlalu ketat, atau `artist_genre` salah | Longgarkan range, cek `artist_genre`, atau bypass `GenreFilter`. |
| Offset menghasilkan slice kosong | `global_pool_size_estimate` > ukuran pool sebenarnya | Set estimate ke ukuran pool terkecil. |
| Pool priority berubah ukuran | Rilis baru / track hilang / filter berubah | Cek `priority_summary.json` dan `priority_tracks.csv`; sesuaikan filter/sumber lalu regenerate. |
| Generator memakai isi pool lama | `cache_mode: short-term` di `SpotifyPlaylist` | Ubah ke `no-cache` sementara atau tunggu cache expire. |
| `SpotifyPlaylist` tidak menemukan pool | URI masih `REPLACE_ME` atau `user` salah | Isi `config/pool_uris.json`; pastikan `user` di template sesuai akun. |
| Deskripsi playlist default / tidak muncul | Node `PlaylistSave` bukan main output atau field Description kosong | Pastikan `main` = `save`, tipe node `PlaylistSave`, dan `description` terisi. |
| Explicit lolos di Morning/Midday | `Explicit` node di-bypass atau weight salah | Pastikan generator clean punya node `Explicit` dengan `explicit: false`. |
| Track series muncul di pool global | `fresh`/`used_series` di-bypass | Pastikan `exclude_series_tracks: true` dan `used_series` berisi 240 URI. |

---

## 10. Hasil validasi saat ini

| Pemeriksaan | Hasil |
|---|---|
| `python tools/validate_config.py` | **0 error, 0 warning** |
| `python tools/validate_programs.py` | **0 error**, 8 warning (hanya placeholder URI pool) |
| API `validate-component` | **26/26 tipe komponen valid** (termasuk `PlaylistSave`) |
| Jumlah pool | 21 (1 priority + 20 genre) |
| Jumlah generator sample | 4 (Morning 01, Midday 01, Afternoon 01, Night 01) |
| Priority track | 1.383 |
| Series exclusion URI | 240 |
| Playlist config | 120 (30 per kategori) |
| Status taxonomy | **Disetujui (2026-10-24)** |
| Bahasa judul & deskripsi | **English** (marketable, professional) |
| Deskripsi playlist | Ditulis via `PlaylistSave` (≤300 karakter) |
| Program/playlist baru dibuat | **0** |

---

## 11. Keputusan desain yang perlu diingat

1. **Program name = playlist name; deskripsi via `PlaylistSave`.** Node `PlaylistSave` adalah main output, sehingga menggantikan auto-save (tidak membuat playlist duplikat) dan menulis deskripsi Inggris ke Spotify.
2. **Pool internal tidak perlu di-follow.** Pool hanya sumber track untuk generator.
3. **Priority pool tidak memakai series exclusion.** Series exclusion hanya untuk pool global. Ini menjaga 1.383 track priority tetap utuh.
4. **60/40 adalah objective, bukan quota hard.** MOS berusaha mendekati; hasil akhir bisa sedikit berbeda.
5. **"Least popular first, then newest" berlaku di urutan kandidat pool priority.** MOS boleh mengubah urutan akhir untuk variasi dan no-consecutive-artist. Jika yang dimaksud adalah urutan akhir yang strictly popularity-ascending, objective MOS perlu diubah (dan no-consecutive-artist bisa sulit dipenuhi).
6. **eL Utama sedikit lebih tinggi** lewat objective `match artist eL Utama` weight `high`. 25 artist lain tidak punya objective `match` khusus.
7. **Global pool mengecualikan 26 artist priority** agar tidak dobel dengan pool priority. Kombinasi 60/40 mengatur porsi akhir.
8. **Taxonomy dan penamaan Inggris sudah disetujui (2026-10-24).** Perubahan setelah pool dibuat akan mengubah nama/filter; regenerate config dan rebuild pool jika taxonomy diubah.
9. **`config/pool_uris.json` adalah sumber URI pool.** Jangan edit `pool_manifest.json`/`playlists_120.draft.json` untuk URI; edit `pool_uris.json` lalu regenerate.
10. **Tidak ada Spotify Developer app.** Auth memakai sesi SmarterPlaylists. Untuk batch-follow 120 playlist nanti, gunakan sesi browser/API yang sama.

---

## 12. Urutan kerja yang disarankan

1. **Review judul & deskripsi** — setujui format English, 5 genre × 6 mood per kategori, explicit policy, dan 60/40.
2. **Regenerate config** — `python tools/build_config.py` lalu `python tools/validate_config.py`.
3. **Build 21 pool** — import + run pool programs.
4. **Isi `config/pool_uris.json`** — 21 URI.
5. **Cek ukuran pool** — set `global_pool_size_estimate` ke ukuran pool global terkecil.
6. **Generate semua 120** — `python tools/generate_programs.py --mode all`.
7. **Validasi** — `python tools/validate_programs.py`; warning placeholder harus 0.
8. **Preview + run 120 generator** — satu per satu atau batch setelah yakin.
9. **Audit hasil** — cek durasi ≤ 6 jam, tidak ada artis berurutan, explicit policy, dan porsi priority/global.
10. **Batch-follow (opsional, fase terpisah)** — follow 120 playlist ke akun personal.

---

## 13. Perintah cepat

```powershell
# Dari C:\Users\USER\Documents\OpenCode\smart-playlist

# 1. Bangun config dari taxonomy + rules
python tools/build_config.py

# 2. Validasi config + export plan Markdown
python tools/validate_config.py
python tools/export_plan_md.py

# 3. Generate 21 pool + 4 sample
python tools/generate_programs.py --mode samples --clean

# 4. Validasi program
python tools/validate_programs.py

# 5. Setelah pool URI terisi, generate semua 120
python tools/generate_programs.py --mode all --clean

# 6. Validasi ulang
python tools/validate_programs.py
```

---

## 14. Yang belum dilakukan

- Belum ada program SmarterPlaylists yang dibuat/diimpor.
- Belum ada pool playlist yang dibuat/dijalankan.
- Belum ada 120 playlist Spotify yang dibuat.
- Belum ada deskripsi playlist yang ditulis ke Spotify (menunggu run generator).
- Belum ada batch-follow.
- Belum ada scheduling.
- Taxonomy dan judul/deskripsi English sudah disetujui; pool dan 120 playlist belum dibuat.

Semua langkah di atas sengaja ditunda sampai judul/deskripsi disetujui dan pool siap dibangun.
