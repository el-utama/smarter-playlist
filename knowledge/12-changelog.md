# Changelog SmarterPlaylists

> Sumber: `/api/changelog` (diunduh saat riset, v3.12.3); 206 entri sejak 0.2.0 (2026-03-04). Bagian ini menampilkan semua entri fitur utama per versi; catatan minor/fix dikelompokkan.

## v3.12.3 (2026-10-02)

- **fix**: Match Filter's "Match Type" dropdown no longer shows attribute names instead of match types (exact, substring, regex)

## v3.12.2 (2026-09-11)

- **fix**: Playlist descriptions containing newlines or control characters no longer cause Spotify API 400 errors

## v3.12.1 (2026-09-10)

- **fix**: Preview no longer shows source_count column for track-output programs that use it on an upstream artist/album stream

## v3.12.0 (2026-09-10)

- **feature**: New source_count attribute on artist and album entities — shows how many times each entity appeared in the source stream, usable in Range Filter and Sorter for frequency-based thresholding
- **improvement**: Artist Filter, Artist De-Dup, and Remove Duplicates now accept all entity types (tracks, artists, albums), not just tracks
- **improvement**: Dedup key is now entity-aware — artists deduplicate by name, albums by title + artist

## v3.11.3 (2026-09-10)

- **fix**: Shared program and program preview pages now correctly show artist/album entity colors (purple/teal headers, dashed edges) instead of defaulting to gray/green

## v3.11.2 (2026-09-10)

- **improvement**: AUTO_PROGRAM_DESCRIPTION now shows adapter steps (to artists, to albums, to tracks), red/orange port exclusions, and reads as a left-to-right pipeline instead of jumbled component names

## v3.11.1 (2026-09-10)

- **improvement**: Admin overview page loads in under a second instead of ~10 seconds — scales to any database size

## v3.11.0 (2026-09-10)

- **feature**: New playlist description variables: ${PROGRAM_DESCRIPTION} (your program's description) and ${AUTO_PROGRAM_DESCRIPTION} (auto-generated summary from the dataflow topology)
- **feature**: Editor now auto-saves your work to the browser — navigate to FAQ, Tutorial, or any other page and come back without losing your program
- **feature**: Orange dot on the Editor tab shows when you have unsaved changes
- **improvement**: Genre Filter: new 'primary genre only' option to match only the artist's first genre, avoiding false positives from deep genre tags
- **improvement**: Artist Filter: the red (exclusion) port now accepts artist entity streams in addition to track streams
- **improvement**: Programs page loads ~40x faster for users with large run histories

## v3.10.1 (2026-09-07)

- **fix**: To Albums adapter now returns singles, compilations, and appears_on albums — was previously hardcoded to full albums only
- **fix**: Album preview now shows the artist name (was blank due to the field being stripped from cached data)
- **improvement**: Date Filter now works on albums as well as tracks
- **improvement**: Album preview shows album type column (album, single, compilation)

## v3.10.0 (2026-09-05)

- **feature**: Artists and albums are now first-class entity types that flow through the graph — not just tracks
- **feature**: New artist sources: My Top Artists, My Artist Library, Artist (by name), Artist URIs, Country Top Artists, Genre Artists
- **feature**: New album sources: My Album Library, Album Entity (by name), Album URIs, Label Albums
- **feature**: New adapters: To Tracks, To Artists, To Albums — convert between entity types with configurable selection modes
- **feature**: Similar Artists adapter — find related artists via Spotify radio
- **feature**: Filters, sorters, and selectors adapt to entity types — Range Filter, Match Filter, and Sort show attributes appropriate for the connected input type
- **improvement**: Color-coded graph edges: violet dashed for artists, teal dashed for albums, solid green for tracks
- **improvement**: Component palette splits sources, filters, orders, and selectors into Generic vs Track-specific subgroups
- **improvement**: Source and adapter node headers colored by output entity type
- **improvement**: Results panel adapts to entity type — artist and album previews show appropriate columns with both Spotify and MusicBrainz genres
- **improvement**: Preview mode allows non-track output for debugging (Run still requires tracks)
- **improvement**: Connection validation checks the full downstream chain — prevents building invalid type pipelines
- **improvement**: Artist name search improved with accent-aware fuzzy matching to avoid wrong-artist results
- **improvement**: Country name resolution supports common aliases: UK, USA, Korea, Deutschland, Holland, and more
- **improvement**: Tutorial and FAQ updated with entity type documentation, attribute tables, and example programs

## v3.9.2 (2026-08-09)

- **fix**: Separate Artists now truly maximizes spacing — every artist's tracks are scheduled at evenly-spaced positions, fixing back-to-back repeats that could slip through

## v3.9.1 (2026-07-28)

- **fix**: Service restart detection now catches dpkg upgrades (e.g. libc6) and apt-daily-upgrade runs that the unattended-upgrades log misses

## v3.9.0 (2026-07-23)

- **feature**: Scheduled programs detect Spotify's 6-month auth expiry — jobs pause immediately and a warning is written to the playlist description
- **improvement**: Service restart events now include context (e.g. unattended-upgrade package list)

## v3.8.1 (2026-07-18)

- **improvement**: Interrupted runs in run history now say whether the scheduler was restarted (deploy) or killed unexpectedly (e.g. memory limit)

## v3.8.0 (2026-07-18)

- **improvement**: Very large fetches are now capped at 10,000 tracks (playlists and Liked Songs); runs that hit the cap show a warning in run history
- **improvement**: Further reduced memory usage when fetching large playlists and libraries

## v3.7.5 (2026-07-01)

- **fix**: Artist Radio, Artist Top Tracks, Similar Tracks, and Tracks By Description now gracefully handle Spotify API errors instead of crashing the entire program

## v3.7.4 (2026-06-29)

- **fix**: Fixed excessive memory usage when fetching large playlists or saved-tracks libraries (10K+ tracks)

## v3.7.3 (2026-06-20)

- **improvement**: Similar Tracks source attribute now shows provenance chain (e.g. 'similar to Radiohead via Your Top Tracks')

## v3.7.2 (2026-06-18)

- **fix**: Similar Tracks now sets the source attribute on output tracks (e.g. 'similar to Radiohead')

## v3.7.1 (2026-06-18)

- **feature**: Added 'random' track attribute — use in MOS with low-weight Maximize to get different playlist orderings each run

## v3.7.0 (2026-06-14)

- **feature**: Added Playable Filter component — removes tracks unavailable in your market, with optional relinking to replace them with playable alternatives

## v3.6.0 (2026-06-12)

- **feature**: Added Similar Tracks component — expands each input track into related tracks by similar artists

## v3.5.5 (2026-06-12)

- **fix**: CSV export now preserves non-English characters (added UTF-8 BOM)

## v3.5.4 (2026-06-11)

- **improvement**: Increased maximum scheduled update run limit from 100 to 365

## v3.5.3 (2026-06-11)

- **fix**: Run history now shows actual tracks saved instead of pre-dedup count when 'No Dups' is enabled

## v3.5.2 (2026-05-23)

- **fix**: Playlist trim no longer resets 'Date added' timestamps for tracks past position 100

## v3.5.1 (2026-05-23)

- **improvement**: Dedup now matches by song title + artist instead of track ID, catching duplicate songs across singles, albums, and reissues

## v3.5.0 (2026-05-23)

- **feature**: New programs auto-name uniquely (Untitled, Untitled 2, ...) so previewing never conflicts
- **feature**: Batch select and delete programs from the Programs page, with schedule warnings

## v3.4.4 (2026-05-23)

- **improvement**: Schedule periodic runs directly from the editor's Program Settings dialog

## v3.4.3 (2026-05-15)

- **improvement**: Scheduler now runs up to 4 jobs concurrently, reducing late starts when many programs are due at once

## v3.4.2 (2026-05-11)

- **fix**: Fixed MOS distribution objective collapsing same-URI tracks from different sources into one entry, making source-based distribution impossible

## v3.4.1 (2026-05-10)

- **feature**: Source alias — set a custom label on any source (in Advanced) for use in distribution objectives and track display
- **improvement**: Duplicate sources are automatically disambiguated with #1, #2 suffixes so distribution objectives can distinguish them

## v3.4 (2026-05-10)

- **feature**: Tag programs for organization — add tags like "daily", "party", or "in progress" from program settings or the quick-tag button on the programs page
- **feature**: Filter programs by tags — clickable tag chips above the programs table to filter by one or more tags
- **improvement**: Tag autocomplete suggests existing tags while typing; comma-separated input for adding multiple tags at once

## v3.3 (2026-05-07)

- **feature**: Run history page — view full run history for any program with status, tracks, API calls, cache hits, duration, and manual vs. scheduled trigger
- **feature**: History button added to program actions for quick access to run history
- **improvement**: Stopped schedules now show a clear error message when a program fails 3 consecutive runs

## v3.2.1 (2026-05-05)

- **fix**: Fixed distribution objective failing to parse multi-word values like 'Quieter gothic metal(20%)'

## v3.2 (2026-05-05)

- **feature**: Added release_decade attribute for filtering, sorting, and displaying tracks by decade (e.g. 1970, 1980)
- **improvement**: Attribute dropdowns are now sorted alphabetically

## v3.1 (2026-05-04)

- **feature**: Configurable track display — add, remove, and drag-to-reorder columns directly on the results table, saved per program

## v3.0 (2026-05-03)

- **feature**: SmarterPlaylists 3.0 — out of beta!

## v0.56.2 (2026-05-03)

- **fix**: Components dragged from palette onto empty canvas now appear at the drop location instead of the center

## v0.56.1 (2026-05-03)

- **fix**: Fixed MusicBrainz ETL cron job failing because uv was not in cron's minimal PATH

## v0.56.0 (2026-05-02)

- **feature**: New Distribution objective for MOS — target percentage distributions of attribute values (e.g. 30% female, 20% rock)
- **fix**: Fixed MOS error messages showing [object Object] instead of readable component names
- **improvement**: MOS reference docs updated with Distribution and Continuity objectives

## v0.55.2 (2026-05-02)

- **fix**: Fixed camelot_num wrap-around in Continuity and Variety objectives — distance from 24 to 1 was treated as 23 instead of 1

## v0.55.1 (2026-05-02)

- **improvement**: Admin dashboard now shows Daily Users and New Users charts alongside Daily Runs

## v0.55.0 (2026-05-02)

- **feature**: Added Continuity objective for Multi-Objective Sequencer — scores candidates by distance from the last track's attribute value, enabling smooth transitions or deliberate contrast
- **fix**: Fixed Camelot attributes (camelot, camelot_num) not being computed when used in filters or sorters — audio features were not fetched as a prerequisite

## v0.54.0 (2026-05-01)

- **feature**: Discover page can be sorted by most shared, trending, newest, oldest, most complex, or least complex
- **improvement**: Discover page now shows component count and share date columns

## v0.53.1 (2026-05-01)

- **improvement**: Multi-Objective Sequencer nodes now display a readable description of all objectives directly on the canvas, with attribute names in bold and weight/slot annotations

## v0.53.0 (2026-05-01)

- **feature**: Match Max Run MOS objective limits consecutive runs of same-value tracks (e.g. max 3 by same artist, then 5 others before repeating)
- **feature**: Range Max Run MOS objective limits consecutive runs of tracks in a numeric range, with configurable separation gap

## v0.52.2 (2026-05-01)

- **fix**: Playlist auto-reset (weekly/monthly) no longer resets on every run during the reset day — only the first run triggers the reset

## v0.52.1 (2026-05-01)

- **fix**: Saving or running a program with an empty name now shows a clear error instead of a cryptic validation message

## v0.52.0 (2026-04-30)

- **feature**: MOS slot syntax now supports section notation (e.g. 1/4 for 'first quarter') that scales proportionally with the playlist limit
- **feature**: Order By objective spread is now a three-way mode: off, full, or segment — segment spread makes each slot segment span the full value range independently
- **improvement**: MOS editor lays out extra objective params on a single row to reduce vertical space

## v0.51.4 (2026-04-30)

- **improvement**: Discover page now paginates (20 per page) instead of showing a fixed top-50 list

## v0.51.3 (2026-04-26)

- **fix**: Scheduled runs with Multi-Objective Sequencer failed because objective types were not registered in the scheduler process

## v0.51.2 (2026-04-26)

- **feature**: Export CSV button on track results to download playlist tracks as a CSV file

## v0.51.1 (2026-04-26)

- **improvement**: Track URIs component accepts space/newline-separated input and Spotify URLs, with a larger text area for bulk pasting

## v0.51.0 (2026-04-25)

- **feature**: Playlist Analytics panel — view summary stats, per-track attribute charts, genre pie chart, and categorical distributions for generated playlists
- **improvement**: Results panel remembers height and selected tab between runs
- **improvement**: Snap-to-half button to quickly expand the results panel
- **improvement**: MOS node titles show a compact objective summary

## v0.50.0 (2026-04-25)

- **feature**: New Multi-Objective Sequencer (MOS) component — sequence tracks using weighted objectives like maximize, minimize, order-by, variety, min-separation, range, target, match, and contains
- **feature**: Dedicated MOS editor with per-objective configuration, validation, and slot-based position targeting
- **feature**: MOS reference guide accessible from the FAQ page

## v0.49.7 (2026-04-21)

- **fix**: Fixed run queue permanently rejecting all programs after a server restart

## v0.49.6 (2026-04-20)

- **improvement**: Added track attributes reference table to FAQ with descriptions of all 35 filterable/sortable attributes

## v0.49.5 (2026-04-19)

- **feature**: Added record label attribute — filter and sort tracks by label via MatchFilter and Sorter

## v0.49.2 (2026-04-19)

- **improvement**: Allow deeper zoom out in the flow editor so large programs fit on screen

## v0.49.1 (2026-04-19)

- **improvement**: Smart Mix now has a limit parameter (default 50) — feed it a large pool and it picks the best N tracks for smooth transitions

## v0.49.0 (2026-04-19)

- **feature**: Added Smart Mix order component — reorders tracks for smooth DJ-style transitions using genre, energy, Camelot harmonic compatibility, and tempo
- **feature**: Added Camelot wheel code as a track attribute (camelot and camelot_num) — derived from key and mode, available for sorting and filtering

## v0.48.2 (2026-04-19)

- **fix**: Save to Playlist now correctly empties the playlist when zero tracks are piped in (replace mode) instead of leaving it untouched

## v0.48.1 (2026-04-19)

- **improvement**: Version number in nav bar is now clickable — links to the changelog

## v0.48.0 (2026-04-18)

- **feature**: Save to Playlist now has a 'no duplicates' option — in append mode, skips tracks already in the playlist; in replace mode, deduplicates incoming tracks

## v0.47.1 (2026-04-13)

- **fix**: Alternator now respects the fail_fast parameter — stops when any input is exhausted instead of always continuing through all streams

## v0.47.0 (2026-04-12)

- **improvement**: Switched Spotify metadata cache from SQLite to Redis — eliminates database locking under concurrent load

## v0.46.0 (2026-04-12)

- **feature**: New Country Top Tracks source — generates popular tracks from artists of a given country using MusicBrainz + Spotify data, with cache-first popularity ranking

## v0.45.1 (2026-04-12)

- **improvement**: Simplified gender filter options: removed ensemble variants, added 'other' for non-binary artists

## v0.45.0 (2026-04-12)

- **feature**: Add artist gender, country, area, type, and active years from MusicBrainz data
- **feature**: New Gender Filter component — filter by vocalist gender (male, female, mixed, instrumental, etc.)
- **feature**: New Country Filter component — filter by artist country (ISO codes like US, GB, JP)
- **feature**: Artist start/end year and is_active available as filter and sort attributes
- **fix**: Fix MatchFilter not triggering decoration for non-base attributes
- **fix**: Fix MusicBrainz area hierarchy resolution (cities now resolve to correct country)

## v0.44.4 (2026-04-09)

- **fix**: Fix startup crash when apt auto-upgrades trigger systemd re-exec — SQLite busy_timeout now set before journal_mode pragma so workers wait for locks instead of failing

## v0.44.3 (2026-03-31)

- **improvement**: Tap a connection to show a delete button — enables editing flows on mobile without a keyboard

## v0.44.2 (2026-03-29)

- **fix**: Fix database locked errors caused by TRUNCATE checkpoints taking exclusive locks — switch to non-blocking PASSIVE checkpoints

## v0.44.1 (2026-03-28)

- **fix**: Fix cache WAL file growing unbounded (40GB+) by checkpointing every 15min with TRUNCATE, adding periodic expired-entry cleanup, and setting journal_size_limit

## v0.44.0 (2026-03-26)

- **feature**: New Intersection component — outputs only tracks that appear in all input streams

## v0.43.1 (2026-03-24)

- **fix**: MySavedAlbums and ArtistDiscography only returning first page of results (50 items max)

## v0.43.0 (2026-03-24)

- **feature**: New Pager component — progressively pages through a source's tracks across scheduled runs, wrapping around at the end
- **fix**: IsDayOfWeek regtest using local timezone instead of UTC, causing spurious failures

## v0.42.0 (2026-03-23)

- **feature**: Cache control on all source components via cache_mode param (auto/no-cache/short-term/long-term)
- **feature**: Last.fm API responses now cached with per-method default TTLs (1h-7d), reducing API calls on repeated runs
- **feature**: Advanced params: component editor has a collapsible Advanced section for power-user settings

## v0.41.0 (2026-03-22)

- **feature**: Per-component persistent state: components can now save/load state across runs via get_state()/set_state()

## v0.40.5 (2026-03-22)

- **fix**: Auto-redirect to login when Spotify session expires instead of showing cryptic JavaScript error

## v0.40.4 (2026-03-22)

- **improvement**: Admin jobs page: 'overdue' filter to see queued jobs, clickable Queue Depth card, overdue duration on Next Run column

## v0.40.3 (2026-03-22)

- **fix**: Infrastructure errors in scheduler no longer count toward 3-strike job stop limit
- **improvement**: Added 'running' and 'interrupted' to admin runs status filter

## v0.40.2 (2026-03-22)

- **fix**: Fixed all scheduled jobs crashing due to sqlite3.Row not supporting .get() for lastfm_username
- **fix**: Scheduler errors during context setup now properly recorded instead of leaving zombie 'running' entries

## v0.40.1 (2026-03-22)

- **fix**: Fixed PlaylistSave renaming existing playlists to 'My Smarter Playlist' when playlist URI is provided with blank name

## v0.40.0 (2026-03-21)

- **feature**: 7 new Last.fm source components — User's Recent Tracks, User's Top Tracks, User's Loved Tracks, Similar Tracks, Tag Top Tracks, Global Top Tracks, and Geo Top Tracks
- **feature**: Last.fm username setting in user profile for default Last.fm identity
- **improvement**: Source palette split into Spotify Sources and Last.fm Sources sections
- **improvement**: Last.fm logo icon on component nodes and palette

## v0.39.2 (2026-03-21)

- **improvement**: Search box on My Programs page to quickly find programs by name

## v0.39.1 (2026-03-21)

- **fix**: Fixed validation errors on My Top Tracks, artist top tracks, and recently played when Spotify returns tracks with null album data

## v0.39.0 (2026-03-20)

- **feature**: Playlist description field on Save to Playlist and Save to New Playlist — supports template variables like ${DATE}, ${NUM_TRACKS}, ${DURATION}, and more
- **improvement**: All playlists now get a default description ('Created by SmarterPlaylists') even without an explicit Save component

## v0.38.2 (2026-03-20)

- **fix**: Reduced 'database is locked' errors by increasing SQLite busy timeout and using non-blocking WAL checkpoints
- **fix**: Prevent unbounded cache WAL growth with periodic checkpoints (avoids disk-full outage)

## v0.38.1 (2026-03-19)

- **improvement**: Admin interface is now mobile-responsive — collapsible sidebar, compact tables with hidden low-priority columns, and tighter spacing on small screens

## v0.38.0 (2026-03-19)

- **feature**: Date-sensitive components now use your local timezone instead of server time — weekday checks, date ranges, playlist resets, and date suffixes all match your actual local date and time

## v0.37.1 (2026-03-18)

- **improvement**: Date Range shows a single date instead of a repeated range when start and end dates match

## v0.37.0 (2026-03-17)

- **feature**: Added Date Range conditional component — route tracks based on whether today falls within a configurable date range, with year-boundary wrap support

## v0.36.1 (2026-03-17)

- **fix**: Fixed admin cache key type breakdown showing 'v3' instead of actual entity types after cache versioning

## v0.36.0 (2026-03-17)

- **feature**: Playlist caching with user-controllable cache mode (auto/no-cache/short-term/long-term) on playlist source components
- **improvement**: Tiered cache TTLs — immutable data (tracks, albums, artists) cached for 7 days instead of 1 hour, reducing API calls by ~50%
- **improvement**: Slimmed cached objects strip to only used fields, reducing cache storage ~96% (5 GB → ~200 MB)

## v0.35.2 (2026-03-16)

- **improvement**: Added 'New Users Today' card to admin overview dashboard

## v0.35.1 (2026-03-16)

- **fix**: Fixed run queue failing with multiple uvicorn workers by switching from in-memory to SQLite-backed storage

## v0.35.0 (2026-03-16)

- **feature**: Interactive run queue — runs are queued instead of rejected when all execution slots are busy, with real-time status feedback
- **improvement**: Admin runs page shows queue wait time and delayed run percentage

## v0.34.8 (2026-03-16)

- **feature**: Admin users page now has search by name or ID
- **improvement**: Admin user detail tables are sortable by clicking column headers, and run rows navigate to the program

## v0.34.7 (2026-03-16)

- **improvement**: Relaxed 'late' threshold for scheduled runs from 1 minute to 14 minutes

## v0.34.6 (2026-03-16)

- **improvement**: Admin databases page loads much faster — parallelized queries across databases, skipped slow per-table size scan on large DBs, batched row counts
- **improvement**: Admin runs page shows scheduled vs interactive percentage, late run percentage, and average duration cards

## v0.34.5 (2026-03-16)

- **feature**: Added hourly runs stacked bar chart to admin runs page showing interactive, scheduled on-time, and scheduled late runs

## v0.34.4 (2026-03-16)

- **improvement**: Replaced reschedule_failed script with rerun_failed — re-runs programs immediately without altering job schedules

## v0.34.3 (2026-03-16)

- **feature**: Admin can run a program on behalf of its owner from the program detail page (useful for re-running after deploy interruptions)
- **improvement**: Admin program detail page now shows links to Spotify playlists updated by the program

## v0.34.2 (2026-03-16)

- **fix**: Fixed attribute range limits for duration, artist followers, tempo, loudness, track/disc number to allow real-world extremes

## v0.34.1 (2026-03-16)

- **fix**: Improved error messages when Spotify API calls fail during program execution
- **fix**: Eliminated unnecessary Spotify album API calls by extracting release_date from track metadata

## v0.34.0 (2026-03-16)

- **feature**: Fan-out support: a component's output can now connect to multiple downstream components, enabling split/parallel processing pipelines

## v0.33.2 (2026-03-15)

- **improvement**: Admin backups panel now shows daily/weekly rotation tiers with individual file sizes

## v0.33.0 (2026-03-15)

- **feature**: Added Max Tracks Per Artist filter — limits how many tracks by any single artist can pass through

## v0.32.0 (2026-03-15)

- **feature**: Validate component parameters on Done click — inline field errors prevent saving invalid settings
- **feature**: Pre-run and pre-schedule validation catches misconfigured programs before Spotify API calls
- **improvement**: Added range constraints to all numeric fields (limits, tempos, separations, durations) to reject nonsensical values
- **fix**: IsDayOfWeek dropdown now renders correctly (was showing as text input due to unresolved JSON Schema $ref)

## v0.31.6 (2026-03-14)

- **fix**: Cache DB lock no longer causes program execution failures — writes are silently skipped

## v0.31.5 (2026-03-14)

- **improvement**: Track 'server busy' rejections in run history with rejection rate stats on admin runs page

## v0.31.4 (2026-03-14)

- **improvement**: Admin jobs page: sort by next run, fix queue depth metric, show day/week stats as cards

## v0.31.3 (2026-03-14)

- **fix**: Fixed SavedAlbumPaging validation crash by bypassing tekore's strict Pydantic parsing for saved albums and tracks

## v0.31.2 (2026-03-14)

- **fix**: Fixed app server crash on startup when cache database is locked by scheduler

## v0.31.0 (2026-03-14)

- **improvement**: Interrupted scheduled runs are now tracked and visible in run history instead of silently lost
- **fix**: Scheduled jobs now run in chronological order when multiple are due at once

## v0.30.5 (2026-03-14)

- **fix**: Fixed crash when Spotify returns null items in saved albums, saved tracks, or other paging responses

## v0.30.4 (2026-03-14)

- **fix**: Fixed overnight scheduled job failures caused by cache database VACUUM holding exclusive lock

## v0.30.3 (2026-03-13)

- **improvement**: Admin DB page shows per-table sizes (data + indexes) with column headers
- **feature**: Vacuum button on admin DB page to reclaim free pages and shrink database files

## v0.30.2 (2026-03-13)

- **improvement**: Improved genre accuracy with Spotify artist ID matching from MusicBrainz, plus alias and text normalization fallbacks

## v0.30.1 (2026-03-13)

- **improvement**: MusicBrainz data moved to separate database file for simpler backups of user data

## v0.30.0 (2026-03-13)

- **improvement**: Genre Filter now uses artist name matching instead of ISRC lookup, reducing MusicBrainz database from 925MB to ~84MB
- **feature**: Admin dashboard DB tab showing size, row counts, cache breakdown, and MusicBrainz ETL status for all databases

## v0.29.1 (2026-03-13)

- **improvement**: Artist objects from followed artists and related artists are now cached individually, preserving Spotify genre data for future lookups

## v0.29.0 (2026-03-13)

- **feature**: New Genre Filter component — filter tracks by MusicBrainz genre using ISRC matching with artist name fallback (81% coverage on test data)
- **improvement**: Spotify API responses now cache individual tracks from list endpoints (playlists, saved tracks, top tracks, artist top tracks), avoiding redundant API calls on subsequent runs

## v0.28.1 (2026-03-13)

- **fix**: Spotify API cache now stores batch results (albums, artists, tracks, audio features) as individual entities instead of per-combination, preventing unbounded cache growth that caused a 46GB database and server outage

## v0.28.0 (2026-03-13)

- **feature**: New Match Filter component — filter tracks by matching title, artist, or album against a value using exact, substring, or regex matching with optional inversion
- **feature**: Title templates now support $ternary(param, trueVal, falseVal) syntax for conditional text in node titles

## v0.27.2 (2026-03-12)

- **fix**: Fixed System Calls and Workers columns in Spotify Failures table showing cumulative totals instead of the 1-minute window around each failure

## v0.27.1 (2026-03-12)

- **fix**: Rate limit indicators on admin API chart are now clearly visible even when dwarfed by normal call volume
- **fix**: Chart tooltip no longer gets stuck in the left third — follows cursor across the full chart width

## v0.27.0 (2026-03-12)

- **feature**: Program run history page — click the run count on any program to see full details: status, tracks, API calls, cache hits, duration, and timing for every run, plus scheduled job status

## v0.26.6 (2026-03-12)

- **feature**: Admin dashboard now shows active run concurrency gauge on System page and heaviest users table on Overview page for faster incident diagnosis

## v0.26.5 (2026-03-12)

- **fix**: Server no longer becomes unresponsive when multiple users run programs simultaneously — concurrent executions are now capped per worker so lightweight API calls always get through

## v0.26.4 (2026-03-12)

- **improvement**: Spotify failures table on admin API page now shows both 429 rate limits and 5xx server errors with system call volume context

## v0.26.3 (2026-03-12)

- **fix**: Fixed rate limit events not appearing in admin API page — retries, errors, and 429s are now recorded in the correct minute bucket when they happen instead of being lost at flush time

## v0.26.2 (2026-03-12)

- **improvement**: Rate limit events table now shows total system API calls (±1min) and active worker count, to help identify the rate limit threshold
- **fix**: Round response time values in API chart tooltip to whole milliseconds

## v0.26.1 (2026-03-12)

- **improvement**: Track results table columns are now sortable — click headers to sort ascending, again for descending, third click to reset

## v0.26.0 (2026-03-12)

- **feature**: New API tab in admin dashboard shows Spotify API call rate over time, rate limit (429) events, cache hit rate, and response times

## v0.25.0 (2026-03-12)

- **feature**: Date Filter now accepts relative dates (e.g. '6 months', '30 days') and partial dates ('2020', '2020-06')
- **improvement**: Unified date/duration parsing across Date Filter, Relative Dated Playlist, and Recently Played components
- **improvement**: Input validation with clear error messages for invalid date and duration values
- **improvement**: Node titles wrap to two lines instead of truncating, with full text on hover tooltip

## v0.24.4 (2026-03-12)

- **improvement**: Admin Activity table now shows scheduled run % and uses compact two-table side-by-side layout
- **improvement**: Run durations display as seconds (e.g. 29.6s) instead of raw milliseconds

## v0.24.3 (2026-03-11)

- **fix**: Fixed 'database is locked' errors during concurrent access by adding SQLite busy_timeout

## v0.24.2 (2026-03-11)

- **improvement**: Added security headers (CSP, X-Frame-Options, X-Content-Type-Options) to all responses
- **improvement**: MOTD messages are now sanitized to prevent XSS
- **improvement**: Program names limited to 255 chars, descriptions to 5000 chars, request bodies to 2MB
- **improvement**: Rate limiting on program create/update/delete, sharing, and migration endpoints
- **improvement**: Share codes increased from 8 to 16 characters for better brute-force resistance

## v0.24.1 (2026-03-11)

- **improvement**: Admin performance metrics now show today/week/overall breakdowns in a table layout

## v0.24.0 (2026-03-11)

- **feature**: Added Recently Played source component — pulls your recent Spotify listening history with optional time window filters (e.g. '2h', '7d')
- **feature**: Added schedule frequency options: every 2 hours, 4 hours, 8 hours, and every 2 weeks
- **fix**: Fixed playlist trim removing all copies of duplicate tracks instead of just the oldest — now correctly preserves newer copies
- **fix**: Fixed playlist trim reading the entire playlist just to check the track count — now uses a single cheap API call to skip trimming when under the cap

## v0.23.0 (2026-03-10)

- **feature**: Added dark mode with three settings: System (follows OS), Light, and Dark — toggle via the icon in the header
- **improvement**: Default canvas zoom is slightly reduced for better overview of large programs

## v0.22.4 (2026-03-10)

- **fix**: Raised max input port limit from 10 to 100 to support programs with many connected sources

## v0.22.3 (2026-03-10)

- **fix**: Error messages in admin runs table now wrap instead of being truncated

## v0.22.2 (2026-03-10)

- **fix**: Fixed blank optional numeric params (num_tracks, num_albums, num_artists) causing validation errors instead of being treated as 'all'
- **improvement**: Validation error messages now show component display name and field-level details instead of raw internal errors

## v0.22.1 (2026-03-10)

- **fix**: Disable caching for all playlist tracks — personalized editorial playlists (37i9d*) were returning stale results

## v0.22.0 (2026-03-10)

- **feature**: Added playlist trim modes (max_tracks, max_age_days) to Save to Playlist for automatic size management when appending
- **feature**: Added auto-reset schedule (weekly/monthly) to Save to Playlist for periodic playlist clearing
- **improvement**: Component editor help text now renders paragraphs with spacing for readability
- **improvement**: Component editor modal widened for better readability

## v0.21.1 (2026-03-10)

- **fix**: Track preview close button moved above the player so it no longer overlaps the Spotify logo
- **fix**: Closing the track preview now pauses playback if the track is playing
- **fix**: Legacy duration filter values are now correctly converted from seconds to milliseconds during migration

## v0.21.0 (2026-03-10)

- **feature**: Click any track in the results panel to preview it via Spotify's embedded player

## v0.20.1 (2026-03-10)

- **improvement**: Component editor modal is now draggable — grab the header to move it and see the canvas behind it
- **improvement**: Track results panel is now vertically resizable — drag the top edge to show more or fewer tracks

## v0.20.0 (2026-03-10)

- **improvement**: Tracks By Description now uses Spotify's curated mix playlists when available, making it much faster
- **improvement**: Deprecated Playlist Radio in favor of Artist Radio

## v0.19.0 (2026-03-10)

- **improvement**: My Followed Artists and My Saved Albums now support artist/album subsetting — limit how many to include and choose most recent, least recent, or random
- **improvement**: My Saved Albums now supports limiting tracks per album

## v0.18.0 (2026-03-10)

- **improvement**: Artist Top Tracks now returns ~50 tracks instead of 10
- **fix**: Artist search no longer returns wrong artist due to Spotify personalization

## v0.17.1 (2026-03-09)

- **fix**: Artist Radio now uses Spotify's algorithmic radio playlists instead of the deprecated related artists API

## v0.17.0 (2026-03-09)

- **improvement**: Promote from Alpha to Beta — your programs and playlists are now preserved across updates

## v0.16.1 (2026-03-09)

- **improvement**: Message of the Day now supports HTML formatting — bold, italics, and links

## v0.16.0 (2026-03-09)

- **feature**: Drag and drop components from the palette onto the canvas, with auto-wiring when dropped on nodes or edges
- **feature**: Drop a component on an edge to insert it into the connection
- **feature**: Drop a component on a node to connect it downstream, splicing in if already connected
- **improvement**: Visual feedback during drag — edges animate and nodes glow when hovering over valid drop targets
- **fix**: Tutorial table of contents links now scroll to the section instead of navigating away

## v0.15.2 (2026-03-09)

- **fix**: Fixed auto-layout making program disappear by fitting the viewport after layout and undo

## v0.15.1 (2026-03-09)

- **fix**: Fixed browser back button not working when leaving a shared program page

## v0.15.0 (2026-03-09)

- **feature**: Added Message of the Day (MOTD) — admins can post dismissable banners visible to all users

## v0.14.2 (2026-03-09)

- **improvement**: Added credit caption to tutorial screenshot

## v0.14.1 (2026-03-09)

- **improvement**: Browser back/forward buttons and page reload now preserve the current tab; tab URLs (e.g. #faq, #discover) are shareable

## v0.14.0 (2026-03-09)

- **feature**: Added Tutorial page with step-by-step guides for building programs, filtering, combining sources, scheduling, and more

## v0.13.2 (2026-03-09)

- **fix**: Fixed Spoken Word filter returning empty results — audio features were not being fetched due to a component name mismatch
- **fix**: Imported programs with audio filters (Danceable, Energy, Live, Spoken Word) now show correct scale labels instead of raw numbers

## v0.13.1 (2026-03-08)

- **fix**: Mixer now properly round-robins across input streams with track pushback, matching legacy behavior — previously skipped tracks that only failed artist separation were lost instead of retried

## v0.13.0 (2026-03-08)

- **feature**: Save to Playlist components now remember the playlist they created — no more duplicate playlists filling your library on repeated runs
- **feature**: Preview mode works with Save components — shows output tracks without writing to Spotify
- **improvement**: Changing a Save component's playlist name creates a new playlist instead of overwriting the old one
- **improvement**: Programs with multiple Save to Playlist components must have unique names (validated before run)
- **fix**: Save to Playlist as main output no longer creates a duplicate playlist alongside the auto-save

## v0.12.4 (2026-03-08)

- **improvement**: Source components now document Spotify API limits (e.g., My Top Tracks max 50, Artist Top Tracks max 10) and enforce valid ranges
- **fix**: Fixed incorrect help text for Artist Tracks (said 'up to 10 albums', actually fetches up to 50)

## v0.12.3 (2026-03-08)

- **improvement**: Validation errors (fan-out, cycles, too many inputs, etc.) now highlight the offending component on the canvas

## v0.12.2 (2026-03-08)

- **fix**: Programs with invalid or legacy parameter values now show clear validation errors instead of crashing with cryptic errors
- **fix**: Range Filter now supports optional min/max bounds (leave blank for no limit) and exact-match filtering via the match parameter
- **fix**: Legacy programs with empty numeric params, epoch timestamps, or list-format values are now handled correctly

## v0.12.1 (2026-03-07)

- **improvement**: Added FAQ entries for playlist saving confusion, where to ask questions, and project attribution

## v0.12.0 (2026-03-07)

- **feature**: Drag and drop playlists, albums, artists, and tracks from the Spotify desktop app directly onto the editor canvas to auto-create components
- **feature**: Multi-track drag from Spotify combines tracks into a single Track URIs node
- **improvement**: Track URIs component now shows track name and artist instead of raw URIs

## v0.11.1 (2026-03-07)

- **fix**: My Followed Artists now fetches all followed artists instead of only the first 50

## v0.11.0 (2026-03-07)

- **feature**: Copy/paste nodes with Cmd+C/Cmd+V, preserving internal edges for duplicating sub-graphs
- **feature**: Splice delete: Shift+Delete removes a node and reconnects its upstream sources to downstream targets
- **feature**: Auto-layout button arranges nodes top-to-bottom with one-step undo
- **feature**: Snap-to-grid toggle for precise node alignment
- **feature**: Multi-select via drag-to-select rectangles and Cmd+Click
- **improvement**: Cycle prevention rejects connections that would create loops in the graph
- **improvement**: Updated FAQ with editor shortcuts and new feature documentation

## v0.10.8 (2026-03-07)

- **improvement**: My Programs table now sorts by most recently updated by default

## v0.10.7 (2026-03-07)

- **improvement**: Clean up component palette: hide Deprecated Source, move Shuffle to Orderers, rename Orders to Orderers, move Comment to its own Annotations section

## v0.10.6 (2026-03-07)

- **improvement**: Show component description in editor and display help text inline without toggle

## v0.10.5 (2026-03-07)

- **improvement**: Hide vestigial Annotator component from palette (annotation is now automatic)

## v0.10.4 (2026-03-07)

- **improvement**: Comment nodes restyle as customizable annotations with style, color, and size options

## v0.10.1 (2026-03-06)

- **fix**: Fix deleting legacy-imported programs (foreign key constraint error)

## v0.10.0 (2026-03-06)

- **feature**: Share programs with a public link — anyone can view the graph, logged-in users can preview or import a copy
- **feature**: Discover tab showing most-imported shared programs
- **feature**: Program Settings dialog for editing descriptions

## v0.9.6 (2026-03-06)

- **improvement**: Add sortable column headers to programs table and admin tables

## v0.9.5 (2026-03-06)

- **fix**: Allow scheduling with all available intervals (3 days, monthly, quarterly, etc.)

## v0.9.4 (2026-03-06)

- **fix**: Fixed excessive vertical spacing in migrated program layouts

## v0.9.1 (2026-03-06)

- **improvement**: Added FAQ entry about importing legacy programs from old SmarterPlaylists

## v0.9.0 (2026-03-06)

- **feature**: Legacy program migration: browse, preview, and selectively import programs from old SmarterPlaylists
- **improvement**: Playlist source searches Spotify by name when no URI is provided
- **improvement**: Run error messages now show the component name and title for easier debugging
- **fix**: Fixed unused import and React Hook dependency warning in frontend

## v0.8.3 (2026-03-05)

- **improvement**: Run stats table disambiguates duplicate component names by appending node ID
- **improvement**: Added scheduling intervals: 3 days, 1/3/6/9 months, 1 year

## v0.8.2 (2026-03-05)

- **fix**: Filters and Sorter now drop tracks that are missing the required attribute instead of passing them through

## v0.8.1 (2026-03-05)

- **improvement**: Duration parameters (No Longer Than, No Shorter Than) now show hours/minutes/seconds inputs instead of raw seconds

## v0.8.0 (2026-03-05)

- **feature**: Auto-resolve Spotify URIs: pasting a URI/URL into a component and tabbing away auto-populates name fields (playlist name/owner, artist name, album title/artist)

## v0.7.4 (2026-03-05)

- **improvement**: Timeout and error responses now include execution stats so users can see which component was consuming all the time
- **improvement**: Components that are mid-execution when a timeout occurs show a 'timed out' indicator in the stats

## v0.7.3 (2026-03-05)

- **improvement**: Improved MixIn and Mixer help text to explain what each port does and how fail_fast behaves

## v0.7.2 (2026-03-05)

- **improvement**: Album metadata fetching (Date Filter, etc.) now batches up to 20 albums per API call instead of one-by-one

## v0.7.1 (2026-03-05)

- **fix**: Fixed Alternator infinite loop when an input stream has no source
- **improvement**: Added 5-minute execution timeout to prevent runaway programs from blocking the API and scheduler
- **feature**: Runtime clock next to Run button shows elapsed time during execution

## v0.7.0 (2026-03-05)

- **feature**: Spotify API rate limit resilience: automatic retry with backoff on 429/5xx errors, proactive request throttling
- **feature**: Per-component run stats: collapsible table showing API calls, cache hits, retries, API time, and track counts for each component
- **feature**: Click a component in the stats table to highlight and pan to it on the canvas

## v0.6.3 (2026-03-05)

- **fix**: Playlists containing local files or podcast episodes no longer cause errors

## v0.6.1 (2026-03-04)

- **improvement**: Schedule dialog now supports total run count and next run time
- **improvement**: Programs page shows next scheduled run date/time

## v0.6.0 (2026-03-04)

- **feature**: Component palette is now resizable, has collapsible sections, and a search box for finding components

## v0.5.1 (2026-03-04)

- **improvement**: Programs page is now the default landing page for logged-in users
- **fix**: Set browser tab title to 'SmarterPlaylists'

## v0.5.0 (2026-03-04)

- **feature**: Run programs directly from the programs page without opening the editor
- **improvement**: Switched action buttons to icons for a cleaner, more compact layout
- **improvement**: Run errors now show the failing component name

## v0.4.1 (2026-03-04)

- **fix**: Fixed personalized data (top tracks, saved tracks, etc.) being shared across users due to missing user ID in cache keys
- **fix**: User-owned playlists are no longer cached, preventing stale data when a program reads its own output playlist

## v0.4.0 (2026-03-04)

- **improvement**: Replaced Spotify library with Tekore for native async I/O — faster concurrent requests, no thread pool overhead
- **improvement**: Separated scheduler into its own process so the web server can run with multiple workers
- **improvement**: Web server now supports multi-worker mode (--workers 4) for better concurrency

## v0.3.1 (2026-03-04)

- **improvement**: Improved server concurrency so multiple users can be served simultaneously

## v0.3.0 (2026-03-04)

- **feature**: Changelog page viewable at #changelog, accessible without login

## v0.2.1 (2026-03-04)

- **fix**: Show detailed error messages when programs fail, including which component caused the error
- **fix**: Highlight the errored component on the canvas with a red border
- **fix**: Audio feature filters (Energy, Danceable, etc.) and Sorter now correctly fetch audio features before filtering

## v0.2.0 (2026-03-04)

- **feature**: Display app version on login page and in navbar
- **fix**: Fix version endpoint crash when versions.json uses array format

