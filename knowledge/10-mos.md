# Konsep Multi-Objective Sequencer (MOS)

> Distilasi dari panduan resmi `/docs/mos-reference` (v3.12.3). Detail parameter per objective ada di `10-mos-objectives.md`.

## Apa itu MOS?

**Multi-Objective Sequencer** adalah node **ordering** yang membangun playlist **track-per-track**, memilih kandidat terbaik di tiap langkah berdasar **banyak tujuan sekaligus** (objectives).

Sederhanakan bayangan: Sorter biasa bisa satu hal (sort tempo, sort popularitas, shuffle acak). MOS bisa:

> "track-nya high-energy, artis jarang berulang, tempo tetap di 110–140 BPM, valence naik secara bertahap."

## Cara konfigurasi

- Feed MOS dengan **pool kandidat** dari sumber apa pun (green input), lalu set **limit** (default 50, maksimum output track).
- Tambahkan **≥1 objective**; setiap objective punya bobot.
- Di kanvas, node menampilkan ringkasan **attribute tebal**; batasi tampilan >6 objective (double-click untuk edit lengkap).
- Setiap track keluaran MOS mendapat **`attribute` `mo_score`** (0 = fit terbaik; tinggi = banyak compromise).

## Bobot (Weight)

| Weight | Nilai | Arti |
|---|---|---|
| `off` | 0 | Objective diabaikan |
| `lowest` | 0.01 | Tiebreaker — hanya menentukan saat seri |
| `low` | 0.25 | Preferensi halus |
| `medium` | 0.5 | Default — keseimbangan |
| `high` | 0.75 | Kuat |
| `highest` | 1.0 | Dominan |
| `unbreakable` | ∞ | Batas keras — track yang melanggar **didiskualifikasi total** bila tak ada kandidat lolos, MOS berhenti (playlist lebih pendek dari limit) |

Skor total dihitung = Σ (skor-objective × bobot), dengan **skor terendah menang** (0 sempurna, 1 terburuk).

> Beberapa objective tidak dapat `unbreakable` karena `maximize/minimize/target/order-by` adalah *ranking* — semua track kecuali 1 akan didiskualifikasi. Untuk preferensi sangat kuat pakai `highest`.

## Kelompok Objective

### Value (tak peduli konteks)

- **maximize** — pilih nilai lebih tinggi.
- **minimize** — pilih nilai lebih rendah.
- **range** — nilai dalam rentang (soft saat weighted, keras saat unbreakable).
- **target** — nilai mendekati target tertentu.
- **match** — nilai persis tertentu (text/numeric).
- **contains** — field mengandung / anggota (substring atau list membership — `mb_genres` include 'rock').
- **distribution** — target persentase bucket value: `female(30%) male(50%)` atau `1970-1979(20%) 1980-1989(30%)` / `rock(20%) jazz(20%)`.

### Sequencing (sadar konteks — lihat isi playlist)

- **variety** — prefer tak serupa dengan yang sudah dipilih (artist, genre, angka). `inverse` = pekat/jumpat.
- **min-separation** — jarak minimal antar nilai sama (artist, genre, dsb.): "default separation 5".
- **order-by** — teruskan arah ascending/descending. `spread` = `off` (sequential) / `full` (span seluruh rentang kandidat) / `segment` (tiap segmen slot span full range).
- **max-match** — cap jumlah item dengan nilai sama (default max_count 1). 
- **match-max-run** — limit run-value sama (mis. maks 3 artis sama, lalu 5 track artis lain = cooldown). `value` kosong = general-match (berlaku per value); `value` terisi = general specific-match (satu nilai tertentu).
- **range-max-run** — limit run numerik range sama (invertible) + cooldown.
- **continuity** — nilai mirip/dilain tracking track sebelumnya (smooth transitions / contrast). `invert` → berbeda jauh.

## Slot Restriction (pembatasan posisi)

Objective bisa hanya berlaku di sebagian posisi output. Slot posisinya **1-indexed**:

| Format | Contoh | Arti |
|---|---|---|
| Tunggal | `1` | posisi 1 saja |
| Range | `1-5` | posisi 1–5 |
| Koma/spasi | `1,3,5` / `1 3 5` | posisi 1, 3, 5 |
| Campuran | `1-3, 7, 10-12` | posisi 1,2,3,7,10,11,12 |
| **Section** | `1/4` | kuarter pertama |
| Campuran section | `1/2, 45-50` | separuh awal + 45–50 |

Section `n/N` membagi playlist limit ke N bagian sama rata (limit tidak habis dibagi → bagian terakhir menyerap sisa). *Pengetahuan kunci:* dua objective sama-tipe tapi berbeda slot → masing-masing **independen** konteks posisi masing-masing. Bisa buat **energy arc** (1/2 ascending, 2/2 descending), buka dengan artis tertentu di slot 1, atau blok genre.

> Slot membatasi *di mana* objective berlaku; kandidat pool tetap utuh.

## Bagaimana MOS Bekerja (algoritma greedy)

Tiap langkah:
1. **Aktifkan objective** yang slot-nya memuat posisi sekarang.
2. **Buang kandidat** yang melanggar objective `unbreakable`.
3. **Skor** setiap kandidat oleh tiap objective weighted; context objectives melihat semua track posisi sebelumnya (atau hanya slot-nya sendiri).
4. **Pilih kandidat dengan total terendah** → tambahkan ke hasil, keluarkan dari pool.
5. Berhenti saat **limit tercapai**, pool habis, atau **tidak ada kandidat lolos unbreakable**.

## Panduan Terbaik (Best Practices resmi)

1. **Mulai sederhana** — 1–2 objective → preview → tambahkan bila ada masalah spesifik.
2. **`unbreakable` jarang** — tiap unbreakable menyempitkan pool; menumpuk unbreakable membuat playlist tidak tercapai (lebih pendek dari limit).
3. **Bobot proporsional** — dua objective setara `high` saling bertarung; utamakan bobot `high` untuk yang paling penting, sisakan `medium/low` untuk sekunder. Yang menentukan adalah **rasio**.
4. **`lowest` untuk tiebreak** — parameter sekunder tulap: popularity `lowest`, misalnya.
5. **Pool besar** — 3–5× pool vs target limit (mis. limit 50 → pool 250+).
6. **Context objective = superpower** — variety/min-separation/order-by/max-match/match-max-run/range-max-run/continuity/distribution melihat isi playlist — tak bisa dengan filter+sort pipeline saja.
7. **`mo_score` = debug** — du preview; kandidat score naik ke akhir artinya pool sudah habis kandidat bagus (longgarkan atau tambah pool).
8. **Combine dengan upstream filter** — buang explicit, batasi genre dulu upstream, MOS menyusun urutan.

## Contoh Kombinasi (dari docs resmi, ringkas)

| Tujuan | Objectives |
|---|---|
| **Party** energy tinggi + varian artis | range energy 0.7–1.0 (high); maximize danceability (high); min-separation artist sep 5 (unbreakable); variety artist (medium) |
| **DJ set** transisi halus | order-by tempo (high); range tempo 115–135 (unbreakable); variety camelot_num inverse (medium); maximize popularity (low) |
| **Discovery mix** deep cut lintas genre | range popularity 5–40 (high); variety mb_genres (high); variety release_year (medium); max-match artist max_count 1 (unbreakable) |
| **Chill fokus** instrumen santai | range energy 0.15–0.45 (unbreakable); range tempo 70–100 (high); maximize instrumentalness (high); minimize speechiness (medium); variety artist (medium) |
| **Balanced sampler** | max-match artist 2 (unbreakable); variety label (medium); variety release_year (low); maximize popularity (lowest = tiebreak) |
| **Gender-balanced** | distribution artist_gender `female(40%) male(40%)` (high); distribution mb_genres `rock(25%) pop(25%) electronic(25%)` (medium); variety artist (high); maximize popularity (lowest) |
| **Energy arc** 50 track | order-by energy (medium, slots 1/2); order-by energy inverse (medium, slots 2/2); min-separation artist 5 (unbreakable) |
| **Anchor/buka-tutup** | match artist "Radiohead" (unbreakable, slots `1`); range energy 0.0–0.3 (unbreakable, slots `50`); variety artist (high); maximize popularity (low) |
| **Genre blocks** | contains mb_genres "rock" (highest, slots 1/2); contains mb_genres "electronic" (highest, slots 2/2); variety artist (high); order-by energy (medium) |
| **Ramp tempo + plateau** | order-by tempo (highest, slots 1-20); range tempo 125–135 (high, slots 21-35); order-by tempo inverse (highest, slots 36-50); variety artist (medium) |
