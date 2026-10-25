# Folder Pengetahuan SmarterPlaylists

> Dihasilkan dari riset mendalam terhadap **smarterplaylists.playlistmachinery.com** versi **3.12.3** (Oktober 2026), mencakup: registry 93 komponen resmi (`/api/inventory`), dokumentasi MOS (`/docs/mos-reference`), schema 14 objective (`/api/objectives`), tutorial & FAQ resmi dari aplikasi, changelog 206 versi, serta artikel pengembang (Music Machinery blog).

## Peta Isi File

| File | Isi |
|---|---|
| `00-arsitektur-dasar.md` | Konsep inti: program, main node, Run vs Preview, port & warna, entitas (track/artist/album), cara kerja penyimpanan playlist otomatis, scheduling, sharing, shortcut keyboard, variabel deskripsi playlist |
| `node-source.md` | 35 node **Sources** — sumber track/artist/album (Spotify, Last.fm, chart) dengan seluruh parameter |
| `node-adapter.md` | 6 node **Adapters** — konversi track↔artist↔album, Similar Artists |
| `node-filter.md` | 22 node **Filters** — penyaring (range, track filter, genre, gender, audio features, dsb.) |
| `node-combiner.md` | 7 node **Combiners** — Concatenate, Alternate, Shuffler, MixIn, Mixer, Intersection, Random |
| `node-selector.md` | 9 node **Selectors** — First, Last, Sample, ShorterThan/LongerThan, Pager, dsb. |
| `node-order.md` | 7 node **Orders** — Sort, Reverse, Weighted Shuffler, Separate Artists, Smart Mix, MOS |
| `node-conditional.md` | 4 node **Conditionals** — Is Weekend, Is Day of Week, Yes/No, Date Range |
| `node-output.md` | 2 node **Outputs** — Save to Playlist / Save to New Playlist |
| `node-annotation.md` | 1 node **Comment** |
| `09-attributes.md` | Tabel lengkap semua **attribute track/artist/album** (definisi & rentang nilai) |
| `10-mos.md` | Panduan konsep **Multi-Objective Sequencer** — objective, bobot, slot, cara kerja, best practices |
| `10-mos-objectives.md` | Referensi teknis **14 objective** MOS beserta parameter & nilai enum |
| `11-resep-playlist.md` | **Resep program siap pakai** (party, DJ set, discovery, chill, gender balance, dsb.) |
| `12-changelog.md` | Ringkasan changelog (fitur utama per versi) |
| `13-faq-ringkas.md` | 30 FAQ resmi distilasi |
| `data/` | Data mentah riset: inventory.json, objectives.json, changelog.json, tutorial asli |

## Cara Pakai Folder Ini (untuk bantuan AI)

Ketika ingin dibuatkan program *Smarter Playlists* (SP), cukup deskripsikan **hasil yang diinginkan** — misalnya:

> "playlist 50 lagu energetic dari playlist favoritku demi lagu, tanpa artis yang sama berurutan"

AI akan:
1. Rancang **topologi node** (string `Sumber → Filter → Combiner → Selector → Order`),
2. Pilih node dari file `node-*.md` dan tulis parameter spesifik,
3. Berikan **langkah manual di editor** (bukan program JS — SP didesain di editor visual),
4. Kalau urutan lagu penting, gunakan MOS (lihat `10-mos.md`).
5. Kamu klik Run → playlist Spotify otomatis diperbarui.
