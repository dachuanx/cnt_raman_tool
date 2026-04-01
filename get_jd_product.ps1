# 尝试获取京东商品信息
Write-Host "尝试获取京东页面信息..."

# 方法1：尝试使用Invoke-WebRequest（可能被屏蔽）
try {
    $url = "https://search.jd.com/Search?keyword=iPhone%2016&enc=utf-8&psort=3"
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
    Write-Host "页面获取成功，长度: $($response.Content.Length)"
    
    # 尝试提取商品链接
    $pattern = '//item\.jd\.com/\d+\.html'
    $matches = [regex]::Matches($response.Content, $pattern)
    if ($matches.Count -gt 0) {
        Write-Host "找到商品链接:"
        $matches[0..4] | ForEach-Object {
            $link = "https:$($_.Value)"
            Write-Host "  $link"
        }
    } else {
        Write-Host "未找到商品链接模式"
    }
} catch {
    Write-Host "直接获取页面失败: $($_.Exception.Message)"
}

# 方法2：提供手动操作指南
Write-Host "`n手动操作指南："
Write-Host "1. Chrome已打开京东搜索页面"
Write-Host "2. 页面按价格从低到高排序"
Write-Host "3. 第一个商品就是最便宜的iPhone 16"
Write-Host "4. 右键点击第一个商品 -> 复制链接地址"
Write-Host "5. 将链接粘贴给我即可"