param(
    [string]$DocPath = "Campus_Lost_and_Found_Project_Documentation.docx",
    [string]$PdfPath = "Campus_Lost_and_Found_Project_Documentation.pdf"
)
$absDoc = (Resolve-Path $DocPath).Path
$absPdf = [System.IO.Path]::GetFullPath($PdfPath)
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($absDoc)
    $pages = $d.ComputeStatistics(2)
    Write-Host "PAGES_COUNT: $pages"
    $d.SaveAs([ref]$absPdf, [ref]17)
    $d.Close([ref]0)
    Write-Host "PDF_EXPORTED: $absPdf"
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
}
