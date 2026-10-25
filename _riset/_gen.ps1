$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$know = Join-Path $dir 'knowledge'
if (-not (Test-Path $know)) { New-Item -ItemType Directory -Path $know | Out-Null }
$utf8 = [System.Text.Encoding]::UTF8

$inv = [IO.File]::ReadAllText((Join-Path $dir 'raw_inventory.json'), $utf8) | ConvertFrom-Json

function Escape-Md($s) {
    if ($null -eq $s) { return '' }
    return ($s -replace '\|', '\|')
}

function Format-Param ($p, $key) {
    $lines = @()
    $title = if ($p.PSObject.Properties['title']) { $p.title } else { $key }
    $ptype = ''
    if ($p.PSObject.Properties['type']) { $ptype = $p.type }
    if ($p.PSObject.Properties['anyOf'] -and $p.anyOf) { $ptype = ($p.anyOf | ForEach-Object { $_.type }) -join ' / ' }
    $def = ''
    if ($p.PSObject.Properties['default']) {
        $d = $p.default
        if ($d -is [array]) { $def = '[' + (($d | ForEach-Object { "$_" }) -join ', ') + ']' }
        elseif ($d -is [bool]) { $def = if ($d) { 'true' } else { 'false' } }
        elseif ($null -ne $d) { $def = "$d" }
        else { $def = '(kosong)' }
    }
    # enum values
    $enumInfo = ''
    if ($p.PSObject.Properties['enum'] -and $p.enum) {
        $vals = $p.enum | ForEach-Object { "$_" }
        $enumInfo = ($vals -join ', ')
    }
    # items enum (array of enum)
    if ($p.PSObject.Properties['items'] -and $p.items -and $p.items.PSObject.Properties['oneOf'] -and $p.items.oneOf) {
        $parts = @()
        foreach ($variant in $p.items.oneOf) {
            if ($variant.PSObject.Properties['properties']) {
                $keys = @()
                foreach ($prop in $variant.properties.PSObject.Properties) {
                    $req = ''
                    if ($variant.PSObject.Properties['required'] -and $variant.required -contains $prop.Name) { $req = '*' }
                    $keys += ("`"$($prop.Name)`"$req")
                }
                $parts += ('{' + ($keys -join ', ') + '}')
            }
        }
        $enumInfo = $parts -join ' / '
    }
    # format for numeric
    $rng = ''
    if ($p.PSObject.Properties['minimum']) { $rng += "min $($p.minimum)" }
    if ($p.PSObject.Properties['maximum']) { if ($rng) { $rng += '; ' }; $rng += "max $($p.maximum)" }
    $rng = $rng.Trim()
    $desc = ''
    if ($p.PSObject.Properties['description']) { $desc = $p.description }
    # format field for display objects
    if ($p.PSObject.Properties['format'] -and $p.format -eq 'display') {
        if ($p.PSObject.Properties['options']) { $enumInfo = ($p.options | ForEach-Object { "$$_" }) -join ', ' }
    }
    $advanced = ''
    if ($p.PSObject.Properties['advanced'] -and $p.advanced) { $advanced = ' (lanjutan)' }
    $line = "- **$title**$advanced - tipe: $ptype"
    if ($def) { $line += ", default: ``$def``" }
    if ($rng) { $line += " (rentang: $rng)" }
    if ($enumInfo) { $line += ". Nilai: ``$enumInfo``" }
    if ($desc) { $line += ". $desc" }
    return $line
}

function Emit-Component ($c, $sb) {
    [void]$sb.AppendLine("### $($c.name)")
    [void]$sb.AppendLine()
    $label = if ($c.PSObject.Properties['display']) { $c.display } else { $c.name }
    $titleTpl = if ($c.PSObject.Properties['title_template']) { $c.title_template } else { '' }
    $outT = 'track'
    if ($c.PSObject.Properties['output_type'] -and $c.output_type) { $outT = $c.output_type }
    elseif ($outT -eq $null) { $outT = '(mengikuti input)' }
    $hidden = ''
    if ($c.PSObject.Properties['hidden'] -and $c.hidden) { $hidden = ' [tersembunyi]' }
    [void]$sb.AppendLine("**Label UI:** ``$label`` | **Output:** $outT | **Judul tampilan node:** ``$titleTpl``$hidden")
    [void]$sb.AppendLine()
    [void]$sb.AppendLine($c.description)
    [void]$sb.AppendLine()

    # Ports
    if ($c.PSObject.Properties['ports'] -and $c.ports) {
        [void]$sb.AppendLine('**Port input:**')
        [void]$sb.AppendLine()
        if ($c.ports.Count -gt 0 -and ($c.ports | Where-Object { $_.max_inputs -gt 0 })) {
            foreach ($po in $c.ports) {
                $desc = $po.description
                $acc = ''
                if ($po.PSObject.Properties['accepted_types'] -and $po.accepted_types -and $po.accepted_types.Count -gt 0) {
                    $acc = " (tipe: $($po.accepted_types -join ', '))"
                } else {
                    $acc = ' (generic: track/artist/album)'
                }
                $max = $po.max_inputs
                $maxTxt = if ($max -ge 100) { 'multi-input' } else { "maks $max" }
                [void]$sb.AppendLine("- Port ``$($po.port)`` - $maxTxt$acc - $desc")
            }
        } else {
            [void]$sb.AppendLine('Tidak ada input (sumber / bertanda parsial).')
        }
        [void]$sb.AppendLine()
    }

    # uri_resolve
    if ($c.PSObject.Properties['uri_resolve'] -and $c.uri_resolve) {
        $ur = $c.uri_resolve
        $nf = ''
        if ($ur.PSObject.Properties['name_fields'] -and $ur.name_fields) {
            $nf = (($ur.name_fields.PSObject.Properties | ForEach-Object { "$($_.Value) -> ``$($_.Name)``" }) -join ', ')
        }
        [void]$sb.AppendLine("**Resolusi URI:** field ``$($ur.uri_field)``, entitas ``$($ur.entity_type)``" + $(if ($nf) { "; pencarian nama: $nf" }))
        [void]$sb.AppendLine()
    }

    # params
    if ($c.PSObject.Properties['params'] -and $c.params -and $c.params.PSObject.Properties['properties'] -and $c.params.properties) {
        [void]$sb.AppendLine('**Parameter:**')
        [void]$sb.AppendLine()
        foreach ($prop in $c.params.properties.PSObject.Properties) {
            [void]$sb.AppendLine((Format-Param $prop.Value $prop.Name))
        }
        [void]$sb.AppendLine()
    } elseif ($c.PSObject.Properties['params'] -and -not $c.params) {
        [void]$sb.AppendLine('**Parameter:** tidak ada (konfigurasi penuh dilakukan oleh engine).')
        [void]$sb.AppendLine()
    }

    if ($c.PSObject.Properties['help'] -and $c.help) {
        [void]$sb.AppendLine('**Dokumentasi resmi (help):**')
        [void]$sb.AppendLine()
        [void]$sb.AppendLine($c.help)
        [void]$sb.AppendLine()
    }
}

$categoryOrder = @('source', 'adapter', 'filter', 'combiner', 'selector', 'order', 'conditional', 'output', 'annotation')
$categoryTitles = @{
    'source'      = 'Sources - Sumber Data'
    'adapter'     = 'Adapters - Konversi Tipe Entitas'
    'filter'      = 'Filters - Penyaring'
    'combiner'    = 'Combiners - Penggabung Stream'
    'selector'    = 'Selectors - Pemilih Item'
    'order'       = 'Orders - Pengurutan'
    'conditional' = 'Conditionals - Percabangan'
    'output'      = 'Outputs - Penyimpanan'
    'annotation'  = 'Annotations - Catatan'
}
$categoryDesc = @{
    'source'      = 'Komponen sumber menghasilkan stream entitas (track, artist, atau album) dari Spotify, Last.fm, atau chart publik. Setiap sumber adalah titik awal alur data; tidak menerima input.'
    'adapter'     = 'Adapter mengubah tipe entitas di dalam stream: track <-> artist <-> album, atau menghitung entitas terkait (misal artis serupa). Ini yang membuat program dapat berjalan lintas tipe: mulai dari artis, ekstrak album, lalu ubah kembali ke track.'
    'filter'      = 'Filter mengurangi stream: membuang item yang tidak memenuhi syarat. Port merah/oranye umumnya adalah daftar eksklusi (dibandingkan port hijau utama).'
    'combiner'    = 'Combiner menggabungkan dua input stream atau lebih menjadi satu stream baru, dengan strategi tertentu (interleave, acak, rasio campuran, atau sambung-sambung).'
    'selector'    = 'Selector memotong stream menjadi subset (N pertama, N terakhir, N acak, batas durasi, hingga paging antar-run). Berguna untuk mengontrol panjang playlist.'
    'order'       = 'Komponen urutan mengatur susunan item: sort deterministik, shuffle acak, shuffle tertimbang, hingga sequencer cerdas (Smart Mix dan Multi-Objective Sequencer).'
    'conditional' = 'Komponen kondisional memilih salah satu dari dua input berdasarkan kondisi waktu/jadwal - untuk playlist yang berubah perilaku, misalnya minggu vs. akhir minggu.'
    'output'      = 'Kecuali pada kasus khusus, TIDAK perlu menaruh komponen output di akhir program: run apa pun otomatis menyimpan hasil ke playlist Spotify bernama sama dengan program. Output digunakan hanya untuk menyimpan ' + 'cabang samping' + ' ke playlist lain.'
    'annotation'  = 'Komponen anotasi tidak masuk dalam alur data - dipakai untuk menandai program agar mudah dibaca.'
}

foreach ($ct in $categoryOrder) {
    $sb = New-Object System.Text.StringBuilder
    $title = $categoryTitles[$ct]
    $list = $inv | Where-Object { $_.component_type -eq $ct }
    $count = $list.Count
    [void]$sb.AppendLine('# ' + $title)
    [void]$sb.AppendLine()
    [void]$sb.AppendLine('> Dihasilkan otomatis dari ``/api/inventory`` **SmarterPlaylists v3.12.3** - total ' + $count + ' komponen dalam kategori ini.')
    [void]$sb.AppendLine()
    [void]$sb.AppendLine($categoryDesc[$ct])
    [void]$sb.AppendLine()
    $n = 0
    foreach ($c in $list) {
        Emit-Component $c $sb
        $sb.AppendLine('---') | Out-Null
        $sb.AppendLine() | Out-Null
        $n++
    }
    $file = Join-Path $know ("node-$ct.md")
    [IO.File]::WriteAllText($file, $sb.ToString(), $utf8)
    Write-Output ("WROTE " + $file + " (" + $n + " komponen)")
}
