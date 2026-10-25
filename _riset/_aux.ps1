$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'

# Changelog summary
$cl = Get-Content (Join-Path $dir 'raw_changelog.json') -Raw | ConvertFrom-Json
Write-Output ("CHANGELOG ENTRIES: " + $cl.Count)
foreach ($e in ($cl | Select-Object -First 12)) {
    Write-Output ("--- version: " + $e.version + " | date: " + $e.date)
    if ($e.PSObject.Properties['notes'] -and $e.notes) {
        foreach ($n in $e.notes) { Write-Output ("    * " + $n) }
    } elseif ($e.PSObject.Properties['changes'] -and $e.changes) {
        foreach ($n in $e.changes) { Write-Output ("    * " + ("{0}: {1}" -f $n.type, $n.description)) }
    }
}

# Download objectives info + version + motd
$dir2 = 'C:\Users\USER\AppData\Local\Temp\opencode'
Invoke-WebRequest -Uri "https://smarterplaylists.playlistmachinery.com/api/objectives" -OutFile (Join-Path $dir2 'sp_objectives.json') -UseBasicParsing
Invoke-WebRequest -Uri "https://smarterplaylists.playlistmachinery.com/api/version" -OutFile (Join-Path $dir2 'sp_version.json') -UseBasicParsing
Write-Output ""
Write-Output "VERSION FILE:"
Get-Content (Join-Path $dir2 'sp_version.json') -Raw
Write-Output ""
$co = Get-Content (Join-Path $dir2 'sp_objectives.json') -Raw
Write-Output ("OBJECTIVES JSON LEN: " + $co.Length)
Copy-Item (Join-Path $dir2 'sp_objectives.json') (Join-Path $dir 'raw_objectives.json')
# summarize objectives
$co2 = $co | ConvertFrom-Json
if ($co2 -is [array]) {
    Write-Output ("OBJECTIVES COUNT: " + $co2.Count)
    foreach ($o in $co2) {
        Write-Output ("OBJ: type=" + $o.type + " | name=" + $o.name + " | title=" + $o.title)
    }
} else {
    Write-Output $co.Substring(0, [Math]::Min(2000, $co.Length))
}
