# Test script to demonstrate the stop condition

Write-Host "=== Testing Stop Condition Logic ==="
Write-Host "Rule: Stop when 3 consecutive images have >5 lines AND lines are NOT 7"
Write-Host ""

# Test case 1: Should NOT stop (has 7)
Write-Host "Test Case 1: [6, 8, 7]"
$test1 = @(6, 8, 7)
Write-Host "  All >5? Yes"
Write-Host "  NOT 7? No (contains 7)"
Write-Host "  Should stop? No"
Write-Host ""

# Test case 2: Should STOP (all >5 and none are 7)
Write-Host "Test Case 2: [6, 8, 9]"
$test2 = @(6, 8, 9)
Write-Host "  All >5? Yes"
Write-Host "  NOT 7? Yes (none are 7)"
Write-Host "  Should stop? Yes"
Write-Host ""

# Test case 3: Should NOT stop (not all >5)
Write-Host "Test Case 3: [6, 4, 8]"
$test3 = @(6, 4, 8)
Write-Host "  All >5? No (contains 4)"
Write-Host "  Should stop? No"
Write-Host ""

# Test case 4: Should NOT stop (has 7)
Write-Host "Test Case 4: [7, 7, 7]"
$test4 = @(7, 7, 7)
Write-Host "  All >5? Yes"
Write-Host "  NOT 7? No (all are 7)"
Write-Host "  Should stop? No"
Write-Host ""

# Test case 5: Should STOP (all >5 and none are 7)
Write-Host "Test Case 5: [6, 6, 6]"
$test5 = @(6, 6, 6)
Write-Host "  All >5? Yes"
Write-Host "  NOT 7? Yes (none are 7)"
Write-Host "  Should stop? Yes"
Write-Host ""

# Function to check condition
function Test-Condition {
    param([array]$values)
    
    if ($values.Count -lt 3) {
        return $false
    }
    
    # Check all >5
    $allGreaterThan5 = $true
    foreach ($v in $values) {
        if ($v -le 5) {
            $allGreaterThan5 = $false
            break
        }
    }
    
    if (-not $allGreaterThan5) {
        return $false
    }
    
    # Check NOT 7
    $noneAreSeven = $true
    foreach ($v in $values) {
        if ($v -eq 7) {
            $noneAreSeven = $false
            break
        }
    }
    
    return $noneAreSeven
}

Write-Host "=== Automated Tests ==="
$tests = @(
    @{Name="Test 1: [6,8,7]"; Values=@(6,8,7); Expected=$false},
    @{Name="Test 2: [6,8,9]"; Values=@(6,8,9); Expected=$true},
    @{Name="Test 3: [6,4,8]"; Values=@(6,4,8); Expected=$false},
    @{Name="Test 4: [7,7,7]"; Values=@(7,7,7); Expected=$false},
    @{Name="Test 5: [6,6,6]"; Values=@(6,6,6); Expected=$true},
    @{Name="Test 6: [8,9,10]"; Values=@(8,9,10); Expected=$true},
    @{Name="Test 7: [6,7,8]"; Values=@(6,7,8); Expected=$false}
)

foreach ($test in $tests) {
    $result = Test-Condition -values $test.Values
    $passed = $result -eq $test.Expected
    $status = if ($passed) { "PASS" } else { "FAIL" }
    Write-Host "$($test.Name): $status (Expected: $($test.Expected), Got: $result)"
}

Write-Host ""
Write-Host "=== Implementation Note ==="
Write-Host "The condition '不是7条' means 'NOT 7 lines'."
Write-Host "So we stop when:"
Write-Host "1. 3 consecutive images have >5 lines"
Write-Host "2. AND NONE of those 3 images have exactly 7 lines"
Write-Host ""
Write-Host "If ANY of the 3 images has exactly 7 lines, we continue."