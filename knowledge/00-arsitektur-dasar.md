# Arsitektur & Konsep Dasar SmarterPlaylists

## 1. Program = Graf Komponen

Sebuah **program** adalah graf node (komponen) terhubung. Aliran data: node **Sources** menghasilkan stream entitas → node lain memfilter/menggabungkannya → hasil akhir jadi playlist Spotify.

- Node dibuat dari **palette di kiri editor**; diklik untuk ditambahkan, atau **drag ke kanvas**.
- **Slot drop cerdas:** drop node ke atas node yang sudah ada → otomatis tersambung (atau dipotong di antaranya); drop ke atas **edge** → node menyisip di tengah sambungan. Edge beranimasi dan node "glow biru" saat target drop valid.
- **Tarik dari aplikasi Spotify desktop:** gayet playlist/album/artis/track langsung ke kanvas → node yang tepat dibuat dan terisi otomatis (beberapa track sekaligus → node *Track URIs*).
- Klik **Layout** (kanan atas) untuk susun otomatis vertikal; **Snap** toggle jendela kisi 20px.

## 2. Main Node (bintang)

Setiap program punya satu **main node** — komponen yang output-nya menjadi hasil akhir program (ditandai ★). Pilih node lalu tekan **Space**. Main node dapat dipindah ke titik mana pun untuk debugging (mis. lihat isi tengah pipeline).

Bintang ≠ halaman elemen terakhir: preview pun berlaku bila main node berada di tengah.

## 3. Run vs. Preview

| Aksi | Efek |
|---|---|
| **Run** | Menjalankan graf, lalu **menyimpan hasil ke playlist Spotify dengan nama sama dengan program**. Run pertama → playlist baru dibuat; run berikutnya → playlist yang sama diperbarui. |
| **Preview** | Menjalankan graf dan menampilkan hasil (kolom attribute lengkap, termasuk audio features), **tanpa** menyimpan apa pun. Ideal untuk uji coba & debug. |

**Rahasia penting:** Tidak perlu node *Save to Playlist* di akhir program — penyimpanan otomatis. Menambahkannya bikin 2 playlist per run (playlist otomatis + playlist komponen yang kamu namai sendiri) — ini #1 sumber kebingungan pengguna. *Save to Playlist* hanya diperlukan untuk **cabang samping** (side branch), mis. menyimpan hasil tahap menengah ke playlist terpisah.

## 4. Entitas & Warna Edge

v3.10+ mendukung tiga **tipe entitas** yang mengalir di graf:

| Entitas | Warna / Gaya edge | Sumber contoh |
|---|---|---|
| **Track** | garis hijau solid | Playlist, My Saved Tracks, Artist Radio |
| **Artist** | garis ungu (violet) putus-putus | My Top Artists, My Artist Library |
| **Album** | garis teal putus-putus | My Album Library, Label Albums |

- Editor **tolak koneksi tipe tak valid** (mis. source artis → filter *Danceable* yang track-only). Validasi memeriksa rantai ke bawah.
- Banyak node bersifat **polimorfik (generic)**: Range Filter, Match Filter, Sort, Shuffler, DeDup, Sample, First, Last, dll. — dropdown attribute berubah otomatis sesuai tipe input.
- Preview panel menyesuaikan kolom sesuai tipe entitas; **Run tetap mensyaratkan output track** (preview boleh non-track untuk debug).

Untuk berpindah tipe, gunakan **Adapters** (To Tracks / To Artists / To Albums / Similar Artists).

## 5. Input Ports & Warna

Setiap node mendefinisikan port sendiri (deskripsi muncul saat hover):

- `green` — input utama (umumnya multi-input 100)
- `red` — daftar **exclusion tracks** (mis. Track Filter, Artist Filter, Mixer) — juga dipakai sebagai input kedua pada Combiner dua-stream (MixIn, Is Weekend)
- `orange` — daftar **exclusion artists** (Mixer, Artist Filter)
- Port kondisional: hijau = ketika kondisi benar, merah = ketika salah.

Fan-out valid: satu output boleh ke banyak node downstream, bagus untuk memproses alur yang sama lewat 2 rantai berbeda lalu digabung lagi.

## 6. Parameter & Caching

- **Double-click node** untuk mengedit parameter.
- Beberapa source punya `cache_mode` (auto / no-cache / short-term daily / long-term weekly) — untuk efek segar saat schdule.
- Beberapa source punya `alias` — label kustom penting saat memakai objective **source-based** di MOS/distribution.

### Variabel dinamis pada deskripsi playlist ( kotak deskripsi di Save komponen / program):

`${DATE}`, `${TIME}`, `${PROGRAM_NAME}`, `${PROGRAM_DESCRIPTION}`, `${AUTO_PROGRAM_DESCRIPTION}` (auto-ringkasan dataflow), `${PLAYLIST_NAME}`, `${NUM_TRACKS}`, `${NUM_ARTISTS}`, `${USER}`, `${DAY-OF-WEEK}`, `${UPDATE_SCHEDULE}`, `${DURATION}` — cukup campur dengan teks bebas. Batas Spotify: 300 karakter deskripsi.

## 7. Scheduling (playlist yang memperbarui dirinya)

1. Buat & simpan program, pastikan **Run pertama sukses**.
2. Di halaman **Programs**, klik kolom **Schedule**.
3. Pilih interval: **hourly / daily / weekly** dan **total runs** (maks 100 kali).
4. Program jalan otomatis; gagal **3x berturut-turut** → jadwal otomatis pause.

Kandidat terbaik untuk scheduling: discovery playlist, conditional playlist (berubah perilaku mingguan), Relative Dated Playlist (reaksi playlist yang di-follow).

## 8. Sharing / Discover

- **Share → Publish** → link publik ke **versi live** (edit diterus ke pengunjung).
- Pengunjung login bisa **Preview** (run dengan Spotify-nya sendiri, hasilnya playlist di akun mereka) atau **Import** (salinan independen).
- *Make discoverable* → muncul di halaman **Discover** berbagi program komunitas.
- Ada **Import tab** untuk memigrasi program versi lama (komponen DeprecatedSource menandai komponen EchoNest yang tak ada lagi).

## 9. Shortcut Keyboard

| Shortcut | Aksi |
|---|---|
| Double-click | Edit parameter node |
| Space | Jadikan node terpilih main (★) |
| Delete / Backspace | Hapus node terpilih |
| Shift+Delete | **Splice-out** node dari rantai (auto-reconnect) |
| Ctrl+C / Ctrl+V | Copy/paste node (edge antar-copied ikut; pastenya offset) |
| Ctrl+Click | Tambah node ke seleksi |
| Drag kanvas | Selection rectangle |

## 10. Mode tema

Icon tema di header bersiklus System → Light → Dark.

## 11. Statistik & debug

Halaman **Programs** menampilkan riwayat run per program. Run tercatat bersama: jumlah **API call per komponen**, jumlah track mengalir per node, cache hits, waktu menunggu API — bagus untuk menemukan bottleneck (mis. Alternate yang banyak skip karena dedup, atau API menunggu panjang di node source).
