$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$utf8 = [System.Text.Encoding]::UTF8
$objs = [IO.File]::ReadAllText((Join-Path $dir 'raw_objectives.json'), $utf8) | ConvertFrom-Json
Write-Output "=== KEYS of first objective (maximize) ==="
$o = $objs[0]
$o.PSObject.Properties.Name | ForEach-Object { Write-Output ("KEY: " + $_) }
Write-Output ""
Write-Output ($o | ConvertTo-Json -Depth 6)
