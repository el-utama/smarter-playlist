$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$utf8 = [System.Text.Encoding]::UTF8
$t = [IO.File]::ReadAllText((Join-Path $dir '_riset\main_bundle.js'), $utf8)
$out = New-Object System.Text.StringBuilder

# 1) All fetch/lib call sites around each /api/... literal
$i = 0
while ($true) {
    $i = $t.IndexOf('/api/', $i)
    if ($i -lt 0) { break }
    $start = [Math]::Max(0, $i - 260)
    $snippet = $t.Substring($start, [Math]::Min(700, $t.Length - $start))
    [void]$out.AppendLine("=== MATCH at $i ===")
    [void]$out.AppendLine($snippet)
    [void]$out.AppendLine()
    $i += 5
}
[IO.File]::WriteAllText((Join-Path $dir '_riset\api_matches.txt'), $out.ToString(), $utf8)
Write-Output ("TOTAL /api/ occurrences: " + ([regex]::Matches($t, '/api/')).Count)
Write-Output "WROTE _riset\api_matches.txt"
