# AIU Archive Search Tool
# Usage: .\search_archive.ps1 "search term"

param(
    [Parameter(Mandatory=$true)]
    [string]$SearchTerm,
    [int]$ContextLines = 2
)

$ArchivePath = "C:\Users\travi\AIU"
$TextFiles = @(
    "Genetic_Drift_extracted.txt",
    "Genetic Drift Introduction.txt",
    "Genetic Drift.txt",
    "Melon Baller 1.txt",
    "Melon Baller 2.txt",
    "MM&MAM19-21.txt",
    "Claude1_extracted.txt",
    "Trav_and_Claude.txt",
    "context_for_claude.md",
    "Context_for_emerging_work.txt",
    "Fire_and_Knives_extracted.txt",
    "YouTube Extraction\video_titles_chronological.txt"
)

Write-Host "`n=== AIU Archive Search ===" -ForegroundColor Cyan
Write-Host "Searching for: '$SearchTerm'" -ForegroundColor Yellow
Write-Host ""

$TotalMatches = 0

foreach ($file in $TextFiles) {
    $FilePath = Join-Path $ArchivePath $file
    if (Test-Path $FilePath) {
        $matches = Select-String -Path $FilePath -Pattern $SearchTerm -Context $ContextLines -AllMatches
        if ($matches) {
            $count = $matches.Count
            $TotalMatches += $count
            Write-Host "--- $file ($count matches) ---" -ForegroundColor Green
            foreach ($match in $matches) {
                Write-Host "  Line $($match.LineNumber):" -ForegroundColor DarkGray
                if ($match.Context.PreContext) {
                    $match.Context.PreContext | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
                }
                Write-Host "    $($match.Line)" -ForegroundColor White
                if ($match.Context.PostContext) {
                    $match.Context.PostContext | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
                }
                Write-Host ""
            }
        }
    }
}

Write-Host "=== Total: $TotalMatches matches ===" -ForegroundColor Cyan
