$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$utf8 = [System.Text.Encoding]::UTF8

# Re-read bundle as UTF-8 and re-extract)
$t = [IO.File]::ReadAllText((Join-Path $dir 'main_bundle.js'), $utf8)

$m = [regex]::Match($t, 'const Jg=`(.*?)`\;function', [System.Text.RegularExpressions.RegexOptions]::Singleline)
if (-not $m.Success) { $m = [regex]::Match($t, 'const Jg=`(.*?)`(?=#|\n|\})', [System.Text.RegularExpressions.RegexOptions]::Singleline) }
$tutorial = $m.Groups[1].Value -replace '`',''
# unescape markdown backticks that were escaped in template literal
$tutorial = $tutorial -replace '\\`','`'
[IO.File]::WriteAllText((Join-Path $dir 'guide_tutorial_raw.md'), $tutorial, $utf8)
Write-Output ("TUTORIAL CHARS: " + $tutorial.Length + " ; template closed: " + $m.Success)

# FAQ re-extract
$fstart = $t.IndexOf('const fu=[')
$fs = $fstart + 9
$depth = 0; $endIdx = -1; $inStr = $false; $q=[char]34; $esc = $false; $inTpl = $false; $tplEsc = $false
for ($i = $fs; $i -lt $t.Length; $i++) {
    $ch = $t[$i]
    if ($inTpl) {
        if ($tplEsc) { $tplEsc = $false }
        elseif ($ch -eq '\') { $tplEsc = $true }
        elseif ($ch -eq '`') { $inTpl = $false }
    } elseif ($inStr) {
        if ($esc) { $esc = $false }
        elseif ($ch -eq '\') { $esc = $true }
        elseif ($ch -eq $q) { $inStr = $false }
    } else {
        if ($ch -eq '`') { $inTpl = $true }
        elseif ($ch -eq $q) { $inStr = $true }
        elseif ($ch -eq '[') { $depth++ }
        elseif ($ch -eq ']') { $depth--; if ($depth -eq 0) { $endIdx = $i; break } }
    }
}
$faqJson = $t.Substring($fs, $endIdx - $fs + 1)
[IO.File]::WriteAllText((Join-Path $dir 'faq_raw.json'), $faqJson, $utf8)
Write-Output ("FAQ JSON CHARS: " + $faqJson.Length)

# Parse FAQ and print questions
$faq = $faqJson | ConvertFrom-Json
Write-Output ("FAQ ENTRIES: " + $faq.Count)
foreach ($f in $faq) { Write-Output (" - " + $f.q) }

# objectives: summarize fully
$objs = [IO.File]::ReadAllText((Join-Path $dir 'raw_objectives.json'), $utf8) | ConvertFrom-Json
Write-Output ""
Write-Output "=== OBJECTIVE SCHEMA SAMPLE (maximize) ==="
foreach ($o in $objs) { if ($o.name -eq 'maximize') { Write-Output ($o | ConvertTo-Json -Depth 8) } }
