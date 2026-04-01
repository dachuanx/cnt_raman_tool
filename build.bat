@echo off
echo 计算器软件打包工具
echo ========================================

REM 检查Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python
    echo 请先安装Python 3.6或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 正在安装PyInstaller...
python -m pip install pyinstaller==6.0.0

if %errorlevel% neq 0 (
    echo PyInstaller安装失败
    pause
    exit /b 1
)

echo 开始构建exe文件...
python -m PyInstaller --name=Calculator --onefile --windowed --clean --noconfirm calculator.py

if %errorlevel% neq 0 (
    echo exe文件构建失败
    pause
    exit /b 1
)

echo 复制到桌面...
if exist "dist\Calculator.exe" (
    copy "dist\Calculator.exe" "%USERPROFILE%\Desktop\Calculator.exe"
    echo 成功! 计算器软件已保存到桌面: Calculator.exe
) else (
    echo 错误: 未找到生成的exe文件
)

echo.
echo 按任意键退出...
pause >nul