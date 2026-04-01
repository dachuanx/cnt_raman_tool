@echo off
echo 正在创建桌面计算器...
echo.

REM 复制HTML文件到桌面
copy "calculator.html" "%USERPROFILE%\Desktop\calculator.html"

REM 创建快捷方式批处理文件
echo @echo off > "%USERPROFILE%\Desktop\运行计算器.bat"
echo start "" "calculator.html" >> "%USERPROFILE%\Desktop\运行计算器.bat"

REM 创建使用默认浏览器打开的批处理文件
echo @echo off > "%USERPROFILE%\Desktop\打开计算器.bat"
echo start "" "%%USERPROFILE%%\Desktop\calculator.html" >> "%USERPROFILE%\Desktop\打开计算器.bat"

echo 计算器文件已创建到桌面！
echo.
echo 使用方法：
echo 1. 双击"运行计算器.bat" - 使用默认浏览器打开计算器
echo 2. 或直接双击"calculator.html"文件
echo.
echo 功能特点：
echo - 基本四则运算
echo - 科学计算功能（三角函数、对数、平方根等）
echo - 键盘支持
echo - 美观的界面设计
echo.
echo 按任意键退出...
pause >nul