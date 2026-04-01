@echo off
echo 正在推送到GitHub...
cd /d "G:\doctorcode\1DMaterialsAnalysisTool"

echo 检查Git状态...
"D:\Program Files\Git\bin\git.exe" status

echo.
echo 添加所有文件...
"D:\Program Files\Git\bin\git.exe" add .

echo.
echo 提交更改...
"D:\Program Files\Git\bin\git.exe" commit -m "Update project files and add English README"

echo.
echo 推送到GitHub...
"D:\Program Files\Git\bin\git.exe" push origin main

echo.
echo 完成！
pause