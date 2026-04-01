# GitHub推送指南

## 已完成的工作

我已经为您完成了以下工作：

1. **创建了英文README文件**：`README_EN.md` - 完整的英文项目文档
2. **更新了项目文件**：添加了推送脚本和说明文档
3. **提交了所有更改**：所有更改已提交到本地Git仓库

## 需要您手动完成的操作

由于GitHub推送需要认证，请您手动完成以下步骤：

### 方法1：使用Git Bash推送（推荐）

1. 打开Git Bash（在开始菜单中搜索"Git Bash"）
2. 切换到项目目录：
   ```bash
   cd /g/doctorcode/1DMaterialsAnalysisTool
   ```
3. 推送代码到GitHub：
   ```bash
   git push origin main
   ```
4. 如果提示输入用户名和密码：
   - 用户名：您的GitHub用户名
   - 密码：使用GitHub Personal Access Token（不是登录密码）

### 方法2：使用命令提示符推送

1. 打开命令提示符（cmd）
2. 切换到项目目录：
   ```cmd
   cd /d G:\doctorcode\1DMaterialsAnalysisTool
   ```
3. 推送代码：
   ```cmd
   "D:\Program Files\Git\bin\git.exe" push origin main
   ```

### 方法3：使用GitHub Desktop（最简单）

1. 打开GitHub Desktop
2. 添加本地仓库：File → Add Local Repository
3. 选择目录：`G:\doctorcode\1DMaterialsAnalysisTool`
4. 点击"Push origin"按钮

## 如果遇到认证问题

### 创建GitHub Personal Access Token

1. 登录GitHub网站
2. 点击右上角头像 → Settings → Developer settings → Personal access tokens → Tokens (classic)
3. 点击"Generate new token (classic)"
4. 设置权限（至少选择"repo"）
5. 生成token并复制

### 使用token推送

在Git Bash或命令提示符中：
```bash
git push https://<您的用户名>:<您的token>@github.com/dachuanx/cnt_raman_tool.git main
```

## 项目文件说明

- `README_EN.md` - 英文项目文档
- `README.md` - 中文项目文档
- `1Dtool.py` - 主程序文件
- `pages/` - 各功能模块界面
- `requirements.txt` - Python依赖包
- `dist/` - 可执行文件目录

## 项目功能概述

这是一个用于分析一维材料光谱数据的桌面应用程序，主要功能包括：

1. **拉曼光谱分析**：峰值检测、基线校正、多谱图对比
2. **吸收光谱分析**：吸收曲线绘制、带隙计算
3. **透射率分析**：透射曲线可视化
4. **现代化界面**：基于PyQt5和QFluentWidgets的现代UI

## 验证推送是否成功

推送完成后，请访问以下链接查看：
https://github.com/dachuanx/cnt_raman_tool

如果看到最新的提交记录和英文README文件，说明推送成功。