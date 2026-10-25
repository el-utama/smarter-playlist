$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\USER\Documents\OpenCode\smart-playlist'
$inv = Get-Content (Join-Path $dir 'raw_inventory.json') -Raw | ConvertFrom-Json
Write-Output ("COMPONENT COUNT: " + $inv.Count)
Write-Output ""
Write-Output "=== COMPONENT LIST ==="
foreach ($c in $inv) {
    Write-Output ("{0} | display={1} | type={2} | out={3} | refs={4}" -f $c.name, $c.display, $c.component_type, $c.output_type, $c.refs)
}
Write-Output ""
Write-Output "=== PARAM KEYS PER COMPONENT ==="
foreach ($c in $inv) {
    $params = @()
    if ($c.PSObject.Properties['params'] -and $c.params) { foreach ($p in $c.params) { $params += $p.name } }
    else { $params += '(none)' }
    $ports = @()
    if ($c.PSObject.Properties['ports'] -and $c.ports) { foreach ($po in $c.ports) { $ports += ('{0}(in:{1})' -f $po.port, $po.max_inputs) } }
    Write-Output ("{0}: ports=[{1}] params=[{2}]" -f $c.name, ($ports -join ','), ($params -join ','))
}
