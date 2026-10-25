$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$utf8 = [System.Text.Encoding]::UTF8
$t = [IO.File]::ReadAllText((Join-Path $dir '_riset\main_bundle.js'), $utf8)
$out = New-Object System.Text.StringBuilder

$needles = @('edges:', 'main_node_id', 'toProgramJson', 'fromProgramJson', 'serialize', 'program_json')
foreach ($nd in $needles) {
    $i = 0; $n = 0
    while ($n -lt 6) {
        $i = $t.IndexOf($nd, $i)
        if ($i -lt 0) { break }
        $start = [Math]::Max(0, $i - 400)
        $snippet = $t.Substring($start, [Math]::Min(1000, $t.Length - $start))
        [void]$out.AppendLine("### NEEDLE [$nd] at $i")
        [void]$out.AppendLine($snippet)
        [void]$out.AppendLine()
        $i += $nd.Length; $n++
    }
}
[IO.File]::WriteAllText((Join-Path $dir '_riset\program_json_matches.txt'), $out.ToString(), $utf8)
Write-Output 'WROTE _riset\program_json_matches.txt'
