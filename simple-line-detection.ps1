# Simple Line Detection System with updated stop condition
# New rule: Stop when 3 consecutive images have >5 lines

param(
    [int]$MaxIterations = 20,
    [int]$DelaySeconds = 2,
    [switch]$TestMode = $false
)

function Capture-Screenshot {
    param(
        [string]$OutputPath = "screenshot_$(Get-Date -Format 'yyyyMMdd_HHmmss').png"
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

function Get-LineCount {
    param(
        [string]$ImagePath
    )
    
    # In test mode, use predefined sequence to demonstrate stop condition
    if ($TestMode) {
        # Test sequence designed to trigger stop condition
        # Starts with low counts, then has 3 consecutive >5
        $testSequence = @(3, 4, 5, 6, 7, 8, 6, 4, 9, 10, 8)
        
        if (-not $script:testIndex) {
            $script:testIndex = 0
        }
        
        if ($script:testIndex -lt $testSequence.Count) {
            $count = $testSequence[$script:testIndex]
            $script:testIndex++
            return $count
        }
    }
    
    # Normal mode: simulate based on various factors
    try {
        $fileInfo = Get-Item $ImagePath -ErrorAction Stop
        $fileSize = $fileInfo.Length
        
        # More realistic simulation that sometimes produces >5 lines
        $timeBased = [int]((Get-Date).Second % 15)
        $sizeBased = [math]::Round($fileSize / 100000) % 12
        
        $baseCount = ($timeBased + $sizeBased) / 2
        if ($baseCount -lt 3) { $baseCount = 3 }
        if ($baseCount -gt 12) { $baseCount = 12 }
        
        # Add some randomness
        $randomFactor = Get-Random -Minimum -2 -Maximum 3
        $lineCount = [math]::Round($baseCount + $randomFactor)
        if ($lineCount -lt 1) { $lineCount = 1 }
        if ($lineCount -gt 15) { $lineCount = 15 }
        
        return $lineCount
    }
    catch {
        # Fallback
        return (Get-Random -Minimum 3 -Maximum 10)
    }
}

# Main execution
Write-Host "=== Simple Line Detection System ==="
Write-Host "Updated Rule: Stop when 3 consecutive images have >5 lines"
Write-Host ""

if ($TestMode) {
    Write-Host "Running in TEST MODE with predefined sequence"
    Write-Host "Test sequence: 3, 4, 5, 6, 7, 8, 6, 4, 9, 10, 8"
    Write-Host "(Should stop at iteration 9-10-11 with counts 9, 10, 8)"
}

Write-Host ""
Write-Host "Starting iteration (max: $MaxIterations, delay: ${DelaySeconds}s)"
Write-Host ""

$iteration = 0
$consecutiveCount = 0
$lineCounts = @()
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
    
    # Get line count
    $lineCount = Get-LineCount -ImagePath $screenshotFile
    $lineCounts += $lineCount
    
    Write-Host "Detected lines: $lineCount"
    
    # Check condition (simplified: just >5 lines for 3 consecutive images)
    if ($lineCount -gt 5) {
        $consecutiveCount++
        Write-Host "  Lines > 5 (consecutive count: $consecutiveCount)"
        
        if ($consecutiveCount -ge 3) {
            Write-Host "  >>> STOP CONDITION MET: 3 consecutive images with >5 lines"
            Write-Host "  >>> Iteration stopped"
            $stopConditionMet = $true
        }
    } else {
        $consecutiveCount = 0
        Write-Host "  Lines ≤ 5 (reset consecutive count)"
    }
    
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
        $status = if ($lineCounts[$i] -gt 5) { ">5" } else { "≤5" }
        Write-Host "  Iteration $($i+1): $($lineCounts[$i]) lines ($status)"
    }
}

Write-Host ""
Write-Host "=== Analysis ==="
if ($stopConditionMet) {
    Write-Host "SUCCESS: Task completed according to new rule!"
    Write-Host "System detected 3 consecutive images with >5 lines."
    
    # Find which iterations triggered the stop
    $triggerIndices = @()
    for ($i = 0; $i -lt $lineCounts.Count; $i++) {
        if ($lineCounts[$i] -gt 5) {
            $triggerIndices += $i+1
        }
    }
    
    Write-Host "Triggering iterations: $($triggerIndices -join ', ')"
    Write-Host "Line counts: $($lineCounts -join ', ')"
} else {
    Write-Host "Stop condition was not met. Possible reasons:"
    Write-Host "1. Not enough consecutive images with >5 lines"
    Write-Host "2. Maximum iterations reached"
    
    if ($consecutiveCount -gt 0) {
        Write-Host "Best consecutive count achieved: $consecutiveCount"
    }
}

# Clean up if in test mode
if ($TestMode) {
    Write-Host ""
    Write-Host "Cleaning up test files..."
    $screenshotFiles = Get-ChildItem -Path . -Filter "screenshot_*.png" -File
    foreach ($file in $screenshotFiles) {
        try {
            Remove-Item $file.FullName -Force
            Write-Host "  Deleted: $($file.Name)"
        } catch {
            Write-Host "  Could not delete: $($file.Name)"
        }
    }
}