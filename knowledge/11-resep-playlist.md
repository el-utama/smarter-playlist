# Resep Program Siap Pakai

> Kumpulan topologi node siap meniru di editor. Setiap resep terdiri dari rantai node → parameter → tips. Semua panjang playlist dikendalikan oleh selector (`First`/`Sample`/MOS `limit`), bukan node Save.

Penting: tidak perlu node Save di akhir — saat Run, program otomatis menyimpan hasil ke playlist Spotify bernama sama dengan program (detail di `00-arsitektur-dasar.md`). Star ★ (main node) menentukan node yang output-nya disimpan.

---

## 1. My Top N — playlist paling dasar

```
My Top Tracks → First (count 25)
```
- My Top Tracks: default 50 track, rentang `medium_term`.
- **★ main**: First.
- Alternatif variasi: `Shuffler` sebelum First untuk acak; `Range Filter popularity` untuk kurasi.

## 2. Top N tanpa artis repeat

```
My Top Tracks → Artist De-Dup → First (25)
```

## 3. Mix dua playlist bergantian (Alternator)

```
Playlist A ┐
           ├─ Alternate → Remove Duplicates (DeDup) → First (50)
Playlist B ┘
```
- Connect **kedua** source ke port `green` Alternate (multi-input round-robin).
- Aktifkan `by_name` pada DeDup agar lagu yang sama (beda karena beda ID platform versi) ikut terhapus.

## 4. Rasio campuran (Mix In)

```
Playlist A(green) ┐
                  ├ Mix In ─…→ First (100)
Playlist B(red)   ┘
```
- Mix In: `n_skips`(green berurutan) vs `n_tracks`(red berurutan); mis. 3 vs 1 → 75% A, 25% B.
- Variant: **Mixer** untuk multi-stream dedup/artis separation built-in (max_tracks, min_artist_separation 4).
- Random interleave: **Random** (RandomSelector).

## 5. Playlist "Fresh" — lagu dari perpustakaan yang jarang didengar belakangan

```
My Saved Tracks (limit 200) ─green┐
                                  ├ Track Filter → Shuffler → First (30)
My Top Tracks ───────────────red┘
```
- Track Filter: menghapus track di red stream dari green stream; `by_name` true.
- Untuk exclude artis: gunakan **Artist Filter** (red = artis) atau port `orange` **Mixer**.

## 6. High-Energy Dance

```
Playlist (BESAR) → Danceable (most) → Energy (more) → First (30)
```
- Filter audio features paling baik saat pool besar.
- Kontrol presisi: Range Filter (attr `danceability`, min 0.6) atau `valence` cheerful.

## 7. Chill / fokus instrumen

```
Playlist → Range Filter energy 0.15-0.45 → Range Filter tempo 70-100 → Sample (30)
```
- atau MOS: range energy unbreakable + maximize instrumentalness + minimize speechiness + variety artist.

## 8. Upbeat di hari kerja, chill saat weekend (scheduled)

```
Upbeat branch (Playlist→Energy most→First 40) ─red┐
                                                  ├ Is Weekend? → Shuffle
Chill branch (Playlist→Energy least→First 40) ─green┘
```
- Port `green` Is Weekend = saat benar (weekend), `red` = saat salah (hari kerja).
- Schedule **daily** → isi playlist berubah karakter otomatis tiap hari (upbeat hari kerja, chill akhir pekan).
- Alternatif: **Is Day of Week** untuk routing beda hari Sen-Min; **Yes or No** switch manual; **Date Range** untuk musim/event.

## 9. Discovery — artis serupa dari favoritku

```
My Top Artists → Similar Artists (count 3) → To Tracks (select most_popular, count 5) → Shuffler → First (50)
```

## 10. Discography satu artis

```
ArtistByName (Radiohead) → To Albums (album_type album) → To Tracks (album_order) → First (30)
```
- To Tracks mode `album_order` mempertahankan rangka album natural.

## 11. Label / era / genre

```
Label Albums (4AD, order most_popular) → Range Filter release_year 1980-1999 → To Tracks (album_order, count 3) → First (40)
```
- v3.10.1+: To Albums mengembalikan juga `single`/`compilation`/`appears_on` — pakai parameter `album_type` di To Albums untuk menyaring, mis. bawaan saja.
- Versi genre: **GenreArtists** source → To Tracks.

## 12. Genre Radio versi Spotify

```
GenreArtists (rock) → ArtistTopTracks per artis (via To Tracks most_popular) → Sample (50)
```
atau langsung node **Artist Radio** (URI artis) untuk membuat "radio" per artis.

## 13. Track by Description ("chill lo-fi")

Tracks By Description source — pencarian lagu via deskripsi (LLM-assisted search); pas untuk "mood".

## 14. Last.fm digunakan bersama Spotify

```
LastFmTagTopTracks (tag: "shoegaze") → GenreFilter mb_genres contains → Sample (40)
```
- Kombinasi sumber Last.fm: loved tracks / recent / top / similar / tag top — bahkan chart negara (**Country Top Tracks**).

## 15. God-mode: playlist via MOS

```
Pool besar (beberapa Playlist digabung) → Multi-Objective Sequencer → selesai
```
- MOS punya parameter `limit` sendiri — tidak perlu `First` setelahnya.
- Set objectives sesuai tabel contoh di `10-mos.md` (party, DJ set, discovery, energy arc, anchor pembuka/penutup via slots).

## 16. Weekly counter / Pager

```
Playlist (Stream total) → Pager (page_size 50) → Run berulang tiap hari → playlist paginated
```

## 17. Chart global Last.fm

```
LastFmGlobalTopTracks → Range Filter release_year (min 2015) → First (20)
```

## 18. Pola debugging

- Pindahkan ★ main ke tengah pipeline → Run dengan node apa pun sebagai output → baca hasil di preview (kolom menyesuaikan tipe entitas).
- Filter hasil MOS berdasarkan `mo_score` (Range Filter `mo_score < 0.4`) untuk membuang hasil yang terlalu banyak kompromi.
- Buka runtime statistik setelah Run: jumlah API call per komponen, track mengalir, cache hit — mempermudah menemukan bottleneck (mis. Alternate yang boros API karena dekorasi attribute).

---

## Cek Cepat saat Error / Hasil Kurang Pas

| Gejala | Punca umum |
|---|---|
| Track lebih sedikit dari limit | terlalu banyak `unbreakable` (MOS berhenti lebih awal); pool kecil; `fail_fast` di mixer menghentikan lebih cepat || Lagu sama tiap minggu | set `cache_mode: no-cache` di source; tambahkan `random`/Shuffler/Sample acak |
| Dua playlist tiap run | ada PlaylistSave di akhir (hapus) — Run otomatis sudah menyimpan |
| Preview terlihat, Run gagal | Run mensyaratkan output track; pastikan ★ main node memproduksi track |
| Genre tidak lolos filter | genre granular (post-grunge vs punk) — pakai `mb_genres contains`; coba opsi `primary genre only` |
| Artis salah di ArtistByName | nama bermasalah dengan aksen; gunakan URI, atau pilih hasil teliti (fuzzy search) |
| Hanya sedikit track lolos filter audio | pool harus besar — filter audio features paling baik di atas pool ratusan track |
| › output artist/album saat Run | Run mensyaratkan output track; gunakan adapter To Tracks, atau cukup Preview untuk debug |
