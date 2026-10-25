# Conditionals - Percabangan

> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total 4 komponen dalam kategori ini.

Komponen kondisional memilih salah satu dari dua input berdasarkan kondisi waktu/jadwal - untuk playlist yang berubah perilaku, misalnya minggu vs. akhir minggu.

### IsWeekend

**Label UI:** `Is Weekend?` | **Output:** track | **Judul tampilan node:** `is weekend?`

Route items based on whether today is a weekend

**Port input:**

- Port `green` - maks 1 (generic: track/artist/album) - Tracks to use on weekends
- Port `red` - maks 1 (generic: track/artist/album) - Tracks to use on weekdays

**Parameter:**


**Dokumentasi resmi (help):**

This component accepts a green and a red stream. If the current day is a weekend, tracks from the green stream are passed through; otherwise tracks from the red stream are passed through.

---

### YesNo

**Label UI:** `Yes or No` | **Output:** track | **Judul tampilan node:** `yes/no`

Select a stream based on a boolean

**Port input:**

- Port `green` - maks 1 (generic: track/artist/album) - Tracks when yes
- Port `red` - maks 1 (generic: track/artist/album) - Tracks when no

**Parameter:**

- **Yes** - tipe: boolean, default: `true`. If true, use the green stream; otherwise use the red stream

**Dokumentasi resmi (help):**

This component accepts a green and a red input stream. If 'yes' is set, tracks from the green stream are passed through; otherwise tracks from the red stream are passed through.

---

### IsDayOfWeek

**Label UI:** `Is Day of Week` | **Output:** track | **Judul tampilan node:** `is $day?`

Route items based on the current day of the week

**Port input:**

- Port `green` - maks 1 (generic: track/artist/album) - Tracks when day matches
- Port `red` - maks 1 (generic: track/artist/album) - Tracks when day doesn't match

**Parameter:**

- **day** - tipe: , default: `Monday`. Day of the week

**Dokumentasi resmi (help):**

This component accepts a green and a red stream. If today matches the specified day, tracks from the green stream are passed through; otherwise tracks from the red stream are passed through.

---

### DateRange

**Label UI:** `Date Range` | **Output:** track | **Judul tampilan node:** `$start_month $start_day to $end_month $end_day`

Route items based on whether today falls within a date range

**Port input:**

- Port `green` - maks 4 (generic: track/artist/album) - Tracks when in range
- Port `red` - maks 4 (generic: track/artist/album) - Tracks when out of range

**Parameter:**

- **start_month** - tipe: , default: `January`. Start month
- **Start Day** - tipe: integer, default: `1` (rentang: min 1; max 31). Start day (1-31)
- **end_month** - tipe: , default: `December`. End month
- **End Day** - tipe: integer, default: `31` (rentang: min 1; max 31). End day (1-31)

**Dokumentasi resmi (help):**

This component accepts a green and a red stream. If today's date falls within the specified range, tracks from the green stream are passed through; otherwise tracks from the red stream are passed through. Handles ranges that wrap around year boundaries (e.g. Dec 1 – Jan 31).

---

