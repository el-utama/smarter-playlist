# FAQ Ringkas (dari aplikasi resmi, v3.12.3)

> 30 pertanyaan & jawaban resmi dari halaman FAQ, distilasi + komentar.

## Dasar produk
- **Produk selesai?** Ya — program & playlist kamu dipertahankan antar-update.
- **Apa itu SP?** Visual graph builder untuk playlist Spotify yang cerdas — mix/filter/sort/combine dari sumber apa pun.
- **Buat program:** Programs → **New Program** (atau tab Editor). Klik komponen di palette → kanvas; drag kabel output → input. Node ★ (main) menentukan output.
- **Klik Run:** graf dieksekusi → hasil disimpan ke playlist Spotify **bernama program**. Run pertama = playlist baru, run beikutnya memperbarui playlist yang sama.
- **Preview:** run **tanpa** menyimpan ke playlist — untuk uji/debug.
- **Save to Playlist di akhir?** Tidak perlu! Ini penyebab #1 playlist dobel. Komponen ini hanya untuk cabang samping.

## Editor
- **Shortcut:** double-click = edit param; Space = jadikan main ★; Del = hapus; Shift+Del = splice-out (auto reconnect); Ctrl+C/V copy/paste subgraf; Ctrl+Click multi-select; drag kanvas rectangle select.
- **Snap & Layout:** Snap = grid 20px; Layout = raw otomatis top-to-bottom (+ Undo setelahnya).
- **Drag palette:** drop ke node → connected-downstream/splice; drop ke edge → sisip; valid target beranimasi/glow.
- **Drag dari Spotify desktop:** playlist/album/artis/track → node dibuat otomatis terisi; multi-track → Track URIs satu node.
- **Port berwarna:** definisi per-komponen (hover lihat deskripsi); umumnya green sehari (primary), red exclusion track, orange exclusion artist. Komponen kondisional: green = benar, red = salah.
- **Bintang:** penanda main output node (tekan Space).

## Program & playlist
- **Schedule:** Programs → kolom Schedule. `hourly/daily/weekly`, total runs maks 100; gagal 3× berturut-turut → auto pause.
- **Tags:** label untuk filter program (dialog Program Settings / icon tag di Actions). Autocomplete dari tag lama.
- **Combine playlist:** banyak sumber → Combiner (Alternate interleave; Shuffler acak; MixIn rasio).
- **Sharring:** Publish → link **live** (edit tetap terlihat); Import = salinan independen; bisa unpublish.
- **Import program lama:** tab Import tampil bila punya program legacy; komponen EchoNest diberi tanda Deprecated.
- **Dark mode:** icon tema: System / Light / Dark.

## Entitas & attribute
- **Artis & album bukan hanya track?** Ya — 3 entitas dengan sumber khusus dan adapter konversi (To Tracks/To Artists/To Albums/Similar Artists). Filter/sort/selector generic otomatis adaptasi attribute.
- **Warna violet & teal:** artist = violet putus-putus; album = teal putus-putus; track = hijau solid; header node source/adapter match tipe output.
- **Attribute audio:** lihat `09-attributes.md` — dari danceability/energy/valence dsb. hingga popularity/release_date/duration/camelot.

## Question konsultasi
- Music Machinery blog (musicmachinery.com), r/smarterplaylists di Reddit, @plamere di Bluesky.

## Komponen apa itu?
- Lihat `node-*.md` per kategori lengkap (93 komponen, parameters).

## MOS (Multi-Objective Sequencer)
- Advanced ordering — menyeimbangkan banyak bobot coords. Random/variety/min-separation dsb. Dokumentasi lengkap: `10-mos.md` & situs `/docs/mos-reference`.
