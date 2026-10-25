# SmarterPlaylists Tutorial

A step-by-step guide to building complex Spotify playlists with SmarterPlaylists.

---

## Table of Contents

1. [What is SmarterPlaylists?](#1-what-is-smarterplaylists)
2. [Getting Started](#2-getting-started)
3. [Your First Program: My Top Tracks](#3-your-first-program-my-top-tracks)
4. [Adding a Filter](#4-adding-a-filter)
5. [Combining Multiple Sources](#5-combining-multiple-sources)
6. [Filtering by Audio Features](#6-filtering-by-audio-features)
7. [Excluding Tracks and Artists](#7-excluding-tracks-and-artists)
8. [Using Conditionals](#8-using-conditionals)
9. [Sorting and Ordering](#9-sorting-and-ordering)
10. [Working with Artists and Albums](#10-working-with-artists-and-albums)
11. [Scheduling Automatic Updates](#11-scheduling-automatic-updates)
12. [Sharing Your Programs](#12-sharing-your-programs)
13. [Tips and Tricks](#13-tips-and-tricks)
14. [Component Reference](#14-component-reference)

---

## 1. What is SmarterPlaylists?

SmarterPlaylists is a visual tool for building Spotify playlists that are smarter than anything you can create in Spotify alone. Instead of manually adding tracks, you **wire together components** in a graph editor to describe *how* your playlist should be built.

Want a playlist of your top tracks mixed with songs from your favorite playlists, filtered to only danceable songs, with no repeated artists? That's a few components and a couple of connections — and you can schedule it to update itself every day.

**Key concepts:**

- A **program** is a graph of connected components
- **Components** are the building blocks — sources that provide tracks, filters that remove tracks, combiners that merge streams, and more
- The **main node** (marked with a star) determines the final output
- When you **run** a program, it saves the output to a Spotify playlist

![the editor with a medium-complexity program](/tutorial/variety-radio.png)
*Variety radio! program by Keeble*

 **[Try it yourself](https://smarterplaylists.playlistmachinery.com/shared/a5Rk7AYJ)** — import
   this program and run it with your own Spotify account.

---

## 2. Getting Started

### Logging in

SmarterPlaylists uses your Spotify account. Click **Log in with Spotify** and grant the requested permissions. SmarterPlaylists needs access to read your playlists, saved tracks, and listening history, and to create and modify playlists on your behalf.

![the login page / landing page](/tutorial/login.png)

### The interface

After logging in, you'll see three main areas:

- **Programs** — a table of all your saved programs, with controls for running, editing, scheduling, and sharing
- **Editor** — the visual graph editor where you build programs
- **FAQ** — answers to common questions

![the programs page](/tutorial/programs.png)

---

## 3. Your First Program: My Top Tracks

Let's start simple — a playlist of your 25 most-listened-to tracks.

### Step 1: Create a new program

Click **New Program** (or go to the **Editor** tab). Give your program a name — something like "My Top 25".

### Step 2: Add a source

In the component palette on the left, find **My Top Tracks** under Sources. Click it to add it to the canvas.

This component pulls your most-listened tracks from Spotify. By default it grabs 50 tracks from your medium-term listening history.

### Step 3: Add a selector

We only want 25 tracks. Under Selectors, click **First** to add it. Double-click it and set the count to \25\.

### Step 4: Connect the nodes

Drag from the output port (bottom) of **My Top Tracks** to the green input port (top) of **First**. You'll see a connection line appear.

![two nodes](/tutorial/two-nodes.png)

### Step 5: Set the main node

Click on the **First** node to select it, then press **Space** to make it the main output. A star icon appears on the node.

### Step 6: Save and run

Click **Save**, then **Run**. After a few seconds, the results panel slides up from the bottom showing your 25 tracks. A Spotify playlist called "My Top 25" has been created in your account — click the Spotify link to open it.

![results panel](/tutorial/results.png)

> **Tip:** Use **Preview** instead of Run to see the output without saving to a playlist. Great for testing.

> **[Try it yourself](https://smarterplaylists.playlistmachinery.com/shared/FuTaqj9S)** — import this program and
   run it with your own Spotify account.

---

## 4. Adding a Filter

Let's make our playlist more interesting by removing duplicate artists — so you get a more varied mix.

### Step 1: Start from the previous program

Open "My Top 25" in the editor (or import the shared version above).

### Step 2: Add the Artist De-Dup filter

In the palette, find **Artist De-Dup** under Filters and click to add it.

### Step 3: Wire it in

This component keeps only the first track it sees from each artist. We want to de-dup *before* we take the first 25, so either:

- **Drag and drop:** Drag **Artist De-Dup** from the palette directly onto the edge between My Top Tracks and First — it will automatically splice itself in.
- **Manual wiring:** Click the connection between My Top Tracks and First to select it, press **Delete**, then connect **My Top Tracks** → **Artist De-Dup** → **First**.

Now we'll get the first 25 tracks from our top tracks, with no artist appearing more than once.

![three-node chain](/tutorial/tutorial-my-top-tracks-filtered.png)

### Step 4: Run it

Click **Save**, then **Run**. Compare the results to the previous version — you should see more variety.

> **[Try it yourself](https://smarterplaylists.playlistmachinery.com/shared/47n7E00i)** — import this program and
   run it with your own Spotify account.


---

## 5. Combining Multiple Sources

One of SmarterPlaylists' most powerful features is mixing tracks from multiple sources. Let's blend your top tracks with tracks from a playlist you like.

### Step 1: Create a new program

Start a new program called "My Mix".

### Step 2: Add two sources

- Add **My Top Tracks** (your personal favorites)
- Add **Playlist** from Sources — double-click it and paste a Spotify playlist URL or URI that you like

### Step 3: Add a combiner

Under Combiners, add **Alternate**. This interleaves tracks from its inputs: one from the first source, one from the second, and so on.

### Step 4: Connect both sources to the combiner

Connect both **My Top Tracks** and **Playlist** to the green input port of **Alternate**. The port accepts multiple inputs.

### Step 5: Add a selector and de-dup

- Add **First** (set to 50)
- Add **Remove Duplicates** — in case a track appears in both sources
- Wire: Alternate → Remove Duplicates → First

### Step 6: Set main and run

Make **First** the main node, save, and run.

<!-- screenshot: two sources feeding into Alternate, then dedup, then First -->

<!-- TODO: add shared program link -->

> **Other combiners to try:**
> - **Shuffle** — randomly reorder all tracks
> - **Mix In** — blend a secondary source at a configurable ratio (e.g., 80% primary, 20% mix-in)
> - **Random** — randomly interleave tracks (instead of strict alternation)

---

## 6. Filtering by Audio Features

Spotify analyzes every track for audio features like danceability, energy, tempo, and more. You can use these to shape your playlists.

### Example: A high-energy dance playlist

### Step 1: Start with a large source

Add a **Playlist** and choose a large playlist (the bigger the better — more tracks to filter from). Or combine multiple playlists using Alternate or Shuffle.

### Step 2: Add audio feature filters

- Add **Danceable** — double-click and set it to **most** (top 25% danceability)
- Add **Energy** — set to **more** (top 50% energy)

### Step 3: Chain them together

Wire: Playlist → Danceable → Energy → First (set to 30) → set as main.

Each filter narrows the stream. Only tracks that are both highly danceable *and* energetic will make it through.

<!-- screenshot: source → danceable → energy → first chain -->

### Step 4: Run and check

Run the program, then look at the results. The results panel shows extra columns for audio features — you can verify that your filters are working.

<!-- TODO: add shared program link -->

> **Available audio feature filters:** Danceable, Energy, Live, Spoken Word, Tempo
>
> **For more control:** Use the **Range Filter** component, which lets you filter on *any* numeric attribute with precise min/max values — including popularity, duration, valence (happiness), acousticness, instrumentalness, and more.

---

## 7. Excluding Tracks and Artists

The **red** and **orange** input ports let you subtract tracks and artists from a stream.

### Example: Fresh discoveries — your saved tracks minus songs you've heard recently

### Step 1: Set up the sources

- Add **My Saved Tracks** (set limit to 200 or more)
- Add **My Top Tracks** (your recently-played favorites — the tracks you want to *exclude*)

### Step 2: Add a Track Filter

Add **Track Filter** from the Filters section.

### Step 3: Connect using colored ports

- Connect **My Saved Tracks** to the **green** port of Track Filter (the primary input)
- Connect **My Top Tracks** to the **red** port of Track Filter (the exclusion list)

The Track Filter will remove any track from the green stream that also appears in the red stream.

### Step 4: Add a shuffle and selector

Wire: Track Filter → Shuffle → First (set to 30) → set as main.

Now you'll get 30 random songs from your saved library that you haven't been listening to recently.

<!-- screenshot: two sources into Track Filter (green and red ports), then shuffle, then first -->

<!-- TODO: add shared program link -->

> **Orange ports** work similarly but filter by *artist* instead of track. Use them with the **Artist Filter** or **Mixer** components to exclude entire artists.

---

## 8. Using Conditionals

Conditionals let your programs behave differently based on when they run — perfect for scheduled playlists.

### Example: Upbeat on weekdays, chill on weekends

### Step 1: Prepare two branches

- Create a high-energy chain (e.g., an upbeat playlist → Energy filter set to "most" → First)
- Create a chill chain (e.g., a mellow playlist → Energy filter set to "least" → First)

### Step 2: Add a conditional

Add **Is Weekend?** from the Conditionals section.

### Step 3: Connect the branches

- Connect the chill chain to the **green** port (played on weekends)
- Connect the upbeat chain to the **red** port (played on weekdays)

Make **Is Weekend?** the main node.

<!-- screenshot: two branches feeding into Is Weekend? -->

### Step 4: Schedule it

This program is most useful when scheduled (see the next section). Run it daily and the playlist will automatically switch between your two moods.

<!-- TODO: add shared program link -->

> **Other conditionals:**
> - **Is Day of Week** — route to different streams based on the current day (Monday through Sunday)
> - **Yes or No** — a simple manual switch between two streams

---

## 9. Sorting and Ordering

You can control the order of tracks in your output.

### Sort by an attribute

Add a **Sort** component and choose what to sort by — popularity, danceability, tempo, release date, title, artist name, and more. Toggle ascending/descending in the parameters.

### Shuffle with control

**Weighted Shuffle** gives you a slider between fully ordered (0) and fully random (1). Set it to 0.3 for a gentle shuffle that mostly preserves order with some variety.

### Separate artists

**Artist Separation** ensures no two tracks by the same artist are too close together. Great for playlists that pull heavily from a few artists.

<!-- screenshot: Sort node parameters -->

---

## 10. Working with Artists and Albums

SmarterPlaylists doesn't just work with tracks — you can flow **artists** and **albums** through the graph too. This opens up creative patterns like "find artists similar to my favorites, grab their newest albums, and make a playlist."

### Entity types

Every connection in a program carries one type of entity:

- **Tracks** (green) — the default, what most components produce
- **Artists** (violet) — artist entities with attributes like popularity, followers, genres, country, etc.
- **Albums** (teal) — album entities with attributes like popularity, release date, label, total tracks

The editor shows you the types visually: dashed violet edges carry artists, dashed teal edges carry albums, and solid green edges carry tracks. Source and adapter nodes are colored to match their output type.

### Artist and album sources

Instead of always starting with tracks, you can start with artist or album entities:

| Source | Output | Description |
|--------|--------|-------------|
| **My Top Artists** | artist | Your most-listened artists |
| **My Artist Library** | artist | Artists you follow |
| **Artist** | artist | Search for an artist by name |
| **Artist URIs** | artist | Load specific artists by URI |
| **My Album Library** | album | Your saved albums |
| **Album Entity** | album | Search for an album by name |
| **Album URIs** | album | Load specific albums by URI |
| **Label Albums** | album | Albums from a record label |

These appear in their own colored sections in the palette — **Artist Sources** (violet) and **Album Sources** (teal).

### Adapters — converting between types

Adapters are the bridge between entity types:

| Adapter | What it does |
|---------|-------------|
| **To Tracks** | Convert artists or albums into their tracks |
| **To Artists** | Extract unique artists from tracks or albums |
| **To Albums** | Extract albums from tracks, or fetch an artist's discography |
| **Similar Artists** | Find related artists using Spotify's radio |

For example, **To Tracks** changes its behavior based on the input type. Feed it artists and you can choose most popular, newest, oldest, or random tracks. Feed it albums and you can choose album order, most popular, or random tracks. The options in the dropdown adapt automatically.

### Filtering and sorting entities

Many components are **polymorphic** — they work with any entity type. The palette marks these as "Generic" vs. "Track-specific":

- **Generic** (works on anything): Range Filter, Match Filter, Sort, Shuffle, DeDup, Sample, First, Last, and more
- **Track-specific**: Danceable, Energy, Tempo, Genre Filter, Gender Filter, etc.

When you connect an artist stream to a Range Filter, the attribute dropdown automatically shows artist attributes (popularity, followers, start year). Connect an album stream and you'll see album attributes (popularity, release date, total tracks).

### Example: Discover new music from similar artists

1. Add **My Top Artists** — your most-listened artists
2. Add **Similar Artists** (set count to 3) — finds 3 related artists per input
3. Add **To Tracks** (set select to "most_popular", count to 5) — grabs 5 top tracks each
4. Add **Shuffle** then **First** (set to 50) — mix and cap at 50
5. Set First as the main node, save, and run

This gives you 50 tracks from artists similar to your favorites — a discovery playlist that updates every time you run it.

### Example: Best albums from a label

1. Add **Label Albums** — enter a label name like "4AD" and set order to "most_popular"
2. Add **Range Filter** — set attribute to "release_date" to filter by era
3. Add **To Tracks** (album_order, count 3) — first 3 tracks from each album
4. Set as main, save, and run

### Type safety

The editor prevents invalid connections. You can't connect an artist source to a track-only filter like Danceable — the connection simply won't attach. If you try to run a program where the main output is an artist or album (not tracks), you'll get a clear error message. Use **Preview** instead of Run to see non-track output for debugging.

---

## 11. Scheduling Automatic Updates

One of the most powerful features: your playlists can update themselves automatically.

### Step 1: Create and save a program

Build any program and save it. Make sure it runs successfully at least once.

### Step 2: Open the schedule dialog

Go to the **Programs** page. Find your program and click in the **Schedule** column.

### Step 3: Configure the schedule

- **Interval**: How often to run — hourly, daily, or weekly
- **Total runs**: How many times to run before stopping (max 100)

Click **Save** to activate the schedule.

<!-- screenshot: schedule dialog -->

### Step 4: Monitor

Back on the Programs page, you'll see the schedule status:
- Next run time
- Runs remaining
- A green indicator when a schedule is active

The program will run automatically at your chosen interval. Each run updates the Spotify playlist with fresh tracks.

<!-- screenshot: Programs page showing schedule column -->

> **Note:** If a program fails 3 times in a row, the schedule is automatically paused to prevent runaway errors.

### Best programs to schedule

- **Discovery playlists** that pull from recommendation sources — get fresh music daily
- **Conditional playlists** that change based on day of the week
- **Dated playlists** that pull recently-added tracks from a playlist you follow

---

## 12. Sharing Your Programs

You can share your programs with other SmarterPlaylists users.

### Publishing a program

1. Open your program in the editor
2. Click the **Share** button in the toolbar
3. Click **Publish** — this generates a unique link
4. Copy the link and share it however you like

<!-- screenshot: share dialog -->

### What others see

Anyone with the link can view your program's graph and description. Logged-in users can:

- **Preview** — run the program with their own Spotify account to see what tracks they'd get
- **Import** — copy the program to their own library

### Discovering programs

Toggle **Make discoverable** in the share dialog to list your program on the **Discover** page, where other users can browse and import community-created programs.

<!-- screenshot: Discover page -->

> **Important details:**
> - Publishing shares the *live version* — if you edit your program, visitors see the updated version
> - When someone imports your program, they get an independent copy — your future edits won't affect their version
> - You can **unpublish** at any time to revoke the link

---

## 13. Tips and Tricks

### Drag and drop from the palette

Instead of clicking to place components, you can **drag them from the palette** directly onto the canvas. Drop anywhere on the canvas to place a component, or drop it onto an existing node or edge to automatically wire it up:

- **Drop on a node** — the new component is connected after that node. If the node already has a downstream connection, the new component is spliced in between.
- **Drop on an edge** — the new component is inserted into that connection, splitting the edge into two.

Edges animate and nodes glow blue as you drag over valid drop targets, so you always know what will happen before you let go. Inserted components are automatically aligned with the upstream node.

This makes building chains fast — drag a source from the palette, then drag a filter onto it, then drag a selector onto that, and you've got a complete pipeline without manually connecting a single wire.

### Drag and drop from Spotify

You can drag playlists, albums, artists, or tracks directly from the **Spotify desktop app** onto the editor canvas. The right component type is created automatically with the name filled in.

### Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| Double-click | Edit node parameters |
| Space | Set selected node as main |
| Delete | Remove selected nodes |
| Shift+Delete | Splice node out of chain (reconnects edges) |
| Cmd/Ctrl+C | Copy selected nodes |
| Cmd/Ctrl+V | Paste |
| Cmd/Ctrl+Click | Multi-select |
| Click+drag on canvas | Rectangle select |

### Auto-layout

Click the **Layout** button (top-right) to automatically arrange your nodes in a clean top-to-bottom layout. Click **Undo** if you don't like the result.

### Splitting a stream (fan-out)

A component's output can feed into **multiple** downstream components. This lets you split a stream to process it in different ways — for example, take one source and run it through two different filter chains, or save the same tracks to two separate playlists.

Just drag multiple connections from a single output port. Each downstream component receives the same tracks, and the upstream component only runs once.

**Example:** Take your top tracks, filter one copy for high energy and another for high danceability, then concatenate the results into one playlist with the best of both.

### You don't need a Save to Playlist component

This is the most common point of confusion. **Every program automatically saves its output to a Spotify playlist** — you don't need to add a Save to Playlist component at the end. If you do, you'll end up with two playlists (the automatic one plus the one from the component).

The Save to Playlist and Save to New Playlist components exist for the rare case where you want to save a *side branch* of your program to a separate playlist.

### Comment nodes

Add **Comment** nodes to document complex programs. You can change the style (sticky note, simple, subtle), color, and size.

### Start big, filter down

Audio feature filters and attribute filters work best when they start with a large pool of tracks. If you filter a 20-track playlist for "most danceable", you'll only get ~5 tracks. Start with hundreds of tracks and filter down to the size you want.

---

## 14. Component Reference

### Sources — generate track streams

| Component | Description |
|-----------|-------------|
| **Playlist** | Tracks from any Spotify playlist (by URL, URI, or name) |
| **My Saved Tracks** | Your Liked Songs library |
| **My Top Tracks** | Most-listened tracks (short/medium/long term) |
| **Album** | All tracks from a Spotify album |
| **Track** | Find a single track by title |
| **Track URIs** | Specific tracks by Spotify URIs |
| **Artist Top Tracks** | An artist's top 10 tracks |
| **Artist Tracks** | All tracks from an artist's catalog |
| **Artist Radio** | Tracks by an artist and similar artists |
| **Playlist Radio** | Community-sourced radio based on playlist theme |
| **Tracks By Description** | Find tracks by description (e.g., "chill lo-fi") |
| **My Followed Artists** | Top tracks from artists you follow |
| **My Saved Albums** | All tracks from your saved albums |
| **Dated Playlist** | Playlist tracks filtered by date added |
| **Relative Dated Playlist** | Playlist tracks added within a time window (e.g., "last 7 days") |
| **Recently Played** | Tracks you've recently listened to on Spotify (max 50) |

### Sources — generate artist streams

| Component | Description |
|-----------|-------------|
| **My Top Artists** | Your most-listened artists (short/medium/long term) |
| **My Artist Library** | Artists you follow on Spotify |
| **Artist** | Search for an artist by name |
| **Artist URIs** | Specific artists by Spotify URIs or URLs |

### Sources — generate album streams

| Component | Description |
|-----------|-------------|
| **My Album Library** | Albums from your saved library |
| **Album Entity** | Search for an album by name |
| **Album URIs** | Specific albums by Spotify URIs or URLs |
| **Label Albums** | Albums from a record label |

### Adapters — convert between entity types

| Component | Input | Output | Description |
|-----------|-------|--------|-------------|
| **To Tracks** | artist or album | track | Get tracks from artists (popular/newest/oldest/random) or albums (album order/popular/random) |
| **To Artists** | track or album | artist | Extract unique artists, optionally including featured artists |
| **To Albums** | track or artist | album | Extract albums from tracks, or fetch an artist's discography (with album type filter) |
| **Similar Artists** | artist | artist | Find related artists via Spotify radio playlists |

### Filters — reduce and refine

Generic filters work on any entity type (tracks, artists, albums). Track filters work only on tracks.

| Component | Entity types | Description |
|-----------|-------------|-------------|
| **Remove Duplicates** | any | Remove duplicate items (by ID or name) |
| **Range Filter** | any | Filter by any numeric attribute with min/max (dropdown adapts to entity type) |
| **Match Filter** | any | Filter by matching a string attribute against a pattern |
| **Track Filter** | track | Remove tracks that appear in the red input |
| **Title Filter** | track | Filter by track title (regex supported) |
| **Artist De-Dup** | track | Keep only first track per artist |
| **Max Tracks Per Artist** | track | Limit how many tracks by any single artist can pass through |
| **Artist Separation** | track | Enforce minimum gap between same-artist tracks |
| **Simple Artist Filter** | track | Exclude tracks by artist name |
| **Artist Filter** | track | Exclude tracks whose artist appears in red input |
| **Date Filter** | track | Filter by release date range |
| **Explicit** | track | Keep only explicit or only clean tracks |
| **Danceable** | track | Filter by danceability |
| **Energy** | track | Filter by energy |
| **Live** | track | Filter by liveness |
| **Spoken Word** | track | Filter by speechiness |
| **Tempo** | track | Filter by BPM range |

### Combiners — merge streams

| Component | Entity types | Description |
|-----------|-------------|-------------|
| **Alternate** | any | Interleave items round-robin from multiple inputs |
| **Shuffle** | any | Randomly reorder all items |
| **Concatenate** | any | Append streams end-to-end |
| **Random** | any | Randomly interleave from multiple streams |
| **Random Stream** | any | Pick one entire stream at random |
| **Mix In** | any | Blend a secondary stream at a configurable ratio |
| **Mixer** | track | Advanced multi-stream mix with dedup and exclusions |

### Selectors — pick subsets

| Component | Entity types | Description |
|-----------|-------------|-------------|
| **First** | any | First N items |
| **Last** | any | Last N items |
| **Sample** | any | Random N items |
| **All But First** | any | Skip first N items |
| **All But Last** | any | Drop last N items |
| **Pager** | any | Page through a source across multiple runs |
| **No Longer Than** | track | Items up to a total time limit |
| **No Shorter Than** | track | Items until a minimum duration is met |

### Orders — sort and arrange

| Component | Entity types | Description |
|-----------|-------------|-------------|
| **Sort** | any | Sort by any attribute (dropdown adapts to entity type) |
| **Reverse** | any | Reverse the item order |
| **Weighted Shuffle** | any | Shuffle with controllable randomness |
| **Separate Artists** | track | Maximize distance between same-artist tracks |
| **Smart Mix** | track | Key/tempo-aware ordering for DJ-style transitions |
| **Multi-Objective Sequencer** | track | Advanced multi-objective track ordering |

### Conditionals — branch on conditions

| Component | Description |
|-----------|-------------|
| **Is Weekend?** | Green on weekends, red on weekdays |
| **Is Day of Week** | Route based on current day |
| **Yes or No** | Manual switch between two streams |

### Outputs — save side branches

| Component | Description |
|-----------|-------------|
| **Save to Playlist** | Save to an existing or new playlist (side effect) |
| **Save to New Playlist** | Create a new playlist with auto-generated name |
