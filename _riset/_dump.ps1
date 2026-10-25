$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$inv = Get-Content (Join-Path $dir 'raw_inventory.json') -Raw | ConvertFrom-Json
# dump a few representative components fully
foreach ($n in @('SpotifyPlaylist','AttributeRangeFilter','TrackFilter','MultiObjectiveSequencer','Mixer')) {
    $c = $inv | Where-Object { $_.name -eq $n }
    Write-Output ("===== " + $n + " =====")
    Write-Output ($c | ConvertTo-Json -Depth 10)
}
