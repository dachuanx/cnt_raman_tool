const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// 使用Windows自带的截图工具
const screenshotPath = path.join(process.cwd(), 'screenshot.png');

// 方法1: 使用PowerShell的截屏命令
const powershellCommand = `Add-Type -AssemblyName System.Windows.Forms;
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds;
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height);
$graphics = [System.Drawing.Graphics]::FromImage($bitmap);
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size);
$bitmap.Save('${screenshotPath}', [System.Drawing.Imaging.ImageFormat]::Png);
$graphics.Dispose();
$bitmap.Dispose();`;

// 执行PowerShell命令
exec(`powershell -Command "${powershellCommand.replace(/"/g, '\\"')}"`, (error, stdout, stderr) => {
  if (error) {
    console.error('Error taking screenshot:', error);
    
    // 方法2: 尝试使用nircmd（如果可用）
    exec('where nircmd', (error2) => {
      if (!error2) {
        exec(`nircmd savescreenshot "${screenshotPath}"`, (error3) => {
          if (error3) {
            console.error('NirCmd also failed:', error3);
            process.exit(1);
          } else {
            console.log(`Screenshot saved to: ${screenshotPath}`);
          }
        });
      } else {
        console.error('No screenshot method available');
        process.exit(1);
      }
    });
  } else {
    console.log(`Screenshot saved to: ${screenshotPath}`);
  }
});