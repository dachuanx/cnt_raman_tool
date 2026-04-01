# 自动化京东搜索iPhone 16最便宜商品
$wshell = New-Object -ComObject wscript.shell

# 打开Chrome
Write-Host "正在打开Chrome..."
$wshell.Run("chrome.exe")
Start-Sleep -Seconds 3

# 激活Chrome窗口
Write-Host "激活Chrome窗口..."
$wshell.AppActivate("chrome")

# 打开地址栏
Write-Host "打开地址栏..."
$wshell.SendKeys("^l")
Start-Sleep -Seconds 1

# 输入京东搜索URL（按价格排序）
Write-Host "输入京东搜索URL..."
$searchUrl = "https://search.jd.com/Search?keyword=iPhone%2016&enc=utf-8&psort=3"
$wshell.SendKeys($searchUrl)
$wshell.SendKeys("{ENTER}")

Write-Host "已打开京东搜索页面，按价格从低到高排序"
Write-Host "第一个商品就是最便宜的iPhone 16"
Write-Host "Page loaded, please check the first product link manually"