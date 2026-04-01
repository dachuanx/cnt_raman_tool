Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$screens = [System.Windows.Forms.Screen]::AllScreens
foreach ($screen in $screens) {
    $bounds = $screen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    
    $filename = "screen_" + $screen.DeviceName.Replace('\', '_') + ".png"
    $path = Join-Path "C:\Users\shida\.openclaw\workspace" $filename
    $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    
    Write-Host "Screenshot saved to: $path"
    
    $graphics.Dispose()
    $bitmap.Dispose()
}

Write-Host "All screens captured successfully!"