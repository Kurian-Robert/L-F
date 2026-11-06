$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open((Resolve-Path "Campus_Lost_and_Found_Project_Documentation.docx").Path)
    $pages = $d.ComputeStatistics(2)
    Write-Host "Total Pages: $pages"

    $targets = @(
        "1. Title of the Project",
        "2. Introduction",
        "3. Objective of the Project",
        "4. Scope of the Project",
        "5. Software Specifications",
        "6. Workflow of the Project",
        "7. Modules of the Project",
        "7.1 Phase 1",
        "7.2 Phase 2",
        "7.3 Phase 3",
        "7.4 Phase 4",
        "7.7 Database Design",
        "7.7.2 Detailed Relational",
        "7.7.3 Database Normalization",
        "8. Source Code",
        "9. Features of the Project",
        "10. Future Enhancements",
        "11. Conclusion",
        "11.3 Academic References"
    )

    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        $pg = $p.Range.Information(3)
        if ($pg -ge 3) {
            foreach ($t in $targets) {
                if ($txt.StartsWith($t)) {
                    Write-Host "$t --> Page $pg"
                    break
                }
            }
        }
    }
    $d.Close([ref]0)
} finally {
    $w.Quit()
}

