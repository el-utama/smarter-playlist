$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$bundle = Join-Path $dir 'main_bundle.js'
Invoke-WebRequest -Uri 'https://smarterplaylists.playlistmachinery.com/assets/main-BuLZt-Yw.js' -OutFile $bundle -UseBasicParsing

$t = Get-Content $bundle -Raw

# --- Extract tutorial markdown template literal ---
$m = [regex]::Match($t, 'const Jg=`(.*?)`(?=,)', [System.Text.RegularExpressions.RegexOptions]::Singleline)
if (-not $m.Success) {
    # fallback: find start index and scan to terminated backtick
    $start = $t.IndexOf('const Jg=`') + 10
    $end = $t.IndexOf('`', $start)
    $tutorial = $t.Substring($start, $end - $start)
} else {
    $tutorial = $m.Groups[1].Value
}
$tutorial = $tutorial -replace '\\n', "`n"
$tpath = Join-Path $dir 'guide_tutorial_raw.md'
[IO.File]::WriteAllText($tpath, $tutorial)
Write-Output ("TUTORIAL CHARS: " + $tutorial.Length)

# --- Extract FAQ array ---
$fstart = $t.IndexOf('const fu=[')
if ($fstart -ge 0) {
    $fs = $fstart + 9
    # find matching close bracket by scan depth
    $depth = 0; $endIdx = -1; $inStr = $false;$q=[char]34; $esc=$false
    for ($i = $fs; $i -lt $t.Length; $i++) {
        $ch = $t[$i]
        if ($inStr) {
            if ($esc) { $esc = $false }
            elseif ($ch -eq '\') { $esc = $true }
            elseif ($ch -eq $q) { $inStr = $false }
            elseif ($ch -eq '`') { # template string escape... treat as normal char
            }
        } else {
            if ($ch -eq $q -or $ch -eq "'") { $inStr = $true }
            elseif ($ch -eq '[') { $depth++ }
            elseif ($ch -eq ']') { $depth--; if ($depth -eq 0) { $endIdx = $i; break } }
        }
    }
    $faqJson = $t.Substring($fs, $endIdx - $fs + 1)
    $fpath = Join-Path $dir 'faq_raw.json'
    [IO.File]::WriteAllText($fpath, $faqJson)
    Write-Output ("FAQ JSON CHARS: " + $faqJson.Length)
}

# --- extract changelog type counts ---
$cl = Get-Content (Join-Path $dir 'raw_changelog.json') -Raw | ConvertFrom-Json
Write-Output ("CHANGELOG: first version " + $cl[$cl.Count-1].version + " date " + $cl[$cl.Count-1].date + " ; count " + $cl.Count)
