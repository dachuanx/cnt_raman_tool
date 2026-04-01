@echo off
chcp 65001 >nul
echo Creating desktop calculator...

REM Copy HTML file to desktop
copy "calculator.html" "%USERPROFILE%\Desktop\calculator.html"

REM Create batch file to open calculator
echo @echo off > "%USERPROFILE%\Desktop\open_calculator.bat"
echo start "" "calculator.html" >> "%USERPROFILE%\Desktop\open_calculator.bat"

echo.
echo Calculator files created on desktop!
echo.
echo Files created:
echo 1. calculator.html - The calculator application
echo 2. open_calculator.bat - Batch file to open the calculator
echo.
echo How to use:
echo 1. Double-click "open_calculator.bat" to open the calculator
echo 2. Or double-click "calculator.html" directly
echo.
echo Features:
echo - Basic arithmetic operations
echo - Scientific functions (sin, cos, tan, log, sqrt, etc.)
echo - Keyboard support
echo - Beautiful modern interface
echo.
pause