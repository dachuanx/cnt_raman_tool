# Test version with controlled line counts to demonstrate stop condition

param(
    [int]$MaxIterations = 10,
    [int]$DelaySeconds = 1
)

# Predefined line counts for testing
# Let's create a scenario where we get >5 lines for 3 consecutive images
# but NOT 7, so we should stop
$predefinedCounts = @(3, 5, 6, 8, 9, 6, 4, 8, 9, 10)
$currentTestIndex = 0

function Capture-Screenshot {
    param(
        [string]$OutputPath = "test_screenshot_$(Get-Date -Format 'yyyyMMdd_HHmmss').png"
    )
    
    try {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        
        $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
        $bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose()
        $bitmap.Dispose()
        
        Write-Host "Screenshot saved to: $OutputPath"
        return $OutputPath
    }
    catch {
        Write-Host "Error capturing screenshot: $_"
        return $null
    }
}

function Get-TestLineCount {
    # Use predefined counts for testing
    if ($currentTestIndex -lt $predefinedCounts.Count) {
        $count = $predefinedCounts[$currentTestIndex]
        $currentTestIndex++
        return $count
    } else {
        # Fallback to random
        return (Get-Random -Minimum 3 -Maximum 12)
    }
}

function Check-StopCondition {
    param(
        [array]$RecentResults
    )
    
    if ($RecentResults.Count -lt 3) {
        return $false
    }
    
    # Check if all 3 have >5 lines
    $allGreaterThan5 = $true
    foreach ($result in $RecentResults) {
        if ($result -le 5) {
            $allGreaterThan5 = $false
            break
        }
    }
    
    if (-not $allGreaterThan5) {
        return $false
    }
    
    # Check if NOT 7 (i.e., none of them are exactly 7)
    $noneAreSeven = $true
    foreach ($result in $RecentResults) {
        if ($result -eq 7) {
            $noneAreSeven = $false
            break
        }
    }
    
    return $noneAreSeven
}

# Main execution
Write-Host "=== Line Detection Test System ==="
Write-Host "Rules:"
Write-Host "1. Stop when 3 consecutive images have >5 lines"
Write-Host "2. AND those lines are NOT 7"
Write-Host ""
Write-Host "Using predefined test sequence: $($predefinedCounts -join ', ')"
Write-Host ""
Write-Host "Starting iteration (max: $MaxIterations, delay: ${DelaySeconds}s)"
Write-Host ""

$iteration = 0
$consecutiveCount = 0
$lineCounts = @()
$recentResults = @()
$stopConditionMet = $false

while ($iteration -lt $MaxIterations -and -not $stopConditionMet) {
    $iteration++
    Write-Host "--- Iteration $iteration ---"
    
    # Capture screenshot
    $screenshotFile = Capture-Screenshot
    if (-not $screenshotFile) {
        Write-Host "Failed to capture screenshot, skipping iteration"
        Start-Sleep -Seconds $DelaySeconds
        continue
    }
    
    # Get line count (from test sequence)
    $lineCount = Get-TestLineCount
    $lineCounts += $lineCount
    
    # Update recent results (keep only last 3)
    $recentResults += $lineCount
    if ($recentResults.Count -gt 3) {
        $recentResults = $recentResults[-3..-1]
    }
    
    Write-Host "Line count: $lineCount"
    
    # Check conditions
    if ($lineCount -gt 5) {
        $consecutiveCount++
        Write-Host "  Lines > 5 (consecutive: $consecutiveCount)"
        
        if ($consecutiveCount -ge 3) {
            Write-Host "  >>> 3 consecutive images with >5 lines detected!"
            
            $shouldStop = Check-StopCondition -RecentResults $recentResults
            if ($shouldStop) {
                Write-Host "  >>> STOP CONDITION MET: Lines are NOT 7"
                Write-Host "  >>> Iteration stopped"
                $stopConditionMet = $true
            } else {
                Write-Host "  >>> Continue: Some images have exactly 7 lines"
            }
        }
    } else {
        $consecutiveCount = 0
        Write-Host "  Lines ≤ 5 (reset consecutive count)"
    }
    
    Write-Host "  Recent results (last 3): $($recentResults -join ', ')"
    Write-Host ""
    
    # Delay before next iteration (unless we're stopping)
    if (-not $stopConditionMet -and $iteration -lt $MaxIterations) {
        Write-Host "Waiting ${DelaySeconds} seconds before next iteration..."
        Start-Sleep -Seconds $DelaySeconds
        Write-Host ""
    }
}

# Summary
Write-Host "=== Summary ==="
Write-Host "Total iterations: $iteration"
Write-Host "Stop condition met: $stopConditionMet"
Write-Host ""

if ($lineCounts.Count -gt 0) {
    Write-Host "Line counts per iteration:"
    for ($i = 0; $i -lt $lineCounts.Count; $i++) {
        Write-Host "  Iteration $($i+1): $($lineCounts[$i]) lines"
    }
}

Write-Host ""
Write-Host "=== Analysis ==="
if ($stopConditionMet) {
    Write-Host "SUCCESS: Task completed! Stop condition was met."
    Write-Host "The system correctly detected:"
    Write-Host "1. 3 consecutive images with >5 lines"
    Write-Host "2. None of those images had exactly 7 lines"
} else {
    Write-Host "Stop condition was not met. Possible reasons:"
    Write-Host "1. Not enough consecutive images with >5 lines"
    Write-Host "2. Some images had exactly 7 lines"
    Write-Host "3. Maximum iterations reached"
}

# Clean up test files
Write-Host ""
Write-Host "Cleaning up test screenshots..."
$testFiles = Get-ChildItem -Path . -Filter "test_screenshot_*.png" -File
foreach ($file in $testFiles) {
    try {
        Remove-Item $file.FullName -Force
        Write-Host "  Deleted: $($file.Name)"
    } catch {
        Write-Host "  Could not delete: $($file.Name)"
    }
}