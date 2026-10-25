# Outputs - Penyimpanan

> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total 2 komponen dalam kategori ini.

Kecuali pada kasus khusus, TIDAK perlu menaruh komponen output di akhir program: run apa pun otomatis menyimpan hasil ke playlist Spotify bernama sama dengan program. Output digunakan hanya untuk menyimpan cabang samping ke playlist lain.

### PlaylistSave

**Label UI:** `Save to Playlist` | **Output:** track | **Judul tampilan node:** `Save to $playlist_name`

Save tracks to a Spotify playlist

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Resolusi URI:** field `playlist_uri`, entitas `playlist`; pencarian nama: playlist_name -> `name`

**Parameter:**

- **Playlist Name** - tipe: string, default: `My Smarter Playlist`. Name for the playlist
- **Playlist Uri** - tipe: string. URI or URL of an existing Spotify playlist. Leave blank to create a new one automatically.
- **Append** - tipe: boolean, default: `false`. Append tracks instead of replacing
- **Trim Mode** - tipe: string, default: `none`. Nilai: `none, max_tracks, max_age_days`. Playlist management: cap total tracks or remove old tracks (only when appending)
- **Trim Value** - tipe: integer, default: `0` (rentang: min 0). Max track count (max_tracks) or max age in days (max_age_days)
- **Auto Reset** - tipe: string, default: `never`. Nilai: `never, weekly, monthly`. Periodically clear the playlist before appending (only when appending)
- **Reset Value** - tipe: integer, default: `0` (rentang: min 0; max 31). Day of week for weekly (0=Mon, 6=Sun), or day of month for monthly (1-31)
- **No Dups** - tipe: boolean, default: `false`. Skip tracks already in the playlist (append mode) or deduplicate incoming tracks (replace mode)
- **Description** - tipe: string, default: `Created by SmarterPlaylists`. Playlist description written to Spotify. Supports variables: ${DATE}, ${TIME}, ${PROGRAM_NAME}, ${PROGRAM_DESCRIPTION}, ${AUTO_PROGRAM_DESCRIPTION}, ${NUM_TRACKS}, ${NUM_ARTISTS}, ${USER}, ${DAY-OF-WEEK}, ${UPDATE_SCHEDULE}, ${DURATION}, ${PLAYLIST_NAME}. See the FAQ for details.

**Dokumentasi resmi (help):**

Saves tracks to a Spotify playlist. Give it a name and it will create the playlist on the first run, then update the same playlist on every run after that — no duplicates.

You can also point it at an existing playlist by pasting in a Spotify URI or URL (leave the URI blank to create a new one automatically). Turn on 'append' to add tracks to the playlist instead of replacing them — great for building up an archive over time (e.g. saving each week's Discover Weekly into one big playlist).

If you change the playlist name, a new playlist will be created with the new name on the next run.

When appending, you can set a trim mode to automatically manage playlist size. 'max_tracks' caps the playlist at N total tracks by removing the oldest when exceeded. 'max_age_days' removes any tracks added more than N days ago before appending new ones.

You can also set an auto-reset schedule to periodically clear the playlist and start fresh. Choose 'weekly' (reset on a given day, 0=Monday through 6=Sunday) or 'monthly' (reset on a given day of the month). On reset days, the playlist is replaced instead of appended to; on other days it appends normally.

The description field is written to the Spotify playlist and supports template variables like ${DATE} and ${NUM_TRACKS}. See the FAQ for the full list.

Turn on 'no duplicates' to prevent the same track from being added twice. In append mode, incoming tracks are checked against the tracks already in the playlist and any duplicates are skipped — great for archiving playlists like Daily Mix without accumulating repeats. In replace mode it just removes duplicates from the incoming tracks.

If this is your program's main output (the starred component), it replaces the automatic save, so you won't get duplicate playlists.

---

### PlaylistSaveToNew

**Label UI:** `Save to New Playlist` | **Output:** track | **Judul tampilan node:** `$playlist_name`

Save tracks to a new playlist with an auto-generated suffix

**Port input:**

- Port `green` - multi-input (tipe: track) - The source of tracks

**Parameter:**

- **Playlist Name** - tipe: string, default: `My Smarter Playlist`. Base name for the playlist
- **Suffix Type** - tipe: string, default: `time`. Nilai: `none, time, date, day-of-week, day-of-month`. Type of suffix to append
- **Description** - tipe: string, default: `Created by SmarterPlaylists`. Playlist description written to Spotify. Supports variables: ${DATE}, ${TIME}, ${PROGRAM_NAME}, ${PROGRAM_DESCRIPTION}, ${AUTO_PROGRAM_DESCRIPTION}, ${NUM_TRACKS}, ${NUM_ARTISTS}, ${USER}, ${DAY-OF-WEEK}, ${UPDATE_SCHEDULE}, ${DURATION}, ${PLAYLIST_NAME}. See the FAQ for details.

**Dokumentasi resmi (help):**

Creates a new playlist each time it runs, with a suffix appended to the name based on the selected type: time (HH:MM), date (YYYY-MM-DD), day-of-week (Monday, etc.), day-of-month (1-31), or none.

The description field is written to the Spotify playlist and supports template variables like ${DATE} and ${NUM_TRACKS}. See the FAQ for the full list.

If used as your program's main output (the starred component), it replaces the automatic save — no duplicate playlists.

---

