# Evaluate actual v1-v5 versions in cntimage directory

$cntimagePath = "C:\Users\shida\Desktop\cntimage"

Write-Host "=== EVALUATING CNTIMAGE VERSIONS v1-v5 ==="
Write-Host "Directory: $cntimagePath"
Write-Host ""

# Check if directory exists
if (-not (Test-Path $cntimagePath)) {
    Write-Host "ERROR: cntimage directory not found at $cntimagePath"
    exit 1
}

# List all files
Write-Host "=== DIRECTORY CONTENTS ==="
$allFiles = Get-ChildItem -Path $cntimagePath -File
Write-Host "Total files: $($allFiles.Count)"
Write-Host ""

# Analyze version files
Write-Host "=== VERSION FILES ==="
$versionFiles = Get-ChildItem -Path $cntimagePath -Filter "test_v*.py" -File | Sort-Object Name
$versionDocs = Get-ChildItem -Path $cntimagePath -Filter "VERSION_v*.md" -File | Sort-Object Name

Write-Host "Python scripts (v1-v5):"
foreach ($file in $versionFiles) {
    Write-Host "  - $($file.Name) ($($file.Length) bytes)"
}

Write-Host ""
Write-Host "Version documentation:"
foreach ($file in $versionDocs) {
    Write-Host "  - $($file.Name) ($($file.Length) bytes)"
}

Write-Host ""
Write-Host "=== ORIGINAL IMAGES ==="
$originalImages = Get-ChildItem -Path $cntimagePath -Filter "cnt_*.png" -File | Sort-Object Name
Write-Host "Original CNT diffraction images: $($originalImages.Count)"
foreach ($img in $originalImages) {
    Write-Host "  - $($img.Name) ($($img.Length) bytes)"
}

Write-Host ""
Write-Host "=== RESULT FILES ANALYSIS ==="

# Analyze result files by version
$resultPatterns = @(
    @{Pattern="result_cnt_*.png"; Version="base"},
    @{Pattern="result_v1*.png"; Version="v1"},
    @{Pattern="result_v2*.png"; Version="v2"},
    @{Pattern="result_v3*.png"; Version="v3"},
    @{Pattern="result_v4*.png"; Version="v4"},
    @{Pattern="result_v5*.png"; Version="v5"}
)

$versionResults = @{}

foreach ($pattern in $resultPatterns) {
    $files = Get-ChildItem -Path $cntimagePath -Filter $pattern.Pattern -File
    if ($files.Count -gt 0) {
        $versionResults[$pattern.Version] = @{
            Count = $files.Count
            Files = $files
            TotalSize = ($files | Measure-Object -Property Length -Sum).Sum
            AvgSize = [math]::Round(($files | Measure-Object -Property Length -Average).Average, 0)
        }
    }
}

Write-Host "Result files by version:"
foreach ($version in $versionResults.Keys | Sort-Object) {
    $result = $versionResults[$version]
    Write-Host "  $version : $($result.Count) files, avg size: $($result.AvgSize) bytes"
}

Write-Host ""
Write-Host "=== VERSION SUMMARY FROM DOCUMENTATION ==="

# Read version summaries
foreach ($docFile in $versionDocs) {
    $version = $docFile.Name -replace 'VERSION_|\.md', ''
    Write-Host "--- $version ---"
    
    # Read first few lines for summary
    $content = Get-Content $docFile.FullName -TotalCount 20
    $summary = $content | Where-Object {$_ -match "策略|目标|问题|方法"} | Select-Object -First 3
    foreach ($line in $summary) {
        Write-Host "  $line"
    }
    Write-Host ""
}

Write-Host "=== ANALYSIS OF VERSION 5 (LATEST) ==="
$v5Doc = Get-Content "$cntimagePath\VERSION_v5.md" -TotalCount 50
$v5Summary = $v5Doc | Where-Object {$_ -match "目标|问题|策略|方法"} | Select-Object -First 10
foreach ($line in $v5Summary) {
    Write-Host "  $line"
}

Write-Host ""
Write-Host "=== KEY FINDINGS ==="
Write-Host ""

# Based on file analysis
Write-Host "1. VERSION PROGRESSION:"
Write-Host "   - v1 to v5: Progressive improvements"
Write-Host "   - v5 is latest: Uses projection analysis + peak detection"
Write-Host "   - v4 limitation: Could only detect 5 lines (from v5 docs)"

Write-Host ""
Write-Host "2. RESULT COVERAGE:"
Write-Host "   - Original images: 10"
Write-Host "   - v2 has most results: 8 files"
Write-Host "   - v5 has only 1 result: result_v5_cnt_0007_n8_m5.png"
Write-Host "   - Suggests v5 may be experimental or limited testing"

Write-Host ""
Write-Host "3. FILE SIZE ANALYSIS:"
Write-Host "   - Original images: ~4-10KB each"
Write-Host "   - Result images: ~40-200KB each"
Write-Host "   - Larger result files suggest detailed visualizations"

Write-Host ""
Write-Host "=== RECOMMENDATIONS FOR V6 ==="
Write-Host ""

# Based on v5 documentation analysis
Write-Host "From VERSION_v5.md analysis:"
Write-Host "1. V5 STRATEGY: Horizontal projection + peak detection"
Write-Host "2. V5 GOAL: Detect 7 horizontal lines (break through v4's 5-line limit)"
Write-Host "3. V5 METHOD: Convert 2D image to 1D signal processing"
Write-Host "4. V5 OUTPUT: 9-subplot visualization per image"

Write-Host ""
Write-Host "V6 DESIGN CONSIDERATIONS:"
Write-Host "1. BUILD ON V5: Start with projection analysis foundation"
Write-Host "2. ADDRESS V4 LIMIT: Ensure can detect 7+ lines when present"
Write-Host "3. IMPROVE PEAK DETECTION: Better noise filtering, adaptive thresholds"
Write-Host "4. ADD VALIDATION: Verify detected lines align with actual diffraction spots"
Write-Host "5. BATCH PROCESSING: Test on all 10 images, not just one"

Write-Host ""
Write-Host "V6 IMPLEMENTATION PLAN:"
Write-Host "1. Create test_v6.py in cntimage directory"
Write-Host "2. Extend v5's projection analysis with:"
Write-Host "   - Multiple projection methods (horizontal, vertical, diagonal)"
Write-Host "   - Advanced peak detection algorithms"
Write-Host "   - Line validation using original spot positions"
Write-Host "3. Test on all 10 images"
Write-Host "4. Generate comprehensive results and analysis"

Write-Host ""
Write-Host "=== NEXT STEPS ==="
Write-Host "1. Review v5 code in detail (test_v5.py)"
Write-Host "2. Analyze the single v5 result image"
Write-Host "3. Create v6 based on v5 foundation"
Write-Host "4. Test v6 on all 10 images"
Write-Host "5. Compare v6 results with previous versions"

# Save analysis report
$reportPath = "$cntimagePath\version_analysis_report.txt"
$report = @"
CNTIMAGE VERSION ANALYSIS REPORT
Analysis time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Directory: $cntimagePath

SUMMARY:
- 5 versions: v1 to v5
- 10 original CNT diffraction images
- Version progression documented in VERSION_v*.md files
- v5 is latest: projection analysis + peak detection

VERSION FILES:
$($versionFiles | ForEach-Object { "  - $($_.Name)" })

ORIGINAL IMAGES:
$($originalImages | ForEach-Object { "  - $($_.Name) ($($_.Length) bytes)" })

RESULT FILES BY VERSION:
$(foreach ($version in $versionResults.Keys | Sort-Object) {
    $result = $versionResults[$version]
    "  $version : $($result.Count) files"
})

V5 ANALYSIS (from VERSION_v5.md):
- Strategy: Horizontal projection analysis + peak detection
- Goal: Detect 7 horizontal lines
- Problem: v4 could only detect 5 lines
- Method: Convert 2D image to 1D signal processing
- Output: 9-subplot visualization per image

RECOMMENDATIONS FOR V6:
1. Build on v5's projection analysis foundation
2. Improve peak detection with adaptive thresholds
3. Add line validation against actual diffraction spots
4. Test on all 10 images (not just one)
5. Generate comprehensive comparison with previous versions
"@

$report | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Analysis report saved to: $reportPath"