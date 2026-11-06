param([string]$DocPath = "Campus_Lost_and_Found_Project_Documentation.docx")
$absPath = (Resolve-Path $DocPath).Path
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($absPath)
    $pages = $d.ComputeStatistics(2)
    Write-Host "PAGES_COUNT: $pages"
    $d.Close([ref][Microsoft.Office.Interop.Word.WdSaveOptions]::wdDoNotSaveChanges)
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
}
