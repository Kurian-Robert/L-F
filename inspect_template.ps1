$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open((Resolve-Path "Project based Learning Documentation format.docx").Path)
    $pages = $d.ComputeStatistics(2)
    Write-Host "Total Template Pages: $pages"

    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(Contents|\d+\.)") {
            $pg = $p.Range.Information(3)
            Write-Host "Page $pg : $txt"
        }
    }
    $d.Close([ref][Microsoft.Office.Interop.Word.WdSaveOptions]::wdDoNotSaveChanges)
} finally {
    $w.Quit()
}
