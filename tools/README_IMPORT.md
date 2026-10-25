# Import & Run 120 Playlist (tanpa login berulang)

Dua script baru ini memungkinkan kamu mengimpor dan menjalankan semua program
SmarterPlaylights dengan **login Spotify hanya sekali**.

## Prasyarat

1. Pastikan 120 program generator sudah di-generate:
   ```powershell
   python tools/generate_programs.py --mode all --clean
   python tools/validate_programs.py
   ```
2. (Sebaiknya) Perbaiki dulu URI pool yang rusak — lihat bagian "Perbaikan wajib" di bawah.

## Langkah 1 — Login sekali

```powershell
python tools/sm_session.py --init
```

- Browser default akan terbuka ke `smarterplaylists.playlistmachinery.com/api/auth/login`.
- Ini akan redirect ke Spotify. **Login ke Spotify dan klik "Izinkan"** untuk
  mengizinkan aplikasi SmarterPlaylights.
- Setelah authorize selesai, Spotify akan redirect **KEMBALI** ke smarterplaylights.
- Tunggu sampai alamat browser kembali ke `smarterplaylists.playlistmachinery.com`.
- Buka **DevTools (F12) > Application > Cookies >**
  `smarterplaylists.playlistmachinery.com`.
- **Copy cookie SESI** (bukan `sp_*` dari open.spotify.com), format:
  `name=value; name2=value2`, paste ke terminal.
- Sesi disimpan ke `auth/session.json`. Script berikutnya akan reuse-nya tanpa
  login lagi sampai session expired.

Cek apakah session masih valid:
```powershell
python tools/sm_session.py --check
```

Hapus session (paksa login ulang):
```powershell
python tools/sm_session.py --logout
```

## Langkah 2 — Impor dan jalankan semua program

Impor 21 pool + 120 generator ke SmarterPlaylights, lalu run satu per satu:

```powershell
python tools/import_run_all.py
```

Opsi yang berguna:

| Opsi | Efek |
|------|------|
| `--import-only` | Hanya impor program, tidak run |
| `--run-only` | Hanya run program yang sudah diimpor sebelumnya |
| `--limit 10` | Proses paling banyak 10 generator (untuk coba-coba dulu) |
| `--delay 3` | Jeda detik antar run (default 2) |
| `--pools-only` | Hanya 21 pool |
| `--gens-only` | Hanya 120 generator |
| `--no-save` | Preview run tanpa menyimpan ke Spotify |

Hasil disimpan ke:
- `config/import_run_log.csv` — satu baris per program
- `config/import_run_log.json` — detail lengkap

## Perbaikan wajib sebelum impor

Audit menemukan **satu URI pool invalid** (hanya 19 karakter, seharusnya 22):

```
config/pool_uris.json  →  POOL Afternoon - Singer-Songwriter
  spotify:playlist:4fn1jCiQbaufmiEvL_S   ← invalid (19 chars)
```

Hal ini memengaruhi 6 generator (Afternoon 25–30). Sebelum impor:
1. Buka Spotify, buka playlist pool `POOL Afternoon - Singer-Songwriter` yang benar.
2. Copy URI-nya (harus 22 karakter alfanumerik setelah `spotify:playlist:`).
3. Edit `config/pool_uris.json`, ganti nilai baris 17.
4. Jalankan `python tools/build_config.py` agar `pool_manifest.json` dan
   `playlists_120.draft.json` ikut terupdate, lalu
   `python tools/generate_programs.py --mode all --clean` untuk regenerate
   generator JSON dengan URI yang benar.

## Catatan

- Program yang sudah ada di SmarterPlaylights (berdasarkan nama) akan di-**update**, tidak dibuat duplikat.
- Setiap program di-run dengan `save=true`, sehingga run pertama membuat playlist Spotify baru dan run berikutnya menimpanya (tidak ada duplikat playlist).
- 141 program (21 pool + 120 generator) run satu per satu; dengan delay 2 detik butuh waktu sekitar 5–8 menit. Gunakan `--limit` untuk mencoba subset dulu.
- Jika session expired di tengah jalan, API akan mengembalikan 401. Jalankan lagi `python tools/sm_session.py --init` lalu `python tools/import_run_all.py --run-only` untuk melanjutkan.
