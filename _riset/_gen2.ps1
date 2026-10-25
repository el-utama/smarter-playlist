$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$know = Join-Path $dir 'knowledge'
if (-not (Test-Path (Join-Path $know 'data'))) { New-Item -ItemType Directory -Path (Join-Path $know 'data') | Out-Null }
$utf8 = [System.Text.Encoding]::UTF8

# copy raw data into knowledge/data for traceability
Copy-Item (Join-Path $dir 'raw_inventory.json')   (Join-Path $know 'data\inventory.json') -Force
Copy-Item (Join-Path $dir 'raw_objectives.json')  (Join-Path $know 'data\objectives.json') -Force
Copy-Item (Join-Path $dir 'raw_changelog.json')   (Join-Path $know 'data\changelog.json') -Force
Copy-Item (Join-Path $dir 'guide_tutorial_raw.md') (Join-Path $know 'data\tutorial-original.md') -Force
Write-Output 'raw data copied'

# ================= 10 MOS objectives =================
$objs = [IO.File]::ReadAllText((Join-Path $dir 'raw_objectives.json'), $utf8) | ConvertFrom-Json
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('# Node: Multi-Objective Sequencer (MOS)')
[void]$sb.AppendLine()
[void]$sb.AppendLine('> Sebagian besar penjelasan konsep ada di ``10-mos.md``; file ini adalah **referensi teknis 14 objective** yang dikonfigurasi di dalam node, langsung dari ``/api/objectives`` (v3.12.3).')
[void]$sb.AppendLine()
[void]$sb.AppendLine('Skema umum semua objective:')
[void]$sb.AppendLine()
[void]$sb.AppendLine('- **field** - attribute numerik/teks/list yang dipakai (daftar attribute untuk track ada di ``09-attributes.md``)')
[void]$sb.AppendLine('- **weight** - ``off | lowest | low | medium | high | highest | unbreakable`` (bila ``allow_unbreakable``: true)')
[void]$sb.AppendLine('- Beberapa objective punya slot ``1-5``, ``3/8`` dsb. (posisi 1-indexed) untuk membatasi posisi berlaku')
[void]$sb.AppendLine()
[void]$sb.AppendLine('Tabel ringkasan:')
[void]$sb.AppendLine()
[void]$sb.AppendLine('| Objective |Deskripsi singkat |unbreakable|')
[void]$sb.AppendLine('|---|---|---|')
foreach ($o in $objs) {
    $ub = if ($o.allow_unbreakable) { 'ya' } else { 'tidak' }
    [void]$sb.AppendLine("| ``$($o.name)`` | $($o.description) | $ub |")
}
[void]$sb.AppendLine()
[void]$sb.AppendLine('---')
[void]$sb.AppendLine()
[void]$sb.AppendLine('## Detail parameter per objective')
[void]$sb.AppendLine()
function Format-ObjParam($p, $k) {
    $title = if ($p.PSObject.Properties['title']) { $p.title } else { $k }
    $ptype = $p.type
    if ($ptype -eq $null) { $ptype = '-' }
    if ($p.PSObject.Properties['anyOf']) { $ptype = ($p.anyOf | ForEach-Object { $_.type }) -join ' / ' }
    $def = ''
    if ($p.PSObject.Properties['default']) {
        $d = $p.default
        if ($d -is [bool]) { $def = if ($d) { 'true' } else { 'false' } } else { $def = "$d" }
    }
    $en = ''
    if ($p.PSObject.Properties['enum'] -and $p.enum) { $en = ($p.enum | ForEach-Object { "$_" }) -join ', ' }
    if ($p.PSObject.Properties['items'] -and $p.items -and $p.items.type -eq 'object') { $en = 'array-of-object (mengikuti UI)' }
    $line = "- **$title** ``$k`` - $ptype"
    if ($def -ne '') { $line += ", default: ``$def``" }
    if ($en) { $line += ". Nilai: ``$en``" }
    if ($p.PSObject.Properties['description'] -and $p.description) { $line += ". $($p.description)" }
    return $line
}
foreach ($o in $objs) {
    [void]$sb.AppendLine("### ``$($o.name)``")
    [void]$sb.AppendLine()
    [void]$sb.AppendLine($o.display + ": " + $o.description)
    [void]$sb.AppendLine()
    if ($o.PSObject.Properties['params'] -and $o.params -and $o.params.PSObject.Properties['properties']) {
        foreach ($p in $o.params.properties.PSObject.Properties) {
            [void]$sb.AppendLine((Format-ObjParam $p.Value $p.Name))
        }
    }
    [void]$sb.AppendLine()
    [void]$sb.AppendLine("Bisa ``unbreakable``: $(if ($o.allow_unbreakable) { 'ya' } else { 'tidak (objective ini ranking, gunakan berat ``highest``)' })")
    if ($o.PSObject.Properties['params'] -and $o.params -and $o.params.PSObject.Properties['properties'] -and $o.params.properties.ToString()) {}
    [void]$sb.AppendLine()
}
$file = Join-Path $know '10-mos-objectives.md'
[IO.File]::WriteAllText($file, $sb.ToString(), $utf8)
Write-Output ('WROTE ' + $file)

# ================= 12 changelog =================
$cl = [IO.File]::ReadAllText((Join-Path $dir 'raw_changelog.json'), $utf8) | ConvertFrom-Json
$sb2 = New-Object System.Text.StringBuilder
[void]$sb2.AppendLine('# Changelog SmarterPlaylists')
[void]$sb2.AppendLine()
[void]$sb2.AppendLine("> Sumber: ``/api/changelog`` (diunduh saat riset, v3.12.3); 206 entri sejak 0.2.0 (2026-03-04). Bagian ini menampilkan semua entri fitur utama per versi; catatan minor/fix dikelompokkan.")
[void]$sb2.AppendLine()
foreach ($e in $cl) {
    [void]$sb2.AppendLine("## v$($e.version) ($($e.date))")
    [void]$sb2.AppendLine()
    if ($e.PSObject.Properties['changes'] -and $e.changes) {
        foreach ($c in $e.changes) {
            $t = if ($c.PSObject.Properties['type']) { $c.type } else { 'note' }
            $d = if ($c.PSObject.Properties['description']) { $c.description } else { "$c" }
            [void]$sb2.AppendLine("- **$t**: $d")
        }
    } elseif ($e.PSObject.Properties['notes'] -and $e.notes) {
        foreach ($nt in $e.notes) { [void]$sb2.AppendLine("- $nt") }
    }
    [void]$sb2.AppendLine()
}
$file2 = Join-Path $know '12-changelog.md'
[IO.File]::WriteAllText($file2, $sb2.ToString(), $utf8)
Write-Output ('WROTE ' + $file2 + ' (' + $cl.Count + ' versi)')
