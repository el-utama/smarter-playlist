# Node: Multi-Objective Sequencer (MOS)

> Sebagian besar penjelasan konsep ada di ``10-mos.md``; file ini adalah **referensi teknis 14 objective** yang dikonfigurasi di dalam node, langsung dari ``/api/objectives`` (v3.12.3).

Skema umum semua objective:

- **field** - attribute numerik/teks/list yang dipakai (daftar attribute untuk track ada di ``09-attributes.md``)
- **weight** - ``off | lowest | low | medium | high | highest | unbreakable`` (bila ``allow_unbreakable``: true)
- Beberapa objective punya slot ``1-5``, ``3/8`` dsb. (posisi 1-indexed) untuk membatasi posisi berlaku

Tabel ringkasan:

| Objective |Deskripsi singkat |unbreakable|
|---|---|---|
| `maximize` | Prefer tracks with higher values for the given attribute | tidak |
| `minimize` | Prefer tracks with lower values for the given attribute | tidak |
| `range` | Prefer tracks with attribute values within the given range | ya |
| `target` | Prefer tracks closest to a target value for the given attribute | tidak |
| `match` | Prefer tracks that match a given value for the given attribute | ya |
| `contains` | Prefer tracks where the attribute contains the given value (substring or membership) | ya |
| `max-match` | Limit how many tracks can share the same value for a given attribute | ya |
| `order-by` | Prefer tracks that continue in ascending (or descending) order by an attribute | tidak |
| `min-separation` | Ensure tracks sharing the same value for a field are spaced apart | ya |
| `match-max-run` | Limit consecutive runs of tracks matching a value, with a mandatory separation gap after hitting the max | ya |
| `range-max-run` | Limit consecutive runs of tracks with attribute values in a numeric range, with a mandatory separation gap | ya |
| `variety` | Maximize diversity of an attribute across the playlist | ya |
| `continuity` | Score candidates by distance from the last selected track's attribute value | ya |
| `distribution` | Target a desired percentage distribution of attribute values. Use value(%) syntax, e.g. 'female(30%) male(50%)' or '1970-1979(20%) 1980-1989(30%)' | tidak |

---

## Detail parameter per objective

### `maximize`

Maximize: Prefer tracks with higher values for the given attribute

- **Field** `field` - string, default: `popularity`. Nilai: `acousticness, album_popularity, artist_end_year, artist_followers, artist_popularity, artist_start_year, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, liveness, loudness, mode, popularity, random, release_decade, release_year, speechiness, tempo, time_signature, track_number, valence`. The attribute to maximize
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: tidak (objective ini ranking, gunakan berat ``highest``)

### `minimize`

Minimize: Prefer tracks with lower values for the given attribute

- **Field** `field` - string, default: `popularity`. Nilai: `acousticness, album_popularity, artist_end_year, artist_followers, artist_popularity, artist_start_year, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, liveness, loudness, mode, popularity, random, release_decade, release_year, speechiness, tempo, time_signature, track_number, valence`. The attribute to minimize
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: tidak (objective ini ranking, gunakan berat ``highest``)

### `range`

In Range: Prefer tracks with attribute values within the given range

- **Field** `field` - string, default: `popularity`. Nilai: `acousticness, album_popularity, artist_end_year, artist_followers, artist_popularity, artist_start_year, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, liveness, loudness, mode, popularity, random, release_decade, release_year, speechiness, tempo, time_signature, track_number, valence`. The attribute to check
- **Min Val** `min_val` - number, default: `0`. Minimum desired value (inclusive)
- **Max Val** `max_val` - number, default: `100`. Maximum desired value (inclusive)
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `target`

Target: Prefer tracks closest to a target value for the given attribute

- **Field** `field` - string, default: `popularity`. Nilai: `acousticness, album_popularity, artist_end_year, artist_followers, artist_popularity, artist_start_year, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, liveness, loudness, mode, popularity, random, release_decade, release_year, speechiness, tempo, time_signature, track_number, valence`. The attribute to target
- **Target** `target` - number, default: `50`. The desired target value
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: tidak (objective ini ranking, gunakan berat ``highest``)

### `match`

Match: Prefer tracks that match a given value for the given attribute

- **Field** `field` - string, default: `artist`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to match on
- **Value** `value` - string. The value to match
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `contains`

Contains: Prefer tracks where the attribute contains the given value (substring or membership)

- **Field** `field` - string, default: `artist`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to check
- **Value** `value` - string. The value to look for
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `max-match`

Max Match: Limit how many tracks can share the same value for a given attribute

- **Field** `field` - string, default: `artist`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to limit
- **Max Count** `max_count` - integer, default: `1`. Maximum allowed tracks with the same value
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `order-by`

Order By: Prefer tracks that continue in ascending (or descending) order by an attribute

- **Field** `field` - string, default: `popularity`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to order by
- **Inverse** `inverse` - boolean, default: `false`. If true, prefer descending order instead
- **Spread** `spread` - string, default: `full`. Nilai: `off, full, segment`. off=sequential, full=span full range, segment=each slot segment spans full range
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: tidak (objective ini ranking, gunakan berat ``highest``)

### `min-separation`

Minimum Separation: Ensure tracks sharing the same value for a field are spaced apart

- **Field** `field` - string, default: `artist`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to enforce separation on
- **Separation** `separation` - integer, default: `5`. Minimum number of tracks between same values
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `match-max-run`

Match Max Run: Limit consecutive runs of tracks matching a value, with a mandatory separation gap after hitting the max

- **Field** `field` - string, default: `artist`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to check
- **Value** `value` - string. Specific value to match (empty = any repeated value)
- **Max Run** `max_run` - integer, default: `3`. Maximum consecutive matching tracks
- **Separation** `separation` - integer, default: `5`. Required non-matching tracks after a maxed run
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `range-max-run`

Range Max Run: Limit consecutive runs of tracks with attribute values in a numeric range, with a mandatory separation gap

- **Field** `field` - string, default: `popularity`. Nilai: `acousticness, album_popularity, artist_end_year, artist_followers, artist_popularity, artist_start_year, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, liveness, loudness, mode, popularity, random, release_decade, release_year, speechiness, tempo, time_signature, track_number, valence`. The numeric attribute to check
- **Low** `low` - number, default: `0`. Lower bound of range (inclusive)
- **High** `high` - number, default: `100`. Upper bound of range (inclusive)
- **Invert** `invert` - boolean, default: `false`. If true, match values outside the range instead
- **Max Run** `max_run` - integer, default: `3`. Maximum consecutive matching tracks
- **Separation** `separation` - integer, default: `5`. Required non-matching tracks after a maxed run
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `variety`

Variety: Maximize diversity of an attribute across the playlist

- **Field** `field` - string, default: `artist`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to diversify
- **Inverse** `inverse` - boolean, default: `false`. If true, prefer similarity instead of variety
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `continuity`

Continuity: Score candidates by distance from the last selected track's attribute value

- **Field** `field` - string, default: `energy`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to measure continuity on
- **Invert** `invert` - boolean, default: `false`. If true, prefer tracks furthest from the last track
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: ya

### `distribution`

Distribution: Target a desired percentage distribution of attribute values. Use value(%) syntax, e.g. 'female(30%) male(50%)' or '1970-1979(20%) 1980-1989(30%)'

- **Field** `field` - string, default: `artist_gender`. Nilai: `acousticness, album, album_popularity, album_release_date, artist, artist_area, artist_country, artist_end_year, artist_followers, artist_gender, artist_popularity, artist_start_year, artist_type, camelot, camelot_num, danceability, disc_number, duration_ms, energy, explicit, instrumentalness, key, label, liveness, loudness, mb_genres, mode, name, popularity, random, release_date, release_decade, release_year, source, speechiness, tempo, time_signature, track_number, uri, valence`. The attribute to control distribution for
- **Values** `values` - string. Space-separated value(%) pairs. Examples: 'female(30%) male(50%)', '1970-1979(20%)', 'rock(20%) jazz(20%)'. Numeric ranges use lo-hi syntax. Text values match exactly (or by list membership for list fields).
- **Weight** `weight` - string, default: `medium`. Nilai: `off, lowest, low, medium, high, highest, unbreakable`. How important this objective is

Bisa `unbreakable`: tidak (objective ini ranking, gunakan berat ``highest``)

