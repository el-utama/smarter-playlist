# Rencana 120 Playlist

> Dokumen ini dihasilkan dari `config/playlists_120.draft.json`. Taxonomy sudah disetujui (2026-10-24). Judul dan deskripsi playlist memakai bahasa Inggris. Belum ada playlist atau program yang dibuat/diimpor/dijalankan.

## Ringkasan

| Item | Nilai |
|---|---|
| Kategori | 4 |
| Genre | 20 |
| Mood | 24 |
| Playlist | 120 |
| Pool | 21 |
| Batas durasi | 6 jam (21.600 detik) |
| Rotasi | 60% priority / 40% global |
| Priority artist | 26 (25 No Detours + eL Utama) |
| Bahasa judul & deskripsi | English (marketable, professional) |

## Format judul & deskripsi

- **Judul:** `{Category} {index:02d} — {Genre} · {Mood}` — contoh: `Morning 01 — Acoustic & Folk · Fresh`.
- **Deskripsi:** category intro + mood/genre + artist-first picks + `Refreshed regularly.` Variable `${NUM_TRACKS}` dan `${DURATION}` diisi otomatis oleh SmarterPlaylists.

| Kategori | Contoh judul | Contoh deskripsi |
|---|---|---|
| Morning | Morning 01 — Acoustic & Folk · Fresh | Start your morning with a fresh acoustic & folk mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}. |
| Midday | Midday 01 — Pop · Upbeat | Power through midday with an upbeat pop mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}. |
| Afternoon | Afternoon 01 — Indie & Alternative · Mellow | Soundtrack your afternoon with a mellow indie & alternative mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}. |
| Night | Night 01 — Ambient & Electronic · Sleepy | Unwind into the night with a sleepy ambient & electronic mix. Artist-first picks and new discoveries, sequenced for a smooth flow. Refreshed regularly. ${NUM_TRACKS} tracks · ${DURATION}. |

## 21 Pool

| Pool | Tipe | Kategori | Genre | Hard filter | Artist genre | Explicit | URI |
|---|---|---|---|---|---|---|---|
| POOL Priority | priority | Priority |  | (off) | - | allow | placeholder |
| POOL Morning - Acoustic & Folk | genre | Morning | Acoustic & Folk | folk | folk | clean | placeholder |
| POOL Morning - Indie Pop | genre | Morning | Indie Pop | indie pop | indie pop | clean | placeholder |
| POOL Morning - Jazz & Soul | genre | Morning | Jazz & Soul | jazz | jazz | clean | placeholder |
| POOL Morning - Classical & Piano | genre | Morning | Classical & Piano | classical | classical | clean | placeholder |
| POOL Morning - Lo-Fi & Chillhop | genre | Morning | Lo-Fi & Chillhop | (off) | lo-fi | clean | placeholder |
| POOL Midday - Pop | genre | Midday | Pop | pop | pop | clean | placeholder |
| POOL Midday - Dance & Electronic | genre | Midday | Dance & Electronic | electronic | electronic | clean | placeholder |
| POOL Midday - Hip-Hop & R&B | genre | Midday | Hip-Hop & R&B | hip hop | hip hop | clean | placeholder |
| POOL Midday - Rock & Alternative | genre | Midday | Rock & Alternative | rock | rock | clean | placeholder |
| POOL Midday - Funk & Groove | genre | Midday | Funk & Groove | funk | funk | clean | placeholder |
| POOL Afternoon - Indie & Alternative | genre | Afternoon | Indie & Alternative | indie | indie | allow | placeholder |
| POOL Afternoon - Soul & R&B | genre | Afternoon | Soul & R&B | soul | soul | allow | placeholder |
| POOL Afternoon - Jazz & Blues | genre | Afternoon | Jazz & Blues | jazz | jazz | allow | placeholder |
| POOL Afternoon - Chillout & Downtempo | genre | Afternoon | Chillout & Downtempo | downtempo | downtempo | allow | placeholder |
| POOL Afternoon - Singer-Songwriter | genre | Afternoon | Singer-Songwriter | singer-songwriter | singer-songwriter | allow | placeholder |
| POOL Night - Ambient & Electronic | genre | Night | Ambient & Electronic | ambient | ambient | allow | placeholder |
| POOL Night - Lo-Fi & Chillhop | genre | Night | Lo-Fi & Chillhop | (off) | lo-fi | allow | placeholder |
| POOL Night - Piano & Classical | genre | Night | Piano & Classical | classical | classical | allow | placeholder |
| POOL Night - Dream Pop & Shoegaze | genre | Night | Dream Pop & Shoegaze | (off) | dream pop | allow | placeholder |
| POOL Night - R&B & Soul | genre | Night | R&B & Soul | soul | soul | allow | placeholder |

## Morning — 30 Playlist

| No | Nama | Genre | Mood | Explicit | Priority offset | Global offset |
|---|---|---|---|---|---|---|
| 01 | Morning 01 — Acoustic & Folk · Fresh | Acoustic & Folk | Fresh | clean | 0 | 0 |
| 02 | Morning 02 — Acoustic & Folk · Calm | Acoustic & Folk | Calm | clean | 200 | 300 |
| 03 | Morning 03 — Acoustic & Folk · Hopeful | Acoustic & Folk | Hopeful | clean | 400 | 600 |
| 04 | Morning 04 — Acoustic & Folk · Warm | Acoustic & Folk | Warm | clean | 600 | 900 |
| 05 | Morning 05 — Acoustic & Folk · Focused | Acoustic & Folk | Focused | clean | 800 | 1200 |
| 06 | Morning 06 — Acoustic & Folk · Gentle | Acoustic & Folk | Gentle | clean | 1000 | 1500 |
| 07 | Morning 07 — Indie Pop · Fresh | Indie Pop | Fresh | clean | 1200 | 1800 |
| 08 | Morning 08 — Indie Pop · Calm | Indie Pop | Calm | clean | 17 | 2100 |
| 09 | Morning 09 — Indie Pop · Hopeful | Indie Pop | Hopeful | clean | 217 | 2400 |
| 10 | Morning 10 — Indie Pop · Warm | Indie Pop | Warm | clean | 417 | 2700 |
| 11 | Morning 11 — Indie Pop · Focused | Indie Pop | Focused | clean | 617 | 0 |
| 12 | Morning 12 — Indie Pop · Gentle | Indie Pop | Gentle | clean | 817 | 300 |
| 13 | Morning 13 — Jazz & Soul · Fresh | Jazz & Soul | Fresh | clean | 1017 | 600 |
| 14 | Morning 14 — Jazz & Soul · Calm | Jazz & Soul | Calm | clean | 1217 | 900 |
| 15 | Morning 15 — Jazz & Soul · Hopeful | Jazz & Soul | Hopeful | clean | 34 | 1200 |
| 16 | Morning 16 — Jazz & Soul · Warm | Jazz & Soul | Warm | clean | 234 | 1500 |
| 17 | Morning 17 — Jazz & Soul · Focused | Jazz & Soul | Focused | clean | 434 | 1800 |
| 18 | Morning 18 — Jazz & Soul · Gentle | Jazz & Soul | Gentle | clean | 634 | 2100 |
| 19 | Morning 19 — Classical & Piano · Fresh | Classical & Piano | Fresh | clean | 834 | 2400 |
| 20 | Morning 20 — Classical & Piano · Calm | Classical & Piano | Calm | clean | 1034 | 2700 |
| 21 | Morning 21 — Classical & Piano · Hopeful | Classical & Piano | Hopeful | clean | 1234 | 0 |
| 22 | Morning 22 — Classical & Piano · Warm | Classical & Piano | Warm | clean | 51 | 300 |
| 23 | Morning 23 — Classical & Piano · Focused | Classical & Piano | Focused | clean | 251 | 600 |
| 24 | Morning 24 — Classical & Piano · Gentle | Classical & Piano | Gentle | clean | 451 | 900 |
| 25 | Morning 25 — Lo-Fi & Chillhop · Fresh | Lo-Fi & Chillhop | Fresh | clean | 651 | 1200 |
| 26 | Morning 26 — Lo-Fi & Chillhop · Calm | Lo-Fi & Chillhop | Calm | clean | 851 | 1500 |
| 27 | Morning 27 — Lo-Fi & Chillhop · Hopeful | Lo-Fi & Chillhop | Hopeful | clean | 1051 | 1800 |
| 28 | Morning 28 — Lo-Fi & Chillhop · Warm | Lo-Fi & Chillhop | Warm | clean | 1251 | 2100 |
| 29 | Morning 29 — Lo-Fi & Chillhop · Focused | Lo-Fi & Chillhop | Focused | clean | 68 | 2400 |
| 30 | Morning 30 — Lo-Fi & Chillhop · Gentle | Lo-Fi & Chillhop | Gentle | clean | 268 | 2700 |

## Midday — 30 Playlist

| No | Nama | Genre | Mood | Explicit | Priority offset | Global offset |
|---|---|---|---|---|---|---|
| 01 | Midday 01 — Pop · Upbeat | Pop | Upbeat | clean | 0 | 0 |
| 02 | Midday 02 — Pop · Energetic | Pop | Energetic | clean | 200 | 300 |
| 03 | Midday 03 — Pop · Confident | Pop | Confident | clean | 400 | 600 |
| 04 | Midday 04 — Pop · Bright | Pop | Bright | clean | 600 | 900 |
| 05 | Midday 05 — Pop · Groovy | Pop | Groovy | clean | 800 | 1200 |
| 06 | Midday 06 — Pop · Motivational | Pop | Motivational | clean | 1000 | 1500 |
| 07 | Midday 07 — Dance & Electronic · Upbeat | Dance & Electronic | Upbeat | clean | 1200 | 1800 |
| 08 | Midday 08 — Dance & Electronic · Energetic | Dance & Electronic | Energetic | clean | 17 | 2100 |
| 09 | Midday 09 — Dance & Electronic · Confident | Dance & Electronic | Confident | clean | 217 | 2400 |
| 10 | Midday 10 — Dance & Electronic · Bright | Dance & Electronic | Bright | clean | 417 | 2700 |
| 11 | Midday 11 — Dance & Electronic · Groovy | Dance & Electronic | Groovy | clean | 617 | 0 |
| 12 | Midday 12 — Dance & Electronic · Motivational | Dance & Electronic | Motivational | clean | 817 | 300 |
| 13 | Midday 13 — Hip-Hop & R&B · Upbeat | Hip-Hop & R&B | Upbeat | clean | 1017 | 600 |
| 14 | Midday 14 — Hip-Hop & R&B · Energetic | Hip-Hop & R&B | Energetic | clean | 1217 | 900 |
| 15 | Midday 15 — Hip-Hop & R&B · Confident | Hip-Hop & R&B | Confident | clean | 34 | 1200 |
| 16 | Midday 16 — Hip-Hop & R&B · Bright | Hip-Hop & R&B | Bright | clean | 234 | 1500 |
| 17 | Midday 17 — Hip-Hop & R&B · Groovy | Hip-Hop & R&B | Groovy | clean | 434 | 1800 |
| 18 | Midday 18 — Hip-Hop & R&B · Motivational | Hip-Hop & R&B | Motivational | clean | 634 | 2100 |
| 19 | Midday 19 — Rock & Alternative · Upbeat | Rock & Alternative | Upbeat | clean | 834 | 2400 |
| 20 | Midday 20 — Rock & Alternative · Energetic | Rock & Alternative | Energetic | clean | 1034 | 2700 |
| 21 | Midday 21 — Rock & Alternative · Confident | Rock & Alternative | Confident | clean | 1234 | 0 |
| 22 | Midday 22 — Rock & Alternative · Bright | Rock & Alternative | Bright | clean | 51 | 300 |
| 23 | Midday 23 — Rock & Alternative · Groovy | Rock & Alternative | Groovy | clean | 251 | 600 |
| 24 | Midday 24 — Rock & Alternative · Motivational | Rock & Alternative | Motivational | clean | 451 | 900 |
| 25 | Midday 25 — Funk & Groove · Upbeat | Funk & Groove | Upbeat | clean | 651 | 1200 |
| 26 | Midday 26 — Funk & Groove · Energetic | Funk & Groove | Energetic | clean | 851 | 1500 |
| 27 | Midday 27 — Funk & Groove · Confident | Funk & Groove | Confident | clean | 1051 | 1800 |
| 28 | Midday 28 — Funk & Groove · Bright | Funk & Groove | Bright | clean | 1251 | 2100 |
| 29 | Midday 29 — Funk & Groove · Groovy | Funk & Groove | Groovy | clean | 68 | 2400 |
| 30 | Midday 30 — Funk & Groove · Motivational | Funk & Groove | Motivational | clean | 268 | 2700 |

## Afternoon — 30 Playlist

| No | Nama | Genre | Mood | Explicit | Priority offset | Global offset |
|---|---|---|---|---|---|---|
| 01 | Afternoon 01 — Indie & Alternative · Mellow | Indie & Alternative | Mellow | allow | 0 | 0 |
| 02 | Afternoon 02 — Indie & Alternative · Romantic | Indie & Alternative | Romantic | allow | 200 | 300 |
| 03 | Afternoon 03 — Indie & Alternative · Nostalgic | Indie & Alternative | Nostalgic | allow | 400 | 600 |
| 04 | Afternoon 04 — Indie & Alternative · Relaxed | Indie & Alternative | Relaxed | allow | 600 | 900 |
| 05 | Afternoon 05 — Indie & Alternative · Golden | Indie & Alternative | Golden | allow | 800 | 1200 |
| 06 | Afternoon 06 — Indie & Alternative · Reflective | Indie & Alternative | Reflective | allow | 1000 | 1500 |
| 07 | Afternoon 07 — Soul & R&B · Mellow | Soul & R&B | Mellow | allow | 1200 | 1800 |
| 08 | Afternoon 08 — Soul & R&B · Romantic | Soul & R&B | Romantic | allow | 17 | 2100 |
| 09 | Afternoon 09 — Soul & R&B · Nostalgic | Soul & R&B | Nostalgic | allow | 217 | 2400 |
| 10 | Afternoon 10 — Soul & R&B · Relaxed | Soul & R&B | Relaxed | allow | 417 | 2700 |
| 11 | Afternoon 11 — Soul & R&B · Golden | Soul & R&B | Golden | allow | 617 | 0 |
| 12 | Afternoon 12 — Soul & R&B · Reflective | Soul & R&B | Reflective | allow | 817 | 300 |
| 13 | Afternoon 13 — Jazz & Blues · Mellow | Jazz & Blues | Mellow | allow | 1017 | 600 |
| 14 | Afternoon 14 — Jazz & Blues · Romantic | Jazz & Blues | Romantic | allow | 1217 | 900 |
| 15 | Afternoon 15 — Jazz & Blues · Nostalgic | Jazz & Blues | Nostalgic | allow | 34 | 1200 |
| 16 | Afternoon 16 — Jazz & Blues · Relaxed | Jazz & Blues | Relaxed | allow | 234 | 1500 |
| 17 | Afternoon 17 — Jazz & Blues · Golden | Jazz & Blues | Golden | allow | 434 | 1800 |
| 18 | Afternoon 18 — Jazz & Blues · Reflective | Jazz & Blues | Reflective | allow | 634 | 2100 |
| 19 | Afternoon 19 — Chillout & Downtempo · Mellow | Chillout & Downtempo | Mellow | allow | 834 | 2400 |
| 20 | Afternoon 20 — Chillout & Downtempo · Romantic | Chillout & Downtempo | Romantic | allow | 1034 | 2700 |
| 21 | Afternoon 21 — Chillout & Downtempo · Nostalgic | Chillout & Downtempo | Nostalgic | allow | 1234 | 0 |
| 22 | Afternoon 22 — Chillout & Downtempo · Relaxed | Chillout & Downtempo | Relaxed | allow | 51 | 300 |
| 23 | Afternoon 23 — Chillout & Downtempo · Golden | Chillout & Downtempo | Golden | allow | 251 | 600 |
| 24 | Afternoon 24 — Chillout & Downtempo · Reflective | Chillout & Downtempo | Reflective | allow | 451 | 900 |
| 25 | Afternoon 25 — Singer-Songwriter · Mellow | Singer-Songwriter | Mellow | allow | 651 | 1200 |
| 26 | Afternoon 26 — Singer-Songwriter · Romantic | Singer-Songwriter | Romantic | allow | 851 | 1500 |
| 27 | Afternoon 27 — Singer-Songwriter · Nostalgic | Singer-Songwriter | Nostalgic | allow | 1051 | 1800 |
| 28 | Afternoon 28 — Singer-Songwriter · Relaxed | Singer-Songwriter | Relaxed | allow | 1251 | 2100 |
| 29 | Afternoon 29 — Singer-Songwriter · Golden | Singer-Songwriter | Golden | allow | 68 | 2400 |
| 30 | Afternoon 30 — Singer-Songwriter · Reflective | Singer-Songwriter | Reflective | allow | 268 | 2700 |

## Night — 30 Playlist

| No | Nama | Genre | Mood | Explicit | Priority offset | Global offset |
|---|---|---|---|---|---|---|
| 01 | Night 01 — Ambient & Electronic · Sleepy | Ambient & Electronic | Sleepy | allow | 0 | 0 |
| 02 | Night 02 — Ambient & Electronic · Dreamy | Ambient & Electronic | Dreamy | allow | 200 | 300 |
| 03 | Night 03 — Ambient & Electronic · Melancholic | Ambient & Electronic | Melancholic | allow | 400 | 600 |
| 04 | Night 04 — Ambient & Electronic · Intimate | Ambient & Electronic | Intimate | allow | 600 | 900 |
| 05 | Night 05 — Ambient & Electronic · Cinematic | Ambient & Electronic | Cinematic | allow | 800 | 1200 |
| 06 | Night 06 — Ambient & Electronic · Nocturnal | Ambient & Electronic | Nocturnal | allow | 1000 | 1500 |
| 07 | Night 07 — Lo-Fi & Chillhop · Sleepy | Lo-Fi & Chillhop | Sleepy | allow | 1200 | 1800 |
| 08 | Night 08 — Lo-Fi & Chillhop · Dreamy | Lo-Fi & Chillhop | Dreamy | allow | 17 | 2100 |
| 09 | Night 09 — Lo-Fi & Chillhop · Melancholic | Lo-Fi & Chillhop | Melancholic | allow | 217 | 2400 |
| 10 | Night 10 — Lo-Fi & Chillhop · Intimate | Lo-Fi & Chillhop | Intimate | allow | 417 | 2700 |
| 11 | Night 11 — Lo-Fi & Chillhop · Cinematic | Lo-Fi & Chillhop | Cinematic | allow | 617 | 0 |
| 12 | Night 12 — Lo-Fi & Chillhop · Nocturnal | Lo-Fi & Chillhop | Nocturnal | allow | 817 | 300 |
| 13 | Night 13 — Piano & Classical · Sleepy | Piano & Classical | Sleepy | allow | 1017 | 600 |
| 14 | Night 14 — Piano & Classical · Dreamy | Piano & Classical | Dreamy | allow | 1217 | 900 |
| 15 | Night 15 — Piano & Classical · Melancholic | Piano & Classical | Melancholic | allow | 34 | 1200 |
| 16 | Night 16 — Piano & Classical · Intimate | Piano & Classical | Intimate | allow | 234 | 1500 |
| 17 | Night 17 — Piano & Classical · Cinematic | Piano & Classical | Cinematic | allow | 434 | 1800 |
| 18 | Night 18 — Piano & Classical · Nocturnal | Piano & Classical | Nocturnal | allow | 634 | 2100 |
| 19 | Night 19 — Dream Pop & Shoegaze · Sleepy | Dream Pop & Shoegaze | Sleepy | allow | 834 | 2400 |
| 20 | Night 20 — Dream Pop & Shoegaze · Dreamy | Dream Pop & Shoegaze | Dreamy | allow | 1034 | 2700 |
| 21 | Night 21 — Dream Pop & Shoegaze · Melancholic | Dream Pop & Shoegaze | Melancholic | allow | 1234 | 0 |
| 22 | Night 22 — Dream Pop & Shoegaze · Intimate | Dream Pop & Shoegaze | Intimate | allow | 51 | 300 |
| 23 | Night 23 — Dream Pop & Shoegaze · Cinematic | Dream Pop & Shoegaze | Cinematic | allow | 251 | 600 |
| 24 | Night 24 — Dream Pop & Shoegaze · Nocturnal | Dream Pop & Shoegaze | Nocturnal | allow | 451 | 900 |
| 25 | Night 25 — R&B & Soul · Sleepy | R&B & Soul | Sleepy | allow | 651 | 1200 |
| 26 | Night 26 — R&B & Soul · Dreamy | R&B & Soul | Dreamy | allow | 851 | 1500 |
| 27 | Night 27 — R&B & Soul · Melancholic | R&B & Soul | Melancholic | allow | 1051 | 1800 |
| 28 | Night 28 — R&B & Soul · Intimate | R&B & Soul | Intimate | allow | 1251 | 2100 |
| 29 | Night 29 — R&B & Soul · Cinematic | R&B & Soul | Cinematic | allow | 68 | 2400 |
| 30 | Night 30 — R&B & Soul · Nocturnal | R&B & Soul | Nocturnal | allow | 268 | 2700 |
