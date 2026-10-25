# Attribute Entitas (Track / Artist / Album)

> Sumber: FAQ resmi aplikasi (tabel attribute) + metadata `x-attribute-meta` dari `/api/inventory` v3.12.3. Attribute ini dipakai di Range Filter, Match Filter, Sort, Genre Filter, MOS objective, dsb. Dropdown komponen generic menyesuaikan daftar attribute dengan tipe entitas input.

## Track Attributes

| Attribute | Tipe | Rentang | Definisi |
|---|---|---|---|
| `acousticness` | number | 0.0–1.0 | Confidence track ini akustik. 1.0 = sangat yakin akustik. |
| `album` | text | – | Nama album. |
| `album_popularity` | number | 0–100 | Skor popularitas album di Spotify. |
| `album_release_date` | date | – | Tanggal rilis album (YYYY-MM-DD). |
| `album_type` | text | – | `album` / `single` / `compilation` (berguna memfilter single). |
| `artist` | text | – | Nama artis utama. |
| `artist_area` | text | – | Area MusicBrainz: kota/region/negara asal artis. |
| `artist_country` | text | – | Kode ISO negara asal: US, GB, JP, DE, ID, ... (untuk Country Filter/Gender). |
| `artist_end_year` | number | – | Tahun artis berhenti aktif (kosong bila masih aktif). |
| `artist_followers` | number | 0+ | Jumlah follower Spotify artis utama. |
| `artist_gender` | text | – | male / female / mixed / instrumental / other / unknown (MusicBrainz) — dipakai Gender Filter & Distribution MOS. |
| `artist_popularity` | number | 0–100 | Popularitas artis di Spotify. |
| `artist_start_year` | number | – | Tahun awal aktivitas artis (MusicBrainz). |
| `artist_type` | text | – | person / group / orchestra / choir / character / other (MusicBrainz). |
| `camelot` | text | 8B, 5A | Kode roda Camelot (DJ key matching). Adjacent code = key kompatibel. |
| `camelot_num` | number | 1–24 | Posisi roda Camelot numerik (wrap-around kompatibel). |
| `danceability` | number | 0.0–1.0 | Kelayakan untuk menari berdasarkan tempo, ritme, beat strength. |
| `disc_number` | number | 1+ | Nomor disc (album multi-disc). |
| `duration_ms` | number | 0+ | Durasi ms (3 menit = 180000); berganti-swap gunakan `ShorterThan` selector untuk batas durasi total. |
| `energy` | number | 0.0–1.0 | Intensitas persepsi: death metal tinggi, Bach rendah. |
| `explicit` | boolean | true/false | Penanda explicit Spotify (gunakan node **Explicit** filter). |
| `followers` | number | 0+ | Follower utama entitas. |
| `instrumentalness` | number | 0.0–1.0 | >0.5 kemungkinan besar instrumental; "ooh/aah" dianggap instrumental. |
| `is_active` | boolean | true/false | Artis masih aktif (tidak punya end date di MB). |
| `key` | number | 0–11 | 0=C, 1=C#, 2=D, 3=D#, 4=E, 5=F, 6=F#, 7=G, 8=G#, 9=A, 10=A#, 11=B. |
| `label` | text | – | Label penerbit (dipakai Label Albums & sort by label). |
| `liveness` | number | 0.0–1.0 | Probabilitas track live (>0.8 → live). |
| `loudness` | number | -60..5 | Loudness rata-rata dB (umum -30..0) untuk volume normalizing. |
| `mb_genres` | text list | – | Genre MusicBrainz artis utama: rock / electronic / jazz — dipakai Genre Filter. |
| `mo_score` | number | 0.0–1.0 | Skor hasil MOS (0 = fit sempurna); hanya ada pada track keluaran MOS. |
| `mode` | number | 0 / 1 | 0 = minor, 1 = major. |
| `name` | text | – | Judul track. |
| `popularity` | number | 0–100 | Popularitas Spotify track (100 = salah satu paling didengar). |
| `random` | number | 0.0–1.0 | Nilai acak regenerate tiap run — trik MOS untuk variasi acak objective. |
| `release_date` | date | – | Tanggal rilis track dari album. |
| `release_decade` | number | 1900–2030 | Dekade rilis (1970, 1980, ...). |
| `release_year` | number | 1900–2030 | Tahun rilis. |
| `speechiness` | number | 0.0–1.0 | >0.66 semua speech (podcast); 0.33–0.66 rap/mix; <0.33 musik. |
| `source_count` | number | 1+ | Berapa kali entitas muncul di stream sumber (sejak 3.10; untuk threshold frekuensi). |
| `tempo` | number | 0–500 BPM | Tempo menit per beat (pop biasanya 90–150 BPM). |
| `time_signature` | number | 3–7 | 4 = 4/4, 3 = waltz 3/4. |
| `track_number` | number | 1+ | Posisi track di album. |
| `total_tracks` | number | 1–500 | Jumlah track di album. |
| `uri` | text | – | `spotify:track:...` — cocok untuk Max Match dedup per URI. |
| `valence` | number | 0.0–1.0 | "Positiveness" musik: tinggi ceria, rendah sedih/gelap. |

## Artist Attributes (entitas artist)

| Attribute | Tipe | Rentang | Definisi |
|---|---|---|---|
| `name` | text | – | Nama artis. |
| `popularity` | number | 0–100 | Popularitas Spotify artis. |
| `followers` | number | 0+ | Follower Spotify. |
| `genres` | text list | – | Genre Spotify ("indie rock", ...). |
| `artist_gender` | text | – | male / female / mixed / instrumental / other / unknown. |
| `artist_type` | text | – | person / group / orchestra / ... |
| `artist_country` | text | – | ISO kode negara asal. |
| `artist_area` | text | – | Area MusicBrainz (bisa kota / region / negara). |
| `artist_start_year` | number | – | Tahun mulai aktif. |
| `artist_end_year` | number | – | Tahun berhenti; kosong bila aktif. |
| `is_active` | boolean | true/false | Masih aktif? |
| `mb_genres` | text list | – | Genre MusicBrainz. |
| `source_count` | number | 1+ | Berapa kali artis muncul di stream sumber (mis. jumlah ketika To Artists dari track count). |
| `uri` | text | – | `spotify:artist:...` |

## Album Attributes (entitas album)

| Attribute | Tipe | Rentang | Definisi |
|---|---|---|---|
| `name` | text | – | Judul album. |
| `artist` | text | – | Nama artis utama album. |
| `popularity` | number | 0–100 | Popularitas album. |
| `release_date` | date | – | Tanggal rilis. |
| `label` | text | – | Label. |
| `total_tracks` | number | 1+ | Jumlah track. |
| `album_type` | text | – | album / single / compilation. |
| `source_count` | number | 1+ | Berapa kali album muncul di stream sumber. |
| `uri` | text | – | `spotify:album:...` |

## Catatan penting memilih attribute

- **Versi 3.12.3**: `source_count` baru untuk artist/album (fitur frequency thresholding).
- `random` dipakai di **MOS objective** untuk ketidakpastian acak per-run.
- `mo_score` dipakai downstream untuk menghapus "result compromise" — mis. Range Filter `mo_score` > `0.4`.
- `is_active` berguna: `artist_end_year` tidak boleh artis yang sudah bubar.
- `label` as text dipakai di `Label Albums` source (pencarian nama) dan pada MOS **variety/label**.
- Genre: `genre` dari Spotify vs `mb_genres` dari MusicBrainz — Genre Filter default ke mb_genres; ada opsi `primary genre only` (v3.11) untuk menghindari false-positive genre granular.
