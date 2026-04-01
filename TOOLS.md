# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Python环境配置

### Conda环境
- **主环境**: yolov11 (Python 3.9.24)
- **环境路径**: `D:\study\miniconda\envs\yolov11`
- **Python可执行文件**: `D:\study\miniconda\envs\yolov11\python.exe`

### 使用规则
1. **首选方式**: 总是使用完整路径调用Python
   ```bash
   D:\study\miniconda\envs\yolov11\python.exe script.py
   ```

2. **不推荐**: 使用`conda activate`命令（需要先运行`conda init`）

3. **验证方法**: 
   ```bash
   D:\study\miniconda\envs\yolov11\python.exe --version
   # 应输出: Python 3.9.24
   ```

4. **环境确认**: 
   ```bash
   D:\study\miniconda\Scripts\conda.exe info --envs
   # 查看所有可用环境
   ```

### 注意事项
- 保持yolov11环境的一致性
- 所有Python相关任务都使用此环境
- 避免使用系统Python或其他conda环境

---

Add whatever helps you do your job. This is your cheat sheet.
